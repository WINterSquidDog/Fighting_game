# src/core/entity.py
import pygame
import abc

class Entity(abc.ABC):
    """Базовый объект мира"""
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity_x = 0  # Скорость по x
        self.velocity_y = 0  # Скорость по y
        self.is_facing_right = True  # Для персонажей и камео
        self.sprite = None  # ✅ ДОБАВЛЕНО: инициализация sprite

    def update(self, dt):  # dt - Время между кадрами
        """Обновление позиции"""
        self.rect.x += self.velocity_x * dt
        self.rect.y += self.velocity_y * dt
    
    @abc.abstractmethod
    def draw(self, surface):
        """В потомках - отрисовка спрайта"""
        pass

    def render(self, surface):
        """✅ ИСПРАВЛЕНО: проверяем наличие спрайта перед отрисовкой"""
        if hasattr(self, 'sprite') and self.sprite:
            surface.blit(self.sprite, self.rect)