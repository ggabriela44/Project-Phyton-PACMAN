import sys
import os, pygame, time

from settings import *
from player_class import *
from enemy_class import *

vec = pygame.math.Vector2

pygame.init()

sound_1 = pygame.mixer.Sound(sounds[0])
sound_3 = pygame.mixer.Sound(sounds[2])



#######################S##### GLOWNE OKNO ###########################
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "START"
        self.cell_width = MAZE_WIDTH // 28
        self.cell_height = MAZE_HEIGHT // 30
        self.walls = []
        self.coins = []
        self.score_coins = 0
        self.p_pos = None
        self.enemies = []
        self.e_pos = []
        self.high_score = 0
        self.repeat = 0
        # self.a1 = None
        self.load()
        
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == "START":
                if self.repeat == 0:
                    sound_1.play(-1)
                    self.repeat = 1
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == "PLAY":
                sound_1.stop()
                self.play_events()
                self.play_update()
                self.play_draw()
            elif self.state == "STOP":
                if self.repeat == 1:
                    sound_3.play()
                    self.repeat = 0
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            elif self.state == "WIN":
                self.win_events()
                self.win_update()
                self.win_draw()
            else:
                self.running = False
            self.clock.tick(REFRESH_TIME)
        pygame.quit()
        sys.exit()

    ############################ FUNKCJE POMOCNICZE ###########################
    # def is_hover(self, rect, pos):
    #     return True if rect.collidepoint(pos[0], pos[1]) else False

    def draw_text(self, word, screen, size, color, font, position, centered=False):
        font = pygame.font.SysFont(font, size)
        text = font.render(word, False, color)
        text_size = text.get_size()
        if centered:
            position[0] = position[0] - text_size[0] // 2
            position[1] = position[1] - text_size[1] // 2
        # self.a1 = pygame.Rect(position[0], position[1], 20, 20)
        screen.blit(text, position)

    def load(self):
        self.background = BACKGROUND_MAZE
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # otwieranie pliku walls
        # tworzenie listy z walls
        path_walls = os.path.join(os.pardir, "game2")
        with open(path_walls + "\walls.txt", "r") as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(x_index, y_index))
                    elif char == "C":
                        self.coins.append(vec(x_index, y_index))
                        self.score_coins += 1
                    elif char == "P":
                        self.p_pos = vec(x_index, y_index)
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append((x_index, y_index))
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (x_index * self.cell_width,
                                                                  y_index * self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def make_enemies(self):
        for index_x, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), index_x))

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height), (WIDTH, x * self.cell_height))

        # ściany_kolor
        # for coin in self.coins:
        #    pygame.draw.rect(self.background, (167, 164, 24), (coin.x * self.cell_width, coin.y * self.cell_height,
        #                                                       self.cell_width, self.cell_height))

    def reset(self):
        self.coins = []
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.started_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.started_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        path_walls = os.path.join(os.pardir, "game2")
        with open(path_walls + "\walls.txt", "r") as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == "C":
                        self.coins.append(vec(x_index, y_index))
        self.state = "PLAY"

    def change_state(self):
        self.state = "WIN"



    ############################ FUNKCJE MENU ###########################

    # petla zdarzen
    def start_events(self):
        # if self.is_hover(self.a1, [WIDTH // 2, HEIGHT // 2]):
        #     print("Ala")
        # else:
        #     print("None")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "PLAY"

    # aktualizacje
    def start_update(self):
        #pos_m = pygame.mouse.get_pos()
        pass

    # rysowanie_panel
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("PUSH SPACE BAR", self.screen, START_TEXT_SIZE, (209, 206, 27), START_FONT,
                       [WIDTH // 2, HEIGHT // 2], centered=True)
        self.draw_text("1 PLAYER ONLY", self.screen, START_TEXT_SIZE, (50, 165, 171), START_FONT,
                       [WIDTH // 2, HEIGHT // 2 + 50], centered=True)
        self.draw_text("PUSH ESCAPE TO EXIT", self.screen, 14, RED, START_FONT,
                       [WIDTH // 2, HEIGHT // 2 + 150], centered=True)
        self.draw_text(f"HIGH SCORE: {self.high_score}", self.screen, START_TEXT_SIZE, (255, 255, 255), START_FONT,
                       [4, 0])
        pygame.display.update()



    ############################ FUNKCJE GRY ###########################

    # petla zdarzen
    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    # aktualizacje
    def play_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

        if self.player.current_score == self.score_coins:
            self.change_state()


    # rysowanie_panel
    def play_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        # self.draw_grid()
        self.draw_text(f"CURRENT SCORE: {self.player.current_score}", self.screen, 18, WHITE, START_FONT, [59, 0])
        self.draw_text(f"HIGH SCORE: {self.high_score}", self.screen, 18, WHITE, START_FONT, [WIDTH // 2 + 59, 0])
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.life -= 1
        if self.player.life == 0:
            self.state = "STOP"

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (153, 153, 0),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    ############################ GAME OVER ###########################
    def game_over_draw(self):
        if self.high_score < self.player.current_score:
            self.high_score = self.player.current_score
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text(f"CURRENT SCORE: {self.high_score}", self.screen, 18, WHITE, START_FONT, [59, 0])

        self.draw_text("GAME OVER", self.screen, 52, RED, "arial", [WIDTH // 2, 100], centered=True)
        self.draw_text(again_text, self.screen, 36, (190, 190, 190), "arial", [WIDTH // 2, HEIGHT // 1.7], centered=True)
        self.draw_text(quit_text, self.screen, 36, (190, 190, 190), "arial", [WIDTH // 2, HEIGHT // 1.5], centered=True)
        pygame.display.update()

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

    def game_over_update(self):
        pass
    ############################ WIN FUNKCJE ###########################

    def win_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("YOU WIN!!!", self.screen, 30, (255, 255, 0), START_FONT,
                       [WIDTH // 2, HEIGHT // 2 + 50], centered=True)
        self.draw_text("PUSH ESCAPE TO EXIT", self.screen, 14, RED, START_FONT,
                       [WIDTH // 2, HEIGHT // 2 + 150], centered=True)
        self.draw_text(f"HIGH SCORE: {self.high_score}", self.screen, START_TEXT_SIZE, (255, 255, 255), START_FONT,
                       [4, 0])
        pygame.display.update()

    def win_update(self):
        pass

    def win_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False