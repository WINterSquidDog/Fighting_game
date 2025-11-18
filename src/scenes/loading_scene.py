# src/scenes/loading_scene.py
import pygame
from src.managers.game_manager import BaseScene

class LoadingScene(BaseScene):
    def __init__(self, gm, target_scene="menu"):
        super().__init__(gm)
        self.target_scene = target_scene
        self.progress = 0
        self.loading_steps = [
            self.gm.settings.get_text("loading_resources"),
            self.gm.settings.get_text("loading_characters"), 
            self.gm.settings.get_text("loading_scenes"),
            self.gm.settings.get_text("loading_complete")
        ]
        self.loading_steps = [
            "Загрузка ресурсов...",
            "Инициализация персонажей...", 
            "Подготовка сцен...",
            "Запуск игры..."
        ]
        self.current_step = 0
        self.step_progress = 0
        
    def on_enter(self):
        self.progress = 0
        self.current_step = 0
        self.step_progress = 0
        self._preload_resources()
        
    def _preload_resources(self):
        pass
        
    def update(self, dt):
        self.step_progress += dt * 0.5
        
        if self.step_progress >= 1.0:
            self.step_progress = 0
            self.current_step += 1
            self.progress = self.current_step / len(self.loading_steps)
            
            if self.current_step >= len(self.loading_steps):
                self.gm.set_scene(self.target_scene)
                return
                
    def draw(self, screen):
        screen.fill((0, 0, 30))
        
        # Заголовок (масштабируемый)
        title_font = self.get_font(48, bold=True)
        title = title_font.render("FIGHTING GAME", True, (255, 255, 255))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, self.s(150)))
        
        # Полоса загрузки (масштабируемая)
        bar_width = self.s(600)
        bar_height = self.s(30)
        bar_x = screen.get_width()//2 - bar_width//2
        bar_y = screen.get_height()//2
        
        # Фон полосы
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Заполненная часть
        fill_width = int(bar_width * self.progress)
        if fill_width > 0:
            pygame.draw.rect(screen, (0, 200, 100), (bar_x, bar_y, fill_width, bar_height))
            
        # Рамка
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Текущий шаг загрузки
        font = self.get_font(24)
        if self.current_step < len(self.loading_steps):
            step_text = font.render(self.loading_steps[self.current_step], True, (200, 200, 200))
            screen.blit(step_text, (screen.get_width()//2 - step_text.get_width()//2, bar_y + self.s(50)))
        
        # Процент загрузки
        percent = int(self.progress * 100)
        percent_text = font.render(f"{percent}%", True, (255, 255, 255))
        screen.blit(percent_text, (screen.get_width()//2 - percent_text.get_width()//2, bar_y - self.s(40)))
        
        # Подсказка
        hint_font = self.get_font(18)
        hint_text = self.gm.settings.get_text("please_wait")
        hint = hint_font.render(hint_text, True, (150, 150, 150))
        screen.blit(hint, (screen.get_width()//2 - hint.get_width()//2, bar_y + self.s(100)))