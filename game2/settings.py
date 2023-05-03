import os, pygame
from pygame.math import Vector2 as vec

#SCREEN
WIDTH, HEIGHT = 610, 670
REFRESH_TIME = 60
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH - TOP_BOTTOM_BUFFER, HEIGHT - TOP_BOTTOM_BUFFER

#COLOR
BLACK = (0,0,0)
RED = (255,0,0)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOR = (255,255,0)

#FONTS
START_TEXT_SIZE = 16
START_FONT = 'arial black'

#PLAYER
PLAYER_START_POSITION = 0

#sounds
sounds = ["sounds\pacman_beginning.wav","sounds\pacman_chomp.wav","sounds\pacman_death.wav"]

#PICURES
path = os.path.join(os.pardir, 'images')
file_names = sorted(os.listdir(path))

file_names.remove('maze.png')
BACKGROUND_MAZE = pygame.image.load(os.path.join(path, 'maze.png'))

for file_name in file_names:
    image_name = file_name[:-4].upper()
    globals()[image_name] = pygame.image.load(os.path.join(path, file_name))


PLAYER_WALK_LIST_L = [PACMAN_STAND,PACMAN_LEFT]
PLAYER_WALK_LIST_R = [PACMAN_STAND, PACMAN_RIGHT]
PLAYER_WALK_LIST_U = [PACMAN_STAND, PACMAN_UP]
PLAYER_WALK_LIST_D = [PACMAN_STAND, PACMAN_DOWN]



