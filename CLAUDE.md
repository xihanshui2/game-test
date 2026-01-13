# CLAUDE.md - Python 游戏开发规范

本文件包含了 [飞机大战] 的开发环境、指令、架构及编码标准。

## 1. 项目基础信息
- **技术栈**: Python 3.10+, Pygame 
- **项目目标**: 开发一个[简单描述，如：飞机大战]
- **核心库**: `pygame`, `numpy`, `pytest` (测试)

## 2. 核心指令
### 环境管理
- **安装依赖**: `pip install -r requirements.txt`
- **激活虚拟环境**: `source venv/bin/activate` (Mac/Linux) 或 `venv\Scripts\activate` (Windows)

### 运行与调试
- **启动游戏**: `python main.py`
- **带调试信息的启动**: `python main.py --debug`
- **运行测试**: `pytest`

### 开发工具
- **格式化代码**: `black .`
- **代码检查**: `flake8 .`
- **类型检查**: `mypy .`

## 3. 编码规范
### 命名约定
- **变量/函数/文件名**: `snake_case` (如 `player_health`, `move_character()`)
- **类名**: `PascalCase` (如 `PlayerSprite`, `EnemyManager`)
- **常量**: `UPPER_SNAKE_CASE` (如 `SCREEN_WIDTH`, `FPS`)

### 项目结构
- `assets/`: 存放图片、音频、字体
- `src/`: 核心代码逻辑
  - `entities/`: 玩家、敌人等对象定义
  - `systems/`: 碰撞检测、物理引擎等逻辑
  - `ui/`: 菜单、HUD 界面
- `main.py`: 游戏入口点
- `config.py`: 全局配置参数（颜色、分辨率、键位）

### 编码风格要求
- **类型提示 (Type Hinting)**: 所有的函数签名必须包含类型声明。
  - 示例: `def take_damage(amount: int) -> None:`
- **文档字符串**: 类和复杂的函数需包含简要的 Docstring。
- **避免硬编码**: 所有的数值（速度、颜色、偏移量）必须定义在 `config.py` 或类的常量中。
- **状态管理**: 倾向于使用状态机（State Machine）来管理游戏菜单、运行中、暂停、死亡等状态。

## 4. 常见开发模式
- **主循环逻辑**: 严格遵守 `事件处理 -> 逻辑更新 -> 画面渲染` 的顺序。
- **资源管理**: 资源加载应集中化，不要在游戏循环中动态加载图片/音频，应在启动时预加载并存入缓存字典。
- **解耦**: 尽量将渲染逻辑 (`draw()`) 与物理逻辑 (`update()`) 分离。

## 5. 常见问题排查 (Troubleshooting)
- 如果遇到声音延迟：检查 `pygame.mixer.pre_init` 设置。
- 如果遇到帧率不稳：确保使用 `pygame.time.Clock().tick(FPS)`。