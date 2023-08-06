# (generated with --quick)

import gymnasium as gym
import rllte.common.distributed_agent
import rllte.xploit.encoder.identity_encoder
import rllte.xploit.encoder.mnih_cnn_encoder
import rllte.xploit.policy.distributed_actor_learner
import rllte.xploit.storage.distributed_storage
import rllte.xplore.distribution.categorical
import rllte.xplore.distribution.diagonal_gaussian
import threading
import torch as th
from torch import nn
from torch.nn import functional as F
from typing import Any, Callable, Dict, Tuple, Type

Categorical: Type[rllte.xplore.distribution.categorical.Categorical]
DiagonalGaussian: Type[rllte.xplore.distribution.diagonal_gaussian.DiagonalGaussian]
DistributedActorLearner: Type[rllte.xploit.policy.distributed_actor_learner.DistributedActorLearner]
DistributedAgent: Type[rllte.common.distributed_agent.DistributedAgent]
DistributedStorage: Type[rllte.xploit.storage.distributed_storage.DistributedStorage]
IdentityEncoder: Type[rllte.xploit.encoder.identity_encoder.IdentityEncoder]
MnihCnnEncoder: Type[rllte.xploit.encoder.mnih_cnn_encoder.MnihCnnEncoder]

class IMPALA(rllte.common.distributed_agent.DistributedAgent):
    __doc__: str
    baseline_coef: float
    discount: float
    ent_coef: float
    eps: float
    feature_dim: int
    lr: float
    max_grad_norm: float
    network_init_method: str
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., num_steps: int = ..., num_actors: int = ..., num_learners: int = ..., num_storages: int = ..., feature_dim: int = ..., batch_size: int = ..., lr: float = ..., eps: float = ..., hidden_dim: int = ..., use_lstm: bool = ..., ent_coef: float = ..., baseline_coef: float = ..., max_grad_norm: float = ..., discount: float = ..., network_init_method: str = ...) -> None: ...
    def update(self, batch: dict, init_actor_states: tuple, lock = ...) -> Dict[str, tuple]: ...

class VTraceLoss:
    __doc__: str
    clip_pg_rho_threshold: float
    clip_rho_threshold: float
    def __call__(self, batch) -> Tuple[Any, Any, Any]: ...
    def __init__(self, clip_rho_threshold: float = ..., clip_pg_rho_threshold: float = ...) -> None: ...
    def compute_ISW(self, target_dist, behavior_dist, action) -> Any: ...

def get_network_init(method: str = ...) -> Callable: ...
