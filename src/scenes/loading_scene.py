# src/scenes/loading_scene.py
import pygame
from src.managers.game_manager import BaseScene
from src.core.resource import resource_path
import sys
import os


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
        self._debug_logo_skip = False  # Для отладки
        
        # Проверяем первый запуск
        self._check_first_launch()
        
    def _check_first_launch(self):
        """Проверяет, нужно ли показывать логотип"""
        # Если явно указано пропустить логотип
        if self.skip_logo:
            print("⏩ Пропуск логотипа (явно указано в параметрах)")
            self.logo_displayed = True
            self._debug_logo_skip = "skip_logo=True"
            return
            
        # Проверяем через save_manager
        if hasattr(self.gm, 'save_manager') and self.gm.save_manager:
            is_first = self.gm.save_manager.is_first_launch()
            print(f"🔍 Проверка первого запуска: is_first_launch() = {is_first}")
            
            if not is_first:
                print("⏩ Пропуск логотипа (не первый запуск)")
                self.logo_displayed = True
                self._debug_logo_skip = "not first launch"
            else:
                print("🎬 Первый запуск! Будет показан логотип")
                self.logo_displayed = False
                self._debug_logo_skip = "first launch, show logo"
        else:
            # Если save_manager нет, показываем логотип
            print("⚠️ SaveManager не найден! Показываем логотип по умолчанию")
            self.logo_displayed = False
            self._debug_logo_skip = "no save_manager"
        
    def on_enter(self):
        self.progress = 0
        self.current_step = 0
        self.step_progress = 0
        self.logo_timer = 0
        
        # Загружаем ресурсы
        self._load_logo()
        self._load_background_art()
        
        # Повторная проверка (на случай, если логотип нужно пропустить)
        self._check_first_launch()
        
        print(f"📋 Статус логотипа: displayed={self.logo_displayed}, причина={self._debug_logo_skip}")
    
    def _load_logo(self):
        """Загружаем логотип"""
        try:
            logo_path = resource_path(os.path.join("Sprites", "arts", "logo.jpg"))
            print(f"🔍 Поиск логотипа: {logo_path}")
            
            if os.path.exists(logo_path):
                screen_width, screen_height = self.gm.screen.get_size()
                self.logo_image = pygame.image.load(logo_path).convert_alpha()
                
                # Масштабируем логотип
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
            extensions = [".jpg", ".jpeg", ".png", ".bmp"]
            art_path = None
            
            for ext in extensions:
                test_path = resource_path(os.path.join("Sprites", "arts", f"loading_bg{ext}"))
                if os.path.exists(test_path):
                    art_path = test_path
                    print(f"✅ Найден фон: {art_path}")
                    break
            
            if art_path:
                screen_width, screen_height = self.gm.screen.get_size()
                self.background_art = pygame.image.load(art_path).convert()
                self.background_art = pygame.transform.scale(self.background_art, (screen_width, screen_height))
                print(f"✅ Загружен фоновый арт: {self.background_art.get_size()}")
            else:
                print("❌ Фоновый арт не найден ни в одном формате!")
                # Создаем градиентный фон
                screen_width, screen_height = self.gm.screen.get_size()
                self.background_art = pygame.Surface((screen_width, screen_height))
                for i in range(screen_height):
                    color_val = int(30 + (i / screen_height) * 50)
                    pygame.draw.line(self.background_art, (color_val, 0, color_val//2), 
                                   (0, i), (screen_width, i))
                self.background_art = self.background_art.convert()
                print("✅ Создан градиентный фон-заглушка")
                
        except Exception as e:
            print(f"❌ Ошибка загрузки фонового арта: {e}")
            self.background_art = None
    
    def _draw_text_with_outline(self, screen, text, x, y, color, outline_color, size, outline_width=2):
        """Рисует текст с обводкой"""
        font = self.get_font(size, bold=True)
        
        # Рисуем обводку
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx == 0 and dy == 0:
                    continue
                outline_surf = font.render(text, True, outline_color)
                screen.blit(outline_surf, (x + dx, y + dy))
        
        # Рисуем основной текст
        text_surf = font.render(text, True, color)
        screen.blit(text_surf, (x, y))
    
    def _preload_resources(self):
        pass
        
    def update(self, dt):
        # Сначала показываем логотип
        if not self.logo_displayed:
            self.logo_timer += dt
            print(f"⏳ Показ логотипа: {self.logo_timer:.1f}/{self.logo_duration} сек")  # Отладка
            
            if self.logo_timer >= self.logo_duration:
                self.logo_displayed = True
                print("✅ Логотип показан, переходим к загрузке")
                
                # Если это был первый запуск, сохраняем флаг
                if hasattr(self.gm, 'save_manager') and self.gm.save_manager:
                    self.gm.save_manager.set_first_launch_false()
                    print("💾 Сохранен флаг первого запуска")
            return
            
        # Затем начинаем загрузку
        self.step_progress += dt * 0.5
        
        if self.step_progress >= 1.0:
            self.step_progress = 0
            self.current_step += 1
            self.progress = self.current_step / len(self.loading_steps)
            
            if self.current_step >= len(self.loading_steps):
                print("✅ Загрузка завершена, переход к сцене:", self.target_scene)
                self.gm.set_scene(self.target_scene)
                return
                
    def draw(self, screen):
        # Фаза 1: Показ логотипа на черном фоне
        if not self.logo_displayed:
            screen.fill((0, 0, 0))
            
            if self.logo_image:
                logo_x = screen.get_width() // 2 - self.logo_image.get_width() // 2
                logo_y = screen.get_height() // 2 - self.logo_image.get_height() // 2
                screen.blit(self.logo_image, (logo_x, logo_y))
            else:
                self._draw_text_with_outline(
                    screen, 
                    "VillianWar", 
                    screen.get_width() // 2 - 200,
                    screen.get_height() // 2 - 50,
                    (255, 255, 255),
                    (0, 0, 0),
                    72,
                    3
                )
            return
            
        # Фаза 2: Основной экран загрузки
        if self.background_art:
            screen.blit(self.background_art, (0, 0))
        else:
            screen.fill((0, 0, 30))
        
        # Название игры с обводкой
        self._draw_text_with_outline(
            screen,
            "VillianWar",
            self.s(50),
            self.s(50),
            (255, 255, 255),
            (0, 0, 0),
            48,
            2
        )
        
        # Полоса загрузки
        bar_width = self.s(600)
        bar_height = self.s(30)
        bar_x = screen.get_width()//2 - bar_width//2
        bar_y = screen.get_height()//2 + self.s(200)
        
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        fill_width = int(bar_width * self.progress)
        if fill_width > 0:
            pygame.draw.rect(screen, (0, 200, 100), (bar_x, bar_y, fill_width, bar_height))
            
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
        
        font = self.get_font(24)
        if self.current_step < len(self.loading_steps):
            step_text = font.render(self.loading_steps[self.current_step], True, (200, 200, 200))
            screen.blit(step_text, (screen.get_width()//2 - step_text.get_width()//2, bar_y - self.s(40)))
        
        percent = int(self.progress * 100)
        percent_text = font.render(f"{percent}%", True, (255, 255, 255))
        screen.blit(percent_text, (screen.get_width()//2 - percent_text.get_width()//2, bar_y + bar_height + self.s(20)))
        
        hint_font = self.get_font(18)
        hint_text = self.gm.settings.get_text("please_wait")
        hint = hint_font.render(hint_text, True, (150, 150, 150))
        screen.blit(hint, (screen.get_width()//2 - hint.get_width()//2, bar_y + bar_height + self.s(60)))
        
        # Отладочная информация (уберите после исправления)
        debug_font = self.get_font(16)
        debug_text = f"Logo: {self.logo_displayed}, Skip: {self.skip_logo}, Debug: {self._debug_logo_skip}"
        debug_surf = debug_font.render(debug_text, True, (255, 255, 0))
        screen.blit(debug_surf, (10, screen.get_height() - 30))