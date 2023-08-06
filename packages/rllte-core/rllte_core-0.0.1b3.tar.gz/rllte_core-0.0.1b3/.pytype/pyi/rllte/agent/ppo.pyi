# (generated with --quick)

import gymnasium as gym
import numpy as np
import rllte.common.on_policy_agent
import rllte.xploit.encoder.identity_encoder
import rllte.xploit.encoder.mnih_cnn_encoder
import rllte.xploit.policy.on_policy_shared_actor_critic
import rllte.xploit.storage.vanilla_rollout_storage
import rllte.xplore.distribution.bernoulli
import rllte.xplore.distribution.categorical
import rllte.xplore.distribution.diagonal_gaussian
import torch as th
from torch import nn
from typing import Callable, Dict, Type

Bernoulli: Type[rllte.xplore.distribution.bernoulli.Bernoulli]
Categorical: Type[rllte.xplore.distribution.categorical.Categorical]
DiagonalGaussian: Type[rllte.xplore.distribution.diagonal_gaussian.DiagonalGaussian]
IdentityEncoder: Type[rllte.xploit.encoder.identity_encoder.IdentityEncoder]
MnihCnnEncoder: Type[rllte.xploit.encoder.mnih_cnn_encoder.MnihCnnEncoder]
OnPolicyAgent: Type[rllte.common.on_policy_agent.OnPolicyAgent]
OnPolicySharedActorCritic: Type[rllte.xploit.policy.on_policy_shared_actor_critic.OnPolicySharedActorCritic]
VanillaRolloutStorage: Type[rllte.xploit.storage.vanilla_rollout_storage.VanillaRolloutStorage]

class PPO(rllte.common.on_policy_agent.OnPolicyAgent):
    __doc__: str
    aug_coef: float
    clip_range: float
    clip_range_vf: float
    ent_coef: float
    eps: float
    lr: float
    max_grad_norm: float
    n_epochs: int
    network_init_method: str
    vf_coef: float
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., pretraining: bool = ..., num_steps: int = ..., eval_every_episodes: int = ..., feature_dim: int = ..., batch_size: int = ..., lr: float = ..., eps: float = ..., hidden_dim: int = ..., clip_range: float = ..., clip_range_vf: float = ..., n_epochs: int = ..., vf_coef: float = ..., ent_coef: float = ..., aug_coef: float = ..., max_grad_norm: float = ..., network_init_method: str = ...) -> None: ...
    def update(self) -> Dict[str, float]: ...

def get_network_init(method: str = ...) -> Callable: ...
