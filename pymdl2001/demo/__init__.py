import pygame
from sys import exit
from constants import *
from random import randint

score_history = 0
score = 0
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

    def update(self):
        self.rect.top += self.speed
        if self.rect.top > WindowGame.SCREEN_HEIGHT:
            global score
            self.kill()
            score -= 1  # 错过敌机，扣除一个分数


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
        self.is_hit = False

    def move(self):
        """
        移动飞机
        :return:
        """
        if self.is_hit:  # 被击中，失去移动能力
            return
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
        if self.is_hit:  # 被击中，失去射击能力
            return
        bullet = Bullet(bullet_img, self.rect.midtop)
        bullet.offset[K_UP] = 8
        self.bullet.add(bullet)


def check_whitespace_quit(event):
    """
    检测暂停或退出事件
    :param event: pygame.event事件
    :return: 0,正常进行;1,暂停
    """
    global pause
    if event.type == QUIT:  # 退出
        quit()
        exit()
    elif event.type == KEYDOWN:
        key_down = event.key
        if key_down == K_ESCAPE:  # 退出
            quit()
            exit()
        elif key_down == K_SPACE:
            pause ^= 1
    return pause


def start():
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
    global score
    global pause
    while True:  # 新一局游戏
        player = Player(plane_imgs, hero_pos)
        enemy = pygame.sprite.Group()
        enemy_destroy = pygame.sprite.Group()
        player_countdown = 1
        score = 0
        while True:
            pygame.time.Clock().tick(128)
            for event in pygame.event.get():
                if check_whitespace_quit(event) == 1:
                    break
                if event.type == KEYDOWN:
                    key_down = event.key
                    if key_down in directions:
                        player.offset[key_down] = 1
                elif event.type == KEYUP:
                    key_up = event.key
                    if key_up in directions:
                        player.offset[key_up] = 0
            player.move()
            if pause == 1:
                continue
            # 绘制背景
            screen.blit(background, (0, 0))
            # 绘制飞机
            if player.is_hit:  # 飞机被击中
                if time.get_ticks() % 24 == 0:  # 开始爆炸动画
                    player_countdown += 1
                if player_countdown > 5:  # 爆炸画面播放完成，本轮游戏结束
                    pause = 1
                    break
                screen.blit(player.image[player_countdown], player.rect)
            else:
                screen.blit(player.image[0 if pygame.time.get_ticks() % 512 > 256 else 1], player.rect)
            # 绘制子弹
            if time.get_ticks() % 8 == 0:
                player.single_shoot(bullet_img)
            player.bullet.draw(screen)
            # 绘制敌机
            if time.get_ticks() % 32 == 0:
                enemy.add(Enemy(enemy_img,
                                (randint(0, WindowGame.SCREEN_WIDTH - enemy_img.get_width()), -enemy_img.get_height())))
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
                        score += 1  # 击毁敌机，分数+1
            # 战机被撞
            player_destroys = pygame.sprite.spritecollide(player, enemy, True)
            if len(player_destroys) > 0:
                enemy_destroy.add(player_destroys)
                player.is_hit = True
            # 显示分数
            if score < 0:
                score = 0
            screen.blit(pygame.font.SysFont(Symbol.Font.SimHei, 30).render("当前得分：" + str(score), 3, (255, 0, 0)), (30, 20))
            # 更新屏幕
            player.bullet.update()
            pygame.display.update()
            if pause == 2:
                pause = 1
        # 游戏结束画面
        global score_history
        if score < 0:
            score = 0
        screen.blit(gameover, (0, 0))
        screen.blit(pygame.font.SysFont(Symbol.Font.SimHei, 30).render("历史最高分：" + str(score_history), 3, (50, 50, 50)),
                    (30, 30))
        screen.blit(pygame.font.SysFont(Symbol.Font.SimHei, 30).render("本次得分：" + str(score), 3, (255, 255, 255)),
                    (60, 70))
        if score > score_history:
            score_history = score
            screen.blit(pygame.font.SysFont(Symbol.Font.SimHei, 16).render("打破记录！", 3, (255, 0, 0)), (380, 78))
            screen.blit(pygame.font.SysFont(Symbol.Font.SimHei, 70).render("恭喜您！", 3, (0, 0, 200)), (125, 200))
        pygame.display.update()
