import pygame


def __trans_key_info_to_chars__(info=[]) -> list:
    """
    将输入信息转换为包括 当前按下所有按键 的字符数组
    :param info:
    :return:
    """
    if len(info) == 0:
        return
    chars = []
    dic = info[-1]
    for c in dic:
        if dic[c] == 1:
            chars.append(c)
    chars.sort()
    return chars


def print_key_info(info=[]):
    """
        对按键信息作输出处理
        :param info:
        :return:
        """
    # for item in info:
    #     print(item)
    print(info)
    for c in __trans_key_info_to_chars__(info):
        print(c, end='')
    else:
        print()


def show_visiable_key_info(screen, info=[]):
    """
    将键盘信息输出到屏幕
    :param screen:
    :param info:
    :return:
    """
    screen.blit(pygame.image.load('resources/back.jpg').convert(), (0, 0))
    for c in __trans_key_info_to_chars__(info):
        locate = [0, 0]
        ky0 = 0
        ky1 = ky0 + 1
        ky2 = ky1 + 1
        kx0 = 0
        kx1 = kx0 + 1
        kx2 = kx1 + 1
        kx3 = kx2 + 1
        kx4 = kx3 + 8
        kx5 = kx4 + 1
        kx6 = kx5 + 1
        kx7 = kx6 + 1
        if c == 'q':
            locate = [kx0, ky0]
        elif c == 'w':
            locate = [kx1, ky0]
        elif c == 'e':
            locate = [kx2, ky0]
        elif c == 'r':
            locate = [kx3, ky0]
        elif c == 'u':
            locate = [kx4, ky0]
        elif c == 'i':
            locate = [kx5, ky0]
        elif c == 'o':
            locate = [kx6, ky0]
        elif c == 'p':
            locate = [kx7, ky0]
        elif c == 'a':
            locate = [kx0, ky1]
        elif c == 's':
            locate = [kx1, ky1]
        elif c == 'd':
            locate = [kx2, ky1]
        elif c == 'f':
            locate = [kx3, ky1]
        elif c == 'j':
            locate = [kx4, ky1]
        elif c == 'k':
            locate = [kx5, ky1]
        elif c == 'l':
            locate = [kx6, ky1]
        elif c == ';':
            locate = [kx7, ky1]
        elif c == 'z':
            locate = [kx0, ky2]
        elif c == 'x':
            locate = [kx1, ky2]
        elif c == 'c':
            locate = [kx2, ky2]
        elif c == 'v':
            locate = [kx3, ky2]
        elif c == 'm':
            locate = [kx4, ky2]
        elif c == ',':
            locate = [kx5, ky2]
        elif c == '.':
            locate = [kx6, ky2]
        elif c == '/':
            locate = [kx7, ky2]
        coord = [20 * locate[0], 30 * locate[1]]
        screen.blit(pygame.font.SysFont(str(pygame.font.get_fonts()[75]), 30).render(c, 3, (0, 0, 255)),coord)
