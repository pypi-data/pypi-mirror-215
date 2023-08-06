# (generated with --quick)

import gymnasium as gym
import numpy as np
import rllte.common.base_reward
import torch as th
from torch import nn
from typing import Any, Type

BaseIntrinsicRewardModule: Type[rllte.common.base_reward.BaseIntrinsicRewardModule]

class Encoder(Any):
    __doc__: str
    linear: Any
    trunk: Any
    def __init__(self, obs_shape: tuple, action_dim: int, latent_dim: int) -> None: ...
    def forward(self, obs) -> Any: ...

class REVD(rllte.common.base_reward.BaseIntrinsicRewardModule):
    __doc__: str
    alpha: float
    average_divergence: bool
    first_update: bool
    k: int
    last_encoded_obs: list
    random_encoder: Any
    def __init__(self, observation_space, action_space, device: str = ..., beta: float = ..., kappa: float = ..., latent_dim: int = ..., alpha: float = ..., k: int = ..., average_divergence: bool = ...) -> None: ...
    def compute_irs(self, samples: dict, step: int = ...) -> Any: ...
    def update(self, samples: dict) -> None: ...
