
import pygame
from dataclasses import dataclass
import math
import numpy as np


class Viewer:

    def __init__(self, width, height):

        self.DISPLAY_NODES = True
        self.DISPLAY_LINES = True

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('GRVisualiser')
        self.screen.fill((0, 0, 0))

        self.node_color = (0, 255, 255)
        self.line_color = (255, 255, 255)
        self.node_size = 2
        self.models = {}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.display()
            #self.models["cube"].rotate_z(self.models["cube"].center, 0.01)
            self.models['cube'].transform(rotmat(0.01))
            pygame.display.flip()

    def display(self):
        self.screen.fill((0, 0, 0))
        for model in self.models.values():
            if self.DISPLAY_NODES:
                for v in model.vert:
                    #print(v)
                    pygame.draw.circle(self.screen, self.node_color,
                                       (v[0], v[1]), self.node_size, 0)
            if self.DISPLAY_LINES:
                for line in model.lines:
                    pygame.draw.aaline(
                        self.screen, self.line_color,
                        (model.vert[line[0]][0], model.vert[line[0]][1]),
                        (model.vert[line[1]][0], model.vert[line[1]][1]))

    def addModel(self, name, model):
        self.models[name] = model


class Model:

    def __init__(self):
        self.vert = np.zeros((0, 4))
        self.lines = []
        self.center = self._center()

    def _center(self):
        return (sum([v.x for v in self.vert]), sum([v.y for v in self.vert]),
                sum([v.z for v in self.vert]))

    def rotate_z(self, center, radians):
        for v in self.vert:
            x = v[0] - center[0]
            y = v[1] - center[1]
            d = math.hypot(y, x)
            theta = math.atan2(y, x) + radians
            v[0] = center[0] + d * math.cos(theta)
            v[1] = center[1] + d * math.cos(theta)

    def add_vert(self, vert_array):
        ones_column = np.ones((len(vert_array), 1))
        ones_added = np.hstack((vert_array, ones_column))
        self.vert = np.vstack((self.vert, ones_added))

    def add_lines(self, line_list):
        self.lines += line_list

    def transform(self, mat):
        self.vert = np.dot(self.vert, mat)


def rotmat(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, -s, s, 0], [s, c, -s, 0], [-s, s, c, 0], [0, 0, 0,
                                                                   1]])


if __name__ == "__main__":
    cube = Model()
    cube.add_vert([[x, y, z] for x in (50, 250) for y in (50, 250)
                   for z in (50, 250)])
    cube.add_lines([(n, n + 4) for n in range(0, 4)])
    cube.add_lines([(n, n + 1) for n in range(0, 8, 2)])
    cube.add_lines([(n, n + 2) for n in (0, 1, 4, 5)])

    v = Viewer(800, 800)
    v.addModel("cube", cube)
    v.run()

