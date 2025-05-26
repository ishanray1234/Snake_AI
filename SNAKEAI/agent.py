import torch
import random
from snake_game_AI import SnakeGameAI, Point, Direction, BLOCK_SIZE, SPEED
import numpy as np
from  collections import deque
from model import Linear_QNet, QTrainer
from helper import plot  # Assuming you have a plot function in helpers.py

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001  # Learning rate

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # Randomness factor, starts at 0 and decays over time
        self.gamma = 0.9 # Discount factor for future rewards
        self.memory = deque(maxlen=MAX_MEMORY) # Memory to store past experiences
        self.model = Linear_QNet(11, 256, 3)  # Input size is 11 (state), hidden size is 256, output size is 3 (actions)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake_body[0]
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)

        dir_l = game.snake_direction == Direction.LEFT
        dir_r = game.snake_direction == Direction.RIGHT
        dir_u = game.snake_direction == Direction.UP
        dir_d = game.snake_direction == Direction.DOWN

        state = [
            (dir_r & game.is_collision(point_r)) or (dir_l & game.is_collision(point_l)) or
            (dir_u & game.is_collision(point_u)) or (dir_d & game.is_collision(point_d)),  # Danger straight

            (dir_u & game.is_collision(point_l)) or (dir_d & game.is_collision(point_r)) or
            (dir_l & game.is_collision(point_u)) or (dir_r & game.is_collision(point_d)),  # Danger left  

            (dir_d & game.is_collision(point_l)) or (dir_u & game.is_collision(point_r)) or
            (dir_r & game.is_collision(point_u)) or (dir_l & game.is_collision(point_d)),  # Danger right

            dir_r,  # Moving right
            dir_l,  # Moving left
            dir_u,  # Moving up
            dir_d,  # Moving down
            game.food.x < game.snake_head.x,  # Food left
            game.food.x > game.snake_head.x,  # Food right
            game.food.y < game.snake_head.y,  # Food up
            game.food.y > game.snake_head.y   # Food down
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > MAX_MEMORY:
            self.memory.popleft()

    def train_long_memory(self):
        if len(self.memory) >  BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        # Unzip the mini sample
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Epsilon-greedy action selection
        # self.epsilon = max(0.1, self.epsilon - 0.001) 
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]  # Default action (no move)  
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)  # Random action
            final_move[move] = 1

        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return np.array(final_move)

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        reward, done, score = game.play(final_move)

        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print(f'Game: {agent.n_games}, Score: {score}, Record: {record}')

            total_score += score
            plot_scores.append(score)
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == "__main__":
    train()