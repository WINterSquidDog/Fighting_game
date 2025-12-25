# src/managers/game_manager.py
"""
GameManager - унифицированная система управления игрой.
Только базовый класс сцены и менеджер, без конкретных сцен.
"""

import pygame
import os
# src/managers/game_manager.py
class BaseScene:
    def __init__(self, game_manager):
        self.gm = game_manager
        
    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    # МЕТОДЫ МАСШТАБИРОВАНИЯ
    def s(self, value):
        """Короткий алиас для scale_value"""
        if hasattr(self.gm, 'settings') and self.gm.settings:
            return self.gm.settings.scale_value(value)
        return value
    
    def r(self, x, y, width, height):
        """Короткий алиас для scale_rect"""
        if hasattr(self.gm, 'settings') and self.gm.settings:
            return self.gm.settings.scale_rect(x, y, width, height)
        return pygame.Rect(x, y, width, height)
    
    def f(self, size):
        """Короткий алиас для scale_font_size"""
        if hasattr(self.gm, 'settings') and self.gm.settings:
            return self.gm.settings.scale_font_size(size)
        return size
    
    def get_font(self, size, bold=False):
        """Получение шрифта с масштабированием"""
        font_size = self.f(size)
        return pygame.font.SysFont("arial", font_size, bold=bold)

class GameManager:
    def __init__(self, resources, input_handler, ui_module=None):
        self.resources = resources
        self.input = input_handler
        self.ui = ui_module
        self.scenes = {}
        self.active_scene = None
        self.delta = 0.0
        self.settings = None
        self.music_playing = False

    def register_scene(self, name, scene):
        self.scenes[name] = scene

    def play_background_music(self):
        """Запускает фоновую музыку если она еще не играет"""
        if self.music_playing:
            return
            
        try:
            music_path = os.path.join("Sounds", "Music", "back_music.mp3")
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.settings.current_settings["music_volume"])
                pygame.mixer.music.play(-1)
                self.music_playing = True
                print("🎵 Фоновая музыка запущена")
            else:
                print(f"⚠️ Файл музыки не найден: {music_path}")
        except Exception as e:
            print(f"❌ Ошибка загрузки музыки: {e}")
    
    def update_music_volume(self):
        """Обновляет громкость музыки"""
        if self.music_playing:
            pygame.mixer.music.set_volume(self.settings.current_settings["music_volume"])

    def set_scene(self, name):
        if self.active_scene:
            if hasattr(self.active_scene, 'on_exit'):
                self.active_scene.on_exit()
        
        self.active_scene = self.scenes.get(name)
        if self.active_scene:
            if hasattr(self.active_scene, 'on_enter'):
                self.active_scene.on_enter()
            elif hasattr(self.active_scene, 'start'):  # ✅ Поддержка старых сцен
                self.active_scene.start()

    def handle_events(self, events):
        if self.active_scene:
            self.active_scene.handle_events(events)

    def update(self, dt):
        self.delta = dt
        if self.active_scene:
            self.active_scene.update(dt)

    def get_scene(self, scene_name):
        """Возвращает сцену по имени"""
        return self.scenes.get(scene_name)

    def draw(self, surface):
        if self.active_scene:
            self.active_scene.draw(surface)