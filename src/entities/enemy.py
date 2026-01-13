"""
敌人实体 - 飞机大战敌人类
"""

import pygame
import random
from typing import Optional
import config


class Enemy(pygame.sprite.Sprite):
    """敌机类"""

    def __init__(self, x: int, y: int) -> None:
        """
        初始化敌人

        Args:
            x: 初始 X 坐标
            y: 初始 Y 坐标
        """
        super().__init__()

        # 创建敌机图像
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self._draw_plane()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.speed: int = random.randint(config.ENEMY_SPEED_MIN, config.ENEMY_SPEED_MAX)
        self.health: int = 20
        self.damage: int = 10

    def _draw_plane(self) -> None:
        """绘制敌机形状（倒置的飞机）"""
        # 机身（倒置）
        pygame.draw.polygon(self.image, config.RED, [
            (20, 5),   # 机尾
            (15, 30),  # 机身右侧
            (20, 35),  # 机头
            (25, 30),  # 机身左侧
        ])
        # 主翼
        pygame.draw.polygon(self.image, config.RED, [
            (5, 15),   # 左翼尖
            (20, 10),  # 中心前
            (20, 25),  # 中心后
            (35, 15),  # 右翼尖
        ])

    def update(self) -> None:
        """更新敌人状态"""
        self.rect.y += self.speed

        # 如果敌人飞出屏幕，标记为删除
        if self.rect.top > config.SCREEN_HEIGHT:
            self.kill()

    def take_damage(self, amount: int) -> None:
        """
        受到伤害

        Args:
            amount: 伤害值
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()


class EnemySpawner:
    """敌人生成器"""

    def __init__(self) -> None:
        """初始化敌人生成器"""
        self.spawn_timer: int = 0
        self.spawn_rate: int = config.ENEMY_SPAWN_RATE

    def update(self, enemy_group: pygame.sprite.Group) -> None:
        """
        更新生成器，定时生成敌人

        Args:
            enemy_group: 敌人精灵组
        """
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer = 0
            self._spawn_enemy(enemy_group)

    def _spawn_enemy(self, enemy_group: pygame.sprite.Group) -> None:
        """
        生成一个新敌人

        Args:
            enemy_group: 敌人精灵组
        """
        x = random.randint(20, config.SCREEN_WIDTH - 20)
        y = -50  # 从屏幕上方生成
        enemy = Enemy(x, y)
        enemy_group.add(enemy)
