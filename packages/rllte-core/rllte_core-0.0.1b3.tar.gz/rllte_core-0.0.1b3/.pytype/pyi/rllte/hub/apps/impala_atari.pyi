# (generated with --quick)

import argparse
import os
import rllte.agent.impala
from typing import Any, Type

IMPALA: Type[rllte.agent.impala.IMPALA]
agent: rllte.agent.impala.IMPALA
args: argparse.Namespace
env: Any
eval_env: Any
parser: argparse.ArgumentParser

def make_atari_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., frame_stack: int = ..., distributed: bool = ...) -> Any: ...
