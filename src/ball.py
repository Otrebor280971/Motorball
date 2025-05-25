from objloader import OBJ
from config import GRAVITY, FLOOR, BOUNCE
from OpenGL.GL import *
from OpenGL.GLU import *

class Ball:
    def __init__(self, path):
        self.model = OBJ(path, swapyz=True)
        self.model.generate()
        self.scale = 15.0
        self.radius = (self.scale / 2) + 5
        
        self.x = 0
        self.y = FLOOR + self.radius
        self.z = 0
        
        self.vx = 0.0
        self.vy = 5.0
        self.vz = 0.0

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(0.0, 0.0, 0.0, 1.0)
        glScale(self.scale, self.scale, self.scale)
        self.model.render()
        glPopMatrix()

    def update(self, stadium):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

        if self.y <= FLOOR + self.radius:
            self.y = FLOOR + self.radius
            self.vy = -self.vy * BOUNCE
            if abs(self.vy) < 0.9:
                self.vy = 0

        ball_box = self.get_aabb()
        for wall in stadium.wall_boxes:
            if (ball_box["min"][0] <= wall["max"][0] and ball_box["max"][0] >= wall["min"][0] and
                ball_box["min"][1] <= wall["max"][1] and ball_box["max"][1] >= wall["min"][1] and
                ball_box["min"][2] <= wall["max"][2] and ball_box["max"][2] >= wall["min"][2]):

                if (ball_box["max"][0] >= wall["min"][0] and ball_box["min"][0] < wall["min"][0]) or \
                   (ball_box["min"][0] <= wall["max"][0] and ball_box["max"][0] > wall["max"][0]):
                    self.vx = -self.vx * BOUNCE
                if (ball_box["max"][2] >= wall["min"][2] and ball_box["min"][2] < wall["min"][2]) or \
                   (ball_box["min"][2] <= wall["max"][2] and ball_box["max"][2] > wall["max"][2]):
                    self.vz = -self.vz * BOUNCE
                
                self.x += self.vx
                self.z += self.vz

    def get_aabb(self):
        return {
            "min": (self.x - self.radius, self.y - self.radius, self.z - self.radius),
            "max": (self.x + self.radius, self.y + self.radius, self.z + self.radius)
        }