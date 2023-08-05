# Configuration YAML file

`optuna-worker run` command requires a positional argument - path to configuration YAML file. This document describes the format and details of the YAML file. Configuration is defined as Pydantic Model in the source code, so you could also refer to the [source code](../src/optuna_worker/model.py) if you want. Here's the top-level keywords and descriptions.

| Key      | Type | Description                                                                                               |
| -------- | ---- | --------------------------------------------------------------------------------------------------------- |
| comand   | map  | (Required) CLI command model that composes training command for every trial. Refer to [command](#command) |
| study    | map  | (Required) Kwargs to be passed to optuna.create_study(). Refer to [study](#study)                         |
| metrics  | list | (Required) Definition of the metrics to be optimized. Refer to [metric](#metric)                          |
| optimize | map  | (Optional) Kwargs to be passed to study.optimize(). Refer to [optimize](#optimize)                        |


## Command

| Key        | Type       | Description                                                                                                                       |
| ---------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| type       | str        | (Required) Type of the cli command (ex: python, bash). It could also be a full path to the execution binary (ex: /usr/bin/python) |
| program    | str        | (Required) Program or script to be executed (ex: tools/train.py).                                                                 |
| args       | list (map) | (Required) List of hyper parameter arguments. Refer to [arg](#arg) for details.                                                   |
| extra_args | list (str) | (Optional) List of static cli arguments apart from hyper parameter to be optimized.                                               |

`command` composes training CLI command for every trial, using suggested parameters from optuna trial. CLI command is constructed as below.

```bash
${type} ${program} ${extra_args_str} ${args_str}
```

- `extra_args_str`: extra arguments joined with space.
- `args_str`: arguments joined with space.
  - each argument is in format of `${arg_key}=${suggested_value}` where suggested value is derived from trial's method.

### Arg

| Key    | Type | Description                                                                                                                |
| ------ | ---- | -------------------------------------------------------------------------------------------------------------------------- |
| key    | str  | (Required) CLI argument keyword including hyphens. (ex: "--lr")                                                            |
| method | str  | (Required) Trial's suggestion method to be used. (ex: suggest_float)                                                       |
| kwargs | map  | (Required) Kwargs to be passed to call suggestion method. (ex: {"name": "param1", "low": -1, "high": 1} for suggest_float) |

`arg` defines hyperparameter to be optimized, which is passed to the trainer via a CLI argument.

## Study

| Key            | Type | Description                                                                          |
| -------------- | ---- | ------------------------------------------------------------------------------------ |
| storage        | str  | (Optional) Database URL. In-memory storage is used if None.                          |
| sampler        | map  | (Optional) Definition of optuna sampler to be used. Refer to [sampler](#sampler)     |
| pruner         | map  | (Optional) Definition of optuna pruner to be used. Refer to [pruner](#pruner)        |
| study_name     | str  | (Optional) The name of the study to be created.                                      |
| load_if_exists | bool | (Optional) Boolean flag to raise an exception if study name exists. (default: False) |

Keyword arguments to be passed to `optuna.create_study()`.

### Sampler

| Key         | Type | Description                                                                           |
| ----------- | ---- | ------------------------------------------------------------------------------------- |
| class_name  | str  | (Required) Name of the sampler class to be created.                                   |
| module_path | str  | (Optional) Module import path to the class to be created. (default: optuna.samplers). |
| init_kwargs | map  | (Optional) kwargs to be passed to initializer.                                        |

Definition of optuna sampler to be created.
Concept of sampler creation:

```python
from module_path import class_name

sampler = class_name(**init_kwargs)
```

### Pruner

| Key         | Type | Description                                                                          |
| ----------- | ---- | ------------------------------------------------------------------------------------ |
| class_name  | str  | (Required) Name of the pruner class to be created.                                   |
| module_path | str  | (Optional) Module import path to the class to be created. (default: optuna.pruners). |
| init_kwargs | map  | (Optional) kwargs to be passed to initializer.                                       |

Definition of optuna pruner to be created.
Concept of pruner creation:

```python
from module_path import class_name

pruner = class_name(**init_kwargs)
```

## Metric

| Key       | Type | Description                                                                                                     |
| --------- | ---- | --------------------------------------------------------------------------------------------------------------- |
| name      | str  | (Required) Name of the metric to be optimized.                                                                  |
| direction | str  | (Required) Direction of the metric to be optimized - {"minimize", "maximize"}                                   |
| parser    | map  | (Required) Definition of metric parser. Either [lambda parser](#lambda-parser) or [regex parser](#regex-parser) |

Definition of the metric to be optimized.
It includes name and direction of the metric.
It also includes the parser to parse metric value from the stdout of the training subprocess.
Two parsers are supported - lambda parser and regex parser.
If `parser.type` is `regex`, it initializes `Regex Parser`. If `parser.type` is `lambda`, it initializes `Lambda Parser`

### Lambda Parser

| Key       | Type | Description                                                                                    |
| --------- | ---- | ---------------------------------------------------------------------------------------------- |
| condition | str  | (Required) Lambda function in string, returning boolean flag whether to execute parser or not. |
| parser    | str  | (Required) Lambda function in string, returning metric value from stdout line.                 |
| type      | str  | (Optional) Type of the metric parser - "lambda"                                                |

Definition of a metric parser using python lambda function.
If `parser.type` is `lambda`, `Lambda Parser` is initialized.
The metric value retrieved by `parser` would be converted into float type.
An example of a lambda parser definition:

```yaml
parser:
  type: lambda
  condition: "lambda x: 'total_loss' in x"
  parser: "lambda x: x.split('total_loss:')[1].split()[0]"
```

### Regex Parser

| Key     | Type | Description                                    |
| ------- | ---- | ---------------------------------------------- |
| pattern | str  | (Required) Regex pattern to find metric value. |
| type    | str  | (Optional) Type of the metric parser - "regex" |

Definition of a metric parser using regex.
If `parser.type` is `regex`, `Regex Parser` is initialized.
The metric value retrieved with `pattern` would be converted into float type.
Be sure to properly handle escape strings.
An example of a regex parser definition:

```yaml
parser:
  type: regex
  pattern: "total_loss: ([\\d.]+)"
```

## Optimize

| Key               | Type       | Description                                                  |
| ----------------- | ---------- | ------------------------------------------------------------ |
| n_trials          | int        | (Optional) Number of trials to be executed with this worker. |
| timeout           | float      | (Optional) Stop study after the given number of second(s).   |
| show_progress_bar | bool       | (Optional) Flag to show progress bars or not.                |
| callbacks         | list (map) | (Optional) List of callbacks. Refer to [callback](#callback) |

Keyword arguments to be passed to `Study.optimize()` method. Refer to the [official optuna documentation](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.optimize) for more details. Following kwargs are not supported in `optuna-worker`.
- n_jobs, catch, gc_after_trial

## Callback

| Key         | Type | Description                                               |
| ----------- | ---- | --------------------------------------------------------- |
| class_name  | str  | (Required) name of the class to be created.               |
| module_path | str  | (Required) module import path to the class to be created. |
| init_kwargs | dict | (Optional) kwargs to be passed to init method.            |

Definition of optuna callbacks to be created.
Concept of callback creation:

```python
from module_path import class_name

callback = class_name(**init_kwargs)
```
