"""
Created on 20 Oct 2016

@author: master_smily
"""
from _csv import writer
from os import environ, name, system
from random import randint

import pygame
from pygame import display, draw, event
from pygame.time import Clock, get_ticks

BLUE = (10, 10, 200)
RED = (250, 0, 0)
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
X = int(25)  # int(input('x_blocks: '))
Y = int(20)  # int(input('y_blocks: '))
D = int(30)
R = int(D / 3)


class Agent:
    def __init__(self):
        self.pos = {'x': int(D / 2),
                    'y': int(D / 2)}
        self.no_pos = {'wall': [0, 0],
                       'cord': [0, 0]}
        self.log = list()
        self.stack = list()
        self.fps = 250
        self.update()
        self.pos_upp = dict()
        self.pos_right = dict()
        self.pos_down = dict()
        self.pos_left = dict()

    def sides(self):
        if self.pos['x'] <= D:
            self.pos_left = self.no_pos
        else:
            self.pos_left = {'wall': [int(self.pos['x'] - D / 2), self.pos['y']],
                             'cord': [int(self.pos['x'] - D), self.pos['y']]}
        if self.pos['y'] <= D:
            self.pos_upp = self.no_pos
        else:
            self.pos_upp = {'wall': [self.pos['x'], int(self.pos['y'] - D / 2)],
                            'cord': [self.pos['x'], int(self.pos['y'] - D)]}
        if self.pos['x'] >= D * X:
            self.pos_right = self.no_pos
        else:
            self.pos_right = {'wall': [int(self.pos['x'] + D / 2), self.pos['y']],
                              'cord': [int(self.pos['x'] + D), self.pos['y']]}
        if self.pos['y'] >= D * Y:
            self.pos_down = self.no_pos
        else:
            self.pos_down = {'wall': [self.pos['x'], int(self.pos['y'] + D / 2)],
                             'cord': [self.pos['x'], int(self.pos['y'] + D)]}

    def move(self, side=None, boost=False):
        step = 15
        for i in range(int(D / step)):
            if side == 'upp':
                self.pos['y'] -= step
            if side == 'right':
                self.pos['x'] += step
            if side == 'down':
                self.pos['y'] += step
            if side == 'left':
                self.pos['x'] -= step
            self.update(boost)

    def update(self, boost=False):
        if boost:
            Clock().tick(self.fps * 2)
        else:
            Clock().tick(self.fps)
        Env.gui.blit(stage, [0, 0])
        draw.circle(Env.gui, BLUE, [self.pos['x'], self.pos['y']], R)
        display.update()

    def bot(self):
        print('Agent.bot')
        while True:
            side = self.side()
            if self.pos == {'x': X * D - D / 2, 'y': Y * D - D / 2}:
                print("bot done")
                break
            elif side:
                side = side[randint(0, side.index(side[-1]))]
                self.stack.append(side)
                self.move(side)
                self.log.append([self.pos['x'], self.pos['y']])
            elif self.stack:
                self.move(self.reverse_side(), True)
                self.stack.pop()
            else:
                raise Exception
        return "Depth solved"

    def side(self):
        # print('Agent.side')
        self.sides()
        side = []
        if Env.gui.get_at(self.pos_upp['wall']) == BLACK \
                and self.pos_upp['cord'] not in self.log:
            side.append('upp')
        if Env.gui.get_at(self.pos_right['wall']) == BLACK \
                and self.pos_right['cord'] not in self.log:
            side.append('right')
        if Env.gui.get_at(self.pos_down['wall']) == BLACK \
                and self.pos_down['cord'] not in self.log:
            side.append('down')
        if Env.gui.get_at(self.pos_left['wall']) == BLACK \
                and self.pos_left['cord'] not in self.log:
            side.append('left')
        return side

    def reverse_side(self):
        if self.stack[-1] == 'upp':
            return 'down'
        if self.stack[-1] == 'down':
            return 'upp'
        if self.stack[-1] == 'right':
            return 'left'
        if self.stack[-1] == 'left':
            return 'right'


def console_clear():
    system('cls' if name == 'nt' else 'clear')


if __name__ == "__main__":
    from Environment import Environment

    print('everything declared')
    environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
    ev = []
    # loop = strtobool(input("loop?"))
    while True:
        pygame.init()
        Env = Environment()

        Env.grid()
        c_method = Env.depth()
        stage = Env.gui.convert()
        Agent = Agent()
        solve_start = get_ticks()
        s_method = Agent.bot()
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
        print('\n\n\n\n')
