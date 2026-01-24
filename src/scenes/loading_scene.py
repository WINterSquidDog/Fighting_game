# src/scenes/loading_scene.py
import pygame
from src.managers.game_manager import BaseScene
import sys
import os
def resource_path(relative_path):
    """ Получает правильный путь к ресурсам для .exe """
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class LoadingScene(BaseScene):
    def __init__(self, gm, target_scene="menu", skip_logo=False):
        super().__init__(gm)
        self.target_scene = target_scene
        self.skip_logo = skip_logo
        self.progress = 0
        self.loading_steps = [
            self.gm.settings.get_text("loading_resources"),
            self.gm.settings.get_text("loading_characters"), 
            self.gm.settings.get_text("loading_scenes"),
            self.gm.settings.get_text("loading_complete")
        ]
        self.current_step = 0
        self.step_progress = 0
        self.background_art = None
        self.logo_displayed = False
        self.logo_timer = 0
        self.logo_duration = 2.0  # 2 секунды показываем логотип
        self.logo_image = None
        
        # Проверяем первый запуск
        if hasattr(gm, 'save_manager') and gm.save_manager:
            self.skip_logo = not gm.save_manager.is_first_launch()
        
    def on_enter(self):
        self.progress = 0
        self.current_step = 0
        self.step_progress = 0
        self.logo_displayed = False
        self.logo_timer = 0
        
        # Если пропускаем логотип, сразу начинаем загрузку
        if self.skip_logo:
            self.logo_displayed = True
            print("⏩ Пропуск логотипа (не первый запуск)")
        else:
            self._load_logo()
            self._load_background_art()
        
    def _load_logo(self):
        """Загружаем логотип"""
        try:
            logo_path = resource_path(os.path.join("Sprites", "arts", "logo.jpg"))
            if os.path.exists(logo_path):
                screen_width, screen_height = self.gm.screen.get_size()
                self.logo_image = pygame.image.load(logo_path).convert_alpha()
                
                # Масштабируем логотип (например, до 50% высоты экрана)
                logo_height = int(screen_height * 0.5)
                original_width, original_height = self.logo_image.get_size()
                scale_factor = logo_height / original_height
                logo_width = int(original_width * scale_factor)
                self.logo_image = pygame.transform.scale(self.logo_image, (logo_width, logo_height))
                print("✅ Загружен логотип")
            else:
                print(f"⚠️ Логотип не найден: {logo_path}")
                self.logo_image = None
        except Exception as e:
            print(f"❌ Ошибка загрузки логотипа: {e}")
            self.logo_image = None
        
    def _load_background_art(self):
        """Загружаем фоновый арт"""
        try:
            art_path = resource_path(os.path.join("Sprites", "arts", "loading_bg.png"))
            if os.path.exists(art_path):
                screen_width, screen_height = self.gm.screen.get_size()
                self.background_art = pygame.image.load(art_path).convert()
                self.background_art = pygame.transform.scale(self.background_art, (screen_width, screen_height))
                print("✅ Загружен фоновый арт загрузки")
            else:
                print(f"⚠️ Фоновый арт не найден: {art_path}")
                self.background_art = None
        except Exception as e:
            print(f"❌ Ошибка загрузки фонового арта: {e}")
            self.background_art = None
        
    def _preload_resources(self):
        pass
        
    def update(self, dt):
        # Сначала показываем логотип
        if not self.logo_displayed:
            self.logo_timer += dt
            if self.logo_timer >= self.logo_duration:
                self.logo_displayed = True
                # Если это был первый запуск, сохраняем флаг
                if hasattr(self.gm, 'save_manager') and self.gm.save_manager:
                    self.gm.save_manager.set_first_launch_false()
            return
            
        # Затем начинаем загрузку
        self.step_progress += dt * 0.5
        
        if self.step_progress >= 1.0:
            self.step_progress = 0
            self.current_step += 1
            self.progress = self.current_step / len(self.loading_steps)
            
            if self.current_step >= len(self.loading_steps):
                self.gm.set_scene(self.target_scene)
                return
                
    def draw(self, screen):
        # Фаза 1: Показ логотипа на черном фоне
        if not self.logo_displayed:
            screen.fill((0, 0, 0))  # Черный фон
            
            if self.logo_image:
                # Центрируем логотип
                logo_x = screen.get_width() // 2 - self.logo_image.get_width() // 2
                logo_y = screen.get_height() // 2 - self.logo_image.get_height() // 2
                screen.blit(self.logo_image, (logo_x, logo_y))
            else:
                # Заглушка если логотипа нет
                font = self.get_font(48, bold=True)
                logo_text = font.render("LOGO", True, (255, 255, 255))
                screen.blit(logo_text, (screen.get_width()//2 - logo_text.get_width()//2, 
                                      screen.get_height()//2 - logo_text.get_height()//2))
            return
            
        # Фаза 2: Основной экран загрузки
        # Фон - арт или черный
        if self.background_art:
            screen.blit(self.background_art, (0, 0))
        else:
            screen.fill((0, 0, 30))
        
        # Название игры в ЛЕВОМ ВЕРХНЕМ УГЛУ
        title_font = self.get_font(36, bold=True)
        title = title_font.render("FIGHTING GAME", True, (255, 255, 255))
        screen.blit(title, (self.s(50), self.s(50)))  # ⬅️ ЛЕВЫЙ ВЕРХНИЙ УГОЛ
        
        # Полоса загрузки (ЕЩЕ НИЖЕ)
        bar_width = self.s(600)
        bar_height = self.s(30)
        bar_x = screen.get_width()//2 - bar_width//2
        bar_y = screen.get_height()//2 + self.s(200)  # ⬅️ ЕЩЕ НИЖЕ
        
        # Фон полосы
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Заполненная часть
        fill_width = int(bar_width * self.progress)
        if fill_width > 0:
            pygame.draw.rect(screen, (0, 200, 100), (bar_x, bar_y, fill_width, bar_height))
            
        # Рамка
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Текущий шаг загрузки (НАД ПОЛОСКОЙ)
        font = self.get_font(24)
        if self.current_step < len(self.loading_steps):
            step_text = font.render(self.loading_steps[self.current_step], True, (200, 200, 200))
            screen.blit(step_text, (screen.get_width()//2 - step_text.get_width()//2, bar_y - self.s(40)))
        
        # Процент загрузки (ПОД ПОЛОСКОЙ)
        percent = int(self.progress * 100)
        percent_text = font.render(f"{percent}%", True, (255, 255, 255))
        screen.blit(percent_text, (screen.get_width()//2 - percent_text.get_width()//2, bar_y + bar_height + self.s(20)))
        
        # Подсказка (ЕЩЕ НИЖЕ)
        hint_font = self.get_font(18)
        hint_text = self.gm.settings.get_text("please_wait")
        hint = hint_font.render(hint_text, True, (150, 150, 150))
        screen.blit(hint, (screen.get_width()//2 - hint.get_width()//2, bar_y + bar_height + self.s(60)))