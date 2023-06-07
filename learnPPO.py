from stable_baselines3 import DQN, A2C, PPO
import matplotlib.pyplot as plt
from kingsheep_gym import  WolfSheepEnv
import os 
from config import *

# Instantiate the environment
env = WolfSheepEnv(CELL_WOLF_1)

# Initialize the reward logs

reward_log_ppo = []

# Number of episodes for training
n_episodes = 2000

plt.ion()  # Turn on interactive mode for matplotlib
fig, axs = plt.subplots()


# PPO
model_ppo = PPO("MlpPolicy", env, verbose=1, device='cuda')
# Define the path to save the best model
save_path = "best_model_ppo_wolf.zip"
# Set the best mean reward to negative infinity
best_mean_reward = float('-inf')

for episode in range(n_episodes):
    print(episode)
    obs = env.reset()
    total_reward = 0
    done = False
    while not done:
        action, _states = model_ppo.predict(obs)
        obs, reward, done, info = env.step(action)
        # os.system('clear')
        # print(env.ks.print_ks(),end='')
        total_reward += reward

    # After each episode, update the model
    model_ppo.learn(total_timesteps=1)
        # Log the reward
    reward_log_ppo.append(total_reward)



    # Check if the mean reward has improved
    mean_reward = sum(reward_log_ppo[-10:]) / 10  # Calculate the mean reward over the last 10 episodes
    if mean_reward > best_mean_reward:
        print('saved')
        best_mean_reward = mean_reward
        model_ppo.save(save_path)  # Save the best model

    # Log the reward
    reward_log_ppo.append(total_reward)

    # Clear the current plot and plot the reward log
    # axs.clear()
    # axs.plot(reward_log_ppo)
    # axs.set_title('PPO Reward over time')
    # axs.set_xlabel('Episode')
    # axs.set_ylabel('Total reward')
    # plt.draw()
    # plt.pause(0.001)  # Pause to update the plot

# plt.ioff()  # Turn off interactive mode
# plt.show()
axs.plot(reward_log_ppo)
axs.set_title('PPO Reward over time')
axs.set_xlabel('Episode')
axs.set_ylabel('Total reward')
plt.savefig('foo.pdf')