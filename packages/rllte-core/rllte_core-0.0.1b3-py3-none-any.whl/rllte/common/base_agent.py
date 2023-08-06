# =============================================================================
# MIT License

# Copyright (c) 2023 Reinforcement Learning Evolution Foundation

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================


import os
import random
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import gymnasium as gym
import numpy as np
import pynvml
import torch as th

# try to load torch_npu
try:
    import torch_npu as torch_npu  # type: ignore
except Exception:
    pass

from rllte.common.base_augmentation import BaseAugmentation as Augmentation
from rllte.common.base_distribution import BaseDistribution as Distribution
from rllte.common.base_encoder import BaseEncoder as Encoder
from rllte.common.base_policy import BasePolicy as Policy
from rllte.common.base_reward import BaseIntrinsicRewardModule as IntrinsicRewardModule
from rllte.common.base_storage import BaseStorage as Storage
from rllte.common.logger import Logger
from rllte.common.timer import Timer


class BaseAgent(ABC):
    """Base class of the agent.

    Args:
        env (gym.Env): A Gym-like environment for training.
        eval_env (gym.Env): A Gym-like environment for evaluation.
        tag (str): An experiment tag.
        seed (int): Random seed for reproduction.
        device (str): Device (cpu, cuda, ...) on which the code should be run.
        pretraining (bool): Turn on pre-training model or not.
        feature_dim (int): Number of features extracted by the encoder.

    Returns:
        Base agent instance.
    """

    def __init__(
        self,
        env: gym.Env,
        eval_env: Optional[gym.Env] = None,
        tag: str = "default",
        seed: int = 1,
        device: str = "cpu",
        pretraining: bool = False,
    ) -> None:
        # change work dir
        path = Path.cwd() / "logs" / tag / datetime.now().strftime("%Y-%m-%d-%I-%M-%S")
        os.makedirs(path)
        os.chdir(path=path)

        # basic setup
        self.work_dir = Path.cwd()
        self.logger = Logger(log_dir=self.work_dir)
        self.timer = Timer()
        self.device = th.device(device)
        self.pretraining = pretraining
        self.num_eval_episodes = 10
        self.global_step = 0
        self.global_episode = 0
        self.logger.info("Invoking RLLTE Engine...")
        self.logger.info(f"Experiment Tag: {tag}")

        # env setup
        self.env = env
        self.eval_env = eval_env
        self.get_env_info(env)

        # set seed
        self.seed = seed
        th.manual_seed(seed=seed)
        if th.cuda.is_available():
            th.cuda.manual_seed_all(seed)
        np.random.seed(seed)
        random.seed(seed)

        # get device info
        if "cuda" in device:
            try:
                device_id = int(device[-1])
            except Exception:
                device_id = 0
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(device_id)
            device_name = pynvml.nvmlDeviceGetName(handle)
            self.logger.info(f"Running on {device_name}...")
        elif "npu" in device:
            npu_name = self.get_npu_name()
            self.logger.info(f"Running on HUAWEI Ascend {npu_name}...")
        else:
            self.logger.info("Running on CPU...")

        # placeholder for Encoder, Storage, Distribution, Augmentation, Reward
        self.encoder = None
        self.policy = None
        self.storage = None
        self.dist = None
        self.aug = None
        self.irs = None

    def get_env_info(self, env: gym.Env) -> None:
        """Get the environment information.

        Args:
            env (gym.Env): A Gym-like environment for training.

        Returns:
            None.
        """
        observation_space = env.observation_space
        action_space = env.action_space
        self.num_envs = env.num_envs
        self.obs_shape = observation_space.shape
        if action_space.__class__.__name__ == "Discrete":
            self.action_shape = action_space.shape
            self.action_dim = int(action_space.n)
            self.action_type = "Discrete"
            self.action_range = [0, int(action_space.n) - 1]
        elif action_space.__class__.__name__ == "Box":
            self.action_shape = action_space.shape
            self.action_dim = action_space.shape[0]
            self.action_type = "Box"
            self.action_range = [
                float(action_space.low[0]),
                float(action_space.high[0]),
            ]
        elif action_space.__class__.__name__ == "MultiBinary":
            self.action_shape = action_space.shape
            self.action_dim = action_space.shape[0]
            self.action_type = "MultiBinary"
            self.action_range = [0, 1]
        else:
            raise NotImplementedError("Unsupported action type!")

    def get_npu_name(self) -> str:
        """Get NPU name."""
        str_command = "npu-smi info"
        out = os.popen(str_command)
        text_content = out.read()
        out.close()
        lines = text_content.split("\n")
        npu_name_line = lines[6]
        name_part = npu_name_line.split("|")[1]
        npu_name = name_part.split()[-1]

        return npu_name

    def check(self) -> None:
        """Check the compatibility of selected modules."""
        self.logger.debug("Checking the Compatibility of Modules...")
        self.logger.debug(f"Selected Agent: {self.__class__.__name__}")
        self.logger.debug(f"Selected Encoder: {self.encoder.__class__.__name__}")
        self.logger.debug(f"Selected Policy: {self.policy.__class__.__name__}")
        self.logger.debug(f"Selected Storage: {self.storage.__class__.__name__}")
        # class for `Distribution` and instance for `Noise`
        dist_name = self.dist.__name__ if isinstance(self.dist, type) else self.dist.__class__.__name__
        self.logger.debug(f"Selected Distribution: {dist_name}")

        if self.aug is not None:
            self.logger.debug(f"Use Augmentation: True, {self.aug.__class__.__name__}")
        else:
            self.logger.debug("Use Augmentation: False")

        if self.pretraining:
            assert self.irs is not None, "When the pre-training mode is turned on, an intrinsic reward must be specified!"

        if self.irs is not None:
            self.logger.debug(f"Use Intrinsic Reward: True, {self.irs.__class__.__name__}")
        else:
            self.logger.debug("Use Intrinsic Reward: False")

        if self.pretraining:
            self.logger.info("Pre-training Mode On...")
        self.logger.debug("Check Accomplished. Start Training...")

    def set(
        self,
        encoder: Optional[Any] = None,
        policy: Optional[Any] = None,
        storage: Optional[Any] = None,
        distribution: Optional[Any] = None,
        augmentation: Optional[Any] = None,
        reward: Optional[Any] = None,
    ) -> None:
        """Set a module for the agent.

        Args:
            encoder (Optional[Any]): An encoder of `rllte.xploit.encoder` or a custom encoder.
            policy (Optional[Any]): A policy of `rllte.xploit.policy` or a custom policy.
            storage (Optional[Any]): A storage of `rllte.xploit.storage` or a custom storage.
            distribution (Optional[Any]): A distribution of `rllte.xplore.distribution` or a custom distribution.
            augmentation (Optional[Any]): An augmentation of `rllte.xplore.augmentation` or a custom augmentation.
            reward (Optional[Any]): A reward of `rllte.xplore.reward` or a custom reward.

        Returns:
            None.
        """
        if encoder is not None:
            assert isinstance(encoder, Encoder), "The `encoder` must be a subclass of `BaseEncoder`!"
            if self.encoder is not None:
                assert (
                    self.encoder.feature_dim == encoder.feature_dim
                ), "The feature dimension of `encoder` must be equal to the previous one!"
            self.encoder = encoder

        if policy is not None:
            assert isinstance(policy, Policy), "The `policy` must be a subclass of `BasePolicy`!"
            self.policy = policy

        if storage is not None:
            assert isinstance(storage, Storage), "The `storage` must be a subclass of `BaseStorage`!"
            self.storage = storage

        if distribution is not None:
            try:
                assert issubclass(distribution, Distribution), "The `distribution` must be a subclass of `BaseDistribution`!"
            except TypeError:
                assert isinstance(distribution, Distribution), "The `noise` must be a subclass of `BaseDistribution`!"
            self.dist = distribution

        if augmentation is not None:
            assert isinstance(augmentation, Augmentation), "The `augmentation` must be a subclass of `BaseAugmentation`!"
            self.aug = augmentation

        if reward is not None:
            assert isinstance(reward, IntrinsicRewardModule), "The `reward` must be a subclass of `BaseIntrinsicRewardModule`!"
            self.irs = reward

    @abstractmethod
    def mode(self) -> None:
        """Set the training mode."""

    @abstractmethod
    def update(self) -> Dict[str, float]:
        """Update the agent."""

    @abstractmethod
    def freeze(self) -> None:
        """Freeze the structure of the agent."""

    @abstractmethod
    def train(self) -> None:
        """Training function."""

    @abstractmethod
    def eval(self) -> Optional[Dict[str, float]]:
        """Evaluation function."""
