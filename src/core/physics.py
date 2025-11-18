# src/physics.py
"""
Physics module
--------------
Содержит базовые физические правила: гравитация, простые столкновения и управление хитбоксами.
Классы:
 - PhysicsWorld: глобальная физика (гравитация, список тел)
 - HitBox / HurtBox: простые классы для хит- и хертбоксов
 - resolve_collisions: простая функция для разрешения пересечений

Как расширять:
 - Добавь более точную систему столкновений (swept AABB, continuous collision)
 - Создай наследников для разных типов тел (kinematic, rigidbody)
"""

import pygame

GRAVITY = 1500.0  # пикселей/с^2 — настраивай по ощущениям

class HitBox:
    """Простой объект хитбокса — AABB, привязан к Entity.rect через смещение."""
    def init(self, owner, offset_x, offset_y, w, h):
        self.owner = owner
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.w = w
        self.h = h

    @property
    def rect(self):
        x = self.owner.rect.x + (self.offset_x if self.owner.is_facing_right else -self.offset_x - self.w)
        y = self.owner.rect.y + self.offset_y
        return pygame.Rect(int(x), int(y), self.w, self.h)

class HurtBox:
    """Ударяемая область (обычно совпадает с body rect)."""
    def init(self, owner, offset_x=0, offset_y=0, w=None, h=None):
        self.owner = owner
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.w = w or owner.rect.width
        self.h = h or owner.rect.height

    @property
    def rect(self):
        x = self.owner.rect.x + self.offset_x
        y = self.owner.rect.y + self.offset_y
        return pygame.Rect(int(x), int(y), self.w, self.h)

class PhysicsWorld:
    """Менеджер физики: гравитация, список тел, простые проверки столкновений."""
    def __init__(self, gravity=GRAVITY):
        self.gravity = gravity
        self.bodies = []  # список сущностей (обычно Character, Projectile и т.д.)

    def add(self, body):
        if body not in self.bodies:
            self.bodies.append(body)

    def remove(self, body):
        if body in self.bodies:
            self.bodies.remove(body)

    def step(self, dt):
        """Обновить физику: гравитация -> интеграция -> простая коррекция столкновений."""
        # применяем гравитацию к всем телам, которые поддерживают velocity_y и не на земле.
        for b in self.bodies:
            # Если у тела есть флаг is_airborne, не трогаем; иначе добавляем гравитацию.
            if hasattr(b, "is_airborne") and b.is_airborne:
                # интеграция
                if hasattr(b, "velocity_y"):
                    b.velocity_y += self.gravity * dt
            else:
                # можно применять небольшую «подпорку» для падений
                pass

            # интегрируем позицию
            if hasattr(b, "update"):
                b.update(dt)

        # Простая коррекция: границы экрана (не физический мир, просто demo)
        for b in list(self.bodies):
            # не позволять выйти за пол по Y
            ground_y = 500  # TODO: сделать configurable / уровень
            if b.rect.bottom >= ground_y:
                # фиксируем положение
                b.rect.bottom = ground_y
                # обнуляем вертикальную скорость
                if hasattr(b, "velocity_y"):
                    b.velocity_y = 0
                if hasattr(b, "is_airborne"):
                    b.is_airborne = False

def detect_hits(attacker, defender, attacker_hitboxes, defender_hurtboxes):
    """
    Детектирование попаданий: возвращает список (hitbox, hurtbox) пар, которые пересеклись.
    attacker_hitboxes / defender_hurtboxes — списки HitBox/HurtBox объектов.
    """
    collisions = []
    for hb in attacker_hitboxes:
        for db in defender_hurtboxes:
            if hb.rect.colliderect(db.rect):
                collisions.append((hb, db))
    return collisions