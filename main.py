from classes import Player
from settings import *
import pygame
pygame.init()


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Game class
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.player = Player("White", WHITE)
        self.opponent = Player("Black", BLACK)
        
    def draw(self):
        screen.fill(GREY)

        self.player.draw(screen)
        self.opponent.draw(screen)

        pygame.display.flip()

    def run(self):
        # Main loop
        running = True
        while running:
            self.clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.player.shoot()
                    if event.key == pygame.K_l:
                        self.opponent.shoot()

            # Handle Mouvement
            self.player.handle_movement('a', 'd')
            self.opponent.handle_movement("left", "right")

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

            self.draw()


game = Game()
game.run()
