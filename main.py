"""
Created on 20 Oct 2016

@author: master_smily
"""
from _csv import writer

import pygame
from os import name, system
from pygame import event
from pygame.time import get_ticks
from random import choice

BLUE = (10, 10, 200)
RED = (250, 0, 0)
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
X = int(25)  # int(input('x_blocks: '))
Y = int(20)  # int(input('y_blocks: '))
D = int(30)
R = int(D / 3)


class SolveMethod:
    type = choice(["Depth solved", "Breadth solved"])

    def __call__(self):
        if self.type == "Depth solved":
            print('SolveMethod: self.method == "Depth solved"')
            return Agent.breadth()
        elif self.type == "Breadth solved":
            print('SolveMethod: self.method == "Breadth solved"')
            return Agent.depth()
        else:
            raise Exception("SolveMethod Error")


def console_clear():
    system('cls' if name == 'nt' else 'clear')


if __name__ == "__main__":
    from Environment import Environment
    from Agent import Agent as Ai

    print('everything declared')
    ev = []
    # loop = strtobool(input("loop?"))
    SolveMethod = SolveMethod()

    while True:
        pygame.init()
        Env = Environment()

        c_method = Env.depth()
        Agent = Ai(Env.gui)
        Env.gui = Agent.gui
        solve_start = get_ticks()
        SolveMethod.type = SolveMethod()
        # s_method =
        solve_end = get_ticks()
        ev.append(event.get())
        with open("stats.csv", 'a') as csvfile:
            writer(csvfile).writerow([c_method, SolveMethod.type, solve_end - solve_start])

        pygame.quit()
        print('\n')
        # break  # debug no loop
