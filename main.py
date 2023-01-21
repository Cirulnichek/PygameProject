import os
import sys
# Я гей
from random import randint

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
        # Я гей
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
        self.health = 100

    def update(self, delta_x, delta_y):
        self.rect.x += delta_x
        self.rect.y += delta_y
        if pygame.sprite.spritecollideany(self, horizontal_borders) or \
                pygame.sprite.spritecollideany(self, vertical_borders) or \
                pygame.sprite.spritecollideany(self, battlefield):
            self.rect.x -= delta_x
            self.rect.y -= delta_y
        if pygame.sprite.spritecollideany(self, enemies):
            self.health -= 1
            if self.health <= 0:
                self.kill()


class Batrank(pygame.sprite.Sprite):
    image = load_image('batrank.png', -1)

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Batrank.image
        self.rect = self.image.get_rect()
        self.rect.x = main_hero.rect.x
        self.rect.y = main_hero.rect.y + 30
        self.add(batranks)
        self.do_kill = 0
        x1, y1, x2, y2 = self.rect.x, self.rect.y, x, y
        try:
            self.k = (y1 - y2) / (x1 - x2)
            self.b = (y1 - self.k * x1)
        except ZeroDivisionError:
            pass
        if x1 < x2:
            self.change = 5
        else:
            self.change = -5
        if abs(self.k) > 1.5:
            self.change //= 5

    def update(self):
        self.rect.x += self.change
        self.rect.y = self.rect.x * self.k + self.b
        if pygame.sprite.spritecollideany(self, horizontal_borders) or \
                pygame.sprite.spritecollideany(self, vertical_borders) or \
                pygame.sprite.spritecollideany(self, battlefield):
            self.do_kill += 20
        if pygame.sprite.spritecollideany(self, enemies):
            self.do_kill += 1
        if self.do_kill > 1:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    sheet_right = load_image('enemy.png')
    sheet_left = pygame.transform.flip(sheet_right, True, False)
    columns = 3
    rows = 2

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(enemies)
        self.frames = []
        self.cut_sheet(Enemy.sheet_left, Enemy.columns, Enemy.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.count = 0
        self.health = 3
        self.check_existing()
# Я гей
    def check_existing(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders) or \
                pygame.sprite.spritecollideany(self, vertical_borders) or \
                pygame.sprite.spritecollideany(self, battlefield):
            enemies.remove(self)
            all_sprites.remove(self)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.count += 1
        # if main_hero.rect.x - self.rect.x - self.rect.w >= 0:
        #     self.frames = []
        #     Я гей
        #     self.cut_sheet(Enemy.sheet_right, Enemy.columns, Enemy.rows)
        # else:
        #     self.frames = []
        #     self.cut_sheet(Enemy.sheet_left, Enemy.columns, Enemy.rows)
        if self.count == 6:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.count = 0
        if pygame.sprite.spritecollideany(self, batranks):
            self.health -= 1
        if self.health <= 0:
            enemies.remove(self)
            all_sprites.remove(self)

        x1, y1, x2, y2 = self.rect.x, self.rect.y, main_hero.rect.x, main_hero.rect.y
        try:
            k = (y1 - y2) / (x1 - x2)
            b = (y1 - k * x1)
            if x1 < x2:
                change = 3
            else:
                change = -3
            if abs(k) > 1.5:
                change //= 6
            self.rect.x += change
            self.rect.y = self.rect.x * k + b
            if pygame.sprite.spritecollideany(self, horizontal_borders) or \
                    pygame.sprite.spritecollideany(self, vertical_borders) or \
                    pygame.sprite.spritecollideany(self, battlefield):
                self.rect.x -= change
                self.rect.y = self.rect.x * k + b
        except ZeroDivisionError:
            pass
# Я гей

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
# Я гей
enemies = pygame.sprite.Group()

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
            if event.pos != (main_hero.rect.x, main_hero.rect.y):
                Batrank(*event.pos)
        if randint(1, 60) == 1:
            Enemy(randint(1, 1000), randint(1, 700))
    if right:
        hero.update(8, 0)
    if left:
        hero.update(-8, 0)
    if up:
        hero.update(0, -8)
    if down:
        hero.update(0, 8)
    print(main_hero.health)
    screen.fill((0, 0, 0))
    hero.update(0, 0)
    enemies.update()
    batranks.update()
    all_sprites.draw(screen)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
