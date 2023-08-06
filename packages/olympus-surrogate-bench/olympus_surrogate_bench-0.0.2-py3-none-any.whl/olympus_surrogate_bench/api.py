from __future__ import annotations

import json
import os
import pickle

import ConfigSpace as CS

from olympus_surrogate_bench.constants import DATASET_NAMES, SAVE_DIR_NAME

import pandas as pd

from sklearn.ensemble import RandomForestRegressor


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_DIR_NAME)
SEARCH_SPACES: dict[str, dict[str, tuple[float, float]]] = json.load(open(os.path.join(DATA_DIR, "search_spaces.json")))
MINIMIZES: dict[str, bool] = json.load(open(os.path.join(DATA_DIR, "minimizes.json")))


class OlympusSurrogateAPI:
    def __init__(self, dataset_id: int):
        self._dataset_name = DATASET_NAMES[dataset_id]
        self._minimize = MINIMIZES[self.dataset_name]
        self._search_space = SEARCH_SPACES[self.dataset_name]
        self._config_space = self.config_space
        self._hp_names = set([name for name in self._config_space])
        with open(os.path.join(DATA_DIR, self.dataset_name, "model.pkl"), "rb") as f:
            self._surrogate: RandomForestRegressor = pickle.load(f)

    def __call__(self, eval_config: dict[str, float]) -> float:
        self._validate_config(eval_config)
        config = {name: eval_config[name] for name in self._search_space}
        return self._surrogate.predict(pd.DataFrame([config]))[0]

    def _validate_config(self, eval_config: dict[str, float]) -> None:
        if any(name not in self._hp_names for name in eval_config):
            raise ValueError(
                f"Keys of eval_config must be identical to {list(self._hp_names)}, but got {eval_config=}."
            )

        for name in self._config_space:
            hp = self._config_space.get_hyperparameter(name)
            if name not in eval_config:
                raise KeyError(f"eval_config must have a key named {name}")

            val = eval_config[name]
            if val < hp.lower or val > hp.upper:
                raise ValueError(f"{name} must be in [{hp.lower}, {hp.upper}], but got {val}.")

    @property
    def config_space(self) -> CS.ConfigurationSpace:
        config_space = CS.ConfigurationSpace()
        config_space.add_hyperparameters(
            [
                CS.UniformFloatHyperparameter(name=name, lower=val_range[0], upper=val_range[1])
                for name, val_range in self._search_space.items()
            ]
        )
        return config_space

    @property
    def dataset_name(self) -> str:
        return self._dataset_name
