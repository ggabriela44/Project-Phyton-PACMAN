import pygame, random
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, game, pos, number):
        self.game = game
        self.grid_pos = pos
        self.started_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.game.cell_width // 2.3)
        self.number = number
        self.color = self.set_color()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()

    def update(self):
        self.pix_pos += self.direction*4
        if self.time_to_move():
            self.move()

        # ustawienie pozycji w referencji na pix
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.game.cell_width // 2) \
                           // self.game.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.game.cell_height // 2) \
                           // self.game.cell_height + 1

    def draw(self):
        pygame.draw.circle(self.game.screen, self.color,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.game.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.game.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "slow":
            self.direction = self.get_random_direction()
        if self.personality == "speedy":
            self.direction = self.get_random_direction()
        if self.personality == "scared":
            self.direction = self.get_random_direction()

    def get_random_direction(self):
        while True:
            number = random.randint(-100, 100)
            # print(number)
            if number == 1:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            # dir = vec(x_dir, y_dir)
            next_pos = vec(x_dir + self.grid_pos.x, y_dir + self.grid_pos.y)
            if next_pos not in self.game.walls:
                break
        return vec(x_dir, y_dir)

    def get_pix_pos(self):
        return vec(
            (self.grid_pos[0] * self.game.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.game.cell_width // 2,
            (self.grid_pos[1] * self.game.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.game.cell_height // 2)

    def set_color(self):
        if self.number == 0:
            return (255, 0, 0)
        if self.number == 1:
            return (0, 255, 0)
        if self.number == 2:
            return (0, 0, 255)
        if self.number == 3:
            return (255, 170, 0)

    def set_personality(self):
        if self.number == 0:
            return "slow"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"
