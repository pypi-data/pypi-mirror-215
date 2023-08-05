from optuna_worker.model import OptunaWorkerModel
from optuna_worker.worker import OptunaWorker


def test_optuna_worker(dummy_script, dummy_optuna_worker_model_data, dummy_trial, tmp_path, monkeypatch):
    monkeypatch.setattr(
        "optuna_worker.model.Trial.suggest_float",
        dummy_trial.suggest_float,
    )

    # dump dummy script
    script_path = tmp_path / "dummy_script.py"
    with open(script_path, "w") as fo:
        fo.write(dummy_script)
    # create dummy model
    dummy_optuna_worker_model_data["command"]["program"] = str(script_path)

    # run optuna worker
    m = OptunaWorkerModel(**dummy_optuna_worker_model_data)
    worker = OptunaWorker(m)
    study = worker.run()
    trials = study.get_trials()

    assert len(trials) == m.optimize.n_trials, "num trials differs"
    assert all(t.values == [999.0] for t in trials), "metrics differ"
