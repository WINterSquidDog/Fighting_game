# src/scenes/battle_scene.py
import pygame
from src.managers.game_manager import BaseScene  # ✅ Импортируем из game_manager

class BattleScene(BaseScene):
    def __init__(self, gm, f_l, f_r):
        super().__init__(gm)
        self.f_l = f_l
        self.f_r = f_r
        self.ended = False
        self.winner = None
        self.timer = 0
    
    def update(self, dt):
        if not self.ended:
            self.f_l.update(dt)
            self.f_r.update(dt)
            if self.f_l.hp <= 0:
                self.ended = True
                self.winner = self.f_r
                self.end_battle()
            elif self.f_r.hp <= 0:
                self.ended = True
                self.winner = self.f_l
                self.end_battle()
        else:
            self.timer += dt
            if self.timer > 3:
                # ✅ Используем новую систему сцен
                self.gm.scenes["victory"].winner = self.winner
                self.gm.set_scene("victory")
    
    def end_battle(self):
        if self.winner:
            self.winner.play_animation("victory")
        self.timer = 0
    
    def draw(self, screen):
        self.f_l.draw(screen)
        self.f_r.draw(screen)