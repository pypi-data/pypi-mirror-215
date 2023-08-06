# (generated with --quick)

import gymnasium as gym
import rllte.common.off_policy_agent
import rllte.xploit.encoder.identity_encoder
import rllte.xploit.encoder.tassa_cnn_encoder
import rllte.xploit.policy.off_policy_deterministic_actor_double_critic
import rllte.xploit.storage.nstep_replay_storage
import rllte.xplore.augmentation.identity
import rllte.xplore.augmentation.random_shift
import rllte.xplore.distribution.truncated_normal_noise
import torch as th
from rllte.agent import utils
from torch.nn import functional as F
from typing import Callable, Dict, Type

Identity: Type[rllte.xplore.augmentation.identity.Identity]
IdentityEncoder: Type[rllte.xploit.encoder.identity_encoder.IdentityEncoder]
NStepReplayStorage: Type[rllte.xploit.storage.nstep_replay_storage.NStepReplayStorage]
OffPolicyAgent: Type[rllte.common.off_policy_agent.OffPolicyAgent]
OffPolicyDeterministicActorDoubleCritic: Type[rllte.xploit.policy.off_policy_deterministic_actor_double_critic.OffPolicyDeterministicActorDoubleCritic]
RandomShift: Type[rllte.xplore.augmentation.random_shift.RandomShift]
TassaCnnEncoder: Type[rllte.xploit.encoder.tassa_cnn_encoder.TassaCnnEncoder]
TruncatedNormalNoise: Type[rllte.xplore.distribution.truncated_normal_noise.TruncatedNormalNoise]

class DrQv2(rllte.common.off_policy_agent.OffPolicyAgent):
    __doc__: str
    critic_target_tau: float
    eps: float
    lr: float
    network_init_method: str
    update_every_steps: int
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., pretraining: bool = ..., num_init_steps: int = ..., eval_every_steps: int = ..., feature_dim: int = ..., batch_size: int = ..., lr: float = ..., eps: float = ..., hidden_dim: int = ..., critic_target_tau: float = ..., update_every_steps: int = ..., network_init_method: str = ...) -> None: ...
    def update(self) -> Dict[str, float]: ...
    def update_actor(self, obs) -> Dict[str, float]: ...
    def update_critic(self, obs, action, reward, discount, next_obs) -> Dict[str, float]: ...

def get_network_init(method: str = ...) -> Callable: ...
