# src/core/animations.py
import pygame
from typing import List, Dict

class Animation:
    """
    Простой покадровый Animation wrapper.
    frames: list[pygame.Surface]
    fps: кадры в секунду
    loop: повторять ли
    """
    def __init__(self, frames: List[pygame.Surface], fps: int = 12, loop: bool = True):
        self.frames = frames or []
        self.fps = fps
        self.loop = loop

        self.index = 0
        self.timer = 0.0

    def update(self, dt: float):
        if not self.frames:
            return
        self.timer += dt
        frame_time = 1.0 / max(1, self.fps)
        while self.timer >= frame_time:
            self.timer -= frame_time
            self.index += 1
            if self.index >= len(self.frames):
                if self.loop:
                    self.index = 0
                else:
                    self.index = len(self.frames) - 1

    def get_frame(self):
        if not self.frames:
            return None
        return self.frames[self.index]

    def reset(self):
        self.index = 0
        self.timer = 0.0

    def draw(self, surface: pygame.Surface, x: int, y: int, flip: bool = False):
        frame = self.get_frame()
        if frame is None:
            return
        if flip:
            frame = pygame.transform.flip(frame, True, False)
        surface.blit(frame, (x, y))


# src/core/animations.py
# УДАЛЯЕМ сломанный метод render() из класса AnimationController:

class AnimationController:
    def __init__(self, animations: Dict[str, Animation] = None, default: str = None, speed: float = 1.0):
        self.animations = animations or {}
        self.current = default
        self.speed = speed

    def update(self, dt: float):
        if self.current is None:
            return
        anim = self.animations.get(self.current)
        if not anim:
            return
        anim.update(dt * self.speed)

    def draw(self, surface: pygame.Surface, x: int, y: int, flip: bool = False):
        if self.current is None:
            return
        anim = self.animations.get(self.current)
        if not anim:
            return
        anim.draw(surface, x, y, flip)

    def change(self, name: str, reset: bool = True):
        if name not in self.animations:
            return
        if self.current == name:
            return
        self.current = name
        if reset:
            anim = self.animations.get(name)
            if anim:
                anim.reset()

    def add(self, name: str, animation: Animation):
        self.animations[name] = animation

    def set_speed(self, speed: float):
        self.speed = speed

    # ❌ УДАЛЯЕМ этот сломанный метод:
    # def render(self, surface):
    #     frame = None
    #     if self.anim and self.anim.current:
    #         frame = self.anim.current.get_frame()
    #     if frame:
    #         surface.blit(frame, self.rect)
    #     elif self.sprite:
    #         surface.blit(self.sprite, self.rect)