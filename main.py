import os
import sys

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
            self.image.fill((255, 255, 255))
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.image.fill((255, 255, 255))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Main_Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        radius = 25
        self.radius = 25
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(500, 500, 2 * radius, 2 * radius)

    def move(self, delta_x, delta_y):
        self.rect.x += delta_x
        self.rect.y += delta_y
        if pygame.sprite.spritecollideany(self, horizontal_borders) or \
            pygame.sprite.spritecollideany(self, vertical_borders) or \
            pygame.sprite.spritecollideany(self, battlefield):
            pass


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

hero = Main_Hero()

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                hero.move(10, 0)
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                hero.move(-10, 0)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()