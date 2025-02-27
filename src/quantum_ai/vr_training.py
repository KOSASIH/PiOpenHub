import numpy as np
import random
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.envs import DummyVecEnv

class VREnvironment(gym.Env):
    def __init__(self):
        super(VREnvironment, self).__init__()
        self.action_space = gym.spaces.Discrete(3)  # Actions: 0 = Task A, 1 = Task B, 2 = Task C
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)
        self.state = 0.5  # Initial state
        self.done = False

    def step(self, action):
        # Simulate the effect of the action on the state
        if action == 0:  # Task A
            self.state += random.uniform(0.1, 0.3)
        elif action == 1:  # Task B
            self.state += random.uniform(-0.1, 0.1)
        elif action == 2:  # Task C
            self.state += random.uniform(-0.3, 0.1)

        # Reward based on the state
        reward = 1.0 if self.state >= 1.0 else -0.1
        self.done = self.state >= 1.0  # End if the task is completed
        return np.array([self.state]), reward, self.done, {}

    def reset(self):
        self.state = 0.5  # Reset to initial state
        return np.array([self.state])

class VRTraining:
    def __init__(self):
        self.env = DummyVecEnv([lambda: VREnvironment()])
        self.model = PPO("MlpPolicy", self.env, verbose=1)

    def train(self, timesteps=10000):
        self.model.learn(total_timesteps=timesteps)

    def simulate_training(self):
        obs = self.env.reset()
        for _ in range(100):
            action, _ = self.model.predict(obs)
            obs, reward, done, _ = self.env.step(action)
            if done:
                obs = self.env.reset()

# Example usage
if __name__ == "__main__":
    vr_training = VRTraining()
    print("Training the VR model...")
    vr_training.train(timesteps=20000)

    print("Simulating training...")
    vr_training.simulate_training()
