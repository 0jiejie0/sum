import pygame
from sys import exit
from constants import *


def start():
    # 初始化
    pygame.init()
    screen = pygame.display.set_mode((WindowGame.SCREEN_WIDTH, WindowGame.SCREEN_HEIGHT))
    pygame.display.set_caption(WindowGame.CAPTION)
    # 载入图片
    background = pygame.image.load('resources/background.png')
    shoot_img = pygame.image.load('resources/shoot.png')
    # 剪切图片
    hero_a = shoot_img.subsurface(pygame.Rect(0, 99, 102, 126))
    hero_b = shoot_img.subsurface(pygame.Rect(165, 360, 102, 126))
    hero_pos = [200, 500]
    directions = (K_LEFT, K_RIGHT, K_UP, K_DOWN)
    offset = {
        directions[0]: 0,
        directions[1]: 0,
        directions[2]: 0,
        directions[3]: 0,
    }
    step_once = 3
    while True:
        pygame.time.Clock().tick(150)
        # 绘制背景
        screen.blit(background, (0, 0))
        # 绘制飞机
        hero_pos[0] += (offset[K_RIGHT] - offset[K_LEFT]) * step_once
        if hero_pos[0] < 0:
            hero_pos[0] = 0
        elif hero_pos[0] > 378:
            hero_pos[0] = 378
        hero_pos[1] += (offset[K_DOWN] - offset[K_UP]) * step_once
        if hero_pos[1] < 200:
            hero_pos[1] = 200
        elif hero_pos[1] > 512:
            hero_pos[1] = 512
        screen.blit(hero_a if time.get_ticks() % 512 < 256 else hero_b, hero_pos)
        # 更新屏幕
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:  # 退出
                quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                key_down = event.key
                if key_down == 27:  # 退出
                    quit()
                    exit()
                elif key_down in directions:
                    offset[key_down] = 1
            elif event.type == pygame.KEYUP:
                key_up = event.key
                if key_up in directions:
                    offset[key_up] = 0
