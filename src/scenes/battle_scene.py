# src/scenes/battle_scene.py
import pygame
from src.managers.game_manager import BaseScene

class BattleScene(BaseScene):
    def __init__(self, gm, fighter_left, fighter_right, game_mode_data=None):
        super().__init__(gm)
        self.f_l = fighter_left
        self.f_r = fighter_right
        self.game_mode_data = game_mode_data or {}
        self.ended = False
        self.winner = None
        self.timer = 0
        
        print(f"🎮 BattleScene создана")
        print(f"  Режим: {self.game_mode_data.get('id', 'unknown')}")
        print(f"  Карта: {self.game_mode_data.get('map', 'unknown')}")
        print(f"  Игрок 1: {self.f_l}")
        print(f"  Игрок 2: {self.f_r}")
    
    def update(self, dt):
        if not self.ended:
            self.f_l.update(dt)
            self.f_r.update(dt)
            if self.f_l.hp <= 0:
                self.ended = True
                self.winner = self.f_r
                self.end_battle()
            elif self.f_r.hp <= 0:
                self.ended = True
                self.winner = self.f_l
                self.end_battle()
        else:
            self.timer += dt
            if self.timer > 3:
                # ✅ Используем новую систему сцен
                victory_scene = self.gm.get_scene("victory")
                if victory_scene:
                    victory_scene.winner = self.winner
                self.gm.set_scene("victory")
    
    def end_battle(self):
        if self.winner:
            self.winner.play_animation("victory")
        self.timer = 0
    
    def draw(self, screen):
        # Рисуем фон в зависимости от карты
        self._draw_background(screen)
        
        self.f_l.draw(screen)
        self.f_r.draw(screen)
        
        # Отображаем информацию о режиме
        self._draw_mode_info(screen)
    
    def _draw_background(self, screen):
        """Отрисовывает фон в зависимости от карты"""
        map_id = self.game_mode_data.get('map', 'random')
        
        # Цвета фона для разных карт
        map_colors = {
            'soul_beach': (135, 206, 235),  # Небесно-голубой для пляжа
            'hall_of_judgement': (70, 70, 90),  # Темно-серый для зала
            'deep_caves': (30, 30, 40),  # Очень темный для пещер
            'everlost': (100, 50, 150),  # Фиолетовый для забытого измерения
        }
        
        color = map_colors.get(map_id, (0, 0, 30))  # По умолчанию темно-синий
        screen.fill(color)
        
        # Отображаем название карты
        font = self.get_font(24)
        map_name = self._get_map_name(map_id)
        text = font.render(f"Карта: {map_name}", True, (255, 255, 255))
        screen.blit(text, (self.s(20), self.s(20)))
    
    def _get_map_name(self, map_id):
        """Возвращает название карты"""
        map_names = {
            'soul_beach': 'Soul Beach',
            'hall_of_judgement': 'Hall of Judgement',
            'deep_caves': 'Deep Caves',
            'everlost': 'Everlost',
            'random': 'Random'
        }
        return map_names.get(map_id, map_id)
    
    def _draw_mode_info(self, screen):
        """Отображает информацию о режиме игры"""
        mode_id = self.game_mode_data.get('id', 'unknown')
        is_training = self.game_mode_data.get('is_training', False)
        
        font = self.get_font(18)
        
        # Название режима
        mode_names = {
            'vs_bot': 'VS BOT',
            'vs_friend': 'Против друга',
            'training': 'Тренировка'
        }
        
        mode_name = mode_names.get(mode_id, mode_id)
        if is_training:
            mode_name += " (Тренировка)"
        
        text = font.render(f"Режим: {mode_name}", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() - text.get_width() - self.s(20), self.s(20)))