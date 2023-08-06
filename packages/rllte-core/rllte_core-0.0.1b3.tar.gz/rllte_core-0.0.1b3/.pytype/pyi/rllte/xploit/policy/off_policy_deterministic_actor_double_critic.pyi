# (generated with --quick)

import gymnasium as gym
import pathlib
import rllte.common.base_policy
import rllte.common.utils
import torch as th
from torch import nn
from typing import Any, Callable, Dict, Optional, Type

BasePolicy: Type[rllte.common.base_policy.BasePolicy]
Distribution: Any
ExportModel: Type[rllte.common.utils.ExportModel]
Path: Type[pathlib.Path]

class DoubleCritic(Any):
    Q1: Any
    Q2: Any
    __doc__: str
    def __init__(self, action_dim: int, feature_dim: int = ..., hidden_dim: int = ...) -> None: ...
    def forward(self, obs, action) -> tuple: ...

class OffPolicyDeterministicActorDoubleCritic(rllte.common.base_policy.BasePolicy):
    __doc__: str
    actor: Any
    actor_opt: Any
    critic: DoubleCritic
    critic_opt: Any
    critic_target: DoubleCritic
    dist: Any
    encoder: Any
    encoder_opt: Any
    def __init__(self, observation_space, action_space, feature_dim: int = ..., hidden_dim: int = ..., opt_class: type = ..., opt_kwargs: Optional[Dict[str, Any]] = ..., init_method: Callable = ...) -> None: ...
    def act(self, obs, training: bool = ..., step: int = ...) -> Any: ...
    def freeze(self, encoder, dist) -> None: ...
    def get_dist(self, obs, step: int) -> Any: ...
    def load(self, path: str, device) -> None: ...
    def save(self, path: pathlib.Path, pretraining: bool = ...) -> None: ...
