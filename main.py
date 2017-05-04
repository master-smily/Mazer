"""
Created on 20 Oct 2016

@author: master_smily
"""
import csv
from os import name, system
from random import choice

import pygame
from pygame import event
from pygame.constants import QUIT
from pygame.time import get_ticks

BLUE = (10, 10, 200, 50)
RED = (250, 0, 0)
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
X = int(66)  # 66
Y = int(34)  # 34
D = int(20)  # 20
R = int(D / 3)


class SolveMethod:
    stack = []
    done = False
    stage = None

    def __call__(self):
        Agent.gui = Env.gui
        Agent.stage = Env.stage
        if self.stack:
            solve = self.stack.pop()
            if solve == "Depth":
                solve = Agent.breadth()
            elif solve == "Breadth":
                solve = Agent.depth()
            elif solve == "A*":
                solve = Agent.a_star()
            elif solve == "A* g/2":
                solve = Agent.a_star(0.5) + " g/2"
            elif solve == "A* g/4":
                solve = Agent.a_star(0.25) + " g/4"
            elif solve == "A* no_g":
                solve = Agent.a_star(0) + " g(n)=0"
            else:
                raise Exception("SolveMethod Error")
        else:
            self.new_stack()
            return self.__call__()
        # Env.gui
        return solve

    def new_stack(self):
        base_stack = ["Depth", "Breadth", "A*", "A* g/4", "A* g/2", "A* no_g"]
        while base_stack:
            next_item = choice(base_stack)
            base_stack.remove(next_item)
            self.stack.append(next_item)
        Env.stage = None
        Env.depth()


def console_clear():
    system('cls' if name == 'nt' else 'clear')


if __name__ == "__main__":
    from Environment import Environment
    from Agent import Agent as Ai

    print('everything declared')
    ev = []
    # loop = strtobool(input("loop?"))
    SolveMethod = SolveMethod()
    done = False
    stage = None
    pygame.init()
    Env = Environment()

    while not done:
        Agent = Ai()
        solve_start = get_ticks()
        s_method = SolveMethod()
        solve_end = get_ticks()
        SolveMethod.gui = Agent.gui
        if s_method is not None:
            with open("stats.csv", 'a', newline='') as csvfile:
                stats = csv.writer(csvfile)
                stats.writerow([s_method, solve_end - solve_start])
        if event.peek(QUIT):
            done = True
        # break  # debug no loop
    pygame.quit()
