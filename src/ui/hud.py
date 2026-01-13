"""
HUD 系统 - 显示游戏信息
"""

import pygame
from typing import Tuple
import config


class HUD:
    """抬头显示器 (Heads-Up Display)"""

    def __init__(self, screen: pygame.Surface) -> None:
        """
        初始化 HUD

        Args:
            screen: 游戏屏幕对象
        """
        self.screen = screen
        self.font_small = pygame.font.Font(None, config.FONT_SIZE_SMALL)
        self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
        self.font_large = pygame.font.Font(None, config.FONT_SIZE_LARGE)

    def draw_health(self, health: int, max_health: int) -> None:
        """
        绘制生命值条

        Args:
            health: 当前生命值
            max_health: 最大生命值
        """
        bar_width = 200
        bar_height = 20
        x = 10
        y = 10

        # 计算生命值百分比
        health_percent = health / max_health

        # 绘制背景
        pygame.draw.rect(self.screen, config.GRAY, (x, y, bar_width, bar_height))

        # 绘制当前生命值
        pygame.draw.rect(
            self.screen,
            config.GREEN,
            (x, y, int(bar_width * health_percent), bar_height),
        )

        # 绘制边框
        pygame.draw.rect(self.screen, config.WHITE, (x, y, bar_width, bar_height), 2)

        # 绘制文字
        text = self.font_small.render(f"HP: {health}/{max_health}", True, config.WHITE)
        self.screen.blit(text, (x + 5, y + 2))

    def draw_score(self, score: int) -> None:
        """
        绘制分数

        Args:
            score: 当前分数
        """
        text = self.font_medium.render(f"Score: {score}", True, config.WHITE)
        rect = text.get_rect()
        rect.topright = (config.SCREEN_WIDTH - 10, 10)
        self.screen.blit(text, rect)

    def draw_fps(self, fps: float) -> None:
        """
        绘制 FPS

        Args:
            fps: 当前帧率
        """
        if config.SHOW_FPS and config.DEBUG_MODE:
            text = self.font_small.render(f"FPS: {fps:.1f}", True, config.YELLOW)
            rect = text.get_rect()
            rect.topright = (config.SCREEN_WIDTH - 10, 40)
            self.screen.blit(text, rect)

    def draw_text_centered(
        self,
        text: str,
        y_offset: int = 0,
        color: Tuple[int, int, int] = config.WHITE,
        font_size: int = None,
    ) -> None:
        """
        在屏幕中央绘制文字

        Args:
            text: 要绘制的文字
            y_offset: Y 轴偏移量
            color: 文字颜色
            font_size: 字体大小
        """
        font = (
            self.font_large if font_size is None else pygame.font.Font(None, font_size)
        )
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        rect.center = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + y_offset)
        self.screen.blit(surface, rect)
