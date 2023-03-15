import numpy as np
from deepsnake.lib.games import SnakeGame
import pygame


# Define the Q-table and
action_size = 4
state_size = 576
q_table = np.zeros((state_size, action_size))

# Define learning rate
alpha = 0.8
gamma = 0.95
num_episodes = 5000


snake_game = SnakeGame()


# Train the Q-Learning algorithm
for episode in range(num_episodes):
    snake_game._create_new_food()
    eating = False
    while not eating:
        # Choose an action
        state = snake_game.get_state()
        action_idx = np.argmax(
            q_table[state, :] + np.random.randn(1, action_size) * (1.0 / (episode + 1))
        )
        action = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT][action_idx]

        # Take the action and observe the new state and reward
        snake_game.read_key(action)
        snake_game.play_step()

        next_state = snake_game.get_state()

        # Update the Q-table
        q_table[state, action_idx] = (1 - alpha) * q_table[
            state, action_idx
        ] + alpha * (snake_game.score + gamma * np.max(q_table[next_state, :]))

"""
# Test the trained Q-Learning algorithm
state = env.reset()
done = False
while not done:
    # Choose an action
    action = np.argmax(q_table[state, :])

    # Take the action
    state, reward, done, _ = env.step(action)
    env.render()
"""
