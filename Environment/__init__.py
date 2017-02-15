from random import randint

from pygame import display, draw, event
from pygame.constants import NOFRAME
from pygame.time import Clock

from main import BLUE, D, RED, WHITE, X, Y


class Environment:
    def __init__(self):
        self.gui = display.set_mode([X * D + 1, Y * D + 1], NOFRAME)
        draw.rect(self.gui, BLUE, ((1, 1), (D - 1, D - 1)), 5)
        self.grid()

    def grid(self):
        """
    crates a grid
        """
        print("Making grid")
        for i in range(X):
            draw.line(self.gui, WHITE, (i * D, 0), (i * D, Y * D), 2)
        for i in range(Y):
            draw.line(self.gui, WHITE, (0, i * D), (X * D, i * D), 2)
        draw.rect(self.gui, RED, ((0, 0), (X * D + 1, Y * D + 1)), 2)  # depth create border
        # draw.rect(gui, RED, ((-(D/2), -(D/2)), (X*D + D, Y*D + D)), 10)  # depth solve border
        display.update()

    def depth(self, fps=0, d=30):
        """
    creates a maze with depth search algorithm.
        """
        print("Starting depth create")
        stack = list()
        x_pos = d * randint(0, X - 1)
        y_pos = d * randint(0, Y - 1)
        log = [[x_pos, y_pos]]
        while True:
            event.pump()
            side = list()
            # check if all sides are available
            if self.gui.get_at([int(x_pos + d / 2), int(y_pos)]) == WHITE:
                if [x_pos, y_pos - d] not in log:
                    side.append('upp')
            if self.gui.get_at((int(x_pos + d), int(y_pos + d / 2))) == WHITE:
                if [x_pos + d, y_pos] not in log:
                    side.append('right')
            if self.gui.get_at((int(x_pos + d / 2), int(y_pos + d))) == WHITE:
                if [x_pos, y_pos + d] not in log:
                    side.append('down')
            if self.gui.get_at((x_pos, int(y_pos + d / 2))) == WHITE:
                if [x_pos - d, y_pos] not in log:
                    side.append('left')
            if side:  # if side: log, stack and erase wall
                Clock().tick(fps)
                side = side[randint(0, side.index(side[-1]))]
                stack.append([x_pos, y_pos])
                if side == 'upp':
                    draw.line(self.gui, (0, 0, 0), (x_pos, y_pos), (x_pos + d, y_pos), 2)
                    y_pos -= d
                elif side == 'right':
                    draw.line(self.gui, (0, 0, 0), (x_pos + d, y_pos), (x_pos + d, y_pos + d), 2)
                    x_pos += d
                elif side == 'down':
                    draw.line(self.gui, (0, 0, 0), (x_pos, y_pos + d), (x_pos + d, y_pos + d), 2)
                    y_pos += d
                elif side == 'left':
                    draw.line(self.gui, (0, 0, 0), (x_pos, y_pos), (x_pos, y_pos + d), 2)
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
        print("Depth create done")
        return "Depth create"

    def recursive_division(self):
        pass
