'''
Created on 20 Oct 2016

@author: william
'''

import pygame
from pygame import display

import environment

scale = 30
x_blocks = 10  # int(input('x_blocks: '))
y_blocks = 10  # int(input('y_blocks: '))
gui = display.set_mode([x_blocks * scale + 1, y_blocks * scale + 1])

if __name__ == '__main__':
    pygame.init()
    environment.create_grid(x_blocks, y_blocks, scale)
