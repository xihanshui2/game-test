"""
玩家实体 - 飞机大战玩家类
"""

import pygame
from typing import Tuple
import config


class Player(pygame.sprite.Sprite):
    """玩家飞机类"""

    def __init__(self, x: int, y: int) -> None:
        """
        初始化玩家

        Args:
            x: 初始 X 坐标
            y: 初始 Y 坐标
        """
        super().__init__()

        # TODO: 加载玩家图片资源
        self.image = pygame.Surface((50, 50))
        self.image.fill(config.GREEN)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.speed: int = config.PLAYER_SPEED
        self.health: int = config.PLAYER_MAX_HEALTH
        self.score: int = 0

    def update(self) -> None:
        """更新玩家状态"""
        # 获取按键状态
        keys = pygame.key.get_pressed()

        # 移动玩家
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # 边界检测
        self._keep_within_bounds()

    def _keep_within_bounds(self) -> None:
        """确保玩家不会飞出屏幕"""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > config.SCREEN_WIDTH:
            self.rect.right = config.SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > config.SCREEN_HEIGHT:
            self.rect.bottom = config.SCREEN_HEIGHT

    def take_damage(self, amount: int) -> None:
        """
        受到伤害

        Args:
            amount: 伤害值
        """
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self) -> bool:
        """
        检查玩家是否存活

        Returns:
            bool: 玩家是否存活
        """
        return self.health > 0

    def get_position(self) -> Tuple[int, int]:
        """
        获取玩家位置

        Returns:
            Tuple[int, int]: (x, y) 坐标
        """
        return (self.rect.centerx, self.rect.centery)
