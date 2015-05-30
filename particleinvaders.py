#! /usr/bin/env python

#
# Particle Invaders!
#
# a gamelet that demonstrates
# very simple particle effects
#
# by Chuck Arellano
# http://www.scriptedfun.com/
#
# MIT License
# March 17, 2007
#

import pygame, random
from pygame.locals import *

SCREENRECT = Rect(0, 0, 640, 480)
MARGINBOTTOM = 16
MARGINSIDES = 32
BLACK = (0, 0, 0)

def shotimage():
    image = pygame.Surface((5, 5))
    pygame.draw.circle(image, (255, 128, 0), (2, 2), 3)
    return image.convert()

def bombimage():
    image = pygame.Surface((3, 3))
    pygame.draw.circle(image, (255, 0, 0), (1, 1), 2)
    return image.convert()

def enemyimagesets(spritesheet):
    imagesets = []
    for y in range(1, 123, 11):
        images = []
        for x in [273, 290]:
            images.append(spritesheet.imgat((x, y, 16, 10)))
        imagesets.append(images)
    return imagesets

class Spritesheet:
    def __init__(self, file):
        self.surface = pygame.image.load(file)
    def imgat(self, rect, colorkey = BLACK):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.surface, (0, 0), rect)
        if colorkey is not None:
            image.set_colorkey(colorkey)
        return pygame.transform.scale2x(image).convert()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.unfire()
        self.rect = self.image.get_rect(bottom = SCREENRECT.height - MARGINBOTTOM)
    def update(self):
        x, y = pygame.mouse.get_pos()
        x = min(max(x, MARGINSIDES), SCREENRECT.width - MARGINSIDES)
        self.rect.centerx = x
        if self.fireon:
            if self.delay > 0:
                self.delay = self.delay - 1
            else:
                self.delay = 3
                Shot((self.rect.left + 3, self.rect.top))
                Shot((self.rect.right - 3, self.rect.top))
    def fire(self):
        self.fireon = True
        self.image = self.images[0]
    def unfire(self):
        self.image = self.images[1]
        self.delay = 0
        self.fireon = False

class Enemy(pygame.sprite.Sprite):
    def __init__ (self, setnum, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = self.imagesets[setnum]
        self.imagenum = 0
        self.image = self.getimage()
        self.rect = self.image.get_rect(center = pos)
        self.dx = 1
        self.frame = 0
    def update(self):
        self.frame = (self.frame + 1) % 5
        if self.frame == 0:
            self.image = self.getimage()
        self.rect.move_ip(self.dx, 0)
        if not random.randrange(600):
            Bomb(self.rect.midbottom)
    def check(self):
        if self.rect.left < MARGINSIDES or self.rect.right > SCREENRECT.width - MARGINSIDES:
            return True
        else:
            return False
    def getimage(self):
        self.imagenum = (self.imagenum + 1) % 2
        return self.images[self.imagenum]
    def kill(self):
        for i in range(3):
            Particle(self.rect.center, random.randrange(-5, 6), random.randrange(-10, 0), 0, 1, 3,
                     [((random.randrange(128, 256), random.randrange(128, 256), random.randrange(128, 256)),
                       (255, 255, 255), 20), ((255, 255, 255), (0, 0, 0), 10)])
        pygame.sprite.Sprite.kill(self)

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, vx, vy, ax, ay, size, colorstructure):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.vx, self.vy, self.ax, self.ay = vx, vy, ax, ay
        self.images = []
        for x in colorstructure:
            start, end, duration = x
            startr, startg, startb = start
            endr, endg, endb = end
            def f(s, e, t):
                return s + int((e - s)*(t/float(duration)))
            for t in range(duration):
                image = pygame.Surface((size, size)).convert()
                image.fill((f(startr, endr, t), f(startg, endg, t), f(startb, endb, t)))
                self.images.append(image)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = pos)
    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        self.vx = self.vx + self.ax
        self.vy = self.vy + self.ay
        if not self.images:
            self.kill()
        else:
            self.image = self.images.pop(0)

class Shot(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect(midbottom = pos)
        self.frame = 0
    def update(self):
        self.rect.move_ip(0, -16)
        if self.rect.top < 0:
            self.kill()
        Particle(self.rect.midtop, 0, random.randrange(1, 5), 0, 0, 2,
                 [((random.randrange(192, 256), random.randrange(64, 128), 0),
                  (0, 0, 0), 5)])

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect(midtop = pos)
    def update(self):
        self.rect.move_ip(0, 4)
        if self.rect.bottom > SCREENRECT.height:
            self.kill()
        Particle(self.rect.midtop, 0, random.randrange(-5, -1), 0, 0, 2,
                 [((255, random.choice([0, 128, 192, 255]), 0),
                  (0, 0, 0), 5)])

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size)
    background = pygame.Surface(SCREENRECT.size).convert()
    clock = pygame.time.Clock()

    shots = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()

    Player.containers = all
    Enemy.containers = all, enemies
    Shot.containers = all, shots
    Particle.containers = all
    Bomb.containers = all, bombs

    spritesheet = Spritesheet('invader.bmp')
    Player.images = [spritesheet.imgat((205, 156, 16, 9)), spritesheet.imgat((222, 156, 16, 9))]
    Shot.image = shotimage()
    Bomb.image = bombimage()
    Enemy.imagesets = enemyimagesets(spritesheet)

    player = Player()

    enemytype = 0
    for y in range(40, 360, 40):
        for x in range(80, 600, 40):
            Enemy(enemytype, (x, y))
        enemytype = enemytype + 1

    while 1:
        all.clear(screen, background)
        all.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if event.type == MOUSEBUTTONDOWN:
                player.fire()
            if event.type == MOUSEBUTTONUP:
                player.unfire()

        esprites = enemies.sprites()
        if esprites:
            change = reduce(lambda x, y: x or y, [enemy.check() for enemy in esprites])
            if change:
                for enemy in esprites:
                    enemy.dx = -enemy.dx

        pygame.sprite.groupcollide(enemies, shots, True, True)

        dirty = all.draw(screen)
        pygame.display.update(dirty)
        clock.tick(30)

if __name__ == '__main__':
    main()
