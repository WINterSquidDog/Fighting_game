# src/core/character.py
import pygame
from src.core.entity import Entity
from src.core.animations import AnimationController, Animation

class Character(Entity):
    """
    Упрощённый Character, интегрированный с AnimationController.
    Конструктор: Character(name, resource_manager, x=100, y=400)
    resource_manager должен предоставлять метод get_image(character, skin, anim_name, frame_index)
    или можно позже заполнить animations вручную.
    """
    def __init__(self, name, resource_manager=None, x=100, y=400):
        # hitbox 80x160 по умолчанию
        super().__init__(x, y, 80, 160)
        self.name = name
        self.resource_manager = resource_manager

        self.is_facing_right = True

        # Animations: dict name -> Animation
        self.anim = AnimationController({}, default=None)
        # простые поля состояния/здоровья
        self.stats = None
        self.hp = 1000

        # Попытка автоматически подгрузить базовые анимации при наличии resource_manager
        self._load_stub_animations()
        # стартовая анимация
        if self.anim.current is None and "idle" in self.anim.animations:
            self.play_animation("idle")

    def _load_stub_animations(self):
        """
        Попытка загрузить из resource_manager: ожидаем структуру
        resource_manager.get_skin_animations(name, skin) -> { anim: [frames] }
        Здесь просто проверяем, если есть, создаём Animation объекты.
        """
        if not self.resource_manager:
            return

        # пытаемся взять default skin
        skins = self.resource_manager._skins.get(self.name, {})
        # если есть хотя бы один скин - берем первый
        skin_name = None
        if skins:
            # взять первый ключ
            skin_name = list(skins.keys())[0]

        if not skin_name:
            return

        anims = skins.get(skin_name, {})
        for anim_name, frames in anims.items():
            # frames уже pygame.Surface list
            if not frames:
                continue
            animation = Animation(frames, fps=12, loop=True)
            self.anim.add(anim_name, animation)

    def play_animation(self, name: str):
        """Включает named анимацию (если есть)."""
        self.anim.change(name, reset=True)

    def update(self, dt: float):
        """Обновление персонажа: анимация, физика (если нужно)."""
        # обновляем анимацию
        self.anim.update(dt)
        # логика движений/стейтов добавлять здесь

    def draw(self, surface: pygame.Surface):
        """Рисуем текущую анимацию в позиции rect.x/y."""
        # flip в зависимости от is_facing_right
        flip = not self.is_facing_right
        self.anim.draw(surface, int(self.rect.x), int(self.rect.y), flip=flip)