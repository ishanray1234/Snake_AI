import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20
SPEED = 10  # Speed of the snake, higher is faster
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 128, 255)
RED = (255, 0, 0)
 
class SnakeGame:
    def __init__(self, w = 640, h = 480):
        self.w = w
        self.h = h
        
        # Initialize the game window
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake Game")

        # init game state
        self.clock = pygame.time.Clock()
        # self.running = True
        self.snake_head = Point(self.w/2, self.h/2)
        self. snake_body = [self.snake_head, Point(self.snake_head.x - BLOCK_SIZE, self.snake_head.y), Point(self.snake_head.x - (2*BLOCK_SIZE), self.snake_head.y)]
        self.snake_direction = Direction.RIGHT
        self.food = None
        self.place_food()
        self.score = 0

    def place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake_body:
            self.place_food() 

    def play(self):
        # collect user input  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake_direction != Direction.DOWN:
                    self.snake_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.snake_direction != Direction.UP:
                    self.snake_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.snake_direction != Direction.RIGHT:
                    self.snake_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.snake_direction != Direction.LEFT:
                    self.snake_direction = Direction.RIGHT

        # move the snake
        self.move(self.snake_direction) # update the snake's position
        self.snake_body.insert(0, self.snake_head)  # add new head to the snake body

        # chaeck if game over
        game_over = False
        if self.is_collision():
            game_over = True
            return game_over, self.score

        # place the food
        if self.snake_head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake_body.pop()

        # update ui and clock 
        self.update_ui()
        self.clock.tick(SPEED)

        # return game over and score
        return game_over, self.score
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
    
    def move(self, direction):
        if direction == Direction.RIGHT:
            self.snake_head = Point(self.snake_head.x + BLOCK_SIZE, self.snake_head.y)
        elif direction == Direction.LEFT:
            self.snake_head = Point(self.snake_head.x - BLOCK_SIZE, self.snake_head.y)
        elif direction == Direction.UP:
            self.snake_head = Point(self.snake_head.x, self.snake_head.y - BLOCK_SIZE)
        elif direction == Direction.DOWN:
            self.snake_head = Point(self.snake_head.x, self.snake_head.y + BLOCK_SIZE)

    def is_collision(self):
        # check if snake collides with walls
        if (self.snake_head.x < 0 or self.snake_head.x >= self.w or
            self.snake_head.y < 0 or self.snake_head.y >= self.h):
            return True
         
        # check if snake collides with itself
        if self.snake_head in self.snake_body[1:]:
            return True
        return False

if __name__ == "__main__":
    game = SnakeGame()

    while True:
        game_over, score = game.play()
        if game_over:
            print(f"Game Over! Your score: {score}")
            break
    
    pygame.quit()