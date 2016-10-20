'''
Created on 20 Oct 2016

@author: william
'''

from pygame import init, display, draw
from random import randint
from Create import grid

init
x_blocks=50#int(input('x_blocks: '))
y_blocks=50#int(input('y_blocks: '))
scale=18
gui=display.set_mode([x_blocks*scale+1, y_blocks*scale+1])
    
while True: #debug
    #color=(randint(0,255),randint(0,255),randint(0,255))
    grid.draw(gui, x_blocks, y_blocks, scale)
    display.update()