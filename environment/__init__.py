import random

from pygame import draw, display


def grid(surface, x, y, d=15, color=(255, 255, 255)):
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
        draw.line(surface, color, (i * d, 0), (i * d, y * d))
    for i in range(y):
        draw.line(surface, color, (0, i * d), (x * d, i * d))
    draw.rect(surface, (250, 0, 0), (0, 0, x * d + 1, y * d + 1), 1)
    display.update()


def depth(surface, x, y, d=15):
    """
creates maze with depth search algorithm.
    :param surface:
    :param d:
    :type d:
    :param x:
    :type x:
    :param y:
    :type y:
    """
    blocks = (x * y) - 1
    white = (255, 255, 255, 255)
    stack = []
    x_pos = random.randint(0, x - 1)
    y_pos = random.randint(0, y - 1)
    while blocks is not None:
        side = []
        stack.append([x_pos, y_pos])
        # check if all sides are available
        if surface.get_at(x_pos + d / 2, y_pos) == white and [x_pos, y_pos - d] not in stack:
            side.append('upp')
        if surface.gui.get_at(x_pos + d, y_pos + 2 * d) == white and [x_pos + d, y_pos] not in stack:
            side.append('right')
        if surface.gui.get_at(x_pos + d / 2, y_pos - d) == white and [x_pos, y_pos + d] not in stack:
            side.append('down')
        if surface.gui.get_at(x_pos - d, y_pos + d * 2) == white and [x_pos - d, y_pos] not in stack:
            side.append('left')

        side.append('stop')
        side = side[random.randint(0, (side.index('stop') - 1))]
        if side == 'upp':
            y_pos -= d
        elif side == 'right':
            x_pos += d
        elif side == 'down':
            y_pos += d
        elif side == 'left':
            x_pos -= d
        else: # go back one step
            stack.pop()
            x_pos = stack[-1][0]
            y_pos = stack[-1][1]
            stack.pop()
