from typing import Any

import pytest

from optuna_worker import model


class DummyCallback:
    def __call__(self, study: Any, trial: Any):
        pass


class DummyTrial:
    def suggest_float(self, name: str, extra: float = 1.0) -> float:
        return 1.0


class DummyPruner:
    pass


class DummySampler:
    pass


@pytest.fixture
def dummy_callback():
    return DummyCallback


@pytest.fixture
def dummy_trial():
    return DummyTrial


@pytest.fixture
def dummy_pruner():
    return DummyPruner


@pytest.fixture
def dummy_sampler():
    return DummySampler


@pytest.fixture
def dummy_command_model_obj():
    return model.CommandModel(
        type="python",
        program="test.py",
        args=[model.ArgModel(key="--test", method="suggest_float", kwargs={"name": "name"})],
        extra_args=["--opt"],
    )


@pytest.fixture
def dummy_command_trial_command():
    return ["python", "test.py", "--opt", "--test=1.0"]


@pytest.fixture
def dummy_optuna_worker_model_data():
    return {
        "command": {
            "type": "python",
            "program": "train.py",
            "args": [
                {
                    "key": "--arg1",
                    "method": "suggest_float",
                    "kwargs": {"name": "arg1"},
                },
            ],
            "extra_args": ["--target", "999"],
        },
        "metrics": [
            {
                "name": "metric_a",
                "direction": "maximize",
                "parser": {
                    "type": "lambda",
                    "condition": "lambda x: \"target\" in x",
                    "parser": "lambda x: x.split(\":\")[1]",
                },
            }
        ],
        "optimize": {
            "n_trials": 3,
        },
        "study": {
            "study_name": "MyStudy",
            "load_if_exists": False,
        },
    }


@pytest.fixture
def dummy_script():
    return "import sys; print('target:', sys.argv[2])"
