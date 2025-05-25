from objloader import OBJ
from config import GRAVITY, FLOOR
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import pygame

class Car:
    def __init__(self, path):
        self.model = OBJ(path, swapyz=True)
        self.model.generate()
        self.scale = 10.0
        self.direction = [0, 0, 1]
        self.size = (8, 4, 16)
        
        self.x = 350
        self.y = FLOOR
        self.z = 0
        self.rotation = -90
        self.speed = 2
        self.turn_speed = 0.75

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, 0, self.z)
        glRotatef(self.rotation, 0, 1, 0)
        glTranslatef(0.0, 0.0, 15.0)
        glScale(self.scale, self.scale, self.scale)
        self.model.render()
        glPopMatrix()

    def update(self):
        pass
    
    def get_aabb(self, x=None, z=None):
        x = x if x is not None else self.x
        z = z if z is not None else self.z
        half_w = self.size[0] / 2
        half_h = self.size[1] / 2
        half_l = self.size[2] / 2
        return {
            "min": (x - half_w, self.y,     z - half_l),
            "max": (x + half_w, self.y + self.size[1], z + half_l)
        }