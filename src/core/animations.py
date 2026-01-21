# src/core/animations.py
import pygame
import os
import sys
from typing import List, Dict, Tuple, Optional
import cv2  # Для работы с видео

# Функция для получения корректного пути к ресурсам в pyinstaller
def resource_path(relative_path):
    """Получает правильный путь к ресурсам для работы как из .py, так и из .exe"""
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def load_video_frames(video_path: str, target_size: Tuple[int, int] = None, 
                     max_frames: int = None) -> Tuple[List[pygame.Surface], int]:
    """
    Загружает видео и конвертирует его в список кадров pygame.Surface
    Возвращает: (список кадров, FPS видео)
    
    Args:
        video_path: путь к видеофайлу
        target_size: целевой размер кадра (ширина, высота)
        max_frames: максимальное количество кадров для загрузки (для оптимизации)
    
    Returns:
        Tuple[List[pygame.Surface], int]: список кадров и FPS
    """
    frames = []
    fps = 60  # значение по умолчанию
    
    # Проверяем существование файла с учетом resource_path
    actual_path = resource_path(video_path)
    
    if not os.path.exists(actual_path):
        # Создаем заглушку
        if target_size:
            placeholder = pygame.Surface(target_size, pygame.SRCALPHA)
            placeholder.fill((80, 80, 150, 255))
            
            # Рисуем сообщение
            font = pygame.font.SysFont("arial", min(24, target_size[0] // 10))
            text = font.render("VIDEO NOT FOUND", True, (255, 255, 255))
            text_rect = text.get_rect(center=(target_size[0]//2, target_size[1]//2))
            placeholder.blit(text, text_rect)
            
            filename_font = pygame.font.SysFont("arial", min(14, target_size[0] // 15))
            filename_text = filename_font.render(os.path.basename(video_path), True, (200, 200, 200))
            filename_rect = filename_text.get_rect(center=(target_size[0]//2, target_size[1]//2 + 30))
            placeholder.blit(filename_text, filename_rect)
            
            frames = [placeholder] * 10  # 10 кадров заглушки
        return frames, fps
    
    try:
        # Пробуем использовать OpenCV для чтения видео
        import cv2
        import numpy as np
        
        cap = cv2.VideoCapture(actual_path)
        
        if not cap.isOpened():
            return frames, fps
        
        # Получаем FPS видео
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps <= 0:
            fps = 30  # значение по умолчанию если FPS не определен
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Ограничиваем количество кадров если нужно
            if max_frames and frame_count >= max_frames:
                break
            
            # Конвертируем BGR (OpenCV) в RGB (Pygame)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Транспонируем ось (height, width, channels) -> (width, height, channels)
            frame_rgb = np.transpose(frame_rgb, (1, 0, 2))
            
            # Создаем Surface из массива numpy
            frame_surface = pygame.surfarray.make_surface(frame_rgb)
            
            # Изменяем размер если нужно
            if target_size:
                frame_surface = pygame.transform.scale(frame_surface, target_size)
            
            frames.append(frame_surface)
            frame_count += 1
        
        cap.release()
        
        if not frames:
            print(f"⚠️ Видео не содержит кадров: {actual_path}")
            # Создаем одну заглушку
            if target_size:
                placeholder = pygame.Surface(target_size, pygame.SRCALPHA)
                placeholder.fill((80, 80, 150, 255))
                frames = [placeholder]
        
        print(f"✅ Загружено {len(frames)} кадров из видео {os.path.basename(video_path)} (FPS: {fps})")
        
    except ImportError:
        print("❌ OpenCV (cv2) не установлен. Не могу загрузить видео.")
        # Создаем анимированную заглушку
        if target_size:
            for i in range(10):  # 10 кадров анимации
                placeholder = pygame.Surface(target_size, pygame.SRCALPHA)
                hue = (i * 25) % 255
                placeholder.fill((hue, 100, 150, 255))
                
                font = pygame.font.SysFont("arial", min(20, target_size[0] // 10))
                text = font.render("NO OPENCV", True, (255, 255, 255))
                text_rect = text.get_rect(center=(target_size[0]//2, target_size[1]//2))
                placeholder.blit(text, text_rect)
                
                frames.append(placeholder)
    
    except Exception as e:
        print(f"❌ Ошибка загрузки видео {video_path}: {e}")
        # Создаем простую заглушку
        if target_size:
            placeholder = pygame.Surface(target_size, pygame.SRCALPHA)
            placeholder.fill((255, 100, 100, 255))
            frames = [placeholder]
    
    return frames, fps


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

class VideoAnimation(Animation):
    """Анимация на основе видео"""
    
    def __init__(self, video_path: str, target_size: Tuple[int, int] = None, 
                 fps: int = None, loop: bool = True, max_frames: int = None):
        """
        Инициализирует анимацию из видео
        
        Args:
            video_path: путь к видеофайлу
            target_size: целевой размер кадра
            fps: кадры в секунду (если None, берется из видео)
            loop: зациклено ли видео
            max_frames: максимальное количество кадров для загрузки
        """
        # Загружаем кадры из видео
        frames, video_fps = load_video_frames(video_path, target_size, max_frames)
        
        # Используем FPS из видео если не указан
        if fps is None:
            fps = video_fps if video_fps > 0 else 30
        
        super().__init__(frames, fps, loop)
        self.video_path = video_path
    
    @classmethod
    def create_looped(cls, video_path: str, target_size: Tuple[int, int] = None, 
                     fps: int = None, max_frames: int = None) -> 'VideoAnimation':
        """Создает зацикленную видео-анимацию"""
        return cls(video_path, target_size, fps, loop=True, max_frames=max_frames)
    
    @classmethod
    def create_single_play(cls, video_path: str, target_size: Tuple[int, int] = None,
                          fps: int = None, max_frames: int = None) -> 'VideoAnimation':
        """Создает одноразовую видео-анимацию (не зацикленную)"""
        return cls(video_path, target_size, fps, loop=False, max_frames=max_frames)


def play_video_animation(surface: pygame.Surface, position: Tuple[int, int], 
                        animation: VideoAnimation, dt: float) -> bool:
    """
    Проигрывает видео-анимацию на поверхности
    
    Args:
        surface: поверхность для отрисовки
        position: позиция (x, y) для отрисовки
        animation: видео-анимация
        dt: время с последнего кадра
    
    Returns:
        bool: True если анимация завершена (для не зацикленных)
    """
    # Обновляем анимацию
    animation.update(dt)
    
    # Получаем текущий кадр
    frame = animation.get_frame()
    
    if frame:
        surface.blit(frame, position)
    
    # Проверяем завершена ли анимация (для не зацикленных)
    if not animation.loop:
        # Анимация завершена если это последний кадр и прошло достаточно времени
        if animation.index == len(animation.frames) - 1:
            # Ждем время отображения последнего кадра
            frame_time = 1.0 / max(1, animation.fps)
            if animation.timer >= frame_time:
                return True
    
    return False


def play_looped_video(surface: pygame.Surface, position: Tuple[int, int],
                     video_path: str, target_size: Tuple[int, int], 
                     dt: float, fps: int = None) -> VideoAnimation:
    """
    Быстрая функция для проигрывания зацикленного видео
    
    Args:
        surface: поверхность для отрисовки
        position: позиция (x, y)
        video_path: путь к видео
        target_size: размер
        dt: время с последнего кадра
        fps: кадры в секунду
    
    Returns:
        VideoAnimation: объект анимации для последующего использования
    """
    # Создаем или получаем существующую анимацию
    if not hasattr(play_looped_video, 'cache'):
        play_looped_video.cache = {}
    
    cache_key = f"{video_path}_{target_size[0]}x{target_size[1]}"
    
    if cache_key not in play_looped_video.cache:
        animation = VideoAnimation.create_looped(video_path, target_size, fps)
        play_looped_video.cache[cache_key] = animation
    else:
        animation = play_looped_video.cache[cache_key]
    
    # Проигрываем анимацию
    animation.update(dt)
    frame = animation.get_frame()
    if frame:
        surface.blit(frame, position)
    
    return animation


def play_single_video(surface: pygame.Surface, position: Tuple[int, int],
                     video_path: str, target_size: Tuple[int, int],
                     dt: float, animation_cache: Dict = None, 
                     fps: int = None) -> Tuple[bool, Optional[VideoAnimation]]:
    """
    Быстрая функция для одноразового проигрывания видео
    
    Args:
        surface: поверхность для отрисовки
        position: позиция (x, y)
        video_path: путь к видео
        target_size: размер
        dt: время с последнего кадра
        animation_cache: кэш для хранения анимаций
        fps: кадры в секунду
    
    Returns:
        Tuple[bool, Optional[VideoAnimation]]: 
            - True если видео завершено
            - объект анимации (None если завершена)
    """
    # Используем кэш если предоставлен
    if animation_cache is not None:
        cache_key = f"{video_path}_{target_size[0]}x{target_size[1]}"
        
        if cache_key not in animation_cache:
            # Создаем новую анимацию
            animation = VideoAnimation.create_single_play(video_path, target_size, fps)
            animation_cache[cache_key] = {
                'animation': animation,
                'completed': False
            }
        
        cache_entry = animation_cache[cache_key]
        
        if cache_entry['completed']:
            return True, None
        
        animation = cache_entry['animation']
        completed = play_video_animation(surface, position, animation, dt)
        
        if completed:
            cache_entry['completed'] = True
            return True, None
        
        return False, animation
    else:
        # Без кэша - создаем новую анимацию каждый раз
        animation = VideoAnimation.create_single_play(video_path, target_size, fps)
        completed = play_video_animation(surface, position, animation, dt)
        
        if completed:
            return True, None
        else:
            return False, animation





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