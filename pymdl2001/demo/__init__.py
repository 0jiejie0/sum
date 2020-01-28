import pygame
from sys import exit
from constants import *


class Bullet(pygame.sprite.Sprite):
    """
    子弹类
    """

    def __init__(self, surface, position):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.left = position[0] - self.rect.width / 2 + 2
        self.rect.top = position[1] - self.rect.height
        self.speed = 8
        self.directions = Symbol.DIRECTIONS
        self.offset = {
            self.directions[0]: 0,
            self.directions[1]: 0,
            self.directions[2]: 0,
            self.directions[3]: 0
        }

    def update(self):
        self.rect.top += (self.offset[K_DOWN] - self.offset[K_UP]) * self.speed
        if self.rect.top < -self.rect.height:
            self.kill()
        elif self.rect.top > WindowGame.SCREEN_HEIGHT:
            self.kill()
        self.rect.left += (self.offset[K_RIGHT] - self.offset[K_LEFT]) * self.speed
        if self.rect.left < -self.rect.width:
            self.kill()
        elif self.rect.left > WindowGame.SCREEN_WIDTH:
            self.kill()


class Player(pygame.sprite.Sprite):
    """
    玩家飞机类
    """

    def __init__(self, surface, position):
        """
        初始化
        :param surface: 飞机图片
        :param position: 飞机初始位置
        """
        super().__init__()
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
        self.bullet = pygame.sprite.Group()

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

    def single_shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        bullet.offset[K_UP] = 1
        self.bullet.add(bullet)


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
    # 子弹图片
    bullet_img = shoot_img.subsurface(pygame.Rect(1004, 987, 9, 21))
    hero_pos = [185, 500]
    player = Player(plane_imgs, hero_pos)
    directions = Symbol.DIRECTIONS
    while True:
        pygame.time.Clock().tick(128)
        # 绘制背景
        screen.blit(background, (0, 0))
        # 绘制飞机
        screen.blit(player.image[0 if pygame.time.get_ticks() % 512 > 256 else 1], player.rect)
        # 绘制子弹
        if time.get_ticks() % 8 == 0:
            player.single_shoot(bullet_img)
        player.bullet.draw(screen)
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
        player.bullet.update()
