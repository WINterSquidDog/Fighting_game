# src/scenes/intro_scene.py
import pygame
from src.managers.game_manager import BaseScene

class IntroSequenceScene(BaseScene):
    def __init__(self, gm, fighter_left, cameo_left, fighter_right, cameo_right, game_mode_data=None):
        super().__init__(gm)
        self.f_l = fighter_left
        self.c_l = cameo_left
        self.f_r = fighter_right
        self.c_r = cameo_right
        self.game_mode_data = game_mode_data or {}
        self.order = [self.f_l, self.c_l, self.f_r, self.c_r]
        self.index = 0
        self.timer = 0
        self.duration = 2.5
        
        print(f"🎬 IntroScene создана")
        print(f"  Режим: {self.game_mode_data.get('id', 'unknown')}")
        print(f"  Карта: {self.game_mode_data.get('map', 'unknown')}")
        print(f"  P1: {self.f_l} + {self.c_l}")
        print(f"  P2: {self.f_r} + {self.c_r}")
    
    def on_enter(self):
        self.order[0].play_animation("intro")

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.order):
                self.gm.set_scene("battle")  # ✅ Используем новый метод
                return 
            self.order[self.index].play_animation("intro")
        for obj in self.order:
            obj.update(dt)

    def draw(self, screen):
        # Рисуем фон в зависимости от карты
        self._draw_background(screen)
        
        for obj in self.order:
            obj.draw(screen)  # ✅ Используем draw вместо render
        
        # Отображаем информацию о предстоящем бое
        self._draw_fight_info(screen)
    
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
    
    def _draw_fight_info(self, screen):
        """Отображает информацию о предстоящем бое"""
        font = self.get_font(32, bold=True)
        
        # Название режима
        mode_id = self.game_mode_data.get('id', 'unknown')
        mode_names = {
            'vs_bot': 'VS BOT',
            'vs_friend': 'ПРОТИВ ДРУГА',
            'training': 'ТРЕНИРОВКА'
        }
        
        mode_name = mode_names.get(mode_id, mode_id)
        text = font.render(f"РЕЖИМ: {mode_name}", True, (255, 255, 255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, self.s(50)))
        
        # Название карты
        map_font = self.get_font(24)
        map_id = self.game_mode_data.get('map', 'random')
        map_names = {
            'soul_beach': 'SOUL BEACH',
            'hall_of_judgement': 'HALL OF JUDGEMENT',
            'deep_caves': 'DEEP CAVES',
            'everlost': 'EVERLOST',
            'random': 'RANDOM MAP'
        }
        
        map_name = map_names.get(map_id, map_id)
        map_text = map_font.render(f"КАРТА: {map_name}", True, (255, 215, 0))
        screen.blit(map_text, (screen.get_width()//2 - map_text.get_width()//2, self.s(100)))
        
        # Счетчик
        timer_font = self.get_font(48, bold=True)
        time_left = max(0, self.duration - self.timer)
        timer_text = timer_font.render(f"{int(time_left) + 1}", True, (255, 100, 100))
        screen.blit(timer_text, (screen.get_width()//2 - timer_text.get_width()//2, 
                               screen.get_height()//2 - timer_text.get_height()//2))