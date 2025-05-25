import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from config import *
from pcar import Car as PCar
from ball import Ball
from ccar import Car as CCar
from stadium import Stadium

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Motorball")

stadium = Stadium()
p_car = PCar("assets/models/car.obj", stadium)
camera_mode = "player"
ball = Ball("assets/models/ball.obj")
c_car = CCar("assets/models/car.obj")

def Init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glLightfv(GL_LIGHT0, GL_POSITION, (0, 200, 0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)

def check_car_ball_collision(car, ball):
    car_box = car.get_aabb()
    ball_box = ball.get_aabb()

    if (car_box["min"][0] <= ball_box["max"][0] and car_box["max"][0] >= ball_box["min"][0] and
        car_box["min"][1] <= ball_box["max"][1] and car_box["max"][1] >= ball_box["min"][1] and
        car_box["min"][2] <= ball_box["max"][2] and car_box["max"][2] >= ball_box["min"][2]):

        dx = ball.x - car.x
        dz = ball.z - car.z
        dist = math.sqrt(dx*dx + dz*dz)
        if dist == 0:
            dist = 0.01
        
        nx = dx / dist
        nz = dz / dist

        impulse_strength = 5 

        ball.vx = nx * impulse_strength
        ball.vz = nz * impulse_strength

        ball.vy = 2

def check_car_car_collision(car1, car2):
    box1 = car1.get_aabb()
    box2 = car2.get_aabb()

    if (box1["min"][0] <= box2["max"][0] and box1["max"][0] >= box2["min"][0] and
        box1["min"][1] <= box2["max"][1] and box1["max"][1] >= box2["min"][1] and
        box1["min"][2] <= box2["max"][2] and box1["max"][2] >= box2["min"][2]):

        dx = car2.x - car1.x
        dz = car2.z - car1.z
        dist = math.sqrt(dx*dx + dz*dz)
        if dist == 0:
            dist = 0.01
        
        nx = dx / dist
        nz = dz / dist

        rebound_speed = 2

        car1.x -= nx * rebound_speed
        car1.z -= nz * rebound_speed
        car2.x += nx * rebound_speed
        car2.z += nz * rebound_speed


    
def lookat():
    cx, cy, cz = p_car.x, p_car.y, p_car.z
    bx, by, bz = ball.x, ball.y, ball.z

    if not camera_mode == "ball":
        dx, dy, dz = p_car.direction
        camera_distance = 60
        camera_height = 30

        eye_x = cx - dx * camera_distance
        eye_y = cy + camera_height
        eye_z = cz - dz * camera_distance

        center_x = cx + dx * 10
        center_y = cy + 10
        center_z = cz + dz * 10

    else:
        dx = bx - cx
        dy = by - cy
        dz = bz - cz

        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        if distance == 0:
            distance = 0.0001

        ndx = dx / distance
        ndz = dz / distance

        camera_offset = 50
        camera_height = 25

        eye_x = cx - ndx * camera_offset
        eye_y = cy + camera_height
        eye_z = cz - ndz * camera_offset


        center_x = bx
        center_y = by + 10
        center_z = bz

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eye_x, eye_y, eye_z, center_x, center_y, center_z, 0, 1, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    stadium.draw()
    p_car.draw()
    p_car.update(keys)
    ball.draw()
    ball.update(stadium)
    c_car.draw()
    c_car.update()
    lookat()
    
    check_car_ball_collision(p_car, ball)
    check_car_ball_collision(c_car, ball)

    check_car_car_collision(p_car, c_car)

Init()
done = False
while not done:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                if camera_mode == "player":
                    camera_mode = "ball"
                else:
                    camera_mode = "player"
            
    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()