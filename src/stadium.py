from objloader import OBJ
from OpenGL.GL import *
from OpenGL.GLU import *

class Stadium:
    def __init__(self):
        self.field = OBJ("assets/models/field.obj", swapyz=True)
        self.walls = OBJ("assets/models/walls.obj", swapyz=True)
        self.net = OBJ("assets/models/net.obj", swapyz=True)

        self.field.generate()
        self.walls.generate()
        self.net.generate()

        self.scale = 100
        
        self.wall_boxes = [
            { "min": (-4.2 * self.scale, 0,    -3.2 * self.scale), "max": (-3.8 * self.scale, 1.5 * self.scale, 3.2 * self.scale) },  # izquierda
            { "min": ( 3.8 * self.scale, 0,    -3.2 * self.scale), "max": ( 4.2 * self.scale, 1.5 * self.scale, 3.2 * self.scale) },  # derecha
            { "min": (-4.2 * self.scale, 0,     3.0 * self.scale), "max": ( 4.2 * self.scale, 1.5 * self.scale, 3.2 * self.scale) },  # fondo
            { "min": (-4.2 * self.scale, 0,    -3.2 * self.scale), "max": ( 4.2 * self.scale, 1.5 * self.scale, -3.0 * self.scale) }, # frente
        ]

    def draw(self):
        glPushMatrix()
        glScalef(self.scale, self.scale, self.scale)

        self.field.render()

        self.walls.render()

        # Portería atrás
        glPushMatrix()
        glTranslatef(0, 0, -0.15)
        glRotatef(90.0, 0.0, 1.0, 0.0) 
        self.net.render()
        glPopMatrix()

        # Portería adelante
        glPushMatrix()
        glTranslatef(0, 0, 0.0)
        glRotatef(-90, 0, 1, 0)
        self.net.render()
        glPopMatrix()


        glPopMatrix()
