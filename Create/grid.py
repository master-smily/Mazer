'''
Created on 21 Oct 2016

@author: william
'''

def draw(gui, x, y, scale=15, color=(255,255,255), ):
    for i in range(x+1):
        draw.line(gui, (color), (i*scale,0), (i*scale,y*scale))
    for i in range(y+1):
        draw.line(gui, (color), (0,i*scale), (x*scale,i*scale))