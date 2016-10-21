'''
Created on 20 Oct 2016
Modified on __updated__
@author: william
'''
from random import randint

from pygame import display, draw
import pygame

from environment import grid


def grid(gui, x, y, scale=15, color=(255, 255, 255)):
    for i in range(x + 1):
        draw.line(gui, (color), (i * scale, 0), (i * scale, y * scale))
    for i in range(y + 1):
        draw.line(gui, (color), (0, i * scale), (x * scale, i * scale))


def create():
    pygame.init()
    x_blocks = 50  # int(input('x_blocks: '))
    y_blocks = 50  # int(input('y_blocks: '))
    scale = 18
    gui = display.set_mode([x_blocks * scale + 1, y_blocks * scale + 1])

    while True:  # debug
        # color=(randint(0,255),randint(0,255),randint(0,255))
        grid.draw(gui, x_blocks, y_blocks, scale)
        display.update()
