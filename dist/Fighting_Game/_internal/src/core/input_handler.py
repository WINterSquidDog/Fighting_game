# src/input_handler.py
"""
InputHandler
------------
Управляет вводом от клавиатуры и геймпада, переводит его в "команды" (action signals).
Поддерживает:
 - профили управления (rebindable)
 - клавиатуру + базовый геймпад (pygame joystick)
 - опрос состояний (is_down, was_pressed_this_frame)
 - интерфейс для получения текущей команды (например 'left', 'attack_1', 'block')

Как наследовать/расширять:
 - Наследуй InputHandler если нужен специфичный парсинг (например хитбокс-контексты)
 - Переопредели метод map_event_to_action(event) для особого поведения
"""

import pygame
from collections import defaultdict

DEFAULT_KEYMAP = {
    "left": [pygame.K_a, pygame.K_LEFT],
    "right": [pygame.K_d, pygame.K_RIGHT],
    "up": [pygame.K_w, pygame.K_UP],
    "down": [pygame.K_s, pygame.K_DOWN],
    "attack_1": [pygame.K_j],
    "attack_2": [pygame.K_k],
    "attack_3": [pygame.K_l],
    "block": [pygame.K_i],
    "special_1": [pygame.K_u],
    "special_2": [pygame.K_o],
    "pause": [pygame.K_ESCAPE]
}

class InputHandler:
    """
    Хранит состояния и предоставляет API:
      - update(events)  -> обработать Pygame события
      - is_down(action) -> держат ли сейчас кнопку
      - was_pressed(action) -> нажата ли была в этом кадре
      - get_axis() -> (-1, 0, 1) горизонтальная ось
    """

    def __init__(self, keymap=None):
        self.keymap = keymap or DEFAULT_KEYMAP.copy()
        # текущие состояния
        self._down = defaultdict(bool)
        self._pressed = defaultdict(bool)
        # джойстики
        self.joysticks = []
        self._init_joysticks()

    def _init_joysticks(self):
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            joy = pygame.joystick.Joystick(i)
            joy.init()
            self.joysticks.append(joy)

    def update(self, events):
        """Обрабатывать список событий pygame.event.get()"""
        # Сбрасываем «нажато в этом кадре»
        self._pressed = defaultdict(bool)

        for e in events:
            # клавиши клавиатуры
            if e.type == pygame.KEYDOWN:
                action = self._key_to_action(e.key)
                if action:
                    self._down[action] = True
                    self._pressed[action] = True
            elif e.type == pygame.KEYUP:
                action = self._key_to_action(e.key)
                if action:
                    self._down[action] = False
            # джойстик (основные кнопки)
            elif e.type == pygame.JOYBUTTONDOWN:
                action = self._joybutton_to_action(e.button)
                if action:
                    self._down[action] = True
                    self._pressed[action] = True
            elif e.type == pygame.JOYBUTTONUP:
                action = self._joybutton_to_action(e.button)
                if action:
                    self._down[action] = False
            # джойстик оси (триггер для оси)
            elif e.type == pygame.JOYAXISMOTION:
                pass  # можно обрабатывать, если нужно
            # всегда можно расширять здесь для мыши/тача

    def _key_to_action(self, key):
        for action, keys in self.keymap.items():
            if key in keys:
                return action
        return None

    def _joybutton_to_action(self, btn):
        # Very simple mapping; расширяй под нужный контроллер
        mapping = {
            0: "attack_1",
            1: "attack_2",
            2: "attack_3",
            3: "block",
            4: "special_1",
            5: "special_2",
            9: "pause"
        }
        return mapping.get(btn)

    def rebind(self, action, keys):
        """Переназначить action на список клавиш."""
        self.keymap[action] = keys

    def is_down(self, action):
        return bool(self._down[action])

    def was_pressed(self, action):
        return bool(self._pressed[action])
    
    def get_horizontal_axis(self):
        """Возвращает -1/0/1 по комбинированию left/right.
           Можно расширить для плавной оси (джойстик).
        """
        left = self.is_down("left")
        right = self.is_down("right")
        if left and not right:
            return -1
        if right and not left:
            return 1
        return 0