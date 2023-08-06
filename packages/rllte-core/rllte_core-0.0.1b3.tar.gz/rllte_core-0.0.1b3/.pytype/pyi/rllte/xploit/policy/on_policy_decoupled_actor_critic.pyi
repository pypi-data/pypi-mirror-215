# (generated with --quick)

import gymnasium as gym
import itertools
import pathlib
import rllte.common.base_policy
import rllte.common.utils
import rllte.xploit.policy.on_policy_shared_actor_critic
import torch as th
from torch import nn
from torch.nn import functional as F
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union

BasePolicy: Type[rllte.common.base_policy.BasePolicy]
BoxActor: Type[rllte.xploit.policy.on_policy_shared_actor_critic.BoxActor]
DiscreteActor: Type[rllte.xploit.policy.on_policy_shared_actor_critic.DiscreteActor]
Distribution: Any
ExportModel: Type[rllte.common.utils.ExportModel]
MultiBinaryActor: Type[rllte.xploit.policy.on_policy_shared_actor_critic.MultiBinaryActor]
Path: Type[pathlib.Path]

_T = TypeVar('_T')

class OnPolicyDecoupledActorCritic(rllte.common.base_policy.BasePolicy):
    __doc__: str
    actor: Union[rllte.xploit.policy.on_policy_shared_actor_critic.BoxActor, rllte.xploit.policy.on_policy_shared_actor_critic.DiscreteActor, rllte.xploit.policy.on_policy_shared_actor_critic.MultiBinaryActor]
    actor_encoder: Any
    actor_opt: Any
    actor_params: itertools.chain
    critic: Any
    critic_encoder: Any
    critic_opt: Any
    critic_params: itertools.chain
    dist: Any
    gae: Any
    def __init__(self, observation_space, action_space, feature_dim: int, hidden_dim: int, opt_class: type = ..., opt_kwargs: Optional[Dict[str, Any]] = ..., init_method: Callable = ...) -> None: ...
    def act(self, obs, training: bool = ...) -> Any: ...
    def evaluate_actions(self, obs, actions = ...) -> tuple: ...
    def freeze(self, encoder, dist) -> None: ...
    def get_value(self, obs) -> Any: ...
    def load(self, path: str, device) -> None: ...
    def save(self, path: pathlib.Path, pretraining: bool = ...) -> None: ...

def deepcopy(x: _T, memo: Optional[Dict[int, Any]] = ..., _nil = ...) -> _T: ...
