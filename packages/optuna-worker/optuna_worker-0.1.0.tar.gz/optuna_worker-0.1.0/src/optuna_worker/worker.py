"""Optuna Worker implementation."""

import subprocess
from functools import partial
from typing import List

import optuna
import yaml
from loguru import logger

from .model import OptunaWorkerModel


class OptunaWorker:
    """Optuna worker class that creates training subprocess.

    It also monitors stdout from training subprocess to retrieve metrics.

    Args:
        model (OptunaWorkerModel): A OptunaWorkerModel instance with the definition of Optuna Worker.
    """

    def __init__(self, model: OptunaWorkerModel):
        self.model = model

    @staticmethod
    def objective(trial: optuna.Trial, model: OptunaWorkerModel) -> List[float]:
        """Optuna proxy objective function.

        1. Creates subprocess that evokes training job.
        2. Get stdout from subprocess to retrieve the metric value to be reported.
        3. Returns final metrics or raise TrialPruned.

        Args:
            trial (optuna.Trial): Optuna Trial object to evalute objective function.
            model (OptunaWorkerModel): Optuna worker model containing configuration for current run.
        """
        cmd = model.command.get_trial_command(trial)
        logger.info(f"Running {trial.number}'th trial: {cmd}")
        p = subprocess.Popen(
            args=cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )
        final_metric_vals = [None] * len(model.metrics)
        step = 0
        reporting_metric = model.metrics[0].name
        for line in p.stdout:
            print(line)
            vals = model.parse_metrics(line)
            for i, val in enumerate(vals):
                # skip none value
                if val is None:
                    continue
                # update metric value to be returned
                final_metric_vals[i] = val
                # report first metric
                if i == 0:
                    logger.info(f"Step: {step} | Metric: {reporting_metric} | Value: {val}")
                    trial.report(value=val, step=step)
                    step += 1
            if trial.should_prune():
                raise optuna.TrialPruned()
        p.wait()
        return_code = p.poll()
        if return_code != 0:
            logger.error("\n" + p.stderr.read().strip())
            raise RuntimeError("Training failed with the above error.")
        if all(f is None for f in final_metric_vals):
            metrics_yaml_str = yaml.safe_dump([m.dict() for m in model.metrics])
            logger.warning(
                "Failed to parse metric values from whole training logs. "
                f"Check if metric type and pattern are properly configured.\n{metrics_yaml_str}"
            )
        final_metrics = {m.name: v for m, v in zip(model.metrics, final_metric_vals)}
        logger.info(f"Final metrics: {final_metrics}")
        return final_metric_vals

    def run(self) -> optuna.Study:
        """Run optuna worker to create study and optimize objective."""
        yaml_str = yaml.safe_dump(self.model.dict())
        logger.info(f"Start running Optuna Worker with following model:\n{yaml_str}")
        study = self.model.create_study()
        objective = partial(OptunaWorker.objective, model=self.model)
        optimize_kwargs = vars(self.model.optimize)
        study.optimize(objective, **optimize_kwargs)
        return study
