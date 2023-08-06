# (generated with --quick)

import gymnasium as gym
import pathlib
import rllte.common.base_agent
import torch as th
from rllte.common import utils
from typing import Dict, Optional, Type

BaseAgent: Type[rllte.common.base_agent.BaseAgent]
Path: Type[pathlib.Path]

class OffPolicyAgent(rllte.common.base_agent.BaseAgent):
    __doc__: str
    eval_every_steps: int
    global_episode: int
    global_step: int
    num_init_steps: int
    training: bool
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., pretraining: bool = ..., num_init_steps: int = ..., eval_every_steps: int = ...) -> None: ...
    def eval(self) -> Dict[str, float]: ...
    def freeze(self) -> None: ...
    def mode(self, training: bool = ...) -> None: ...
    def train(self, num_train_steps: int = ..., init_model_path: Optional[str] = ...) -> None: ...
    def update(self) -> Dict[str, float]: ...
