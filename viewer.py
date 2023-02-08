
import pygame
import math
import numpy as np

from OpenGL.GL  import *
from OpenGL.GLU import *

from dataclasses import dataclass

class Viewer:

    def __init__(self, width, height):

        self.DISPLAY_VERTS = True
        self.DISPLAY_LINES = False 

        self.res = (width, height)
        self.screen = pygame.display.set_mode(self.res, pygame.DOUBLEBUF|pygame.OPENGL)
        pygame.display.set_caption('GRVisualiser')

        gluPerspective(45, (self.res[0]/self.res[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -30)

        self.node_color = (0, 255, 255)
        self.line_color = (255, 255, 255)
        self.node_size = 2
        self.models = {}

    def run(self):
        glRotate(20, 1, 0, 0)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #x = glGetDoublev(GL_MODELVIEW_MATRIX)
            glRotate(0.5, 0, 45, 0)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.display()
            #self.models['cube'].transform(rotmat(0.01))
            pygame.display.flip()
            pygame.time.wait(10)

    def display(self):
        self.screen.fill((0, 0, 0))
        for model in self.models.values():
            if self.DISPLAY_VERTS:
                glEnable(GL_POINT_SMOOTH)
                glBegin(GL_POINTS)
                for v in model.vert:
                    #pygame.draw.circle(self.screen, self.node_color, (v[0], v[1]), self.node_size, 0)
                    x, y, z = v[:3].tolist()
                    glVertex3d(x, y, z)
                glEnd()
            if self.DISPLAY_LINES:
                glBegin(GL_LINES)
                for line in model.lines:
                    for v in line:
                        glVertex3fv(model.vert[v][:3].tolist())
                glEnd()

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
    return np.array([[c, -s, s, 0], [s, c, -s, 0], [-s, s, c, 0], [0, 0, 0, 1]])


if __name__ == "__main__":
    cube = Model()
    cube.add_vert([[x, y, z] for x in range(-4, 4) for y in range(-4, 4) for z in range(-4 ,4)])
    cube.add_lines([(n, n + 4) for n in range(0, 4)])
    cube.add_lines([(n, n + 1) for n in range(0, 8, 2)])
    cube.add_lines([(n, n + 2) for n in (0, 1, 4, 5)])

    v = Viewer(1000, 1000)
    v.addModel("cube", cube)
    v.run()

