#!/usr/bin/env python3

from typing import Optional, List
import sys
import os
import argparse
import toml
import yaml

# pyright: reportMissingTypeStubs=false
from kevbits import logconfig
from kevbits.misc import map_deep

from logfile_metrics.logfile_metrics import main2


PROGRAM_VERSION = "0.1.0"


def main(argv: Optional[List[str]] = None):
    "Main function."
    program_description = __doc__

    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description=program_description,
        epilog=None,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )

    parser.add_argument("--version", action="version", version=PROGRAM_VERSION)

    parser.add_argument(
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit.",
    )

    parser.add_argument(
        "-c",
        "--config",
        dest="configfile",
        required=True,
        type=str,
        help="""Path to configuration file in TOML format.""",
    )

    args = parser.parse_args(argv)

    # Load configuration
    configfile = os.path.normpath(os.path.expandvars(args.configfile))
    config = toml.load(configfile)
    # Preprocess string parameters in configuration (expand environment variables)
    config = map_deep(
        config, lambda v: v if not isinstance(v, str) else os.path.expandvars(v)
    )

    # Configure logging
    logging_config_yaml_file = os.path.normpath(
        config["main"]["logging_config_yaml_file"]
    )
    with open(logging_config_yaml_file, "r", encoding="utf-8") as fyaml:
        logger = logconfig.from_dict(yaml.safe_load(fyaml.read()))
    logger.info("")
    logger.info("-" * 80)

    main2(config, logger)


if __name__ == "__main__":
    main()
