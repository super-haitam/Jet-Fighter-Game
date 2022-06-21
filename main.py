from classes import Player, AI_Opponent
from settings import *
import pygame
import time
import sys
sys.path.append("game_touches_help")
from get_game_touches_help_img import CreateImage, get_pygame_img 
pygame.init()


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jet Fighter")

# Choice Images
choice_w = WIDTH/5.5
player_choice_img = pygame.image.load("assets/player_icon.png")
player_choice_img = pygame.transform.scale(player_choice_img,
        (choice_w, choice_w / (player_choice_img.get_width()/player_choice_img.get_height())))
player_choice_rect = player_choice_img.get_rect(x=WIDTH/5, y=HEIGHT*(2/3))
robot_choice_img = pygame.image.load("assets/robot_icon.png")
robot_choice_img = pygame.transform.scale(robot_choice_img,
        (choice_w, choice_w / (robot_choice_img.get_width()/robot_choice_img.get_height())))
robot_choice_rect = robot_choice_img.get_rect(x=WIDTH*(4/5)-robot_choice_img.get_width(), y=HEIGHT*(2/3))

w1, w2 = WIDTH/5, WIDTH/9
# Player Movement images
player_turn_img = get_pygame_img(CreateImage(GREY, {"Turn Left/Right": ['a', 'd']}, color=WHITE))
player_turn_img = pygame.transform.scale(player_turn_img, (w1, w1 / (player_turn_img.get_width()/player_turn_img.get_height())))
player_shoot_img = get_pygame_img(CreateImage(GREY, {"Shoot": 'z'}, color=WHITE))
player_shoot_img = pygame.transform.scale(player_shoot_img, (w2, w2 / (player_shoot_img.get_width()/player_shoot_img.get_height())))
# Opponent Movement images
opponent_turn_img = get_pygame_img(CreateImage(GREY, {"Turn Left/Right": ['left', 'right']}, color=BLACK))
opponent_turn_img = pygame.transform.scale(opponent_turn_img, (w1, w1 / (opponent_turn_img.get_width()/opponent_turn_img.get_height())))
opponent_shoot_img = get_pygame_img(CreateImage(GREY, {"Shoot": 'l'}, color=BLACK))
opponent_shoot_img = pygame.transform.scale(opponent_shoot_img, (w2, w2 / (opponent_shoot_img.get_width()/opponent_shoot_img.get_height())))

# Game class
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.player = Player("White", WHITE, WIDTH/5)

    def draw_welcome(self):
        screen.fill(GREY)

        font = pygame.font.SysFont("comicsans", 50)
        wlcm_txt = font.render("WELCOME TO", True, WHITE)
        game_name = font.render(pygame.display.get_caption()[0], True, random_color(0, 255))
        game_txt = font.render("GAME", True, WHITE)

        for num, txt in enumerate([wlcm_txt, game_name, game_txt]):
            screen.blit(txt, ((WIDTH-txt.get_width())/2, HEIGHT/4 * (num+1) - txt.get_height()/2))

        pygame.display.flip()

    def draw_choice(self):
        screen.fill(GREY)

        font = pygame.font.SysFont("comicsans", 55)
        txt = font.render("Select a choice", True, DARK_GREY)
        screen.blit(txt, ((WIDTH-txt.get_width())/2, HEIGHT/4))

        screen.blit(player_choice_img, player_choice_rect.topleft)
        screen.blit(robot_choice_img, robot_choice_rect.topleft)

        pygame.draw.rect(screen, BLACK, player_choice_rect, width=1)
        pygame.draw.rect(screen, BLACK, robot_choice_rect, width=1)

        # Touches Help
        screen.blit(player_turn_img, (0, HEIGHT/2.6))
        screen.blit(player_shoot_img, (player_shoot_img.get_width()/3, HEIGHT/2))
        screen.blit(opponent_turn_img, (WIDTH-opponent_turn_img.get_width(), HEIGHT/2.6))
        screen.blit(opponent_shoot_img, (WIDTH-opponent_shoot_img.get_width()*(4/3), HEIGHT/2))

        pygame.display.flip()

    def draw_winner(self):
        screen.fill(GREY)

        if self.player.score < self.opponent.score:
            winner = self.opponent
        elif self.opponent.score < self.player.score:
            winner = self.player

        font = pygame.font.SysFont("comicsans", 60)
        the_winner_txt = font.render("The Winner", True, DARK_GREY)
        is_txt = font.render("is", True, DARK_GREY)
        winner_txt = font.render(f"{winner.color_name}Jet", True, winner.color)

        for num, txt in enumerate([the_winner_txt, is_txt, winner_txt]):
            screen.blit(txt, ((WIDTH-txt.get_width())/2, HEIGHT/4 * (num+1) - txt.get_height()/2))

        pygame.display.flip()

    def draw(self):
        screen.fill(GREY)

        self.player.draw(screen)
        self.opponent.draw(screen)

        pygame.display.flip()

    def run(self):
        # Main loop
        running = True
        is_started = False
        is_choosing = False
        while running:
            self.clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and not is_started:
                    is_started = True
                    is_choosing = True

                elif event.type == pygame.MOUSEBUTTONDOWN and is_choosing:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if player_choice_rect.collidepoint(mouse_x, mouse_y):
                        player_bool = True
                        robot_bool = False
                        is_choosing = False
                        self.opponent = Player("Black", BLACK, WIDTH*(4/5))
                    if robot_choice_rect.collidepoint(mouse_x, mouse_y):
                        player_bool = False
                        robot_bool = True
                        is_choosing = False
                        self.opponent = AI_Opponent("Black", BLACK, WIDTH*(4/5), self.player)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.player.shoot()
                    if event.key == pygame.K_l:
                        self.opponent.shoot()

            if not is_started:
                self.draw_welcome()
                continue

            if is_choosing:
                self.draw_choice()
                continue

            # Handle Movement
            self.player.handle_movement('a', 'd')
            if player_bool:
                self.opponent.handle_movement("left", "right")
            elif robot_bool:
                self.opponent.move_AI(screen)

            # Collision Player and Bullet
            for player in [self.player, self.opponent]:
                opponent = self.player if player == self.opponent else self.opponent
                for bullet in player.bullets:
                    offset = (opponent.rect.x - bullet.rect.x, opponent.rect.y - bullet.rect.y)
                    if bullet.mask.overlap(opponent.get_mask(), offset):
                        player.score += 1

                        # Destroy bullet
                        player.bullets.pop(player.bullets.index(bullet))
                        break

            # Winner
            if max(self.player.score, self.opponent.score) == 10:
                self.draw()
                self.draw_winner()
                time.sleep(2)

                self.__init__()
                if player_bool:
                    self.opponent.__init__("Black", BLACK, WIDTH*(4/5))
                elif robot_bool:
                    self.opponent.__init__("Black", BLACK, WIDTH*(4/5), self.player)

                is_started = False

            self.draw()


game = Game()
game.run()
