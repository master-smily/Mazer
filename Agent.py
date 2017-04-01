from math import sqrt
from random import choice, randint, sample

from pygame import display, draw, event
from pygame.time import Clock

from main import BLACK, BLUE, D, R, X, Y


class Agent:
    def __init__(self, gui):
        self.end = (X * D - D / 2, Y * D - D / 2)
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
        return self.pos['x'], self.pos['y']

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
        while True:
            if self.end in self.child_nodes or self.end in self.parent_nodes:
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

    def a_star(self):  # https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
        start = (self.pos['x'], self.pos['y'])
        open_set = Stack()
        closed_set = []
        # last = open_set.read(start)
        open_set.add(start, 0, self.heuristic(start))

        while open_set:
            active = open_set.lowest_f()
            if active == self.end:
                print("A* done")
                return "A* solved"
            self.calc_cord(active)
            sides = self.side()
            closed_set.append(active)
            while sides:
                self.calc_cord(active)
                next_cell = choice(sides)
                sides.remove(next_cell)
                next_cell = self.move(next_cell, D)
                if next_cell in closed_set:
                    continue
                new_g = open_set.read(active)['g'] + 15
                if next_cell not in open_set:
                    open_set.add(next_cell, new_g, self.heuristic(next_cell))
            open_set.remove(active)
        raise Exception("A* Error")

    def heuristic(self, pos):
        x_dist = self.end[0] - pos[0]
        y_dist = self.end[1] - pos[1]
        return sqrt(x_dist**2 + y_dist**2)


class Stack:
    def __init__(self):
        self.stack = dict()

    def add(self, cell, g=float("inf"), h=float("inf")):
        self.stack[cell] = {'g': g, 'h': h, 'f': g + h}

    def __bool__(self):
        if self.stack:
            return True
        else:
            return False

    def lowest_f(self) -> tuple:
        f = min(self.stack.keys(), key=lambda key: self.stack[key]['f'])
        return tuple(f)

    def remove(self, cell):
        return self.stack.pop(cell)

    def read(self, cell):
        return self.stack[cell]

    def __contains__(self, item):
        if item in self.stack:
            return True
        else:
            return False