from math import sqrt
from random import choice, randint, sample

from pygame import display, draw, event
from pygame.time import Clock

from main import BLACK, BLUE, D, R, X, Y


class Agent:
    def __init__(self, gui):
        self.pos = {'x': int(D / 2),
                    'y': int(D / 2)}
        self.no_pos = {'wall': [0, 0],
                       'cord': [0, 0]}
        self.log = []
        self.stack = []
        self.fps = 100
        self.pos_upp = dict()
        self.pos_right = dict()
        self.pos_down = dict()
        self.pos_left = dict()
        self.gui = gui
        self.stage = self.gui.convert()
        self.update()
        self.nodes = {}
        self.parent_nodes = set()
        self.child_nodes = set()
        self.parent_nodes.add((self.pos['x'], self.pos['y']))

    def neighbours(self):
        if self.pos['x'] <= D:
            self.pos_left = self.no_pos
        else:
            self.pos_left = {'wall': [int(self.pos['x'] - D / 2), self.pos['y']],
                             'cord': [int(self.pos['x'] - D), self.pos['y']]}
        if self.pos['y'] <= D:
            self.pos_upp = self.no_pos
        else:
            self.pos_upp = {'wall': [self.pos['x'], int(self.pos['y'] - D / 2)],
                            'cord': [self.pos['x'], int(self.pos['y'] - D)]}
        if self.pos['x'] >= D * X:
            self.pos_right = self.no_pos
        else:
            self.pos_right = {'wall': [int(self.pos['x'] + D / 2), self.pos['y']],
                              'cord': [int(self.pos['x'] + D), self.pos['y']]}
        if self.pos['y'] >= D * Y:
            self.pos_down = self.no_pos
        else:
            self.pos_down = {'wall': [self.pos['x'], int(self.pos['y'] + D / 2)],
                             'cord': [self.pos['x'], int(self.pos['y'] + D)]}

    def move(self, side=None, step=15):
        for i in range(int(D / step)):
            if side == 'upp':
                self.pos['y'] -= step
            if side == 'right':
                self.pos['x'] += step
            if side == 'down':
                self.pos['y'] += step
            if side == 'left':
                self.pos['x'] -= step
            self.update()

    def update(self):
        Clock().tick(self.fps)
        self.gui.blit(self.stage, [0, 0])
        draw.circle(self.gui, BLUE, [self.pos['x'], self.pos['y']], R)
        event.pump()
        display.update()

    def depth(self):
        print('Agent.depth')
        while True:
            side = self.side()
            if self.pos == {'x': X * D - D / 2, 'y': Y * D - D / 2}:
                print("Depth done")
                break
            elif side:
                side = side[randint(0, side.index(side[-1]))]
                self.stack.append(side)
                self.move(side, D)
                self.log.append([self.pos['x'], self.pos['y']])
            elif self.stack:
                self.move(self.reverse_side(), D)
                self.stack.pop()
            else:
                raise Exception("Depth Error")
        return "Depth solved"

    def side(self):
        # print('Agent.side')
        self.neighbours()
        sides = []
        if self.gui.get_at(self.pos_upp['wall']) == BLACK \
                and self.pos_upp['cord'] not in self.log:
            sides.append('upp')
        if self.gui.get_at(self.pos_right['wall']) == BLACK \
                and self.pos_right['cord'] not in self.log:
            sides.append('right')
        if self.gui.get_at(self.pos_down['wall']) == BLACK \
                and self.pos_down['cord'] not in self.log:
            sides.append('down')
        if self.gui.get_at(self.pos_left['wall']) == BLACK \
                and self.pos_left['cord'] not in self.log:
            sides.append('left')
        return sides

    def reverse_side(self):
        if self.stack[-1] == 'upp':
            return 'down'
        if self.stack[-1] == 'down':
            return 'upp'
        if self.stack[-1] == 'right':
            return 'left'
        if self.stack[-1] == 'left':
            return 'right'

    def evaluate_node(self, cell):
        self.calc_cord(cell)
        sides = self.side()
        for i in range(len(sides)):
            self.calc_cord(cell)
            self.move(sides[i], D)
            self.child_nodes.add((self.pos['x'], self.pos['y']))
            self.log.append([self.pos['x'], self.pos['y']])

    def breadth(self):
        print("Agent.breadth")
        goal = (X * D - D / 2, Y * D - D / 2)
        while True:
            if goal in self.child_nodes or goal in self.parent_nodes:
                print("breadth done")
                break
            elif self.parent_nodes:  # explore the current list
                active = sample(self.parent_nodes, 1)
                self.parent_nodes.remove(active[-1])
                self.evaluate_node(active[-1])
            elif self.child_nodes:
                self.parent_nodes = self.child_nodes
                self.child_nodes = set()
            else:
                raise Exception("Breadth Error")
        return "Breadth solved"

    def calc_cord(self, cell):
        self.pos['x'] = cell[0]
        self.pos['y'] = cell[1]

    def a_star(self):
        start = (self.pos['x'], self.pos['y'])
        end = (X * D - D / 2, Y * D - D / 2)
        open_set = Stack()
        closed_set = []
        open_set.__add__(start, 0, self.heuristic(start, end))

        while open_set:
            active = open_set.lowest_f()
            self.calc_cord(active)
            if active == end:
                print("A* done")
                return "A* solved"
            open_set.remove(active)
            closed_set.append(active)
            sides = self.side()
            while sides:
                next_cell = choice(sides)

    @staticmethod
    def heuristic(a, b):
        x_dist = b[0] - a[0]
        y_dist = b[1] - a[1]
        return sqrt(x_dist**2 + y_dist**2)


class Stack:
    def __init__(self):
        self.stack = dict()

    def __add__(self, cell, g=float("inf"), h=float("inf")):
        self.stack[cell] = {'g': g, 'h': h, 'f': g + h}

    def __bool__(self):
        if self.stack:
            return True
        else:
            return False

    def lowest_f(self):
        return min(self.stack.keys(), key=lambda key: self.stack[key]['f'])

    def remove(self, cell):
        return self.stack.pop(cell)
