
import pygame
import sys
from pygame.locals import *

from classes.snakeClass import Snake
from classes.appleClass import Apple

# ========= CONSTANTS ===========
WIDTH = 400
HEIGHT = 400
CELL_WIDTH = 10
assert WIDTH % CELL_WIDTH == 0 and HEIGHT % CELL_WIDTH == 0, "CELL_WIDTH can't be divided by current resolution"

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


class Game():
    def __init__(self, snake=None, apple=None):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.WIDTH = 400
        self.HEIGHT = 400
        self.CELL_WIDTH = 10    
        self.snake = snake
        self.apple = apple
        self.myfont = pygame.font.SysFont("Arial", 30)
        self.crash = False

    def main_loop(self, display=True):
        self.snake.moves_left -= 1
        
        if display:
            self.surface.fill(WHITE)
            self.draw_apple()
            self.draw_snake()
            pygame.display.update()

    def display_score(self, score):
        textsurface = self.myfont.render("Score: " + str(score), False, GRAY)
        self.surface.blit(textsurface,(0,0))

    def display_moves_left(self):
        textsurface = self.myfont.render("Moves left: " + str(self.snake.moves_left), False, GRAY)
        self.surface.blit(textsurface,(0,30))

    def check_snake_collision(self):
        """
        Return True if snake crashed
        """

        for piece in self.snake.body[1:]:
            if piece == self.snake.body[0]:
                self.game_over()
                return True

        # check border collision
        if self.snake.body[0]["x"] >= self.WIDTH / self.CELL_WIDTH or self.snake.body[0]["y"] >= self.HEIGHT / self.CELL_WIDTH or self.snake.body[0]["x"] < 0 or self.snake.body[0]["y"] < 0:
            self.game_over()
            return True

        # check if snake has eaten apple
        if self.snake.body[0] == self.apple.coords:
            del self.apple
            self.apple = Apple(self.WIDTH, self.HEIGHT, self.CELL_WIDTH, self.snake.body)
            self.snake.ate = True
            self.snake.moves_left = 400
            return False

    def draw_apple(self):
        rect = pygame.Rect(self.apple.coords["x"] * self.CELL_WIDTH, self.apple.coords["y"] * self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        pygame.draw.rect(self.surface, RED, rect)

    def draw_snake(self):
        for piece in self.snake.body:
            rect = pygame.Rect(piece["x"] * self.CELL_WIDTH, piece["y"] * self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
            pygame.draw.rect(self.surface, BLACK, rect)
    
    def game_over(self):
        del self.snake
        del self.apple

        self.snake = Snake()
        self.apple = Apple(self.WIDTH, self.HEIGHT, self.CELL_WIDTH, self.snake.body)
        self.crash = True
