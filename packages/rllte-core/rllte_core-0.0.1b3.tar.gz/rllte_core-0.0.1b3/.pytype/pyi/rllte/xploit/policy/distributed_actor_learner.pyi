# (generated with --quick)

import gymnasium as gym
import pathlib
import rllte.common.base_distribution
import rllte.common.base_policy
import rllte.common.utils
import torch as th
from torch import nn
from torch.nn import functional as F
from typing import Any, Callable, Dict, Optional, Tuple, Type, TypeVar, Union

BasePolicy: Type[rllte.common.base_policy.BasePolicy]
Distribution: Type[rllte.common.base_distribution.BaseDistribution]
ExportModel: Type[rllte.common.utils.ExportModel]
Path: Type[pathlib.Path]

_T = TypeVar('_T')

class ActorCritic(Any):
    __doc__: str
    action_dim: int
    action_range: list
    action_shape: tuple
    action_type: str
    actor: Union[BoxActor, DiscreteActor]
    critic: Any
    dist: rllte.common.base_distribution.BaseDistribution
    encoder: Any
    lstm: Any
    policy_reshape_dim: int
    use_lstm: bool
    def __init__(self, obs_shape: tuple, action_shape: tuple, action_dim: int, action_type: str, action_range: list, feature_dim: int, hidden_dim: int = ..., use_lstm: bool = ...) -> None: ...
    def act(self, inputs: Dict[str, Any], lstm_state: tuple = ..., training: bool = ...) -> Tuple[Dict[str, Any], tuple]: ...
    def get_dist(self, outputs) -> rllte.common.base_distribution.BaseDistribution: ...
    def init_state(self, batch_size: int) -> tuple: ...

class BoxActor(Any):
    __doc__: str
    actor_logstd: Any
    actor_mu: Any
    def __init__(self, obs_shape: tuple, action_dim: int, feature_dim: int, hidden_dim: int) -> None: ...
    def forward(self, obs) -> Any: ...
    def get_policy_outputs(self, obs) -> Tuple[Any, Any]: ...

class DiscreteActor(Any):
    __doc__: str
    actor: Any
    def __init__(self, obs_shape: tuple, action_dim: int, feature_dim: int, hidden_dim: int) -> None: ...
    def forward(self, obs) -> Any: ...
    def get_policy_outputs(self, obs) -> Tuple[Any]: ...

class DistributedActorLearner(rllte.common.base_policy.BasePolicy):
    __doc__: str
    actor: ActorCritic
    learner: ActorCritic
    opt: Any
    def __init__(self, observation_space, action_space, feature_dim: int, hidden_dim: int = ..., opt_class: type = ..., opt_kwargs: Optional[Dict[str, Any]] = ..., init_method: Callable = ..., use_lstm: bool = ...) -> None: ...
    def freeze(self, encoder, dist: rllte.common.base_distribution.BaseDistribution) -> None: ...
    def load(self, path: str, device) -> None: ...
    def save(self, path: pathlib.Path) -> None: ...
    def to(self, device) -> None: ...

def deepcopy(x: _T, memo: Optional[Dict[int, Any]] = ..., _nil = ...) -> _T: ...
