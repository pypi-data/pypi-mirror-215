# (generated with --quick)

import gymnasium as gym
import pathlib
import rllte.common.base_policy
import rllte.common.utils
import rllte.xploit.policy.off_policy_deterministic_actor_double_critic
import torch as th
from torch import nn
from typing import Any, Callable, Dict, Optional, Tuple, Type

BasePolicy: Type[rllte.common.base_policy.BasePolicy]
Distribution: Any
DoubleCritic: Type[rllte.xploit.policy.off_policy_deterministic_actor_double_critic.DoubleCritic]
ExportModel: Type[rllte.common.utils.ExportModel]
Path: Type[pathlib.Path]

class OffPolicyStochasticActorDoubleCritic(rllte.common.base_policy.BasePolicy):
    __doc__: str
    actor: Any
    actor_opt: Any
    critic: rllte.xploit.policy.off_policy_deterministic_actor_double_critic.DoubleCritic
    critic_opt: Any
    critic_target: rllte.xploit.policy.off_policy_deterministic_actor_double_critic.DoubleCritic
    dist: Any
    encoder: Any
    encoder_opt: Any
    log_std_max: Any
    log_std_min: Any
    def __init__(self, observation_space, action_space, feature_dim: int = ..., hidden_dim: int = ..., opt_class: type = ..., opt_kwargs: Optional[Dict[str, Any]] = ..., init_method: Callable = ..., log_std_range: tuple = ...) -> None: ...
    def act(self, obs, training: bool = ..., step: int = ...) -> Tuple[Any]: ...
    def freeze(self, encoder, dist) -> None: ...
    def get_dist(self, obs, step: int) -> Any: ...
    def load(self, path: str, device) -> None: ...
    def save(self, path: pathlib.Path, pretraining: bool = ...) -> None: ...
