"""
Created on 20 Oct 2016

@author: william
"""

import pygame
from pygame import display

from environment import grid

x_blocks = 10  # int(input('x_blocks: '))
y_blocks = 10  # int(input('y_blocks: '))
length = 30
GUI = display.set_mode([x_blocks * length + 1, y_blocks * length + 1])

if __name__ == "__main__":
    pygame.init()
    grid(GUI, x_blocks, y_blocks, length)
