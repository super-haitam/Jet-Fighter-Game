from settings import *
import pygame
import math
import time


class Jet:
    def __init__(self, color_name: str, color: tuple, x):
        image = pygame.image.load(f"assets/{color_name}Jet.png")
        ratio = image.get_width()/image.get_height()
        width = WIDTH/20

        self.original_image = pygame.transform.scale(image, (width, width / ratio))
        self.image = self.original_image
        self.rect = self.original_image.get_rect(x=x, y=HEIGHT/2)
        self.x = x

        self.angle = 0
        self.rotation_angle = 3
        self.speed = 2
        self.color = color
        self.color_name = color_name

        self.score = 0
        self.off_x = 0
        self.off_y = 0

        self.bullets = []

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def shoot(self):
        self.bullets.append(Bullet(self.rect.centerx, self.rect.centery, self.angle, self.color, self.color_name))

    def rotate_image(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        rad = 2*math.pi - math.radians(self.angle)
        hor = math.sin(rad) * self.speed
        ver = - math.cos(rad) * self.speed

        self.rect.x += hor + self.off_x
        self.rect.y += ver + self.off_y

        # For more accuray in rotation
        self.off_x = hor - int(hor)
        self.off_y = ver - int(ver)

    def handle_shooting(self):
        for bullet in self.bullets:
            bullet.move()

            # Out Borders Rigth or Left
            if bullet.rect.centerx < 0:
                bullet.rect.centerx = WIDTH
            elif WIDTH < bullet.rect.centerx:
                bullet.rect.centerx = 0

            # Out Borders Up or Down
            if bullet.rect.centery < 0:
                bullet.rect.centery = HEIGHT
            elif HEIGHT < bullet.rect.centery:
                bullet.rect.centery = 0

            if bullet.lifetime <= time.time() - bullet.lauch_time:
                self.bullets.pop(self.bullets.index(bullet))

    def handle_out_borders(self):
        # Out Borders Rigth or Left
        if self.rect.centerx < 0:
            self.rect.centerx = WIDTH
        elif WIDTH < self.rect.centerx:
            self.rect.centerx = 0

        # Out Borders Up or Down
        if self.rect.centery < 0:
            self.rect.centery = HEIGHT
        elif HEIGHT < self.rect.centery:
            self.rect.centery = 0

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

        font = pygame.font.SysFont("comicsans", 60)
        txt = font.render(str(self.score), True, self.color)
        screen.blit(txt, (self.x - txt.get_width()/2, 0))

        screen.blit(self.image, self.rect.topleft)


class Player(Jet):
    def __init__(self, color_name: str, color: tuple, x):
        super().__init__(color_name, color, x)

    def handle_rotation(self, left_key, right_key):
        dictionary = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT,
                    'a': pygame.K_a, 'd': pygame.K_d
                     }

        pressed = pygame.key.get_pressed()
        if pressed[dictionary[right_key]]:
            self.angle -= self.rotation_angle
        elif pressed[dictionary[left_key]]:
            self.angle += self.rotation_angle

        self.rotate_image()

    def handle_movement(self, left_key, right_key):
        self.handle_rotation(left_key, right_key)
        self.move()
        self.handle_shooting()

        self.handle_out_borders()


class Line:
    def __init__(self, m, p):
        self.m = m
        self.p = p
        self.points = [((y-p)/m, y) for y in range(HEIGHT)]


class AI_Opponent(Jet):
    def __init__(self, color_name, color, x, player):
        super().__init__(color_name, color, x)
        self.player = player
        self.shoot_time = time.time()
        self.shoot_interval = .5

    def rotate_AI(self, screen):
        player_rect = self.player.rect
        if player_rect.centerx != self.rect.centerx and player_rect.centery != self.rect.centery:
            m = (player_rect.centery-self.rect.centery)/(player_rect.centerx-self.rect.centerx)
            p = self.rect.centery - m*self.rect.centerx
            line = Line(m, p)

            X = player_rect.centerx - self.rect.centerx
            Y = player_rect.centery - self.rect.centery
            angle = math.pi/2 - math.atan(Y/X)

            # To face the right direction
            if self.rect.centerx < player_rect.centerx:
                angle += math.pi
            
            rad = math.radians(self.angle)
            if rad < angle:  # Has to go left
                self.angle += self.rotation_angle
            elif angle < rad:  # Has to go right
                self.angle -= self.rotation_angle

            precision = math.radians(2)
            dt = time.time() - self.shoot_time
            if abs(rad - angle) < precision and self.shoot_interval < dt:
                self.shoot_time = time.time()
                self.shoot()

    def move_AI(self, screen):
        self.move()
        self.handle_out_borders()

        self.handle_shooting()

        self.rotate_AI(screen)
        self.rotate_image()


class Bullet:
    def __init__(self, x, y, angle, color, color_name):
        size = 4
        self.image = pygame.transform.scale(
            pygame.image.load(f"assets/{color_name}Bullet.png"), (size, size))
        self.rect = self.image.get_rect(x=x-size/2, y=y)
        self.mask = pygame.mask.from_surface(self.image)

        self.color = color
        self.angle = angle
        self.speed = 4

        self.lauch_time = time.time()
        self.lifetime = 2

    def move(self):
        rad = 2*math.pi - math.radians(self.angle)
        hor = math.sin(rad) * self.speed
        ver = - math.cos(rad) * self.speed

        self.rect.x += hor
        self.rect.y += ver

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
