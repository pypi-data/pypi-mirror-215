"""Cli module for Optuna Worker."""

import click
import optuna
from pydantic import ValidationError

import optuna_worker
from optuna_worker.model import OptunaWorkerModel
from optuna_worker.worker import OptunaWorker


@click.group()
def cli():
    """Base cli group."""
    pass


@cli.command()
def version() -> None:
    """Print versions of optuna and optuna-worker."""
    click.echo(f"optuna: {optuna.__version__}")
    click.echo(f"optuna-worker: {optuna_worker.__version__}")


@cli.command()
@click.argument("config-file", type=click.Path(exists=True))
def validate(config_file: str) -> None:
    """Validate the format of CONFIG_FILE."""
    try:
        _ = OptunaWorkerModel.from_yaml(config_file)
        click.echo(f"Config file is VALID: {config_file}")
    except ValidationError as exc:
        print(exc)
        click.echo(f"Config file is INVALID: {config_file}")


@cli.command()
@click.argument("config-file", type=click.Path(exists=True))
def run(config_file: str) -> None:
    """Run optuna study with a given CONFIG_FILE."""
    model = OptunaWorkerModel.from_yaml(config_file)
    worker = OptunaWorker(model)
    worker.run()


if __name__ == '__main__':
    cli()
