import pygame
from constants import *


class DemoClass:
    """规范样例

    模块命名采用小写+下划线‘_’
    类命名采用驼峰命名法
    一个模块中包含若干相似类，不必一个类分出一个模块来

    书山有路勤为径
    学海无涯苦作舟
    """

    def demo(self):
        """函数样例
        和Java不同的是，这里的函数说明写在函数体里面
        :return: 一条hello字符串
        """
        statement_hello = "Hello world.\nHello Demo."
        # print(statement_hello)
        return statement_hello

    def demo_add(self, a, b):
        return a + b


class KeyInput:
    def lunch(self):
        # 初始化
        pygame.init()
        screen = pygame.display.set_mode([Window.SCREEN_WIDTH, Window.SCREEN_HEIGHT])
        pygame.display.set_caption(Window.CAPTION)
        status = {}
        while True:
            for event in pygame.event.get():
                info = []
                if event.type == QUIT:  # 退出
                    quit()
                    exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == 27:  # 退出
                        quit()
                        exit()
                    info.append('按下' if event.type == pygame.KEYDOWN else '松开')
                    temp_state = 1 if event.type == pygame.KEYDOWN else 0
                    if event.mod == pygame.KMOD_NONE:
                        info.append('普通按键')
                        if event.key in Symbol.KEYS:
                            c = chr(event.key)
                            info.append(c)
                            status.update({c: temp_state})
                    else:
                        if event.mod & pygame.KMOD_LSHIFT:
                            info.append('左上档键')
                        if event.mod & pygame.KMOD_RSHIFT:
                            info.append('右上档键')
                        if event.mod & pygame.KMOD_SHIFT:
                            info.append('上档键')
                elif event.type == MOUSEMOTION:
                    continue
                else:
                    info.append(time.get_ticks())
                info.append(event)
                info.append(status)
                self.output(info)
        # return temp

    def output(self, info=[]):
        """
        对按键信息作输出处理
        :param info:
        :return:
        """
        # for item in info:
        #     print(item)
        print(info)
        chars = []
        dic = info[-1]
        for c in dic:
            if dic[c] == 1:
                chars.append(c)
        chars.sort()
        for c in chars:
            print(c, end='')
        else:
            print()
