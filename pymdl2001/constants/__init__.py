from pygame import *


class Window:
    CAPTION = '洒墨 - 天涯咫尺 待君挥毫'  # 窗口标题
    SCREEN_WIDTH = 305
    SCREEN_HEIGHT = 90


class WindowGame:
    CAPTION = '洒墨 - 简单小游戏'  # 窗口标题
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 640


class WindowTest:
    CAPTION = '洒墨 - 测试用例'  # 窗口标题
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 640


class Symbol:
    DIRECTIONS = (K_LEFT, K_RIGHT, K_UP, K_DOWN)
    KEYS = [
        K_q,
        K_w,
        K_e,
        K_r,
        K_a,
        K_s,
        K_d,
        K_f,
        K_z,
        K_x,
        K_c,
        K_v,
        K_u,
        K_i,
        K_o,
        K_p,
        K_j,
        K_k,
        K_l,
        K_m,

        # K_t,
        # K_y,
        # K_g,
        # K_h,
        # K_b,
        # K_n,

        K_SEMICOLON,
        K_COMMA,
        K_PERIOD,
        K_SLASH
    ]

    class Font:
        SimHei = "SimHei"
