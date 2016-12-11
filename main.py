"""
Created on 20 Oct 2016

@author: master_smily
"""
from os import environ
from random import randint

import pygame
from pygame import display, draw, event
from pygame.constants import KEYDOWN, KEYUP, K_DOWN, K_LEFT, K_RIGHT, K_UP, NOFRAME
from pygame.time import Clock

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)


def grid(x, y, d=30, color=(255, 255, 255, 255)):
    """
crates a grid
    :param x:
    :type x:
    :param y:
    :type y:
    :param d:
    :type d:
    :param color:
    :type color:
    """
    for i in range(x):
        draw.line(gui, color, (i * d, 0), (i * d, y * d), 2)
    for i in range(y):
        draw.line(gui, color, (0, i * d), (x * d, i * d), 2)
    draw.rect(gui, (250, 0, 0), (0, 0, x * d + 1, y * d + 1), 2)
    display.update()


def depth(x, y, fps=0, d=30):
    """
creates maze with depth search algorithm.
    :param fps:
    :param d:
    :type d:
    :param x:
    :type x:
    :param y:
    :type y:
    """
    stack = []
    x_pos = d * randint(0, x - 1)
    y_pos = d * randint(0, y - 1)
    log = [[x_pos, y_pos]]
    loop = 0
    while True:
        event.pump()
        loop += 1
        side = []
        # check if all sides are available
        if gui.get_at([int(x_pos + d / 2), int(y_pos)]) == WHITE:
            if [x_pos, y_pos - d] not in log:
                side.append('upp')
        if gui.get_at((int(x_pos + d), int(y_pos + d / 2))) == WHITE:
            if [x_pos + d, y_pos] not in log:
                side.append('right')
        if gui.get_at((int(x_pos + d / 2), int(y_pos + d))) == WHITE:
            if [x_pos, y_pos + d] not in log:
                side.append('down')
        if gui.get_at((x_pos, int(y_pos + d / 2))) == WHITE:
            if [x_pos - d, y_pos] not in log:
                side.append('left')
        if side:  # if side: log, stack and erase wall
            Clock().tick(fps)
            side = side[randint(0, side.index(side[-1]))]
            stack.append([x_pos, y_pos])
            if side == 'upp':
                draw.line(gui, (0, 0, 0), (x_pos, y_pos), (x_pos + d, y_pos), 2)
                y_pos -= d
            elif side == 'right':
                draw.line(gui, (0, 0, 0), (x_pos + d, y_pos), (x_pos + d, y_pos + d), 2)
                x_pos += d
            elif side == 'down':
                draw.line(gui, (0, 0, 0), (x_pos, y_pos + d), (x_pos + d, y_pos + d), 2)
                y_pos += d
            elif side == 'left':
                draw.line(gui, (0, 0, 0), (x_pos, y_pos), (x_pos, y_pos + d), 2)
                x_pos -= d
            log.append([x_pos, y_pos])
        elif stack:  # go back one step
            # print((x_pos, y_pos), stack)
            x_pos = stack[-1][0]
            y_pos = stack[-1][1]
            stack.pop()
        else:
            break
        display.update()


def play(d=30):
    r = int(d / 3)
    main = Player()
    if botmode:
        stack = []
        log = [main.pos]
        while True:
            side = []
            stack.append(main.pos)
            if gui.get_at(main.pos_upp) == BLACK and main.pos_upp not in log:
                side.append('upp')
            if gui.get_at(main.pos_right) == BLACK and main.pos_right not in log:
                side.append('right')
            if gui.get_at(main.pos_down) == BLACK and main.pos_down not in log:
                side.append('down')
            if gui.get_at(main.pos_left) == BLACK and main.pos_left not in log:
                side.append('left')
            if side:
                side = side[randint(0, side.index(side[-1]))]
                if side == 'upp':
                    pass
            log.append(main.pos)
    else:
        while True:
            for event in pygame.event.get(KEYDOWN):
                if event.key == K_UP and gui.get_at(main.pos_upp) == BLACK:
                    main.move('upp')
                if event.key == K_RIGHT and gui.get_at(main.pos_right) == BLACK:
                    main.move('right')
                if event.key == K_DOWN and gui.get_at(main.pos_down) == BLACK:
                    main.move('down')
                if event.key == K_LEFT and gui.get_at(main.pos_left) == BLACK:
                    main.move('left')


class Player:
    r = int(30 / 3)

    def __init__(self):
        self.pos = [self.r+3, self.r+3]
        self.pos_upp = [self.pos[0], self.pos[1] - (self.r + 1)]
        self.pos_right = [self.pos[0] + self.r, self.pos[1]]
        self.pos_down = [self.pos[0], self.pos[1] + self.r]
        self.pos_left = [self.pos[0] - (self.r + 1), self.pos[1]]

    def move(self, side=None):
        while True:
            self.__init__()
            gui.blit(stage, [0, 0])
            draw.circle(gui, (10, 10, 200), self.pos, self.r)
            display.update()
            pygame.event.pump()
            Clock().tick(50)
            if side == 'upp' and gui.get_at(self.pos_upp):
                self.pos[1] -= 1
            if side == 'right' and gui.get_at(self.pos_right):
                self.pos[0] += 1
            if side == 'down' and gui.get_at(self.pos_down):
                self.pos[1] += 1
            if side == 'left' and gui.get_at(self.pos_left):
                self.pos[0] -= 1
            if event.peek(KEYUP) or side is None:
                event.clear()
                break


if __name__ == "__main__":
    environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
    x_blocks = 20  # int(input('x_blocks: '))
    y_blocks = 20  # int(input('y_blocks: '))
    length = 30
    gui = display.set_mode([x_blocks * length + 1, y_blocks * length + 1], NOFRAME)

    pygame.init()
    grid(x_blocks, y_blocks)
    depth(x_blocks, y_blocks)
    stage = gui.convert()
    # botmode = strtobool(input('bot mode?'))
    botmode=0
    play()
    while True:
        pass