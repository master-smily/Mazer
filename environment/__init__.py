import random

from pygame import draw

from main import GUI


def grid(gui, x, y, d=15, color=(255, 255, 255)):
    """
crates a grid
    :param gui:
    :type gui:
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
        draw.line(gui, color, (i * d, 0), (i * d, y * d))
    for i in range(y):
        draw.line(gui, color, (0, i * d), (x * d, i * d))
    draw.rect(gui, (250, 0, 0), (0, 0, x * d + 1, y * d + 1), 1)


def depth(x, y, d=15):
    """
creates maze with depth search algorithm.
    :param d:
    :type d:
    :param x:
    :type x:
    :param y:
    :type y:
    """
    blocks = x * y
    white = (255, 255, 255, 255)
    stack = []
    x_pos = random.randint(0, x - 1)
    y_pos = random.randint(0, y - 1)
    while blocks is not None:
        side = []
        # check if all sides are available
        if GUI.get_at(x_pos + d / 2, y_pos) == white:
            if [x_pos, y_pos - d] not in stack:
                side.append('upp')
        if GUI.get_at(x_pos + d, y_pos + 2 * d) == white:
            if [x_pos + d, y_pos] not in stack:
                side.append('right')
        if GUI.get_at(x_pos + d / 2, y_pos - d) == white:
            if [x_pos, y_pos + d] not in stack:
                side.append('down')
        if GUI.get_at(x_pos - d, y_pos + d * 2) == white:
            if [x_pos - d, y_pos] not in stack:
                side.append('left')
        side.append('stop')
        side = side[random.randint(0, (side.index('stop') - 1))]
        if side == 'upp':
            pass
            # go upp
        if side == 'right':
            pass
            # go right
        if side == 'down':
            pass
            # go down
        if side == 'left':
            pass
            # go left
