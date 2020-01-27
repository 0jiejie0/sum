import pygame
from sys import exit
from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, surface, position):
        """
        玩家飞机类
        :param surface: 飞机图片
        :param position: 飞机初始位置
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image[0].get_rect()
        self.rect.left = position[0]
        self.rect.top = position[1]
        self.speed = 3
        self.directions = Symbol.DIRECTIONS
        self.offset = {
            self.directions[0]: 0,
            self.directions[1]: 0,
            self.directions[2]: 0,
            self.directions[3]: 0
        }

    def move(self):
        """
        移动飞机
        :return:
        """
        self.rect.top += (self.offset[K_DOWN] - self.offset[K_UP]) * self.speed
        if self.rect.top < 200:
            self.rect.top = 200
        elif self.rect.top > WindowGame.SCREEN_HEIGHT - self.rect.height:
            self.rect.top = WindowGame.SCREEN_HEIGHT - self.rect.height
        self.rect.left += (self.offset[K_RIGHT] - self.offset[K_LEFT]) * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.left > WindowGame.SCREEN_WIDTH - self.rect.width:
            self.rect.left = WindowGame.SCREEN_WIDTH - self.rect.width


def start():
    # 初始化
    pygame.init()
    screen = pygame.display.set_mode((WindowGame.SCREEN_WIDTH, WindowGame.SCREEN_HEIGHT))
    pygame.display.set_caption(WindowGame.CAPTION)
    # 载入图片
    background = pygame.image.load('resources/background.png')
    shoot_img = pygame.image.load('resources/shoot.png')
    # 剪切图片
    plane_imgs = [
        shoot_img.subsurface(pygame.Rect(0, 99, 102, 126)),
        shoot_img.subsurface(pygame.Rect(165, 360, 102, 126))]
    hero_pos = [185, 500]
    player = Player(plane_imgs, hero_pos)
    directions = Symbol.DIRECTIONS
    while True:
        pygame.time.Clock().tick(150)
        # 绘制背景
        screen.blit(background, (0, 0))
        # 绘制飞机
        screen.blit(player.image[0 if pygame.time.get_ticks() % 512 > 256 else 1], player.rect)
        # 更新屏幕
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:  # 退出
                quit()
                exit()
            elif event.type == KEYDOWN:
                key_down = event.key
                if key_down == K_ESCAPE:  # 退出
                    quit()
                    exit()
                elif key_down in directions:
                    player.offset[key_down] = 1
            elif event.type == KEYUP:
                key_up = event.key
                if key_up in directions:
                    player.offset[key_up] = 0
        player.move()
