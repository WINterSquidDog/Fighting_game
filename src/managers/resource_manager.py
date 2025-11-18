# src/managers/resource_manager.py
"""
Единый менеджер ресурсов - загрузка изображений, звуков, анимаций
"""

import pygame
import os

class ResourceManager:
    def __init__(self, base_sprite_dir="Sprites", base_sound_dir="Sounds"):
        self.base_sprite_dir = base_sprite_dir
        self.base_sound_dir = base_sound_dir
        self._images = {}
        self._sounds = {}
        self._skins = {}  # { character: { skin_name: { anim_name: [frames] } } }
        pygame.mixer.init()

    def load_image(self, path):
        """Загрузка изображения с кэшированием"""
        if path in self._images:
            return self._images[path]
        if not os.path.exists(path):
            print(f"Warning: Image not found: {path}")
            return self._create_placeholder_surface(64, 64)
        
        try:
            img = pygame.image.load(path).convert_alpha()
            self._images[path] = img
            return img
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            return self._create_placeholder_surface(64, 64)

    def _create_placeholder_surface(self, width, height):
        """Создание заглушки если изображение не найдено"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((255, 0, 255))  # Магический розовый
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, width, height), 2)
        return surface

    def load_sound(self, path):
        """Загрузка звука с кэшированием"""
        if path in self._sounds:
            return self._sounds[path]
        if not os.path.exists(path):
            print(f"Warning: Sound not found: {path}")
            return None
        
        try:
            snd = pygame.mixer.Sound(path)
            self._sounds[path] = snd
            return snd
        except pygame.error as e:
            print(f"Error loading sound {path}: {e}")
            return None

    def load_character_skins(self, character_name):
        """
        Загружает все скины для персонажа
        Возвращает dict: { skin_name: { anim_name: [frames] } }
        """
        if character_name in self._skins:
            return self._skins[character_name]
            
        char_dir = os.path.join(self.base_sprite_dir, character_name)
        if not os.path.isdir(char_dir):
            print(f"Warning: Character directory not found: {char_dir}")
            self._skins[character_name] = {}
            return {}

        skins = {}
        for skin_name in os.listdir(char_dir):
            skin_dir = os.path.join(char_dir, skin_name)
            if not os.path.isdir(skin_dir):
                continue
                
            animations = self._load_animations_from_folder(skin_dir)
            if animations:  # Только если есть анимации
                skins[skin_name] = animations

        self._skins[character_name] = skins
        return skins

    def _load_animations_from_folder(self, folder_path):
        """Загрузка анимаций из папки"""
        animations = {}
        
        for anim_name in os.listdir(folder_path):
            anim_dir = os.path.join(folder_path, anim_name)
            if not os.path.isdir(anim_dir):
                continue
                
            frames = []
            # Сортируем файлы для правильной последовательности кадров
            frame_files = sorted([f for f in os.listdir(anim_dir) 
                                if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            
            for fname in frame_files:
                fpath = os.path.join(anim_dir, fname)
                frame = self.load_image(fpath)
                if frame:
                    frames.append(frame)
            
            if frames:
                animations[anim_name] = frames

        return animations

    def get_skin_animations(self, character_name, skin_name):
        """Получить анимации для конкретного скина"""
        return self._skins.get(character_name, {}).get(skin_name, {})

    def get_animation_frame(self, character_name, skin_name, anim_name, frame_index):
        """Получить конкретный кадр анимации"""
        anims = self.get_skin_animations(character_name, skin_name)
        frames = anims.get(anim_name, [])
        if frames and 0 <= frame_index < len(frames):
            return frames[frame_index]
        return None
    
    def preload_character(self, character_name):
        """Предзагрузка всех ресурсов персонажа"""
        return self.load_character_skins(character_name)