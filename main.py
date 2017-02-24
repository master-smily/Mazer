"""
Created on 20 Oct 2016

@author: master_smily
"""
from _csv import writer
from os import environ, name, system
from random import choice

import pygame
from pygame import event
from pygame.time import get_ticks

BLUE = (10, 10, 200)
RED = (250, 0, 0)
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
X = int(25)  # int(input('x_blocks: '))
Y = int(20)  # int(input('y_blocks: '))
D = int(30)
R = int(D / 3)


def console_clear():
    system('cls' if name == 'nt' else 'clear')


def solve_method():
    if s_method == "Depth solved":
        return Agent.depth()
    elif s_method == "Breadth solved":
        return Agent.breadth()
    else:
        return choice([Agent.depth(), Agent.breadth()])


if __name__ == "__main__":
    from Environment import Environment
    from Agent import Agent as Ai

    print('everything declared')
    environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
    ev = []
    # loop = strtobool(input("loop?"))
    while True:
        pygame.init()
        Env = Environment()

        c_method = Env.depth()
        Agent = Ai(Env.gui)
        Env.gui = Agent.gui
        solve_start = get_ticks()
        s_method = solve_method()
        # s_method =
        solve_end = get_ticks()
        ev.append(event.get())
        with open("stats.csv", 'w') as csvfile:
            writer(csvfile).writerow([c_method, s_method, solve_end - solve_start, solve_end])
        # raise Exception
        # if not loop:
        #     pygame.quit()
        #     break
        # else:
        #     quit()
        pygame.quit()
        print('\n\n\n')
        # break  # debug no loop
