"""
飞机大战 - 主入口文件
游戏的启动点，包含主循环和初始化逻辑
"""

import pygame
import sys
from typing import Optional

import config
from src.systems.state_machine import GameStateMachine


def init_pygame() -> pygame.Surface:
    """
    初始化 Pygame 并返回主屏幕对象

    Returns:
        pygame.Surface: 主游戏屏幕
    """
    # 初始化 mixer
    pygame.mixer.pre_init(
        config.MIXER_FREQUENCY,
        config.MIXER_SIZE,
        config.MIXER_CHANNELS,
        config.MIXER_BUFFER
    )

    # 初始化所有 Pygame 模块
    pygame.init()
    pygame.mixer.init()

    # 创建主屏幕
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.CAPTION)

    # 创建时钟对象
    clock = pygame.time.Clock()

    return screen


def parse_arguments() -> bool:
    """
    解析命令行参数

    Returns:
        bool: 是否启用调试模式
    """
    debug_mode = False
    if len(sys.argv) > 1 and "--debug" in sys.argv:
        debug_mode = True
        print("调试模式已启用")
    return debug_mode


def main() -> None:
    """
    游戏主函数
    """
    # 解析命令行参数
    debug_mode = parse_arguments()
    config.DEBUG_MODE = debug_mode

    # 初始化 Pygame
    screen = init_pygame()
    clock = pygame.time.Clock()

    # 初始化状态机
    state_machine = GameStateMachine(screen)

    # 主游戏循环
    running = True
    while running:
        # 1. 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                state_machine.handle_event(event)

        # 2. 逻辑更新
        state_machine.update()

        # 3. 画面渲染
        state_machine.draw(screen)

        # 更新屏幕
        pygame.display.flip()

        # 控制帧率
        clock.tick(config.FPS)

        # 显示 FPS (如果启用)
        if config.SHOW_FPS and config.DEBUG_MODE:
            fps = clock.get_fps()
            pygame.display.set_caption(f"{config.CAPTION} - FPS: {fps:.2f}")

    # 退出游戏
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
