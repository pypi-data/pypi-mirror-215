import os
import re
from datetime import datetime
import fileinput
import time
import glob
import subprocess as sp
import json
from typing import (
    Optional,
    List,
    Set,
    Any,
    Dict,
    KeysView,
    Pattern,
    cast,
    Callable,
    FrozenSet,
    Tuple,
    Union,
)
import logging

from kevbits.misc import format_exception  # pyright: ignore[reportMissingTypeStubs]


class ProgramError(Exception):
    ...


class BaseServiceMetricsFactory:
    timestamp: Dict[str, str]
    inputerror: Dict[str, str]


def unix_epoch_seconds() -> float:
    "Return seconds since Unix epoch (1970)"
    return (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()


def check_keys(
    keys: Union[KeysView[str], List[str]],
    req: Optional[List[str]] = None,
    opt: Optional[List[str]] = None,
    mutex: Optional[List[str]] = None,
    *,
    where: str,
):
    "Check the list of keys against the lists of required, optional and mutually exclusive ones."

    def raise_error(msg: str, errkeys: Set[str]):
        raise ProgramError(f"{msg}: {', '.join(sorted(errkeys))} (in {where})")

    keyset = set(keys)

    req, opt, mutex = [([] if x is None else x) for x in (req, opt, mutex)]

    misreq = set(req).difference(keys)
    if misreq:
        raise_error("missing keys", misreq)

    if mutex:
        inters = keyset.intersection(mutex)
        if not inters:
            raise_error("one of keys expected", set(mutex))
        if len(inters) > 1:
            raise_error("incompatible keys", inters)

    unknown = keyset.difference(req, opt, mutex)
    if unknown:
        raise_error("unexpected keys", unknown)


def extract_fields(
    line: str, rules: List[Dict[str, Any]], patterns: Dict[str, Pattern[str]]
) -> Dict[str, str]:
    "Extract fields from the line."
    fields: Dict[str, str] = {"": line}

    # Iterate over rules
    for rule in rules:
        field = rule["field"]
        field_text = None
        match: Optional[Dict[str, str]] = None

        try:
            field_text = fields[field]
        except KeyError:
            if not rule.get("opt", False):
                raise

        if field_text is not None:
            pat_name = rule["pattern"]
            if pat_name != "<json>":
                pattern = patterns[pat_name]
                pm = pattern.match(field_text)
                if pm is not None:
                    match = pm.groupdict()
            else:
                try:
                    match = json.loads(field_text)
                    assert isinstance(match, dict)
                    # Convert values into strings
                    match = {k: str(v) for k, v in match.items()}
                except Exception:  # pylint: disable=broad-exception-caught
                    pass

        if match is not None:
            # Update fields from match object
            fields.update(match)
            # Add new fields if given
            for assignment in rule.get("add", []):
                dest, src = [s.strip() for s in assignment.split("=")]
                fields[dest] = fields[src]
        else:
            if rule.get("mismatch_break", False):
                break

    return fields


class LabelsetNoField(Exception):
    "Derived exception class. For the convenience of testing."


def compute_labelset(
    labeldefs: List[Dict[str, str]], fields: Dict[str, str]
) -> FrozenSet[Tuple[str, str]]:
    "Compute labelset for given labels definitions."
    labels: Dict[str, str] = {}

    for ld in labeldefs:
        name = ld["name"]
        if "value" in ld:
            labels[name] = ld["value"]
        if "field" in ld:
            field = ld["field"]
            try:
                labels[name] = fields[field]
            except KeyError:
                raise LabelsetNoField(
                    f"Missing field '{field}' for label '{name}'."
                ) from None

    return frozenset(sorted(labels.items()))


def update_metric(
    metric: Dict[str, Any], *, fields: Dict[str, str], inputlabel: Optional[str]
):
    "Update metric dict using the given fields."
    try:
        field = metric["field"]
    except KeyError:
        raise ProgramError("Missing 'field' in metric definition") from None

    if field not in fields:
        return

    labeldefs = metric.get("labels", [])
    if inputlabel is not None:
        labeldefs.append({"name": "input", "value": inputlabel})
    labelset = compute_labelset(labeldefs, fields)

    mettype = metric["type"]
    if mettype == "counter":
        metric.setdefault("values", {}).setdefault(labelset, 0)
        metric["values"][labelset] += 1
    elif mettype == "gauge":
        metric["values"][labelset] = float(fields[field])
    else:
        raise ProgramError(f"Metric type is not supported: {mettype}")


def format_metrics_lines(
    metrics: List[Dict[str, Any]], job_labels: Dict[str, str]
) -> List[str]:
    "Create metrics lines for Prometheus."
    lines: List[str] = []

    for m in metrics:
        values = m["values"]
        if not values:
            continue

        metname = m["name"]
        lines.append(f"# HELP {metname} {m['help']}")
        lines.append(f"# TYPE {metname} {m['type']}")

        for labelset, metvalue in values.items():
            labels = dict(labelset)
            labels.update(job_labels)
            if not labels:
                fullname = metname
            else:
                # Make a fullname as a name with labels: metname{label1="value1",label2="value2"}
                labelstring = ",".join(
                    [f'{name}="{val}"' for name, val in sorted(labels.items())]
                )
                fullname = f"{metname}{{{labelstring}}}"
            lines.append(f"{fullname} {metvalue}")

    return lines


def compile_patterns(patterns: Dict[str, str]) -> Dict[str, Pattern[str]]:
    "Compile regexp patterns."
    assert isinstance(patterns, dict), "'patterns' is expected to be a dict"
    result: Dict[str, Pattern[str]] = {}
    for name, regexp in patterns.items():
        try:
            result[name] = re.compile(regexp)
        except Exception as e:
            raise ProgramError(f"failed to compile pattern '{name}': {e}") from None
    return result


def process_job(
    job: Dict[str, Any],
    global_patterns: Dict[str, Pattern[str]],
    *,
    service_metrics: BaseServiceMetricsFactory,
    logger: logging.Logger,
    seconds: Optional[Callable[[], float]] = None,
):
    "Process single job."
    # pylint: disable=too-many-locals,too-many-nested-blocks,too-many-branches,too-many-statements

    if seconds is None:
        seconds = unix_epoch_seconds

    check_keys(
        job.keys(),
        req=["name", "inputs", "rules", "metrics", "output"],
        opt=["patterns", "labels"],
        where="job configuration",
    )

    inputs = job["inputs"]
    assert isinstance(inputs, list), "job 'inputs' is expected to be an array"
    inputs = cast(
        List[Dict[str, Any]], inputs
    )  # Do nothing at runtime, for type checker only.
    for inp in inputs:
        check_keys(
            inp.keys(),
            req=[],
            mutex=["files", "command"],
            opt=["label", "encoding", "timeout"],
            where="input configuration",
        )
        if "files" in inp:
            assert isinstance(
                inp["files"], list
            ), "job input 'files' is expected to be an array"
        if "command" in inp:
            assert isinstance(
                inp["command"], list
            ), "job input 'command' is expected to be an array"
    if len(inputs) > 1:
        assert len(inputs) == len(
            set(inp["label"] for inp in inputs if "label" in inp)
        ), "job 'inputs' must have different 'label' values"

    rules = job["rules"]
    assert isinstance(rules, list), "job 'rules' is expected to be an array"
    rules = cast(
        List[Dict[str, Any]], rules
    )  # Do nothing at runtime, for type checker only.
    for rule in rules:
        check_keys(
            rule.keys(),
            req=["field", "pattern"],
            opt=["opt", "mismatch_break", "add"],
            where="rule configuration",
        )
        addlist = rule.get("add", [])
        assert isinstance(addlist, list), "'add' is expected to be an array"
        for a in addlist:
            assert (
                isinstance(a, str) and len(a.split("=")) == 2
            ), "'add' items must be strings of 'dest = src' format ('dest' and 'src' are fields names)"

    metrics = job["metrics"]
    assert isinstance(metrics, list), "job 'metrics' is expected to be an array"
    metrics = cast(
        List[Dict[str, Any]], metrics
    )  # Do nothing at runtime, for type checker only.
    for metric in metrics:
        check_keys(
            metric.keys(),
            req=["name", "help", "type", "field"],
            opt=["labels"],
            where="metric configuration",
        )
        metlabels = metric.get("labels", [])
        assert isinstance(metlabels, list), "metric 'labels' is expected to be an array"
        for ml in metlabels:
            check_keys(
                ml.keys(),
                req=["name"],
                mutex=["value", "field"],
                where=f"'labels' for metric '{metric['name']}'",
            )

    job_patterns = compile_patterns(job.get("patterns", {}))
    patterns = {**global_patterns, **job_patterns}

    # Prepare service metrics
    inputerror_metric = service_metrics.inputerror.copy()
    timestamp_metric = service_metrics.timestamp.copy()
    inputerror_metric["field"] = "__INPUTERROR__"  # any uniq value will do
    timestamp_metric["field"] = "__TIMESTAMP__"
    metrics.extend([inputerror_metric, timestamp_metric])

    for metric in metrics:
        metric["values"] = {}

    labeldefs = job.get("labels", [])
    assert isinstance(labeldefs, list), "job 'labels' is expected to be an array"
    job_labels = {}
    for ld in labeldefs:
        check_keys(ld.keys(), req=["name", "value"], where="job 'labels' configuration")
        job_labels[ld["name"]] = ld["value"]

    def process_line(line: str, inputlabel: Optional[str]):
        "Process the line."
        fields = extract_fields(line, rules, patterns)
        for m in metrics:
            update_metric(m, fields=fields, inputlabel=inputlabel)

    for inp in inputs:
        inputlabel = inp.get("label", None)
        try:
            filemasks = inp.get("files", [])
            if filemasks:
                filenames: List[str] = []
                for mask in filemasks:
                    if mask in ["-", "stdin"]:
                        filenames.append("-")
                    else:
                        names = glob.glob(mask)
                        if not names:
                            raise ProgramError(f"no files found for the mask '{mask}'")
                        filenames += names
                encoding = inp.get("encoding", "utf-8")
                openhook = fileinput.hook_encoded(encoding)
                with fileinput.input(files=filenames, openhook=openhook) as fin:
                    for line in fin:
                        process_line(line, inputlabel)

            command = inp.get("command", [])
            if command:
                timeout = inp.get("timeout", None)
                encoding = inp.get("encoding", "utf-8")
                cprocess = sp.run(
                    command,
                    capture_output=True,
                    check=True,
                    encoding=encoding,
                    timeout=timeout,
                )
                for line in cprocess.stdout.splitlines():
                    process_line(line, inputlabel)

        except Exception:  # pylint: disable=broad-exception-caught
            update_metric(
                inputerror_metric,
                fields={inputerror_metric["field"]: "1.0"},
                inputlabel=inputlabel,
            )
            logger.error(
                f"Error while processing job '{job['name']}', input '{inputlabel}': "
                + format_exception(tb=True)
            )

    # Update timestamp service metric
    update_metric(
        timestamp_metric,
        fields={timestamp_metric["field"]: str(seconds())},
        inputlabel=None,
    )

    lines = format_metrics_lines(metrics, job_labels)

    if job["output"] == "stdout":
        for line in lines:
            print(line)
    else:
        outfname = job["output"]
        tmpfname = outfname + ".$$$"
        with open(tmpfname, "w", encoding="utf-8") as f:
            f.writelines([s + "\n" for s in lines])
        # Replace output file with newer version
        attempts = 0
        while True:
            try:
                os.replace(tmpfname, outfname)
                break
            except IOError:
                attempts += 1
                if attempts == 3:
                    raise
                time.sleep(0.1)


class ServiceMetricsFactory(BaseServiceMetricsFactory):
    "Build service metrics."

    def __init__(self, mainconf: Dict[str, Any]) -> None:
        self.timestamp = {
            "name": mainconf.get(
                "timestamp_metric_name", "logfile_metrics_job_timestamp_seconds"
            ),
            "help": mainconf.get(
                "timestamp_metric_help",
                "logfile_metrics: job processing time since unix epoch in seconds.",
            ),
            "type": "gauge",
        }
        self.inputerror = {
            "name": mainconf.get(
                "inputerror_metric_name", "logfile_metrics_input_error"
            ),
            "help": mainconf.get(
                "inputerror_metric_help",
                "logfile_metrics: processing result for job input (0 - success).",
            ),
            "type": "gauge",
        }


def main2(config: Dict[str, Any], logger: logging.Logger):
    "main2 function"
    try:
        check_keys(
            config.keys(), req=["main", "jobs"], opt=["patterns"], where="configuration"
        )

        patterns = compile_patterns(config.get("patterns", {}))

        service_metrics = ServiceMetricsFactory(config["main"])

        jobs = config["jobs"]
        assert isinstance(jobs, list), "'jobs' is expected to be an array"
        jobs = cast(
            List[Dict[str, Any]], jobs
        )  # Do nothing at runtime, for type checker only.

        for i, job in enumerate(jobs):
            try:
                jobname = job["name"]
            except KeyError:
                raise ProgramError(f"Missing 'name' for the job #{i+1}.") from None

            try:
                logger.info(f"processing job #{i+1} '{jobname}'")
                process_job(
                    job, patterns, service_metrics=service_metrics, logger=logger
                )

            except Exception:  # pylint: disable=broad-exception-caught
                logger.error(
                    f"Error while processing job #{i+1} '{jobname}': {format_exception(tb=True)}"
                )

    except Exception:  # pylint: disable=broad-exception-caught
        logger.error(f"Error: {format_exception(tb=True)}")
