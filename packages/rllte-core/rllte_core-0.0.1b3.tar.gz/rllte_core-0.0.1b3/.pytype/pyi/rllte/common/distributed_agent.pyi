# (generated with --quick)

import collections
import gymnasium as gym
import numpy as np
import os
import pathlib
import rllte.common.base_agent
import threading
import time
import torch as th
import traceback
from torch import multiprocessing as mp
from typing import Any, Dict, Optional, Type

BaseAgent: Type[rllte.common.base_agent.BaseAgent]
Path: Type[pathlib.Path]
deque: Type[collections.deque]

class DistributedAgent(rllte.common.base_agent.BaseAgent):
    __doc__: str
    batch_size: Any
    env: Any
    lr_scheduler: Any
    num_actors: int
    num_learners: int
    num_steps: int
    num_storages: int
    training: bool
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., num_steps: int = ..., num_actors: int = ..., num_learners: int = ..., num_storages: int = ..., **kwargs) -> None: ...
    def eval(self) -> Dict[str, float]: ...
    def freeze(self) -> None: ...
    def mode(self, training: bool = ...) -> None: ...
    def run(self, env: Environment, actor_idx: int, free_queue, full_queue, init_actor_state_storages: list) -> None: ...
    def train(self, num_train_steps: int = ..., init_model_path: Optional[str] = ...) -> None: ...
    def update(self) -> Dict[str, float]: ...

class Environment:
    __doc__: str
    action_dim: Any
    action_type: str
    env: Any
    episode_return: Any
    episode_step: Any
    def __init__(self, env) -> None: ...
    def _format_obs(self, obs: np.ndarray) -> Any: ...
    def close(self) -> None: ...
    def reset(self, seed) -> Dict[str, Any]: ...
    def step(self, action) -> Dict[str, Any]: ...
