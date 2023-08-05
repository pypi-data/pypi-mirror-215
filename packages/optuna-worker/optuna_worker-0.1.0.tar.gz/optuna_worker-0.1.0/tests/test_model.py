"""Test Optuna Worker Models."""
from contextlib import contextmanager

import pytest
import yaml

import optuna_worker
from optuna_worker import model


@contextmanager
def patch_optuna_worker_module(cls_name: str, cls_var: type):
    setattr(optuna_worker, cls_name, cls_var)
    try:
        yield
    finally:
        delattr(optuna_worker, cls_name)


@pytest.mark.parametrize(
    "method,kwargs",
    [
        ("suggest_float", {"name": "name"}),
        ("suggest_float", {"name": "name", "extra": 2.0}),
    ],
)
def test_arg_model(method, kwargs, monkeypatch, dummy_trial):
    monkeypatch.setattr(
        "optuna_worker.model.Trial.suggest_float",
        dummy_trial.suggest_float,
    )
    m = model.ArgModel(key="--test", method=method, kwargs=kwargs)
    assert m.suggest(dummy_trial()) == "1.0"


def test_command_model(monkeypatch, dummy_trial, dummy_command_model_obj, dummy_command_trial_command):
    monkeypatch.setattr(
        "optuna_worker.model.Trial.suggest_float",
        dummy_trial.suggest_float,
    )
    assert dummy_command_model_obj.get_trial_command(dummy_trial()) == dummy_command_trial_command


@pytest.mark.parametrize("line,value,pattern", [("test target: 123 post", 123.0, "target: ([\\d.]+)")])
def test_regex_parser_model(line, value, pattern):
    parser = model.RegexParserModel(pattern=pattern)
    assert parser.parse(line) == value


@pytest.mark.parametrize(
    "line,value,condition,parser",
    [("test target: 123 post", 123.0, "lambda x: 'target' in x", "lambda x: x.split()[2]")],
)
def test_lambda_parser_model(line, value, condition, parser):
    parser = model.LambdaParserModel(condition=condition, parser=parser)
    assert parser.parse(line) == value


@pytest.mark.parametrize("direction", ["minimize", "maximize"])
@pytest.mark.parametrize(
    "parser",
    [
        {"type": "regex", "pattern": "."},
        {"type": "lambda", "condition": "lambda x: False", "parser": "lambda x: x"},
    ],
)
def test_metric_model(direction, parser):
    _ = model.MetricModel(name="x", direction=direction, parser=parser)


def test_sampler_model(dummy_sampler):
    class_name = "DummySampler"
    with patch_optuna_worker_module(class_name, dummy_sampler):
        m = model.SamplerModel(class_name=class_name, module_path="optuna_worker")
        m.create()


def test_pruner_model(dummy_pruner):
    class_name = "DummyPruner"
    with patch_optuna_worker_module(class_name, dummy_pruner):
        m = model.PrunerModel(class_name=class_name, module_path="optuna_worker")
        m.create()


def test_callback_model(dummy_callback):
    class_name = "DummyCallback"
    with patch_optuna_worker_module(class_name, dummy_callback):
        _ = model.CallbackModel(class_name=class_name, module_path="optuna_worker")


def test_optuna_worker_model(monkeypatch, dummy_trial, dummy_optuna_worker_model_data, tmp_path):
    yaml_path = tmp_path / "test.yaml"
    yaml.safe_dump(dummy_optuna_worker_model_data, open(yaml_path, "w"))
    monkeypatch.setattr(
        "optuna_worker.model.Trial.suggest_float",
        dummy_trial.suggest_float,
    )
    m = model.OptunaWorkerModel.from_yaml(yaml_path)
    study = m.create_study()
    assert study.direction.name == "MAXIMIZE"
