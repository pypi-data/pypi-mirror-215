# (generated with --quick)

import collections
import gymnasium as gym
import numpy as np
import rllte.common.base_reward
import torch as th
from torch import nn
from torch.nn import functional as F
from typing import Any, Type

BaseIntrinsicRewardModule: Type[rllte.common.base_reward.BaseIntrinsicRewardModule]
DataLoader: Any
TensorDataset: Any
deque: Type[collections.deque]

class Encoder(Any):
    __doc__: str
    linear: Any
    policy: Any
    trunk: Any
    def __init__(self, obs_shape: tuple, action_dim: int, latent_dim: int) -> None: ...
    def encode(self, obs) -> Any: ...
    def forward(self, obs, next_obs) -> Any: ...

class PseudoCounts(rllte.common.base_reward.BaseIntrinsicRewardModule):
    __doc__: str
    batch_size: int
    c: float
    encoder: Any
    episodic_memory: collections.deque
    k: int
    kernel_cluster_distance: float
    kernel_epsilon: float
    loss: Any
    opt: Any
    sm: float
    def __init__(self, observation_space, action_space, device: str = ..., beta: float = ..., kappa: float = ..., latent_dim: int = ..., lr: float = ..., batch_size: int = ..., capacity: int = ..., k: int = ..., kernel_cluster_distance: float = ..., kernel_epsilon: float = ..., c: float = ..., sm: float = ...) -> None: ...
    def compute_irs(self, samples: dict, step: int = ...) -> Any: ...
    def pseudo_counts(self, e) -> Any: ...
    def update(self, samples: dict) -> None: ...
