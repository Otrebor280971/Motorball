from objloader import OBJ
from config import *
from stadium import Stadium
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import pygame

class Car:
    def __init__(self, path, stadium):
        self.model = OBJ(path, swapyz=True)
        self.model.generate()
        self.scale = 10.0
        self.direction = [0, 0, 1]
        self.size = (8, 4, 16)
        
        self.x = -350
        self.y = FLOOR
        self.z = 0
        self.rotation = 90
        self.speed = 6
        self.turn_speed = 3
    
        self.vy = 1
        self.on_ground = True
        
        self.stadium = stadium

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rotation, 0, 1, 0)
        glTranslatef(0.0, 0.0, 15.0)
        glScale(self.scale, self.scale, self.scale)
        self.model.render()
        glPopMatrix()

    def update(self, keys, joystick):
        dx, dz = 0, 0

        if keys[pygame.K_w]:
            dx += self.speed * math.sin(math.radians(self.rotation))
            dz += self.speed * math.cos(math.radians(self.rotation))
        if keys[pygame.K_s]:
            dx -= self.speed * math.sin(math.radians(self.rotation))
            dz -= self.speed * math.cos(math.radians(self.rotation))
        if keys[pygame.K_a]:
            self.rotation += self.turn_speed
        if keys[pygame.K_d]:
            self.rotation -= self.turn_speed
            
        if joystick:
            stick = joystick.get_axis(0)
            rtrigger = joystick.get_axis(5)
            ltrigger = joystick.get_axis(4)
            deadzone = 0.2
            
            if rtrigger > deadzone:
                dx += self.speed * math.sin(math.radians(self.rotation))
                dz += self.speed * math.cos(math.radians(self.rotation))
            if ltrigger > deadzone:
                dx -= self.speed * math.sin(math.radians(self.rotation))
                dz -= self.speed * math.cos(math.radians(self.rotation))
            if stick < -deadzone:
                self.rotation += self.turn_speed
            if stick > deadzone:
                self.rotation -= self.turn_speed

        rad = math.radians(self.rotation)
        self.direction[0] = math.sin(rad)
        self.direction[2] = math.cos(rad)

        next_x = self.x + dx
        next_z = self.z + dz

        next_box = self.get_aabb(x=next_x, z=next_z)
        collided = False
        for wall in self.stadium.wall_boxes:
            if (next_box["min"][0] <= wall["max"][0] and next_box["max"][0] >= wall["min"][0] and
                next_box["min"][1] <= wall["max"][1] and next_box["max"][1] >= wall["min"][1] and
                next_box["min"][2] <= wall["max"][2] and next_box["max"][2] >= wall["min"][2]):
                collided = True
                break

        if not collided:
            self.x = next_x
            self.z = next_z

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = 5
            self.on_ground = False
        self.vy += GRAVITY
        self.y += self.vy

        if self.y <= FLOOR:
            self.y = FLOOR
            self.vy = 0
            self.on_ground = True
           
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
        
    def check_collision_with_ball(self, ball):
        car_box = self.get_aabb()
        ball_box = ball.get_aabb()

        overlap = (
            car_box["min"][0] <= ball_box["max"][0] and car_box["max"][0] >= ball_box["min"][0] and
            car_box["min"][1] <= ball_box["max"][1] and car_box["max"][1] >= ball_box["min"][1] and
            car_box["min"][2] <= ball_box["max"][2] and car_box["max"][2] >= ball_box["min"][2]
        )

        if overlap:
            dir_x = ball.x - self.x
            dir_z = ball.z - self.z
            length = math.sqrt(dir_x**2 + dir_z**2) or 1

            dir_x /= length
            dir_z /= length

            impulse_strength = 5.0

            ball.vx = dir_x * impulse_strength
            ball.vz = dir_z * impulse_strength

            ball.vy = 2.0

            return True
        return False

    def check_collision_with_car(self, other_car):
        car_box = self.get_aabb()
        other_box = other_car.get_aabb()

        overlap = (
            car_box["min"][0] <= other_box["max"][0] and car_box["max"][0] >= other_box["min"][0] and
            car_box["min"][1] <= other_box["max"][1] and car_box["max"][1] >= other_box["min"][1] and
            car_box["min"][2] <= other_box["max"][2] and car_box["max"][2] >= other_box["min"][2]
        )

        if overlap:
            self.x -= self.speed * math.sin(math.radians(self.rotation))
            self.z -= self.speed * math.cos(math.radians(self.rotation))
            other_car.x -= other_car.speed * math.sin(math.radians(other_car.rotation))
            other_car.z -= other_car.speed * math.cos(math.radians(other_car.rotation))
            return True
        return False