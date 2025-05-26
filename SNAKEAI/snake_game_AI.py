import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
from math import log

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20
SPEED = 50000  # Speed of the snake, higher is faster
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 128, 255)
RED = (255, 0, 0)
 
class SnakeGameAI:
    def __init__(self, w = 640, h = 480):
        self.w = w
        self.h = h
        
        # Initialize the game window
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.reset()  # Reset the game state
       
        # self.running = True
    def reset(self):
        self.snake_head = Point(self.w/2, self.h/2)
        self. snake_body = [self.snake_head, Point(self.snake_head.x - BLOCK_SIZE, self.snake_head.y), Point(self.snake_head.x - (2*BLOCK_SIZE), self.snake_head.y)]
        self.snake_direction = Direction.RIGHT
        self.food = None
        self.place_food()
        self.score = 0
        self.frame_iteration = 0  # To keep track of the number of frames

    def place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake_body:
            self.place_food()  

    def play(self, action=None):
        self.frame_iteration += 1
        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # move the snake
        self.move(action) # update the snake's position
        self.snake_body.insert(0, self.snake_head)  # add new head to the snake body

        # chaeck if game over
        reward = 0
        self.frame_iteration += 1
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake_body):
            game_over = True
            reward = -10
            # distance reward = At time step t, we denote the snake’s lengthas Ltand denote the distance between the target and the headof the snake as Dt.
            # log((len(self.snake_body) + sqrt(self.food.x - self.snake_head.x)**2 + (self.food.y - self.snake_head.y)**2)/(len(self.snake_body) + sqrt(self.food.x - self.snake_body[0].x)**2 + (self.food.y - self.snake_body[0].y)**2))
            # reward = log((len(self.snake_body) + np.sqrt((self.food.x - self.snake_head.x)**2 + (self.food.y - self.snake_head.y)**2)) /
            #             (len(self.snake_body) + np.sqrt((self.food.x - self.snake_body[0].x)**2 + (self.food.y - self.snake_body[0].y)**2)), 2)
            return reward, game_over, self.score

        # place the food
        if self.snake_head == self.food:
            reward = 10  # reward for eating food
            # reward = log((len(self.snake_body) + np.sqrt((self.food.x - self.snake_head.x)**2 + (self.food.y - self.snake_head.y)**2)) /
            #             (len(self.snake_body) + np.sqrt((self.food.x - self.snake_body[0].x)**2 + (self.food.y - self.snake_body[0].y)**2)), 2)
            self.score += 1
            self.place_food()
        else:
            self.snake_body.pop()

        # update ui and clock 
        self.update_ui()
        self.clock.tick(SPEED)

        # return game over and score
        return reward,  game_over, self.score
        # pass

    def update_ui(self):
        self.display.fill(BLACK)

        for point in self.snake_body:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(point.x+4, point.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = pygame.font.SysFont('arial', 20).render(f'Score: {self.score}', True, WHITE)
        self.display.blit(text, [2,2])
        pygame.display.flip()
    
    def move(self, action):
        # [straight, right, left]
         
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.snake_direction)

        if np.array_equal(action, [1, 0, 0]):  # straight
            direction = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):  # right
            idx = (idx + 1) % 4
            direction = clock_wise[idx]
        elif np.array_equal(action, [0, 0, 1]):  # left
            idx = (idx - 1) % 4
            direction = clock_wise[idx]

        self.snake_direction = direction

        if direction == Direction.RIGHT:
            self.snake_head = Point(self.snake_head.x + BLOCK_SIZE, self.snake_head.y)
        elif direction == Direction.LEFT:
            self.snake_head = Point(self.snake_head.x - BLOCK_SIZE, self.snake_head.y)
        elif direction == Direction.UP:
            self.snake_head = Point(self.snake_head.x, self.snake_head.y - BLOCK_SIZE)
        elif direction == Direction.DOWN:
            self.snake_head = Point(self.snake_head.x, self.snake_head.y + BLOCK_SIZE)

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.snake_head
        # check if snake collides with walls
        if (pt.x < 0 or pt.x >= self.w or
            pt.y < 0 or pt.y >= self.h):
            return True
         
        # check if snake collides with itself
        if pt in self.snake_body[1:]:
            return True
        return False
