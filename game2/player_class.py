import pygame, time
from settings import *

vec = pygame.math.Vector2



class Player():
    def __init__(self, game, pos):
        self.game = game
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(0, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 4
        self.life = 1
        self._count = 0
        self.started_pos = [pos.x, pos.y]
        self.i =4
        self.sound_2 = pygame.mixer.Sound(sounds[1])

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()


        # pozycja pacmana na siatce pix
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.game.cell_width // 2)\
                           // self.game.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.game.cell_height // 2) \
                           // self.game.cell_height + 1

        #zliczenie coins
        if self.on_coin():
            self.eat_coin()

    def draw(self):
        # self.game.screen.blit(self.image, self.rect)
        pygame.draw.circle(self.game.screen, PLAYER_COLOR,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.game.cell_width // 2 - 2 )
        #pozycja podświetlenie
        # pygame.draw.rect(self.game.screen, RED, (self.grid_pos[0] * self.game.cell_width + TOP_BOTTOM_BUFFER // 2,
        #                                          self.grid_pos[1] * self.game.cell_height + TOP_BOTTOM_BUFFER // 2,
        #                                          self.game.cell_width, self.game.cell_height), 1)

    def on_coin(self):
        if self.grid_pos in self.game.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.game.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.game.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.i+=2
        self.game.coins.remove(self.grid_pos)
        self.current_score += 1
        if self.i % 6 == 0:
            self.sound_2.play()

    def move(self, direction):
        self.stored_direction = direction


    def get_pix_pos(self):
        return vec(
            (self.grid_pos[0] * self.game.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.game.cell_width // 2,
            (self.grid_pos[1] * self.game.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.game.cell_height // 2)
        # print(self.grid_pos, self.pix_pos)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.game.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.game.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.game.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

    # def _move(self, image_list):
    #     self.image = image_list[self._count//2]
    #
    #     self._count = (self._count + 1) % 4