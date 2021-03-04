
import pygame
import sys
from pygame.locals import *

from classes.snakeClass import Snake
from classes.appleClass import Apple
from classes.gameClass import Game
from classes.agentClass import Agent
from API import get_state

from keras.utils import to_categorical
import random
from random import randint
import numpy as np

import matplotlib.pyplot as plt

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

FPS = 144

WIDTH = 885
HEIGHT = 500

offsetx = 30
offsety = 25
borderwidth = 10


def define_parameters():
    params = dict()
    # Neural Network
    params["epsilon_decay_linear"] = 1/75
    params["learning_rate"] = 0.0005
    params["first_layer_size"] = 50  # neurons in the first layer
    params["second_layer_size"] = 300   # neurons in the second layer
    params["third_layer_size"] = 50   # neurons in the third layer
    params["episodes"] = 200
    # Settings
    params["weights_path"] = "weights/final.hdf5"
    params["load_weights"] = True
    params["train"] = False
    params["plot_score"] = True
    params["show_every"] = 1

    return params


class App():
    def __init__(self): 
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.border = pygame.Surface((game.WIDTH + borderwidth * 2, game.HEIGHT + borderwidth * 2))
        self.myfont = pygame.font.SysFont("Arial", 30)

    def main_loop(self):
        counter_games = 1
        score = 0
        score_plot = []
        avg_plot = []
        max_score = 0
        if params['load_weights']:
            agent.model.load_weights(params["weights_path"])
            print("weights loaded")

        while counter_games < params["episodes"]:
            score = 0
            while not game.crash:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        counter_games = params["episodes"]
                        break

                if not params["train"]:
                    agent.epsilon = 0
                else:
                    agent.epsilon = 1 - (counter_games * params["epsilon_decay_linear"])
                # get old state
                state_old = get_state(game.snake, game.apple, game)

                if random.uniform(0, 1) < agent.epsilon:
                    final_move = to_categorical(randint(0, 3), num_classes=4)
                else:
                    prediction = agent.model.predict(state_old.reshape((1,11)))
                    final_move = to_categorical(np.argmax(prediction[0]), num_classes=4)
                
                if np.array_equal(final_move, [1,0,0,0]):
                    game.snake.direction = "right"
                elif np.array_equal(final_move, [0,1,0,0]):
                    game.snake.direction = "up"
                elif np.array_equal(final_move, [0,0,1,0]):
                    game.snake.direction = "down"
                elif np.array_equal(final_move, [0,0,0,1]):
                    game.snake.direction = "left"

                score = len(game.snake.body) - 3
                if score > max_score:
                    max_score = score

                game.check_snake_collision()
                game.snake.move()
                
                state_new = get_state(game.snake, game.apple, game)

                # set reward for the new state
                reward = agent.set_reward(game.snake, game.check_snake_collision())

                if params["train"]:
                    agent.train(state_old, final_move, reward, state_new, game.check_snake_collision())
                
                if counter_games % params["show_every"] == 0:
                    game.main_loop(True)
                    self.render(state_old, final_move, score)
                    pygame.display.update()
                    self.clock.tick(FPS)

                if game.crash:
                    score_plot.append(score)
                    avg = sum(score_plot) / len(score_plot)
                    avg_plot.append(avg)
                    print(f"ep: {counter_games} | score: {score} | avg: {avg} | best: {max_score}")
                    

            counter_games += 1
            game.crash = False

        if params["plot_score"]:
            # plot all games
            plt.plot(range(len(score_plot)), score_plot, "o", label="Skóre", linewidth=3)
            plt.plot(range(len(avg_plot)), avg_plot, "o", color="red", label="Priemer", linewidth=2)
            plt.xlabel("Epizódy")
            plt.ylabel("Skóre")
            plt.legend()
            plt.show()

        if params["train"]:
            agent.model.save_weights(params["weights_path"])


    def event_handler(self):
        """
        Handles input
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def render(self, state, output, c_score):
        self.screen.fill((WHITE))
        self.screen.blit(self.border, (offsetx - borderwidth, offsety - borderwidth/2))           
        self.screen.blit(game.surface, (offsetx, offsetx))
        input_tensor = self.myfont.render(f"Vstupný tenzor: {state}", False, BLACK)
        output_tensor = self.myfont.render(f"Výstupný tenzor: {output}", False, BLACK)
        curr_score = self.myfont.render(f"Skóre: {c_score}", False, BLACK)
        self.screen.blit(input_tensor,(offsetx + game.WIDTH + 30, 60))
        self.screen.blit(output_tensor,(offsetx + game.WIDTH + 30, 110))
        self.screen.blit(curr_score,(offsetx + game.WIDTH + 30, 160))


if __name__ == "__main__":
    pygame.init()
    
    game = Game()
    game.snake = Snake()
    game.apple = Apple(game.WIDTH, game.HEIGHT, game.CELL_WIDTH, game.snake.body)
    app = App()

    params = define_parameters()
    agent = Agent(params)

    app.main_loop()

