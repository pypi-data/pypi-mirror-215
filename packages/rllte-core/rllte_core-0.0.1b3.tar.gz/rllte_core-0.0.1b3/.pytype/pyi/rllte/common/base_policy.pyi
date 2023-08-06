# (generated with --quick)

import gymnasium as gym
import pathlib
import torch as th
from torch import nn
from typing import Any, Callable, Dict, List, Optional, Type, Union

Path: Type[pathlib.Path]

class BasePolicy(Any):
    __doc__: str
    action_dim: Any
    action_range: List[Union[float, int]]
    action_shape: Any
    action_type: str
    feature_dim: int
    hidden_dim: int
    init_method: Callable
    obs_shape: Any
    opt_class: Any
    opt_kwargs: Optional[Dict[str, Any]]
    def __init__(self, observation_space, action_space, feature_dim: int, hidden_dim: int, opt_class: type = ..., opt_kwargs: Optional[Dict[str, Any]] = ..., init_method: Callable = ...) -> None: ...
    def act(self, obs, training: bool = ...) -> Any: ...
    def freeze(self) -> None: ...
    def load(self, path: str) -> None: ...
    def save(self, path: pathlib.Path, pretraining: bool = ...) -> None: ...
