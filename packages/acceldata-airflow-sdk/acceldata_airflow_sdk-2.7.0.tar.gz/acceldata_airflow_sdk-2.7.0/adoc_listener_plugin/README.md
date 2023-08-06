# ADOC Listener Plugin
A plugin that integrates [Airflow `DAGs`]() for automatic observation in `ADOC`.

## Features
The plugin will do below things without writing any additional code in your Airflow DAG if instrumentation is not disabled based on the environment variables.

* On DAG start:
  * Creating the pipeline if doesn’t exist in ADOC.
  * Creating a new pipeline run in ADOC.

* On TaskInstance start:
  * Creating the Jobs in ADOC for each of the airflow operators and constructing job input nodes based on the upstream tasks.
  * Creating the span and associating it with the Jobs.
  * Emitting span events with metadata.

* On TaskInstance complete:
  * Emitting span events with metadata.
  * Ending the spans with success/failure.

* On DAG complete:
  * Updating the pipeline run with success/failure in ADOC.

## Requirements
- [Python 3.6+](https://www.python.org/downloads)
- [Airflow 2.3+](https://pypi.org/project/apache-airflow)

## Configuration

###  Plugin Environment Variables

`adoc_listener_plugin` uses accedlata-sdk [https://pypi.org/project/acceldata-sdk/] to push data to the ADOC backend.

The adoc client depends on environment variables:

* `TORCH_CATALOG_URL` - URL of the torch catalog
* `TORCH_ACCESS_KEY` - API access key generated from torch UI
* `TORCH_SECRET_KEY` - API secret key generated from torch UI

By default, all the dags will be observed. Below set of environment variables could be used to override this behaviour.
Environment variables to either ignore / observe are mutually exclusive . 

Below environment variables if matched with the dag ids, will ignore observation of the matched dag ids. All other dag ids will be observed.
* `DAGIDS_TO_IGNORE` = "Comma separated dag ids to ignore observation"
* `DAGIDS_REGEX_TO_IGNORE` = "Regex for dag ids to ignore observation"

Below environment variables if matched with the dag ids, will be observed observation of dag ids. All other dag ids will be ignored.
* `DAGIDS_TO_OBSERVE` = "Comma separated dag ids to observe"
* `DAGIDS_REGEX_TO_OBSERVE` = "Regex for dag ids to observe"
