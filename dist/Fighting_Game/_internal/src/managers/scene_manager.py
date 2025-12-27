# src/managers/scene_manager.py
"""
Псевдоним для обратной совместимости - теперь перенаправляет в game_manager
"""

from src.managers.game_manager import BaseScene

# Для обратной совместимости оставляем старый SceneManager
class SceneManager:
    def __init__(self):
        self.current = None

    def set(self, scene):
        self.current = scene
        if scene and hasattr(scene, 'start'):
            scene.start()

    def update(self, dt):
        if self.current:
            self.current.update(dt)

    def draw(self, surface):
        if self.current:
            self.current.draw(surface)

    def handle_event(self, event):
        if self.current and hasattr(self.current, 'handle_event'):
            self.current.handle_event(event)