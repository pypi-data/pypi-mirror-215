# logfile_metrics - Сканирование лог-файлов с целью формирования метрик для Prometheus.

## Steps to release a new package version
* Run tests, linter, formatter, ...: `poetry run pytest (pylint, black, ...)`
* Bump project's version: `poetry version ...`
* Build: `poetry build`
* Publish: `poetry publish`
