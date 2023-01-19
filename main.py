import os
import sys

import math

import pygame

pygame.init()
pygame.display.set_caption('My Game')
size = width, height = 1000, 700
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Wall(pygame.sprite.Sprite):
    image = load_image('wall.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Wall.image
        self.rect = self.image.get_rect()
        self.rect.x = 100 * x
        self.rect.y = 100 * y
        self.add(all_sprites)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Main_Hero(pygame.sprite.Sprite):
    image = load_image('hero.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Main_Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500

    def update(self, delta_x, delta_y):
        self.rect.x += delta_x
        self.rect.y += delta_y
        if pygame.sprite.spritecollideany(self, horizontal_borders) or \
                pygame.sprite.spritecollideany(self, vertical_borders) or \
                pygame.sprite.spritecollideany(self, battlefield):
            self.rect.x -= delta_x
            self.rect.y -= delta_y


class Batrank(pygame.sprite.Sprite):
    image = load_image('batrank.png', -1)

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Batrank.image
        self.rect = self.image.get_rect()
        self.rect.x = main_hero.rect.x
        self.rect.y = main_hero.rect.y + 30
        delta_x = x - main_hero.rect.x
        delta_y = y - main_hero.rect.y
        self.alpha = math.atan(delta_x / delta_y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed * math.sin(self.alpha)
        self.rect.y += self.speed * math.cos(self.alpha)
        if pygame.sprite.spritecollideany(self, horizontal_borders) or \
                pygame.sprite.spritecollideany(self, vertical_borders) or \
                pygame.sprite.spritecollideany(self, battlefield):
            self.kill()


all_sprites = pygame.sprite.Group()

battlefield = pygame.sprite.Group()

Wall(0, 0, battlefield)
Wall(1, 0, battlefield)
Wall(2, 0, battlefield)
Wall(0, 1, battlefield)
for i in range(10):
    Wall(i, 6, battlefield)
Wall(6, 5, battlefield)
Wall(7, 5, battlefield)
Wall(8, 5, battlefield)
Wall(9, 5, battlefield)
Wall(2, 3, battlefield)
Wall(3, 3, battlefield)
Wall(4, 3, battlefield)
Wall(5, 3, battlefield)
Wall(8, 4, battlefield)
Wall(9, 4, battlefield)

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

Border(0, 200, 0, 600)
Border(300, 0, 1000, 0)
Border(999, 0, 999, 800)

hero = pygame.sprite.Group()
main_hero = Main_Hero()
main_hero.add(hero)

batranks = pygame.sprite.Group()

left = right = up = down = False

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_d]:
                right = True
            if pygame.key.get_pressed()[pygame.K_a]:
                left = True
            if pygame.key.get_pressed()[pygame.K_w]:
                up = True
            if pygame.key.get_pressed()[pygame.K_s]:
                down = True
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_d, pygame.K_a]:
                left = right = False
            if event.key in [pygame.K_w, pygame.K_s]:
                up = down = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Batrank(*event.pos).add(batranks)
    if right:
        hero.update(8, 0)
    if left:
        hero.update(-8, 0)
    if up:
        hero.update(0, -8)
    if down:
        hero.update(0, 8)
    batranks.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
