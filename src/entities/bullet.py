"""
子弹实体 - 飞机大战子弹类
"""

import pygame
import config


class Bullet(pygame.sprite.Sprite):
    """子弹类"""

    def __init__(self, x: int, y: int) -> None:
        """
        初始化子弹

        Args:
            x: 初始 X 坐标
            y: 初始 Y 坐标
        """
        super().__init__()

        # 创建子弹图像
        self.image = pygame.Surface((6, 16), pygame.SRCALPHA)
        # 绘制子弹形状
        pygame.draw.ellipse(self.image, config.YELLOW, (0, 0, 6, 16))
        pygame.draw.ellipse(self.image, (255, 255, 200), (1, 2, 4, 8))  # 高光

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.speed: int = config.BULLET_SPEED
        self.damage: int = config.BULLET_DAMAGE

    def update(self) -> None:
        """更新子弹状态"""
        self.rect.y -= self.speed

        # 如果子弹飞出屏幕，标记为删除
        if self.rect.bottom < 0:
            self.kill()


class BulletManager:
    """子弹管理器"""

    def __init__(self) -> None:
        """初始化子弹管理器"""
        self.cooldown_timer: int = 0
        self.cooldown: int = config.BULLET_COOLDOWN

    def can_shoot(self) -> bool:
        """
        检查是否可以射击

        Returns:
            bool: 是否可以射击
        """
        return self.cooldown_timer == 0

    def update(self) -> None:
        """更新冷却计时器"""
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def shoot(self, x: int, y: int, bullet_group: pygame.sprite.Group) -> None:
        """
        发射子弹

        Args:
            x: 子弹 X 坐标
            y: 子弹 Y 坐标
            bullet_group: 子弹精灵组
        """
        if self.can_shoot():
            bullet = Bullet(x, y)
            bullet_group.add(bullet)
            self.cooldown_timer = self.cooldown
