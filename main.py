"""
Created on 20 Oct 2016

@author: master_smily
"""
from os import environ
from random import randint

import pygame
from pygame import display, draw
from pygame.constants import NOFRAME
from pygame.time import Clock


def grid(x, y, d=30, color=(255, 255, 255, 255)):
    """
crates a grid
    :param surface:
    :type surface:
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


def depth(x, y, fps=100, d=30):
    """
creates maze with depth search algorithm.
    :param fps:
    :param gui:
    :param d:
    :type d:
    :param x:
    :type x:
    :param y:
    :type y:
    """
    white = (255, 255, 255, 255)
    stack = []
    x_pos = d * randint(0, x - 1)
    y_pos = d * randint(0, y - 1)
    log = [[x_pos, y_pos]]
    loop = 0
    while True:
        loop += 1
        side = []
        # check if all sides are available
        if gui.get_at((int(x_pos + d / 2), int(y_pos))) == white:
            if [x_pos, y_pos - d] not in log:
                side.append('upp')
        if gui.get_at((int(x_pos + d), int(y_pos + d / 2))) == white:
            if [x_pos + d, y_pos] not in log:
                side.append('right')
        if gui.get_at((int(x_pos + d / 2), int(y_pos + d))) == white:
            if [x_pos, y_pos + d] not in log:
                side.append('down')
        if gui.get_at((x_pos, int(y_pos + d / 2))) == white:
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
            print((x_pos, y_pos), stack)
            x_pos = stack[-1][0]
            y_pos = stack[-1][1]
            stack.pop()
        else:
            break
        display.update()

if __name__ == "__main__":
    environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
    x_blocks = 45  # int(input('x_blocks: '))
    y_blocks = 24  # int(input('y_blocks: '))
    length = 30
    gui = display.set_mode([x_blocks * length + 1, y_blocks * length + 1], NOFRAME)

    pygame.init()
    grid(x_blocks, y_blocks)
    depth(x_blocks, y_blocks)
    while True:
        pass
