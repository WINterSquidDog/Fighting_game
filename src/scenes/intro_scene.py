# src/scenes/intro_scene.py
import pygame
from src.managers.game_manager import BaseScene  # ✅ Импортируем из game_manager

class IntroSequenceScene(BaseScene):
    def __init__(self, gm, fighter_left, cameo_left, fighter_right, cameo_right):
        super().__init__(gm)
        self.f_l = fighter_left
        self.c_l = cameo_left
        self.f_r = fighter_right
        self.c_r = cameo_right
        self.order = [self.f_l, self.c_l, self.f_r, self.c_r]
        self.index = 0
        self.timer = 0
        self.duration = 2.5
    
    def start(self):
        super().start()
        self.order[0].play_animation("intro")

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.order):
                self.gm.set_scene("battle")  # ✅ Используем новый метод
                return 
            self.order[self.index].play_animation("intro")
        for obj in self.order:
            obj.update(dt)

    def draw(self, screen):
        for obj in self.order:
            obj.draw(screen)  # ✅ Используем draw вместо render