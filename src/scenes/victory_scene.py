# src/scenes/victory_scene.py
import pygame
from src.managers.game_manager import BaseScene

class VictoryScene(BaseScene):
    def __init__(self, gm, winner, game_mode_data=None):
        super().__init__(gm)
        self.winner = winner
        self.game_mode_data = game_mode_data or {}
        self.timer = 0
        self.duration = 5.0
        
        print(f"🏆 VictoryScene создана")
        print(f"  Победитель: {self.winner}")
        print(f"  Режим: {self.game_mode_data.get('id', 'unknown')}")
        print(f"  Карта: {self.game_mode_data.get('map', 'unknown')}")
    
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            # Возвращаемся в меню
            self.gm.set_scene("menu")
    
    def draw(self, screen):
        screen.fill((30, 30, 50))
        
        # Заголовок победы
        title_font = self.get_font(48, bold=True)
        title_text = "ПОБЕДА!" if self.winner else "НИЧЬЯ!"
        title = title_font.render(title_text, True, (255, 215, 0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, self.s(100)))
        
        # Информация о победителе
        if self.winner:
            winner_font = self.get_font(36)
            winner_text = f"Победитель: {self.winner}"
            winner = winner_font.render(winner_text, True, (100, 255, 100))
            screen.blit(winner, (screen.get_width()//2 - winner.get_width()//2, self.s(200)))
        
        # Информация о режиме
        info_font = self.get_font(24)
        mode_id = self.game_mode_data.get('id', 'unknown')
        mode_names = {
            'vs_bot': 'VS BOT',
            'vs_friend': 'Против друга',
            'training': 'Тренировка'
        }
        mode_name = mode_names.get(mode_id, mode_id)
        
        mode_text = f"Режим: {mode_name}"
        mode = info_font.render(mode_text, True, (200, 200, 200))
        screen.blit(mode, (screen.get_width()//2 - mode.get_width()//2, self.s(280)))
        
        # Карта
        map_id = self.game_mode_data.get('map', 'unknown')
        map_names = {
            'soul_beach': 'Soul Beach',
            'hall_of_judgement': 'Hall of Judgement',
            'deep_caves': 'Deep Caves',
            'everlost': 'Everlost',
            'random': 'Случайная'
        }
        map_name = map_names.get(map_id, map_id)
        
        map_text = f"Карта: {map_name}"
        map = info_font.render(map_text, True, (200, 200, 200))
        screen.blit(map, (screen.get_width()//2 - map.get_width()//2, self.s(320)))
        
        # Таймер возврата
        timer_font = self.get_font(20)
        time_left = max(0, self.duration - self.timer)
        timer_text = f"Возврат в меню через: {int(time_left)} сек."
        timer = timer_font.render(timer_text, True, (150, 150, 150))
        screen.blit(timer, (screen.get_width()//2 - timer.get_width()//2, self.s(400)))
        
        # Подсказка
        hint_font = self.get_font(18)
        hint_text = "Нажмите любую клавишу для быстрого возврата"
        hint = hint_font.render(hint_text, True, (100, 100, 100))
        screen.blit(hint, (screen.get_width()//2 - hint.get_width()//2, self.s(450)))
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # Быстрый возврат в меню
                self.gm.set_scene("menu")