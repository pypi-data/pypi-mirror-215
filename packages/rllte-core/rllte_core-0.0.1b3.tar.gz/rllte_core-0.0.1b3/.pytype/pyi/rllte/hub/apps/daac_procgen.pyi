# (generated with --quick)

import argparse
import rllte.agent.daac
import rllte.xploit.encoder.espeholt_residual_encoder
from typing import Any, Type

DAAC: Type[rllte.agent.daac.DAAC]
EspeholtResidualEncoder: Type[rllte.xploit.encoder.espeholt_residual_encoder.EspeholtResidualEncoder]
agent: rllte.agent.daac.DAAC
args: argparse.Namespace
encoder: rllte.xploit.encoder.espeholt_residual_encoder.EspeholtResidualEncoder
env: Any
eval_env: Any
feature_dim: int
parser: argparse.ArgumentParser

def make_procgen_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., gamma: float = ..., num_levels: int = ..., start_level: int = ..., distribution_mode: str = ...) -> Any: ...
