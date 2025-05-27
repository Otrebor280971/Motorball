import math
from objloader import OBJ
from config import GRAVITY, FLOOR
from OpenGL.GL import *
from OpenGL.GLU import *

class Car:
    def __init__(self, path, stadium, is_left_goal=True):
        self.model = OBJ(path, swapyz=True)
        self.model.generate()
        self.scale = 10.0
        self.direction = [0, 0, 1]
        self.size = (8, 4, 16)
        self.x = 350
        self.y = FLOOR
        self.z = 0
        self.rotation = -90
        self.speed = 6
        self.turn_speed = 3
        self.stadium = stadium
        self.is_left_goal = is_left_goal

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, 0, self.z)
        glRotatef(self.rotation, 0, 1, 0)
        glTranslatef(0.0, 0.0, 15.0)
        glScale(self.scale, self.scale, self.scale)
        self.model.render()
        glPopMatrix()

    def update(self, ball, opponent_car, depth=2):
        # pruning (UNICAMENTE EXPANDIMOS POR DONDE SI IREMOS)
        best_score = -float('inf')
        best_action = None
        actions = self.get_possible_actions()
        for action in actions:
            score = self.minimax(self.simulate_action(action, ball, opponent_car), depth-1, False, -float('inf'), float('inf'))
            if score > best_score:
                best_score = score
                best_action = action
        if best_action:
            self.apply_action(best_action)

    def get_possible_actions(self):
        # acciones
        # mover: -1 atras, 0 nada, 1 adelante
        # girar izq -1, no girar 0, girar derecha 1
        # no le puse brincar jejeje (no se como meterlo en el minimax xd)
        return [
            (1, 0), (1, -1), (1, 1),
            (0, 0), (0, -1), (0, 1),
            (-1, 0), (-1, -1), (-1, 1)
        ]

    def simulate_action(self, action, ball, opponent_car):
        move, turn = action
        car_x, car_z, car_rot = self.x, self.z, self.rotation
        car_rot += turn * self.turn_speed
        dx = move * self.speed * math.sin(math.radians(car_rot))
        dz = move * self.speed * math.cos(math.radians(car_rot))
        next_x = car_x + dx
        next_z = car_z + dz
        next_box = self.get_aabb(x=next_x, z=next_z)
        collided = False
        for wall in self.stadium.wall_boxes:
            if (next_box["min"][0] <= wall["max"][0] and next_box["max"][0] >= wall["min"][0] and
                next_box["min"][1] <= wall["max"][1] and next_box["max"][1] >= wall["min"][1] and
                next_box["min"][2] <= wall["max"][2] and next_box["max"][2] >= wall["min"][2]):
                collided = True
                break
        if collided:
            next_x, next_z = car_x, car_z
        # nuevo estado
        return ((next_x, next_z, car_rot), (ball.x, ball.z), (opponent_car.x, opponent_car.z))

    def minimax(self, state, depth, maximizing, alpha, beta):
        if depth == 0:
            return self.heuristic(state)
        car_state, ball_state, opponent_state = state
        if maximizing:
            max_eval = -float('inf')
            for action in self.get_possible_actions():
                next_state = self.simulate_action_for_state(car_state, action)
                eval = self.minimax((next_state, ball_state, opponent_state), depth-1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for action in self.get_possible_actions():
                next_state = self.simulate_action_for_state(opponent_state, action)
                eval = self.minimax((car_state, ball_state, next_state), depth-1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def simulate_action_for_state(self, state, action):
        x, z = state
        rot = self.rotation
        move, turn = action
        rot += turn * self.turn_speed
        dx = move * self.speed * math.sin(math.radians(rot))
        dz = move * self.speed * math.cos(math.radians(rot))
        next_x = x + dx
        next_z = z + dz
        return (next_x, next_z)

    def heuristic(self, state):
        car_state, ball_state, opponent_state = state
        car_x, car_z, _ = car_state
        ball_x, ball_z = ball_state
        if self.is_left_goal:
            goal_x, goal_z = -400, 0
        else:
            goal_x, goal_z = 400, 0
        dist_to_ball = math.sqrt((car_x - ball_x)**2 + (car_z - ball_z)**2)
        dist_ball_to_goal = math.sqrt((ball_x - goal_x)**2 + (ball_z - goal_z)**2)
        # menor distancia al balon + menor distancia a porteria = mejor
        return -dist_to_ball - 0.5 * dist_ball_to_goal

    def apply_action(self, action):
        move, turn = action
        self.rotation += turn * self.turn_speed
        dx = move * self.speed * math.sin(math.radians(self.rotation))
        dz = move * self.speed * math.cos(math.radians(self.rotation))
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

    def get_aabb(self, x=None, z=None):
        x = x if x is not None else self.x
        z = z if z is not None else self.z
        half_w = self.size[0] / 2
        half_h = self.size[1] / 2
        half_l = self.size[2] / 2
        return {
            "min": (x - half_w, self.y, z - half_l),
            "max": (x + half_w, self.y + self.size[1], z + half_l)
        } 