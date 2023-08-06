# (generated with --quick)

import collections
import gymnasium as gym
import numpy as np
import pathlib
import rllte.common.base_agent
import torch as th
from rllte.common import utils
from typing import Any, Dict, Optional, Type

BaseAgent: Type[rllte.common.base_agent.BaseAgent]
Path: Type[pathlib.Path]
deque: Type[collections.deque]

class OnPolicyAgent(rllte.common.base_agent.BaseAgent):
    __doc__: str
    eval_every_episodes: int
    global_episode: int
    global_step: Any
    num_steps: int
    training: bool
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., pretraining: bool = ..., num_steps: int = ..., eval_every_episodes: int = ...) -> None: ...
    def eval(self) -> Dict[str, float]: ...
    def freeze(self) -> None: ...
    def mode(self, training: bool = ...) -> None: ...
    def train(self, num_train_steps: int = ..., init_model_path: Optional[str] = ...) -> None: ...
    def update(self) -> Dict[str, float]: ...
