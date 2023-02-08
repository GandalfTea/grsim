
import pygame
import math
import numpy as np

from OpenGL.GL  import *
from OpenGL.GLU import *

from dataclasses import dataclass

class Viewer:

    def __init__(self, width, height):

        self.DISPLAY_VERTS = True
        self.DISPLAY_LINES = True 

        self.res = (width, height)
        self.screen = pygame.display.set_mode(self.res, pygame.DOUBLEBUF|pygame.OPENGL)
        pygame.display.set_caption('GRVisualiser')

        gluPerspective(45, (self.res[0]/self.res[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -30)

        self.models = {}

    def run(self):
        glRotate(20, 1, 0, 0)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #x = glGetDoublev(GL_MODELVIEW_MATRIX)
            glRotate(0.1, 0, 45, 0)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glClearColor(0.05, 0.066, 0.09, 1)
            self.display()
            #self.models['cube'].transform(rotmat(0.01))
            pygame.display.flip()
            pygame.time.wait(10)

    def display(self):
        for model in self.models.values():
            maxval = max(model.vert.tolist())[0]
            if self.DISPLAY_VERTS:
                glEnable(GL_POINT_SMOOTH)
                glPointSize(3)
                glBegin(GL_POINTS)
                for v in model.vert:
                    val = [abs(i) for i in v.tolist()]
                    val = (sum(val)/len(val))/maxval
                    glColor3f(abs(val-0.3), abs(val-0.9), abs(val-0.9))
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

    def _center(self):
        return (sum([v.x for v in self.vert]), sum([v.y for v in self.vert]),
                sum([v.z for v in self.vert]))

    def add_vert(self, vert_array):
        ones_column = np.ones((len(vert_array), 1))
        ones_added = np.hstack((vert_array, ones_column))
        self.vert = np.vstack((self.vert, ones_added))

    def add_lines(self, line_list):
        self.lines += line_list

    def transform(self, mat):
        self.vert = np.dot(self.vert, mat)


def lattice(size):
    size = size//2
    lattice = Model()
    lattice.add_vert([[x, y, z] for x in range(-size, size) for y in range(-size, size) for z in range(-size, size)])

    #lattice.add_lines([(n, n + 4) for n in range(0, 4)])
    #lattice.add_lines([(n, n + 1) for n in range(0, 8, 2)])
    #lattice.add_lines([(n, n + 2) for n in (0, 1, 4, 5)])
    return lattice



if __name__ == "__main__":

    l = lattice(8)
    v = Viewer(1500, 1500)

    v.addModel("lattice", l)
    v.run()

