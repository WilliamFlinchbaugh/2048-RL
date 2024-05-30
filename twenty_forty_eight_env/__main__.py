import gymnasium as gym
import numpy as np
import pygame as pg
import twenty_forty_eight_env
from gymnasium.utils.play import play

env = gym.make("TwentyFortyEight-v0", render_mode="rgb_array")

keys_to_action = {
    (pg.K_UP,): 0,
    (pg.K_DOWN,): 1,
    (pg.K_LEFT,): 2,
    (pg.K_RIGHT,): 3
}

play(env, keys_to_action=keys_to_action, noop=4, fps=10)