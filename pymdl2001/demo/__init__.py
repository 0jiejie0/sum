import pygame
from constants import *
from demo.demo_module import PlaneWar


def start():
    # 初始化
    pygame.init()
    screen = pygame.display.set_mode((Window.SCREEN_WIDTH, Window.SCREEN_HEIGHT))
    pygame.display.set_caption(Window.CAPTION)
    update = False
    while True:
        pygame.time.Clock().tick(128)
        for event in pygame.event.get():
            PlaneWar().check_whitespace_quit(event)
            print("", end="")
        if update:
            update = False
