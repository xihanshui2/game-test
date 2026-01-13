"""
碰撞检测系统 - 处理游戏实体间的碰撞
"""

import pygame
from typing import List, Tuple
import config


class CollisionSystem:
    """碰撞检测系统"""

    def __init__(self) -> None:
        """初始化碰撞系统"""
        pass

    def check_bullet_enemy_collision(
        self, bullets: pygame.sprite.Group, enemies: pygame.sprite.Group
    ) -> List[pygame.sprite.Sprite]:
        """
        检测子弹与敌人的碰撞

        Args:
            bullets: 子弹精灵组
            enemies: 敌人精灵组

        Returns:
            List[pygame.sprite.Sprite]: 被击中的敌人列表
        """
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        hit_enemies = []

        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                enemy.take_damage(bullet.damage)
                hit_enemies.append(enemy)

        return hit_enemies

    def check_player_enemy_collision(
        self, player: pygame.sprite.Sprite, enemies: pygame.sprite.Group
    ) -> bool:
        """
        检测玩家与敌人的碰撞

        Args:
            player: 玩家精灵
            enemies: 敌人精灵组

        Returns:
            bool: 是否发生碰撞
        """
        hits = pygame.sprite.spritecollide(player, enemies, True)
        return len(hits) > 0

    def check_collisions(
        self,
        player: pygame.sprite.Sprite,
        bullets: pygame.sprite.Group,
        enemies: pygame.sprite.Group,
    ) -> Tuple[List[pygame.sprite.Sprite], bool]:
        """
        检测所有碰撞

        Args:
            player: 玩家精灵
            bullets: 子弹精灵组
            enemies: 敌人精灵组

        Returns:
            Tuple[List[pygame.sprite.Sprite], bool]: (被击中的敌人列表, 玩家是否被撞击)
        """
        hit_enemies = self.check_bullet_enemy_collision(bullets, enemies)
        player_hit = self.check_player_enemy_collision(player, enemies)

        return hit_enemies, player_hit
