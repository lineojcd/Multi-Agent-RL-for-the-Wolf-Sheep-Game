import gym
from gym import spaces
import pygame
import numpy as np

import copy
import importlib
import time
from multiprocessing import Pool, TimeoutError
# from kingsheep import *
from config import *
import os
from mlp_player import MLPPlayer
import time 

debug = False
verbosity = 5
graphics = False
slowdown = 0.0

class KsField:
    """Implements a Kingsheep Game Field"""

    def __init__(self, filepath):
        # initialize the field with empty cells.
        self.field = [[CELL_EMPTY for x in range(FIELD_WIDTH)] for y in range(FIELD_HEIGHT)]
        self.read_field(filepath)
        self.init_field = copy.deepcopy(self.field)
        self.score1 = 0
        self.score2 = 0
        self.grading1 = 0
        self.grading2 = 0
        self.name1 = 'Player 1'
        self.name2 = 'Player 2'
        self.verbosity = 1000

    def reset(self):
        self.field = copy.deepcopy(self.init_field)
        self.score1 = 0
        self.score2 = 0
        self.grading1 = 0
        self.grading2 = 0
        self.name1 = 'Player 1'
        self.name2 = 'Player 2'
        self.verbosity = 1000
    # Field related functions

    def read_field(self, fp):
        file = open(fp, 'r')
        for lineno, line in enumerate(file, 1):
            # turn the line into a string, strip the tangling \n and then assign it to the field variable
            self.field[lineno - 1] = list(str(line).strip('\n'))

    def get_field(self):
        return copy.deepcopy(self.field)

    def print_ks(self):
        if verbosity > 3:
            i = -1
            for line in self.field:
                i = i + 1
                print('{:2d}  {}'.format(i, ''.join(line)))
            print('    0123456789012345678')


        if verbosity > 0:
            print('Scores: {}: {:3d}   {}: {:3d}'.format(self.name1, self.score1, self.name2, self.score2))

    # Movement

    def get_position(self,figure):
        # Next statement is a list comprehension.
        # it first generated a list of all x's in self. field, where figure is in that particular x
        # it then returns the first element (which is the row that contaions the figure),
        # as we know that there is only one of each of these figures
        x = [x for x in self.field if figure in x][0]
        return (self.field.index(x), x.index(figure))

    def new_position(self, x_old, y_old, move):
        if move == MOVE_LEFT:
            return (x_old, y_old-1)
        elif move == MOVE_RIGHT:
            return (x_old, y_old+1)
        elif move == MOVE_UP:
            return (x_old-1, y_old)
        elif move == MOVE_DOWN:
            return (x_old+1, y_old)

    def valid(self, figure, x_new, y_new):
        # Rule book valid moves

        # Neither the sheep nor the wolf, can step on a square outside the map. Imagine the map is surrounded by fences.
        if x_new > FIELD_HEIGHT - 1:
            return False
        elif x_new < 0:
            return False
        elif y_new > FIELD_WIDTH -1:
            return False
        elif y_new < 0:
            return False

        # Neither the sheep nor the wolf, can enter a square with a fence on.
        if self.field[x_new][y_new] == CELL_FENCE:
            return False

        # Wolfs can not step on squares occupied by the opponents wolf (wolfs block each other).
        # Wolfs can not step on squares occupied by the sheep of the same player .
        if figure == CELL_WOLF_1:
            if self.field[x_new][y_new] == CELL_WOLF_2:
                return False
            elif self.field[x_new][y_new] == CELL_SHEEP_1:
                return False
        elif figure == CELL_WOLF_2:
            if self.field[x_new][y_new] == CELL_WOLF_1:
                return False
            elif self.field[x_new][y_new] == CELL_SHEEP_2:
                return False


        # Sheep can not step on squares occupied by the wolf of the same player.
        # Sheep can not step on squares occupied by the opposite sheep.
        if figure == CELL_SHEEP_1:
            if self.field[x_new][y_new] == CELL_SHEEP_2 or \
                self.field[x_new][y_new] == CELL_WOLF_1:
                return False
        elif figure == CELL_SHEEP_2:
            if self.field[x_new][y_new] == CELL_SHEEP_1 or \
                    self.field[x_new][y_new] == CELL_WOLF_2:
                return False

        return True

    def award(self, figure):
        if figure == CELL_RHUBARB:
            return AWARD_RHUBARB
        elif figure == CELL_GRASS:
            return AWARD_GRASS
        else:
            return 0


    def move(self, figure, move,reason):
        if move != MOVE_NONE:
            (x_old, y_old) = self.get_position(figure)
            (x_new, y_new) = self.new_position(x_old, y_old, move)

            if self.valid(figure, x_new, y_new):
                target_figure = self.field[x_new][y_new]

                # wolf of player1 catches the sheep of player2 the game ends immediately and player1 wins and
                # is awarded all the points for the current run and vice versa

                # If the sheep steps on a food object, the food object is consumed (removed from the map) and a score
                # is awarded.

                if figure == CELL_SHEEP_1:
                    if target_figure == CELL_WOLF_2:    
                        self.field[x_old][y_old] = CELL_SHEEP_1_d
                        self.score2 += self.score1
                        self.score1 = -100
                        return True,'sheep1 suicide'
                    else:
                        # self.score1 += self.award(target_figure)
                        self.score1 = self.award(target_figure)

                elif figure == CELL_SHEEP_2:
                    if target_figure == CELL_WOLF_1:    
                        self.field[x_old][y_old] = CELL_SHEEP_2_d
                        self.score1 += self.score2
                        self.score2 = -1 
                        return True, 'sheep2 suicide'
                    else:
                        self.score2 += self.award(target_figure)

                # If the wolf steps on a food object, the food object gets removed but no score is awarded.

                elif figure == CELL_WOLF_1:
                    if target_figure == CELL_SHEEP_2:   
                        self.field[x_new][y_new] = CELL_SHEEP_2_d
                        self.score1 = 100
                        # self.score1 += self.score2
                        self.score2 = -1 
                        return True, 'sheep2 eaten'
                    else: 
                        self.score1 = -1 * self.award(target_figure)

                elif figure == CELL_WOLF_2:
                    if target_figure == CELL_SHEEP_1:   
                        self.field[x_new][y_new] = CELL_SHEEP_1_d
                        self.score2 += self.score1
                        self.score1 = -1 
                        return True, 'sheep1 eaten'

                # actual figure move
                self.field[x_new][y_new] = figure
                self.field[x_old][y_old] = CELL_EMPTY
                return False,reason
            
            else: #if move is not valid
                # print("your move is not valid, reason is ", reason)
                return False,reason
        
        else: #if move = none
            return False,reason




class WolfSheepEnv(gym.Env):
    def __init__(self,figure):
        super(WolfSheepEnv, self).__init__()

        self.figure = figure
        mod2 = importlib.import_module("random_player")
        player2class = getattr(mod2, "RandomPlayer")

        if verbosity > 2:
            print('\n >>> Starting up Kingsheep\n')

        self.ks = KsField("resources/test.map")
        self.player = MLPPlayer()
        player2 = player2class()


        # ks.name1 = player1.name
        self.ks.name2 = player2.name
        
        self.player_sheep = self.player.get_sheep_model()
        self.player_wolf = self.player.get_wolf_model()

        self.ks.verbosity = verbosity
        self.steps = 0

        self.map = self.ks.get_field()

        self.mapping = {'.': 0, 'W': 1, 'S': 2, 'g': 3, 'r': 4, '#': 5, 's': 6, 'w': 7,'U':8,'u':9}
        # self.rev_mapping = { 0:'.', 1:'W', 2:'S', 3:'g', 4:'r', 5:'#', 6:'s', 7:'w',8:'U',9:'u'}

        self.grid_size = (len(self.map), len(self.map[0]))
        self.action_space = spaces.Discrete(5)  # Up, Down, Left, Right, None
        
        # transform the map to a numeric grid
        self.state = self.reset()
        self.observation_space = spaces.Box(low=0, high=16, shape=self.state.shape, dtype=np.uint8)
        # self.current_position = self.ks.get_position(CELL_SHEEP_1)#self.start_position.copy()CELL_WOLF_1
        self.current_position = self.ks.get_position(self.figure)#self.start_position.copy()

    def transform_map(self):
        numeric_map = [[self.mapping[char] for char in row] for row in self.map]
        return np.array(numeric_map)




    def reset(self):
        self.ks.reset()
        # self.current_position = self.ks.get_position(CELL_SHEEP_1)
        self.current_position = self.ks.get_position(self.figure)
        # Reset step counter
        self.steps = 0
        
        teacher_action, vector = self.player.move_sheep_costum(1,self.ks.get_field(),self.player_sheep) 
        self.state = np.array(vector)
        return self.state


    # MOVE_NONE = 0
    # MOVE_UP = -1
    # MOVE_DOWN = 1
    # MOVE_LEFT = -2
    # MOVE_RIGHT = 2
    def step(self, action):
        # print(teacher_action,action)
        if action == 0: action = -1
        if action == 1: action = 1
        if action == 2: action = -2
        if action == 3: action = 2
        if action == 4: action = 0
        
        reward = 0
        teacher_action, vector = self.player.move_sheep_costum(1,self.ks.get_field(),self.player_sheep)
        teacher_action= teacher_action[0]
        # action = teacher_action
        # print(teacher_action,action)

        if action == teacher_action: reward += 0
        # elif action == -1* teacher_action: reward += -3
        else: reward += -0.001
        
        # result2_game_over = self.ks.move(CELL_SHEEP_1, action, '')[0]
        result2_game_over = self.ks.move(self.figure, action, '')[0]

        
        # Increase step counter
        self.steps += 1
        
        done = self.steps >= 100 or result2_game_over

        reward += -0.2 + self.ks.score1  # Every step costs -0.5.
         
        self.state = np.array(vector)
        return self.state, reward, done, {}



if __name__ == '__main__':
    from stable_baselines3 import PPO

    # Instantiate the environment
    env = WolfSheepEnv(CELL_SHEEP_1)

    # Path to the saved model file
    model_file = "best_model_vector_ppo_sheep copy.zip"

    # Load the saved model
    model_ppo = PPO.load(model_file)

    # Run a single episode using the loaded model
    obs = env.reset()
    done = False
    while not done:
        action, _ = model_ppo.predict(obs)
        obs, reward, done, info = env.step(action)
        os.system('clear')
        # print(action)
        print(env.ks.print_ks())
        time.sleep(0.1)
