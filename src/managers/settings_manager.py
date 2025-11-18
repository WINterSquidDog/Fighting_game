# src/managers/settings_manager.py
import json
import os
import pygame

class SettingsManager:
    def __init__(self):
        self.settings_file = "game_settings.json"
        self.base_resolution = (1280, 720)
        self.default_settings = {
            "music_volume": 0.5,
            "sound_volume": 0.7,
            "fullscreen": False,
            "resolution": [1280, 720],
            "language": "Русский"
        }
        self.current_settings = self.default_settings.copy()
        self.scale_factor = 1.0
        self.current_resolution = self.base_resolution
        
        # Сначала загружаем настройки
        self.load_settings()
        
        # Потом инициализируем LanguageManager
        from src.managers.language_manager import LanguageManager
        self.language_manager = LanguageManager()
        
        # Устанавливаем язык из настроек
        self.language_manager.set_language(self.current_settings["language"])
        
        self.update_scale_factor(self.current_resolution[0])
    
    def load_settings(self):
        """Загрузка настроек из файла"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    for key, value in loaded.items():
                        if key in self.current_settings:
                            self.current_settings[key] = value
                print("✅ Настройки загружены")
            else:
                self.save_settings()
        except Exception as e:
            print(f"❌ Ошибка загрузки настроек: {e}")
            self.save_settings()
    
    def save_settings(self):
        """Сохранение настроек в файл"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Ошибка сохранения настроек: {e}")
    
    def set_language(self, language_name):
        """Установка языка с сохранением в настройках"""
        success = self.language_manager.set_language(language_name)
        if success:
            self.current_settings["language"] = language_name
            self.save_settings()
            print(f"✅ Язык установлен и сохранен: {language_name}")
        return success
    
    def get_text(self, key, default=None):
        """Короткий метод для получения перевода"""
        return self.language_manager.get(key, default)
    
    # ... остальные методы без изменений ...
    def update_scale_factor(self, current_width):
        self.scale_factor = current_width / self.base_resolution[0]
        return self.scale_factor
    
    def scale_value(self, value):
        return int(value * self.scale_factor)
    
    def scale_rect(self, x, y, width, height):
        return pygame.Rect(
            self.scale_value(x),
            self.scale_value(y), 
            self.scale_value(width),
            self.scale_value(height)
        )
    
    def scale_font_size(self, size):
        return max(8, int(size * self.scale_factor))
    
    def apply_graphics_settings(self):
        try:
            flags = pygame.FULLSCREEN if self.current_settings["fullscreen"] else 0
            resolution = tuple(self.current_settings["resolution"])
            screen = pygame.display.set_mode(resolution, flags)
            self.current_resolution = resolution
            self.update_scale_factor(resolution[0])
            print(f"🖥️ Применены настройки: {resolution}, Scale: {self.scale_factor:.2f}")
            return screen
        except Exception as e:
            print(f"❌ Ошибка применения настроек: {e}")
            return None