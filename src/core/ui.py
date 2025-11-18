# src/ui.py
"""
UI utilities and widgets.

Содержит:
 - HealthBar: рисует HP
 - MeterBar: рисует 300-point meter и сегменты 100/200/300
 - CameoIndicator: отображает активность камео
 - MessageOverlay: текстовые сообщения (Fight!, KO, Round X)
 - DebugOverlay: fps, позиции, хитбоксы

Как использовать:
 - Создай UIManager, добавь виджеты или вызывай helper-функции в main loop
 - Передавай surface для рисования

Замечание:
 - Функции используют pygame.draw и текстовую отрисовку. Можешь заменить на sprited images.
"""

import pygame

pygame.font.init()
DEFAULT_FONT = pygame.font.SysFont("arial", 18)

def draw_health_bar(surface, x, y, width, height, current_hp, max_hp):
    """Рисует простую полосу здоровья."""
    pct = max(0, min(1.0, current_hp / float(max_hp)))
    fill_w = int(width * pct)
    # фон
    pygame.draw.rect(surface, (60, 60, 60), (x, y, width, height))
    # заполняем
    pygame.draw.rect(surface, (200, 20, 20), (x, y, fill_w, height))
    # рамка
    pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height), 2)

def draw_meter_bar(surface, x, y, width, height, meter_value, meter_max=300):
    """
    Рисует 3-сегментную шкалу.
    meter_value: 0..300
    сегменты: 0-100, 100-200, 200-300
    """
    # фон
    pygame.draw.rect(surface, (40, 40, 40), (x, y, width, height))
    # деление на 3
    seg_w = width // 3
    colors = [(120, 120, 255), (100, 180, 255), (200, 200, 100)]
    # нарисуем заполнение по пикселям для точности
    filled_px = int(width * (max(0, min(meter_value, meter_max)) / meter_max))
    pygame.draw.rect(surface, (80, 160, 255), (x, y, filled_px, height))
    # сегменты индикаторы
    for i in range(3):
        sx = x + i * seg_w
        pygame.draw.rect(surface, (0, 0, 0), (sx, y, seg_w, height), 1)
    # рамка
    pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height), 2)

def draw_cameo_icon(surface, x, y, cameo, available=False):
    """
    Отобразить иконку камео (если cameo объект имеет name или image).
    available — окрашивает иконку, если доступна.
    """
    size = 48
    rect = pygame.Rect(x, y, size, size)
    color = (200, 200, 200) if available else (100, 100, 100)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (0,0,0), rect, 2)
    if cameo:
        txt = DEFAULT_FONT.render(cameo.name[:2].upper(), True, (0,0,0))
        surface.blit(txt, (x + 6, y + 12))

def draw_message(surface, text, x, y, size=36, color=(255,255,255)):
    font = pygame.font.SysFont("arial", size)
    txt = font.render(text, True, color)
    surface.blit(txt, (x, y))

def draw_hitbox(surface, rect, outline=(255,0,0)):
    pygame.draw.rect(surface, outline, rect, 1)

def draw_debug_overlay(surface, fps, position=(10,10), extra_lines=None):
    x,y = position
    lines = [f"FPS: {int(fps)}"]
    if extra_lines:
        lines.extend(extra_lines)
    for i, line in enumerate(lines):
        txt = DEFAULT_FONT.render(line, True, (255,255,255))
        surface.blit(txt, (x, y + i*18))