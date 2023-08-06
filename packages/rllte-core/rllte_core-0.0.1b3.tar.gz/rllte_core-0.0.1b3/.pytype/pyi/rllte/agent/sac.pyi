# (generated with --quick)

import gymnasium as gym
import numpy as np
import rllte.common.off_policy_agent
import rllte.xploit.encoder.identity_encoder
import rllte.xploit.encoder.tassa_cnn_encoder
import rllte.xploit.policy.off_policy_stochastic_actor_double_critic
import rllte.xploit.storage.vanilla_replay_storage
import rllte.xplore.distribution.squashed_normal
import torch as th
from rllte.agent import utils
from torch.nn import functional as F
from typing import Annotated, Any, Callable, Dict, Tuple, Type

IdentityEncoder: Type[rllte.xploit.encoder.identity_encoder.IdentityEncoder]
OffPolicyAgent: Type[rllte.common.off_policy_agent.OffPolicyAgent]
OffPolicyStochasticActorDoubleCritic: Type[rllte.xploit.policy.off_policy_stochastic_actor_double_critic.OffPolicyStochasticActorDoubleCritic]
SquashedNormal: Type[rllte.xplore.distribution.squashed_normal.SquashedNormal]
TassaCnnEncoder: Type[rllte.xploit.encoder.tassa_cnn_encoder.TassaCnnEncoder]
VanillaReplayStorage: Type[rllte.xploit.storage.vanilla_replay_storage.VanillaReplayStorage]

class SAC(rllte.common.off_policy_agent.OffPolicyAgent):
    __doc__: str
    alpha: Annotated[Any, 'property']
    betas: Tuple[float, ...]
    critic_target_tau: float
    discount: float
    eps: float
    fixed_temperature: bool
    log_alpha: Any
    log_alpha_opt: Any
    lr: float
    network_init_method: str
    target_entropy: Any
    update_every_steps: int
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., pretraining: bool = ..., num_init_steps: int = ..., eval_every_steps: int = ..., feature_dim: int = ..., batch_size: int = ..., lr: float = ..., eps: float = ..., hidden_dim: int = ..., critic_target_tau: float = ..., update_every_steps: int = ..., log_std_range: Tuple[float, ...] = ..., betas: Tuple[float, ...] = ..., temperature: float = ..., fixed_temperature: bool = ..., discount: float = ..., network_init_method: str = ...) -> None: ...
    def update(self) -> Dict[str, float]: ...
    def update_actor_and_alpha(self, obs, weights) -> Dict[str, float]: ...
    def update_critic(self, obs, action, reward, terminated, truncateds, next_obs, weights, aug_obs, aug_next_obs) -> Dict[str, float]: ...

def get_network_init(method: str = ...) -> Callable: ...
