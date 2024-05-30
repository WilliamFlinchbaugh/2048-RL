import gymnasium as gym
import twenty_forty_eight_env
from stable_baselines3 import PPO

env = gym.make("TwentyFortyEight-v0", render_mode="rgb_array")

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./ppo_2048_tensorboard/")
model.learn(total_timesteps=1_000_000)

vec_env = model.get_env()
obs = vec_env.reset()
for i in range(1000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    vec_env.render("human")
    # VecEnv resets automatically
    # if done:
    #   obs = vec_env.reset()