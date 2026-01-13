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
        from src.ui.hud import HUD
        self.hud = HUD(screen)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_state = config.STATE_RUNNING

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(config.BLACK)
        # 绘制菜单标题
        self.hud.draw_text_centered("飞机大战", -50, config.GREEN, 48)
        self.hud.draw_text_centered("按 ENTER 开始游戏", 50, config.WHITE, 24)
        self.hud.draw_text_centered("方向键/WASD 移动，空格键射击", 100, config.GRAY, 18)


class RunningState(GameState):
    """游戏运行状态"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        # 初始化游戏实体
        from src.entities.player import Player
        from src.entities.enemy import EnemySpawner
        from src.entities.bullet import BulletManager
        from src.systems.collision import CollisionSystem
        from src.ui.hud import HUD

        self.player = Player(config.PLAYER_START_X, config.PLAYER_START_Y)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.enemy_spawner = EnemySpawner()
        self.bullet_manager = BulletManager()
        self.collision_system = CollisionSystem()
        self.hud = HUD(screen)

        self.clock = pygame.time.Clock()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = config.STATE_PAUSED
            elif event.key == pygame.K_SPACE:
                # 发射子弹
                pos = self.player.get_position()
                self.bullet_manager.shoot(pos[0], pos[1], self.bullets)

    def update(self) -> None:
        # 检查玩家是否存活
        if not self.player.is_alive():
            self.next_state = config.STATE_GAME_OVER
            return

        # 更新所有精灵
        self.all_sprites.update()
        self.enemies.update()
        self.bullets.update()

        # 更新生成器和管理器
        self.enemy_spawner.update(self.enemies)
        self.bullet_manager.update()

        # 碰撞检测
        hit_enemies, player_hit = self.collision_system.check_collisions(
            self.player, self.bullets, self.enemies
        )

        # 处理被击中的敌人
        for enemy in hit_enemies:
            if not enemy.alive():
                self.player.score += config.SCORE_ENEMY_KILL

        # 处理玩家被撞击
        if player_hit:
            self.player.take_damage(20)

        # 移除死亡敌人
        for enemy in self.enemies:
            if not enemy.alive():
                enemy.kill()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(config.BLACK)

        # 绘制所有精灵
        self.all_sprites.draw(screen)
        self.enemies.draw(screen)
        self.bullets.draw(screen)

        # 绘制 HUD
        self.hud.draw_health(self.player.health, config.PLAYER_MAX_HEALTH)
        self.hud.draw_score(self.player.score)

        # 显示 FPS（调试模式）
        if config.DEBUG_MODE:
            fps = self.clock.get_fps()
            self.hud.draw_fps(fps)


class PausedState(GameState):
    """暂停状态"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        from src.ui.hud import HUD
        self.hud = HUD(screen)

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

        # 绘制暂停菜单
        self.hud.draw_text_centered("暂停", -50, config.YELLOW, 48)
        self.hud.draw_text_centered("按 ESC 继续游戏", 30, config.WHITE, 24)
        self.hud.draw_text_centered("按 Q 返回菜单", 70, config.GRAY, 20)


class GameOverState(GameState):
    """游戏结束状态"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        from src.ui.hud import HUD
        self.hud = HUD(screen)
        self.final_score = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_state = config.STATE_MENU

    def set_score(self, score: int) -> None:
        """设置最终分数"""
        self.final_score = score

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(config.BLACK)
        # 绘制游戏结束画面
        self.hud.draw_text_centered("游戏结束", -80, config.RED, 48)
        self.hud.draw_text_centered(f"最终分数: {self.final_score}", 0, config.WHITE, 32)
        self.hud.draw_text_centered("按 ENTER 返回菜单", 80, config.GRAY, 20)


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
            score = getattr(self.current_state, 'player', None)
            score_value = score.score if score and hasattr(score, 'score') else None
            self.change_state(self.current_state.next_state, score_value)

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

    def change_state(self, state_name: str, score: int = None) -> None:
        """
        切换游戏状态

        Args:
            state_name: 目标状态名称
            score: 可选的分数参数
        """
        if state_name in self.states:
            # 如果切换到游戏结束状态，传递分数
            if state_name == config.STATE_GAME_OVER and score is not None:
                if isinstance(self.current_state, RunningState):
                    self.states[state_name].set_score(score)

            self.current_state = self.states[state_name]
            self.current_state.next_state = None
