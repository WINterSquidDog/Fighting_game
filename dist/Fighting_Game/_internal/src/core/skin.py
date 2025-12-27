# src/core/skin.py (упрощенный)
"""
Базовая структура скина - теперь основная логика в ResourceManager
"""

class Skin:
    def __init__(self, name, sprite_path, sound_path):
        self.name = name
        self.sprite_path = sprite_path
        self.sound_path = sound_path
        self.animations = {}