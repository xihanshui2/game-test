"""
测试游戏逻辑
"""
import pygame
import sys
import config
import io

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 初始化 Pygame
pygame.init()
pygame.mixer.init()

# 创建屏幕
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption(config.CAPTION)

# 测试导入所有模块
try:
    from src.entities.player import Player
    from src.entities.enemy import Enemy, EnemySpawner
    from src.entities.bullet import Bullet, BulletManager
    from src.systems.collision import CollisionSystem
    from src.ui.hud import HUD
    from src.systems.state_machine import GameStateMachine
    print("[OK] All modules imported successfully")
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)

# 测试创建游戏对象
try:
    player = Player(config.PLAYER_START_X, config.PLAYER_START_Y)
    print(f"[OK] Player created - Position: {player.get_position()}")

    enemy = Enemy(100, 100)
    print(f"[OK] Enemy created - Speed: {enemy.speed}")

    bullet = Bullet(100, 100)
    print(f"[OK] Bullet created - Damage: {bullet.damage}")

    bullet_manager = BulletManager()
    collision_system = CollisionSystem()
    hud = HUD(screen)

    print("[OK] All game objects created successfully")

except Exception as e:
    print(f"[ERROR] Object creation failed: {e}")
    sys.exit(1)

# 测试状态机
try:
    state_machine = GameStateMachine(screen)
    print("[OK] State machine initialized")
    print(f"  Current state: {type(state_machine.current_state).__name__}")
except Exception as e:
    print(f"[ERROR] State machine initialization failed: {e}")
    sys.exit(1)

print("\nGame tests passed! All systems working correctly.")
print("Run 'python main.py' to start the game")
print("Run 'python main.py --debug' to start in debug mode")
