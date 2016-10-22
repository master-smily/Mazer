'''
Created on 20 Oct 2016

@author: william
'''
import random

from pygame import display, draw

from main import GUI

scale = 30
def grid(gui, x, y, scale=15, color=(255, 255, 255)):
    for i in range(x):
        draw.line(gui, (color), (i * scale, 0), (i * scale, y * scale))
    for i in range(y):
        draw.line(gui, (color), (0, i * scale), (x * scale, i * scale))
    draw.rect(gui, (250, 0, 0), (0, 0, x * scale + 1, y * scale + 1), 1)


def create_grid(x, y):
    grid(GUI, x, y, scale)

    while True:  # debug
        # color=(randint(0,255),randint(0,255),randint(0,255))
        display.update()


def depth(x, y):
    blocks = x * y
    x_pos = random.randint(0, x - 1)
    y_pos = random.randint(0, y - 1)
    while blocks is not None:
        side = ['upp', 'right', 'left', 'down']
        # check if all sides are available
        if x_pos + scale == (x * scale):
            print('')

            # if side == 1:
            #    x_pos =+  scale
            #    draw.line(gui, (0,0,0),())
            # elif side == 2:
