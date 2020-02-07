from random import randint

import pygame
from constants import *
from output import *


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
    """
    控制台输出键盘状态
    ==>  输出转到窗体
    """

    def __init__(self) -> None:
        super().__init__()
        self.__lunch__()

    def __lunch__(self):
        # 初始化
        pygame.init()
        screen = pygame.display.set_mode([Window.SCREEN_WIDTH, Window.SCREEN_HEIGHT])
        pygame.display.set_caption(Window.CAPTION)
        status = {}
        while True:
            pygame.time.Clock().tick(256)
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
                    info.append(event)
                    info.append(status)
                    show_visiable_key_info(screen, info)
                    continue
                elif event.type == MOUSEMOTION:
                    continue
                else:
                    info.append(time.get_ticks())
                info.append(event)
                info.append(status)
                print_key_info(info)
            pygame.display.update()


class DishesFishOnTable:
    """
    饭桌上的碗筷背景 + ？？鱼光标
    """

    def __init__(self) -> None:
        super().__init__()
        self.__lunch__()

    def __lunch__(self):
        # 初始化
        pygame.init()
        screen = pygame.display.set_mode((WindowGame.SCREEN_WIDTH, WindowGame.SCREEN_HEIGHT))
        pygame.display.set_caption(WindowGame.CAPTION)
        # 载入图片
        background = pygame.image.load('resources/back.jpg').convert()
        cursor = pygame.image.load('resources/cur.png').convert_alpha()
        while True:
            # 绘制背景
            screen.blit(background, (0, 0))
            # 鼠标位置
            x, y = pygame.mouse.get_pos()
            # 计算左上角位置
            x -= cursor.get_width() / 2
            y -= cursor.get_height() / 2
            # 绘制光标
            screen.blit(cursor, (x, y))
            # 更新屏幕
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:  # 退出
                    quit()
                    exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == 27:  # 退出
                        quit()
                        exit()


class PlaneWar:
    """
    飞机大战
    """
    # 最高分
    score_history = 0
    # 玩家当前获得分数
    score = 0
    # 暂停游戏标识，初始化2代表打开游戏（需要加载游戏画面），1代表暂停，0代表正常进行
    pause = 2

    class Enemy(pygame.sprite.Sprite):
        """
        敌人类
        """

        def __init__(self, surface, position):
            super().__init__()
            self.image = surface
            self.rect = self.image.get_rect()
            self.rect.left = position[0]
            self.rect.top = position[1]
            self.speed = 6
            self.countdown = 0
            self.offset = 0

        def update(self):
            if PlaneWar.score < 0:
                PlaneWar.score = 0
            level = PlaneWar.score >> 3  # 作战等级
            self.rect.top += self.speed * ((level * 0.3) + 1)
            if self.rect.top > WindowGame.SCREEN_HEIGHT:
                self.kill()
                PlaneWar.score -= 1  # 错过敌机，扣除一个分数
            self.offset += level * level * self.speed * (
                    randint(0, WindowGame.SCREEN_WIDTH) - (WindowGame.SCREEN_WIDTH >> 1))  # 左右移动敌机
            self.offset = int(self.offset) >> 1
            self.offset //= WindowGame.SCREEN_WIDTH
            if self.offset > (self.speed * ((level * 0.3) + 1)):
                self.offset = (self.speed * ((level * 0.3) + 1))
            elif self.offset < -(self.speed * ((level * 0.3) + 1)):
                self.offset = -(self.speed * ((level * 0.3) + 1))
            self.rect.left += self.offset
            if self.offset == -1:
                self.offset = 0
            if self.rect.left < 0:  # 边界检查
                self.rect.left = 0 - self.rect.left
            elif self.rect.left > WindowGame.SCREEN_WIDTH - self.image.get_width():
                self.rect.left = WindowGame.SCREEN_WIDTH - self.image.get_width()

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
            self.speed = 1
            self.directions = Symbol.DIRECTIONS
            self.offset = {
                self.directions[0]: 0,
                self.directions[1]: 0,
                self.directions[2]: 0,
                self.directions[3]: 0
            }

        def update(self):
            self.rect.top += (self.offset[K_DOWN] - self.offset[K_UP]) * \
                             self.speed * ((PlaneWar.score >> 3) * 0.3 + 1)
            if self.rect.top < -self.rect.height:
                self.kill()
            elif self.rect.top > WindowGame.SCREEN_HEIGHT:
                self.kill()
            self.rect.left += (self.offset[K_RIGHT] - self.offset[K_LEFT]) * \
                              self.speed * ((PlaneWar.score >> 3) * 0.3 + 1)
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
            self.is_hit = False

        def move(self):
            """
            移动飞机
            :return:
            """
            if self.is_hit:  # 被击中，失去移动能力
                return
            # 高度平移
            self.rect.top += (self.offset[K_DOWN] - self.offset[K_UP]) * \
                             self.speed * ((PlaneWar.score >> 3) * 0.4 + 1)
            if self.rect.top < 200:
                self.rect.top = 200
            elif self.rect.top > WindowGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top = WindowGame.SCREEN_HEIGHT - self.rect.height
            # 左右平移
            self.rect.left += (self.offset[K_RIGHT] - self.offset[K_LEFT]) * \
                              self.speed * ((PlaneWar.score >> 3) * 0.4 + 1)
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.left > WindowGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left = WindowGame.SCREEN_WIDTH - self.rect.width

        def single_shoot(self, bullet_img):
            if self.is_hit:  # 被击中，失去射击能力
                return
            bullet = PlaneWar.Bullet(bullet_img, self.rect.midtop)
            bullet.offset[K_UP] = 9  # 射击速度
            self.bullet.add(bullet)

    def check_whitespace_quit(self, event):
        """
        检测暂停或退出事件
        :param event: pygame.event事件
        :return: 0,正常进行;1,暂停
        """
        if event.type == QUIT:  # 退出
            quit()
            exit()
        elif event.type == KEYDOWN:
            key_down = event.key
            if key_down == K_ESCAPE:  # 退出
                quit()
                exit()
            elif key_down == K_SPACE:
                self.pause ^= 1
        return self.pause

    def start(self):
        """
        逻辑主入口
        :return:
        """
        # 初始化
        pygame.init()
        screen = pygame.display.set_mode((WindowGame.SCREEN_WIDTH, WindowGame.SCREEN_HEIGHT))
        pygame.display.set_caption(WindowGame.CAPTION)
        # 载入图片
        background = pygame.image.load('resources/background.png')
        gameover = pygame.image.load('resources/gameover.png')
        shoot_img = pygame.image.load('resources/shoot.png')
        # 剪切图片
        plane_imgs = [
            shoot_img.subsurface(pygame.Rect(0, 99, 102, 126)),
            shoot_img.subsurface(pygame.Rect(165, 360, 102, 126)),
            shoot_img.subsurface(pygame.Rect(165, 234, 102, 126)),
            shoot_img.subsurface(pygame.Rect(330, 624, 102, 126)),
            shoot_img.subsurface(pygame.Rect(330, 498, 102, 126)),
            shoot_img.subsurface(pygame.Rect(432, 624, 102, 126)),
        ]
        # 子弹图片
        bullet_img = shoot_img.subsurface(pygame.Rect(1004, 987, 9, 21))
        # 敌机图片
        enemy_img = shoot_img.subsurface(pygame.Rect(534, 612, 57, 43))
        enemy_destory_img = [
            shoot_img.subsurface(pygame.Rect(267, 347, 57, 43)),
            shoot_img.subsurface(pygame.Rect(873, 697, 57, 43)),
            shoot_img.subsurface(pygame.Rect(267, 296, 57, 43)),
            shoot_img.subsurface(pygame.Rect(930, 697, 57, 43))
        ]
        hero_pos = [185, 500]
        directions = Symbol.DIRECTIONS
        while True:  # 新一局游戏
            player = PlaneWar.Player(plane_imgs, hero_pos)
            enemy = pygame.sprite.Group()
            enemy_destroy = pygame.sprite.Group()
            player_countdown = 1
            PlaneWar.score = 0
            temp_score = -1
            while True:
                pygame.time.Clock().tick(128)
                for event in pygame.event.get():  # 监听键盘和窗口退出事件
                    self.check_whitespace_quit(event)
                    if event.type == KEYDOWN:
                        key_down = event.key
                        if key_down in directions:
                            player.offset[key_down] = 1
                    elif event.type == KEYUP:
                        key_up = event.key
                        if key_up in directions:
                            player.offset[key_up] = 0
                if self.pause == 1:
                    continue
                player.move()
                # 绘制背景
                screen.blit(background, (0, 0))
                # 绘制飞机
                if player.is_hit:  # 飞机被击中
                    if time.get_ticks() % 24 == 0:  # 开始爆炸动画
                        player_countdown += 1
                    if player_countdown > 5:  # 爆炸画面播放完成，本轮游戏结束
                        self.pause = 1
                        break
                    screen.blit(player.image[player_countdown], player.rect)
                else:
                    screen.blit(player.image[0 if pygame.time.get_ticks() % 512 > 256 else 1], player.rect)
                # 绘制子弹
                if time.get_ticks() % 6 == 0:
                    player.single_shoot(bullet_img)
                player.bullet.draw(screen)
                # 绘制敌机
                if time.get_ticks() % 32 == 0:
                    enemy.add(PlaneWar.Enemy(enemy_img, (randint(0, WindowGame.SCREEN_WIDTH - enemy_img.get_width()),
                                                         -enemy_img.get_height())))
                enemy.update()
                enemy.draw(screen)
                # 子弹与敌机碰撞
                enemy_destroy.add(pygame.sprite.groupcollide(enemy, player.bullet, True, True))
                # 飞机坠落切换动画
                for e_dest in enemy_destroy:
                    screen.blit(enemy_destory_img[e_dest.countdown], e_dest.rect)
                    if time.get_ticks() % 14 == 0:
                        if e_dest.countdown < 3:
                            e_dest.countdown += 1
                        else:
                            e_dest.kill()
                            enemy_destroy.remove(e_dest)
                            PlaneWar.score += 1  # 击毁敌机，分数+1
                # 战机被撞
                player_destroys = pygame.sprite.spritecollide(player, enemy, True)
                if len(player_destroys) > 0:
                    enemy_destroy.add(player_destroys)
                    player.is_hit = True
                    # 玩家最终得分为：战机击毁前得分+战机撞击敌机数目
                    temp_score = PlaneWar.score + len(player_destroys)
                # 显示分数
                if temp_score != -1:
                    PlaneWar.score = temp_score
                if PlaneWar.score < 0:
                    PlaneWar.score = 0
                screen.blit(
                    pygame.font.SysFont(Symbol.Font.SimHei, 30).render("当前得分：" + str(PlaneWar.score), 3, (255, 0, 0)),
                    (30, 20))
                # 更新屏幕
                player.bullet.update()
                pygame.display.update()
                if self.pause == 2:  # 打开游戏，加载一帧画面后静止
                    self.pause = 1
            # 游戏结束画面
            PlaneWar.score = temp_score
            if PlaneWar.score < 0:
                PlaneWar.score = 0
            screen.blit(gameover, (0, 0))
            screen.blit(pygame.font.SysFont(Symbol.Font.SimHei, 30)
                        .render("历史最高分：" + str(PlaneWar.score_history), 3, (50, 50, 50)), (30, 30))
            screen.blit(pygame.font.SysFont(Symbol.Font.SimHei, 30)
                        .render("本次得分：" + str(PlaneWar.score), 3, (255, 255, 255)), (60, 70))
            if PlaneWar.score > PlaneWar.score_history:
                PlaneWar.score_history = PlaneWar.score
                screen.blit(pygame.font.SysFont(Symbol.Font.SimHei, 16).render("打破记录！", 3, (255, 0, 0)), (380, 78))
                screen.blit(pygame.font.SysFont(Symbol.Font.SimHei, 70).render("恭喜您！", 3, (0, 0, 200)), (125, 200))
            pygame.display.update()


class SysFonts:
    def show(self):
        # 初始化
        pygame.init()
        screen = pygame.display.set_mode((1280, 640))
        pygame.display.set_caption('洒墨 - 系统字体展示')
        # 载入图片
        background = pygame.image.load('resources/background.png')
        # 绘制背景
        # screen.blit(background, (0, 0))
        r = 0  # 行
        c = 0  # 列
        n = 0
        for f in pygame.font.get_fonts():
            n += 1
            if (78 <= n) and (n <= 79):
                continue
            color_ = (255, 255, 255)
            if n == 0:
                color_ = (0, 255, 0)
            screen.blit(pygame.font.SysFont(str(f), 20).render("洒墨" + str(f)[0:9], 3, color_),
                        (160 * c, 21 * r))
            r += 1
            if r == 30:
                c += 1
                r = 0
        screen.blit(
            pygame.font.SysFont(str(pygame.font.get_fonts()[78]), 20).render(str(43543435)[0:14], 3, (255, 255, 255)),
            (160 * c, 21 * 28))
        screen.blit(
            pygame.font.SysFont(str(pygame.font.get_fonts()[79]), 20).render(str("hell撒旦法？？?")[0:14], 3,
                                                                             (255, 255, 255)),
            (160 * c, 21 * 29))
        # 更新屏幕
        pygame.display.update()
        while True:
            pygame.time.Clock().tick(128)
            for event in pygame.event.get():
                PlaneWar().check_whitespace_quit(event)
                print("", end="")
