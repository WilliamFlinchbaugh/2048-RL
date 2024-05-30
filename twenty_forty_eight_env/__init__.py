from .twenty_forty_eight_env import TwentyFortyEightEnv
from gymnasium.envs.registration import register

__all__ = [TwentyFortyEightEnv]

register(
    id="TwentyFortyEight-v0", 
    entry_point="twenty_forty_eight_env:TwentyFortyEightEnv",
    max_episode_steps=10_000,
)