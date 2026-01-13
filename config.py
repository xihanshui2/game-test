"""
配置文件 - 飞机大战
包含所有游戏常量、颜色、分辨率等配置参数
"""

from typing import Tuple, Dict, Any

# 屏幕设置
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60
CAPTION: str = "飞机大战"

# 颜色定义 (RGB)
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)
BLUE: Tuple[int, int, int] = (0, 0, 255)
YELLOW: Tuple[int, int, int] = (255, 255, 0)
GRAY: Tuple[int, int, int] = (128, 128, 128)

# 游戏状态
STATE_MENU: str = "menu"
STATE_RUNNING: str = "running"
STATE_PAUSED: str = "paused"
STATE_GAME_OVER: str = "game_over"

# 玩家设置
PLAYER_START_X: int = SCREEN_WIDTH // 2
PLAYER_START_Y: int = SCREEN_HEIGHT - 100
PLAYER_SPEED: int = 5
PLAYER_MAX_HEALTH: int = 100

# 敌人设置
ENEMY_SPEED_MIN: int = 2
ENEMY_SPEED_MAX: int = 5
ENEMY_SPAWN_RATE: int = 60  # 帧数间隔

# 子弹设置
BULLET_SPEED: int = 10
BULLET_COOLDOWN: int = 15  # 帧数间隔
BULLET_DAMAGE: int = 10

# 音频设置 (预初始化)
MIXER_FREQUENCY: int = 44100
MIXER_SIZE: int = -16
MIXER_CHANNELS: int = 2
MIXER_BUFFER: int = 512

# 资源路径
ASSETS_DIR: str = "assets"
IMAGES_DIR: str = f"{ASSETS_DIR}/images"
AUDIO_DIR: str = f"{ASSETS_DIR}/audio"
FONTS_DIR: str = f"{ASSETS_DIR}/fonts"

# 游戏设置
DEBUG_MODE: bool = False
SHOW_FPS: bool = True
VOLUME: float = 0.7  # 0.0 到 1.0

# 字体设置
FONT_SIZE_SMALL: int = 18
FONT_SIZE_MEDIUM: int = 24
FONT_SIZE_LARGE: int = 36

# 分数设置
SCORE_ENEMY_KILL: int = 100
SCORE_BOSS_KILL: int = 1000
SCORE_PER_SECOND: int = 10
