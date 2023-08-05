"""Definition of Optuna Worker models."""

import importlib
import inspect
import re
from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict, Optional, List, Literal, Union

import optuna
import yaml
from optuna import Trial
from pydantic import BaseModel, Field
from pydantic.decorator import validator


def _get_invalid_args(func: Callable, args: List[str], is_method: bool = True) -> List[str]:
    """Check if given arguments are valid for a given function.

    Args:
        func (callable): Function to be evaluated.
        args (list_of_str): Argument names to be evaluted.
        is_method (bool): True if func is a method.

    Returns:
        A list of argument names in string that does not exist in func arguments.
    """
    spec = inspect.getfullargspec(func)
    invalid_kwargs = []
    defaults = spec.defaults or []
    kwargs = set(spec.args[-len(defaults) :])
    for arg in spec.args:
        if (is_method and arg == "self") or (arg in kwargs):
            continue
        if arg not in args:
            invalid_kwargs.append(arg)
    return invalid_kwargs


class ArgModel(BaseModel):
    """Model for a CLI argument, which is also a hyperparameter to be optimized.

    Args:
        key (str): CLI argument keyword including hyphens.
        method (str): Trial's suggestion method to be used. (ex: suggest_float)
        kwargs(dict): Kwargs to be passed to call suggestion method.
                      (ex: {"name": "param1", "low": -1, "high": 1} for suggest_float)
    """

    key: str
    method: str
    kwargs: Dict[str, Any] = Field(default_factory=dict)

    @validator("method")
    def check_method(cls, v: str) -> str:
        """Check if method is valid."""
        valid_methods = set(m for m in dir(Trial) if m.startswith("suggest"))
        if v not in valid_methods:
            raise ValueError(f"Invalid method `{v}`. ")
        return v

    @validator("kwargs")
    def check_kwargs_existance(cls, v: Dict[str, Any], values: Dict, **kwargs) -> Dict[str, Any]:
        """Check if keywords in kwargs are valid."""
        func_name = "Trial." + values["method"]
        invalid_args = _get_invalid_args(eval(func_name), list(v), is_method=True)
        if not invalid_args:
            return v
        raise ValueError(f"Found invalid arguments for `{func_name}` - {invalid_args}")

    def suggest(self, trial: Trial) -> str:
        """Get suggested parameter from trial."""
        method = getattr(trial, self.method)
        return str(method(**self.kwargs))


class CommandModel(BaseModel):
    """CLI command model that composes training command for every trial.

    Args:
        type (str): Type of the cli command. (ex: python, bash)
                    or full path to the execution binary (ex: /usr/bin/python)
        program (str): Program or script to be executed (ex: tools/train.py)
        args (list_or_argmodel): List of ArgModel. Refer to ArgModel for details.
        extra_args (list_or_str): List of static cli arguments apart from hyperparameter tuning.
    """

    type: str
    program: str
    args: List[ArgModel]
    extra_args: List[str] = Field(default_factory=list)

    def get_trial_command(self, trial: Trial) -> List[str]:
        """Get cli command for given trial.

        Arg:
            trial (Trial): Optuan trial object.

        Returns:
            A list of string of CLI command to be executed.
        """
        cmd = [self.type, self.program] + self.extra_args
        for arg in self.args:
            arg_str = f"{arg.key}={arg.suggest(trial)}"
            cmd.append(arg_str)
        return cmd


class _MetricParserModel(BaseModel, metaclass=ABCMeta):
    """Baseclass for metric parser models.

    Args:
        type (str): Metric parser type
    """

    @abstractmethod
    def parse(self, line: str) -> Optional[float]:
        """Abstractmethod to parse a metric value from stdout line.

        Args:
            line (str): stdout line from training subprocess.

        Returns:
            A float value for the metric or None if not exists
        """
        pass


class LambdaParserModel(_MetricParserModel):
    """Definition of a metric parser using python lambda function.

    Args:
        condition (str): lambda returning bool if to execute parser or not.
        parser (str): lambda returning metric value from stdout line.
    """

    condition: str
    parser: str
    type: str = "lambda"

    @property
    def condition_func(self):
        return eval(self.condition)

    @property
    def parser_func(self):
        return eval(self.parser)

    def parse(self, line: str) -> Optional[float]:
        """Parse a metric value from stdout line.

        Args:
            line (str): stdout line from training subprocess.

        Returns:
            A float value for the metric or None if not exists
        """
        if self.condition_func(line):
            return float(self.parser_func(line))
        return

    def _check_lambda_eval(cls, v: str, type: str) -> None:
        try:
            _ = eval(v)
        except Exception:
            raise ValueError(f"{type} cannot be evaluated.")

    @validator("condition")
    def check_condition(cls, v: str) -> str:
        cls._check_lambda_eval(cls, v, "condition")
        return v

    @validator("parser")
    def check_parser(cls, v: str) -> str:
        cls._check_lambda_eval(cls, v, "parser")
        return v


class RegexParserModel(_MetricParserModel):
    """Definition of a metric parser using regex.

    Args:
        pattern (str): Regex pattern to find metric value.
        type (str): Metric parser type - "regex"
    """

    pattern: str
    type: str = "regex"

    def parse(self, line) -> Optional[float]:
        """Parse a metric value from stdout line.

        Args:
            line (str): stdout line from training subprocess.

        Returns:
            A float value for the metric or None if not exists
        """
        match = re.search(self.pattern, line)
        if match:
            return float(match.group(1))
        return


class MetricModel(BaseModel):
    """Definition of the metric to be optimized.

    Args:
        name (str): Name of the metric to be optimized.
        direction (str): Direction of the metric to be optimized - {"minimize", "maximize"}
        parser (_MetricParserModel): Definition of metric parser model.
    """

    name: str
    direction: Literal["minimize", "maximize"]
    parser: Union[LambdaParserModel, RegexParserModel]

    @validator("parser", pre=True)
    def check_parser(cls, v: dict) -> Union[LambdaParserModel, RegexParserModel]:
        if v["type"] == "lambda":
            return LambdaParserModel(**v)
        if v["type"] == "regex":
            return RegexParserModel(**v)
        raise ValueError("Invalid metric parser type. Only supports lambda, regex.")

    def parse(self, line: str) -> Optional[float]:
        """Parse a metric value from stdout line.

        Args:
            line (str):  stdout line from training subprocess.

        Returns:
            A float value for the metric or None if not exists
        """
        return self.parser.parse(line)


class _CreationModel(BaseModel):
    """Definition of a model to imported classes from module path and init with init_kwargs.

    Args:
        class_name (str): name of the class to be created.
        module_path (str): module import path to the class to be created.
        init_kwargs (dict): kwargs to be passed to __init__.
    """

    class_name: str
    module_path: str
    init_kwargs: dict = Field(default_factory=dict)

    @classmethod
    def _get_class_from_module(cls, module_path: str, class_name: str) -> type:
        try:
            module = importlib.import_module(module_path)
        except ImportError:
            raise ImportError(f"Cannot import module `{module_path}`")
        try:
            cls = getattr(module, class_name)
        except AttributeError:
            raise RuntimeError(f"Cannot get `{class_name}` from `{module_path}`")
        return cls

    @validator("module_path")
    def check_class_import(cls, v: str, values: dict, **kwargs) -> str:
        try:
            cls._get_class_from_module(module_path=v, class_name=values["class_name"])
        except Exception as e:
            raise ValueError(e)
        return v

    @validator("init_kwargs")
    def check_class_init(cls, v: dict, values: dict, **kwargs) -> dict:
        cls_ = cls._get_class_from_module(module_path=values["module_path"], class_name=values["class_name"])
        try:
            cls_(**v)
        except Exception as e:
            raise ValueError(e)
        return v

    @validator("class_name")
    def check_class_name(cls, v: str) -> str:
        if "." in v:
            raise ValueError("class_name should not contain '.'")
        return v

    def create(self) -> Any:
        """Create given class with given module path and init kwargs.

        Returns:
            An initialized object of class_name type.
        """
        cls = self._get_class_from_module(module_path=self.module_path, class_name=self.class_name)
        return cls(**self.init_kwargs)


class SamplerModel(_CreationModel):
    """Definition of optuna sampler to be created.

    Args:
        class_name (str): name of the sampler class to be created.
        module_path (str): module import path to the class to be created. (default: optuna.samplers).
        init_kwargs (dict): kwargs to be passed to __init__.
    """

    module_path: str = "optuna.samplers"


class PrunerModel(_CreationModel):
    """Definition of optuna pruner to be created.

    Args:
        class_name (str): name of the class to be created.
        module_path (str): module import path to the class to be created. (default: optuna.pruners).
        init_kwargs (dict): kwargs to be passed to __init__.
    """

    module_path: str = "optuna.pruners"


class StudyModel(BaseModel):
    """Kwargs to be passed to optuna.create_study.

    `directon` or `direcitons` argument is automatically evaluted and passed by OptunaWorker.

    Args:
        storage (str): Database URL. In-memory storage is used if None.
        sampler (SamplerModel): Refer to SamplerModel.
        pruner (PrunerModel): Refer to PrunerModel.
        study_name (str): The name of the study to be created.
        load_if_exists (bool): False if to raise an exception if study name exists.
    """

    storage: Optional[str] = None
    sampler: Optional[SamplerModel] = None
    pruner: Optional[PrunerModel] = None
    study_name: Optional[str] = None
    load_if_exists: bool = False


class CallbackModel(_CreationModel):
    """Definition of a callback model to imported classes from module path and init with init_kwargs.

    Args:
        class_name (str): name of the class to be created.
        module_path (str): module import path to the class to be created.
        init_kwargs (dict): kwargs to be passed to __init__.
    """

    @validator("module_path")
    def check_callback_call_args(cls, v: str, values: dict, **kwargs) -> str:
        cls_ = cls._get_class_from_module(v, values["class_name"])
        call_method = getattr(cls_, "__call__")
        args = inspect.getfullargspec(call_method).args
        assert args == ["self", "study", "trial"]


class OptimizeModel(BaseModel):
    """Kwargs to be passed to study.optimize(). Kwargs such as n_jobs are not supported.

    Args:
        n_trials (optional, int): number of trials to be executed with this worker.
        timeout (optional, float): Stop study after the given number of second(s).
        show_progress_bar (bool): Flag to show progress bars or not.
        callbacks (optional, list_of_callback_model): Refer to CallbackModel.
    """

    n_trials: Optional[int] = None
    timeout: Optional[float] = None
    show_progress_bar: bool = False
    callbacks: List[CallbackModel] = Field(default_factory=list)


class OptunaWorkerModel(BaseModel):
    """Definition of optuna worker model.

    Args:
        command (CommandModel): Refer to CommandModel.
        study (StudyModel): Refer to StudyModel.
        metric: (list of MetricModel): Refer to MetricModel.
        optimize (OptimizeModel): Refer to OpimizeModel.
    """

    command: CommandModel
    study: StudyModel
    metrics: List[MetricModel]
    optimize: OptimizeModel = Field(default_factory=OptimizeModel)

    def create_study(self) -> optuna.Study:
        kwargs = vars(self.study)
        for k, v in kwargs.items():
            if isinstance(v, _CreationModel):
                kwargs[k] = v.create()
        directions = [m.direction for m in self.metrics]
        if len(directions) == 0:
            kwargs["direction"] = directions[0]
        else:
            kwargs["directions"] = directions
        return optuna.create_study(**kwargs)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "OptunaWorkerModel":
        """Create OptunaWorkerModel object based on yaml file.

        Args:
            yaml_path (str): Path to yaml file with worker model data.

        Returns:
            A OptunaWorkerModel instance with data from input yaml file.
        """
        return cls(**yaml.safe_load(open(yaml_path)))

    def parse_metrics(self, line: str) -> List[Optional[float]]:
        """Parse metric values from stdout line.

        Args:
            line (str):  stdout line from training subprocess.

        Returns:
            A list of float or none typed values.
        """
        return [metric.parse(line) for metric in self.metrics]
