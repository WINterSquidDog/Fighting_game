# src/scenes/victory_scene.py
import pygame
from src.managers.game_manager import BaseScene  # ✅ Импортируем из game_manager

class VictoryScene(BaseScene):
    def __init__(self, gm, winner):
        super().__init__(gm)
        self.winner = winner
        self.timer = 0
        self.duration = 3

    def start(self):
        super().start()
        if self.winner:
            self.winner.play_animation("victory")
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            # Можно перейти к меню или рестарту
            print("Victory scene completed")
    
    def draw(self, screen):
        if self.winner:
            self.winner.draw(screen)