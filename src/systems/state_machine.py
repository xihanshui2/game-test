"""
状态机系统 - 管理游戏的不同状态
"""

import pygame
from typing import Optional, Dict, Any
import config


class GameState:
    """游戏状态基类"""

    def __init__(self, screen: pygame.Surface):
        """
        初始化游戏状态

        Args:
            screen: 游戏屏幕对象
        """
        self.screen = screen
        self.next_state: Optional[str] = None

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        处理事件

        Args:
            event: Pygame 事件对象
        """
        pass

    def update(self) -> None:
        """更新状态逻辑"""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        绘制状态

        Args:
            screen: 游戏屏幕对象
        """
        pass


class MenuState(GameState):
    """菜单状态"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        # TODO: 初始化菜单 UI 元素

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_state = config.STATE_RUNNING

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(config.BLACK)
        # TODO: 绘制菜单 UI


class RunningState(GameState):
    """游戏运行状态"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        # TODO: 初始化游戏实体

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = config.STATE_PAUSED

    def update(self) -> None:
        # TODO: 更新游戏逻辑
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(config.BLUE)
        # TODO: 绘制游戏实体


class PausedState(GameState):
    """暂停状态"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = config.STATE_RUNNING
            elif event.key == pygame.K_q:
                self.next_state = config.STATE_MENU

    def draw(self, screen: pygame.Surface) -> None:
        # 绘制半透明遮罩
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(config.BLACK)
        screen.blit(overlay, (0, 0))
        # TODO: 绘制暂停菜单


class GameOverState(GameState):
    """游戏结束状态"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_state = config.STATE_MENU

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(config.RED)
        # TODO: 绘制游戏结束画面


class GameStateMachine:
    """游戏状态机"""

    def __init__(self, screen: pygame.Surface):
        """
        初始化状态机

        Args:
            screen: 游戏屏幕对象
        """
        self.screen = screen
        self.states: Dict[str, GameState] = {
            config.STATE_MENU: MenuState(screen),
            config.STATE_RUNNING: RunningState(screen),
            config.STATE_PAUSED: PausedState(screen),
            config.STATE_GAME_OVER: GameOverState(screen),
        }
        self.current_state: GameState = self.states[config.STATE_MENU]

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        处理事件

        Args:
            event: Pygame 事件对象
        """
        self.current_state.handle_event(event)

        # 检查是否需要切换状态
        if self.current_state.next_state:
            self.change_state(self.current_state.next_state)

    def update(self) -> None:
        """更新当前状态"""
        self.current_state.update()

    def draw(self, screen: pygame.Surface) -> None:
        """
        绘制当前状态

        Args:
            screen: 游戏屏幕对象
        """
        self.current_state.draw(screen)

    def change_state(self, state_name: str) -> None:
        """
        切换游戏状态

        Args:
            state_name: 目标状态名称
        """
        if state_name in self.states:
            self.current_state = self.states[state_name]
            self.current_state.next_state = None
