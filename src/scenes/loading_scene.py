# src/scenes/loading_scene.py
import pygame
from src.managers.game_manager import BaseScene
from src.core.resource import resource_path
from src.core.animations import VideoAnimation
import sys
import os

class LoadingScene(BaseScene):
    def __init__(self, gm, target_scene="menu", skip_logo=False):
        super().__init__(gm)
        self.target_scene = target_scene
        self.skip_logo = skip_logo
        self.background_art = None
        self.logo_image = None
        
        # Прогресс загрузки
        self._all_loaded = False
        self._total_assets = 7   # количество этапов загрузки
        self._loaded_assets = 0
        
        # Логотип
        self.show_logo = False
        self.logo_timer = 0.0
        self.logo_duration = 2.0

    def on_enter(self):
        """Определяем, нужно ли показывать логотип, и загружаем логотип."""
        # Загружаем логотип заранее (он нужен для отображения)
        self._load_logo()
        
        # Если явно пропущен – не показываем
        if self.skip_logo:
            self.show_logo = False
            print("⏩ Логотип пропущен (skip_logo=True)")
            self._start_loading()
            return
        
        # Показываем логотип только если в этой сессии ещё не показывали
        if not self.gm._logo_shown:
            self.show_logo = True
            self.logo_timer = 0.0
            print("🆕 Показываем логотип 2 секунды")
        else:
            self.show_logo = False
            print("⏩ Логотип уже был показан – пропускаем")
            self._start_loading()

    def _start_loading(self):
        """Запускает загрузку всех ресурсов (кроме логотипа, он уже загружен)."""
        self._load_all_resources()

    def _load_all_resources(self):
        """Последовательно загружает все группы ресурсов."""
        self._load_background_art()
        self._load_music()
        self._load_icons()
        self._load_card_assets()          # character_skins, cameo_skins, character_cards, cameo_cards
        self._load_character_selection_cards()
        self._load_shop_skins()
        self._load_video_assets()
        # После загрузки всего – устанавливаем флаг
        self._all_loaded = True

    # ------------------------------------------------------------
    # 1. Логотип (загружается отдельно в on_enter)
    # ------------------------------------------------------------
    def _load_logo(self):
        """Загружает логотип."""
        try:
            logo_path = resource_path(os.path.join("Sprites", "arts", "logo.jpg"))
            if os.path.exists(logo_path):
                screen_width, screen_height = self.gm.screen.get_size()
                self.logo_image = pygame.image.load(logo_path).convert_alpha()
                logo_height = int(screen_height * 0.5)
                original_width, original_height = self.logo_image.get_size()
                scale_factor = logo_height / original_height
                logo_width = int(original_width * scale_factor)
                self.logo_image = pygame.transform.scale(self.logo_image, (logo_width, logo_height))
                print("✅ Загружен логотип")
            else:
                print(f"⚠️ Логотип не найден: {logo_path}")
                self.logo_image = None
        except Exception as e:
            print(f"❌ Ошибка загрузки логотипа: {e}")
            self.logo_image = None

    # ------------------------------------------------------------
    # 2. Фоновый арт для загрузочного экрана
    # ------------------------------------------------------------
    def _load_background_art(self):
        try:
            extensions = [".jpg", ".jpeg", ".png", ".bmp"]
            art_path = None
            for ext in extensions:
                test_path = resource_path(os.path.join("Sprites", "arts", f"loading_bg{ext}"))
                if os.path.exists(test_path):
                    art_path = test_path
                    break
            if art_path:
                screen_width, screen_height = self.gm.screen.get_size()
                self.background_art = pygame.image.load(art_path).convert()
                self.background_art = pygame.transform.scale(self.background_art, (screen_width, screen_height))
                print("✅ Загружен фоновый арт")
            else:
                print("❌ Фоновый арт не найден, создаём градиент")
                screen_width, screen_height = self.gm.screen.get_size()
                self.background_art = pygame.Surface((screen_width, screen_height))
                for i in range(screen_height):
                    color_val = int(30 + (i / screen_height) * 50)
                    pygame.draw.line(self.background_art, (color_val, 0, color_val//2),
                                   (0, i), (screen_width, i))
                self.background_art = self.background_art.convert()
        except Exception as e:
            print(f"❌ Ошибка загрузки фонового арта: {e}")
            self.background_art = None
        self._loaded_assets += 1

    # ------------------------------------------------------------
    # 3. Музыка
    # ------------------------------------------------------------
    def _load_music(self):
        try:
            music_path = resource_path(os.path.join("Sounds", "Music", "back_music.mp3"))
            if os.path.exists(music_path):
                # Загружаем музыку в плеер, но не запускаем (запустим в меню)
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.gm.settings.current_settings["music_volume"])
                print("✅ Музыка загружена")
                # Сохраняем путь в ассеты, чтобы потом проверить
                self.gm.assets["music_path"] = music_path
            else:
                print(f"⚠️ Музыка не найдена: {music_path}")
        except Exception as e:
            print(f"❌ Ошибка загрузки музыки: {e}")
        self._loaded_assets += 1

    # ------------------------------------------------------------
    # 4. Иконки
    # ------------------------------------------------------------
    def _load_icons(self):
        icons = {}
        icon_names = ["coin", "trophy", "unlocked", "locked", "arrow_left", "arrow_right", "currency"]
        for name in icon_names:
            icon = self._load_icon_image(name)
            if icon:
                icons[name] = icon
            else:
                # создаём заглушку
                icons[name] = self._create_icon_placeholder(name, 24)
        self.gm.assets["icons"] = icons
        self._loaded_assets += 1
        print(f"✅ Загружено {len(icons)} иконок")

    def _load_icon_image(self, name, size=24):
        try:
            path = resource_path(os.path.join("Sprites", "Icons", f"{name}.png"))
            if os.path.exists(path):
                icon = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(icon, (size, size))
        except:
            pass
        return None

    def _create_icon_placeholder(self, name, size):
        icon = pygame.Surface((size, size), pygame.SRCALPHA)
        if "coin" in name.lower():
            icon.fill((255, 215, 0, 255))
            text = "C"
        elif "trophy" in name.lower():
            icon.fill((255, 200, 100, 255))
            text = "T"
        elif "unlock" in name.lower():
            icon.fill((100, 255, 100, 255))
            text = "U"
        elif "lock" in name.lower():
            icon.fill((255, 100, 100, 255))
            text = "L"
        elif "currency" in name.lower():
            icon.fill((100, 150, 255, 255))
            text = "$"
        else:
            icon.fill((200, 200, 200, 255))
            text = "I"
        font = pygame.font.SysFont("arial", max(10, size // 2))
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(size//2, size//2))
        icon.blit(text_surface, text_rect)
        pygame.draw.rect(icon, (255, 255, 255), (0, 0, size, size), 1)
        return icon

    # ------------------------------------------------------------
    # 5. Карточки для меню + структуры скинов
    # ------------------------------------------------------------
    def _load_card_assets(self):
        """Загружает карточки и структуры скинов для персонажей и камео."""
        card_size = self._get_card_size()
        character_skins = {}
        cameo_skins = {}
        character_cards = {}
        cameo_cards = {}

        # Определяем списки персонажей и камео с их скинами
        # (данные берём из старых структур – они должны совпадать с тем, что было в menu_scene)
        chars = ["1x1x1x1", "chara", "steve"]
        cameos_list = ["c00lk1d", "papyrus"]
        # Словарь скинов: для каждого entity и скина – название, цена, разблокирован по умолчанию?
        # Пока зададим жёстко, позже можно вынести в отдельный файл.
        skins_data = {
            "1x1x1x1": {
                "default": {"name": "Обычный", "price": 0, "unlocked": True},
                "timeless": {"name": "Бессмертный", "price": 0, "unlocked": True}
            },
            "chara": {
                "default": {"name": "Обычный", "price": 0, "unlocked": True},
                "second_time": {"name": "Second Time", "price": 500, "unlocked": False}
            },
            "steve": {
                "default": {"name": "Обычный", "price": 0, "unlocked": True},
                "void_god": {"name": "Бог пустоты", "price": 500, "unlocked": False}
            },
            "c00lk1d": {
                "default": {"name": "Обычный", "price": 0, "unlocked": True},
                "tag_time": {"name": "Время тегов", "price": 100, "unlocked": False}
            },
            "papyrus": {
                "default": {"name": "Обычный", "price": 0, "unlocked": True},
                "withered": {"name": "Withered", "price": 200, "unlocked": False}
            }
        }

        # Загружаем карточки
        for entity, skins in skins_data.items():
            for skin_id, skin_info in skins.items():
                normal_path = resource_path(os.path.join("Sprites", "cards", f"{entity}_{skin_id}_normal.jpg"))
                special_path = resource_path(os.path.join("Sprites", "cards", f"{entity}_{skin_id}_special.jpg"))
                normal = None
                special = None
                if os.path.exists(normal_path):
                    normal = pygame.image.load(normal_path).convert_alpha()
                    normal = pygame.transform.scale(normal, (card_size, card_size))
                else:
                    # создаём заглушку
                    normal = self._create_placeholder_card(entity, skin_id, False, card_size)
                if os.path.exists(special_path):
                    special = pygame.image.load(special_path).convert_alpha()
                    special = pygame.transform.scale(special, (card_size, card_size))
                else:
                    special = self._create_placeholder_card(entity, skin_id, True, card_size)

                # Сохраняем в структуры скинов
                if entity in chars:
                    if entity not in character_skins:
                        character_skins[entity] = {}
                    character_skins[entity][skin_id] = {
                        "name": skin_info["name"],
                        "price": skin_info["price"],
                        "unlocked": skin_info["unlocked"],
                        "card_normal": normal,
                        "card_special": special
                    }
                    # Для меню сохраняем только default скин
                    if skin_id == "default":
                        if entity not in character_cards:
                            character_cards[entity] = {}
                        character_cards[entity]["default"] = {"normal": normal, "special": special}
                else:  # cameo
                    if entity not in cameo_skins:
                        cameo_skins[entity] = {}
                    cameo_skins[entity][skin_id] = {
                        "name": skin_info["name"],
                        "price": skin_info["price"],
                        "unlocked": skin_info["unlocked"],
                        "card_normal": normal,
                        "card_special": special
                    }
                    if skin_id == "default":
                        if entity not in cameo_cards:
                            cameo_cards[entity] = {}
                        cameo_cards[entity]["default"] = {"normal": normal, "special": special}

        self.gm.assets["character_skins"] = character_skins
        self.gm.assets["cameo_skins"] = cameo_skins
        self.gm.assets["character_cards"] = character_cards
        self.gm.assets["cameo_cards"] = cameo_cards
        self._loaded_assets += 1
        print(f"✅ Загружены карточки для {len(character_skins)} персонажей и {len(cameo_skins)} камео")

    def _create_placeholder_card(self, entity, skin_id, is_special, size):
        card = pygame.Surface((size, size), pygame.SRCALPHA)
        if is_special:
            card.fill((180, 150, 50, 255))
            border = max(3, size // 40)
            pygame.draw.rect(card, (255, 215, 0), (size//20, size//20, size*0.9, size*0.9), border)
            pygame.draw.rect(card, (100, 255, 100), (size//40, size//40, size*0.95, size*0.95), border//2)
        else:
            card.fill((80, 80, 150, 255))
            border = max(3, size // 40)
            pygame.draw.rect(card, (255, 255, 255), (size//20, size//20, size*0.9, size*0.9), border)
        font = pygame.font.SysFont("arial", max(10, size // 12))
        text = font.render(f"{entity}_{skin_id}", True, (255, 255, 255))
        card.blit(text, (size//20, size//2))
        placeholder_font = pygame.font.SysFont("arial", max(12, size//10), bold=True)
        placeholder = placeholder_font.render("ЗАГЛУШКА", True, (255, 255, 255))
        card.blit(placeholder, (size//2 - placeholder.get_width()//2, size//3))
        return card

    def _get_card_size(self):
        base_size = 280
        if self.gm.settings.scale_factor > 1.5:
            return int(base_size * 1.3)
        elif self.gm.settings.scale_factor > 1.2:
            return int(base_size * 1.15)
        return base_size

    # ------------------------------------------------------------
    # 6. Карточки для character_selection_scene
    # ------------------------------------------------------------

    def _load_character_selection_cards(self):
        """
        Подготавливает карточки для сцены выбора персонажей.
        Ожидается, что character_cards и cameo_cards уже загружены в gm.assets.
        """
        character_cards = self.gm.assets.get("character_cards", {})
        cameo_cards = self.gm.assets.get("cameo_cards", {})
        
        self.gm.assets["character_selection_cards"] = {
            "characters": character_cards,
            "cameos": cameo_cards
        }
        self._loaded_assets += 1
        print("✅ Подготовлены карточки для выбора персонажей")

    def _load_card_assets(self):
        """Загружает карточки и структуры скинов для персонажей и камео."""
        card_size = self._get_card_size()
        character_skins = {}
        cameo_skins = {}
        character_cards = {}
        cameo_cards = {}

        # Списки персонажей и камео (имена в исходном регистре, но мы будем приводить к нижнему)
        chars = ["1x1x1x1", "chara", "steve"]
        cameos_list = ["c00lk1d", "papyrus"]
        
        # Данные о скинах (цены, названия, разблокированы ли по умолчанию)
        skins_data = {
            "1x1x1x1": {
                "default": {"name": "Обычный", "price": 0, "unlocked": True},
                "timeless": {"name": "Бессмертный", "price": 0, "unlocked": True}
            },
            "chara": {
                "default": {"name": "Обычный", "price": 0, "unlocked": True},
                "second_time": {"name": "Second Time", "price": 500, "unlocked": False}
            },
            "steve": {
                "default": {"name": "Обычный", "price": 0, "unlocked": True},
                "void_god": {"name": "Бог пустоты", "price": 500, "unlocked": False}
            },
            "c00lk1d": {
                "default": {"name": "Обычный", "price": 0, "unlocked": True},
                "tag_time": {"name": "Время тегов", "price": 100, "unlocked": False}
            },
            "papyrus": {
                "default": {"name": "Обычный", "price": 0, "unlocked": True},
                "withered": {"name": "Withered", "price": 200, "unlocked": False}
            }
        }

        for entity, skins in skins_data.items():
            entity_lower = entity.lower()  # ключ в нижнем регистре
            for skin_id, skin_info in skins.items():
                normal_path = resource_path(os.path.join("Sprites", "cards", f"{entity}_{skin_id}_normal.jpg"))
                special_path = resource_path(os.path.join("Sprites", "cards", f"{entity}_{skin_id}_special.jpg"))
                normal = None
                special = None
                if os.path.exists(normal_path):
                    normal = pygame.image.load(normal_path).convert_alpha()
                    normal = pygame.transform.scale(normal, (card_size, card_size))
                else:
                    normal = self._create_placeholder_card(entity, skin_id, False, card_size)
                if os.path.exists(special_path):
                    special = pygame.image.load(special_path).convert_alpha()
                    special = pygame.transform.scale(special, (card_size, card_size))
                else:
                    special = self._create_placeholder_card(entity, skin_id, True, card_size)

                # Определяем, персонаж это или камео
                is_char = entity in chars
                if is_char:
                    if entity_lower not in character_skins:
                        character_skins[entity_lower] = {}
                    character_skins[entity_lower][skin_id] = {
                        "name": skin_info["name"],
                        "price": skin_info["price"],
                        "unlocked": skin_info["unlocked"],
                        "card_normal": normal,
                        "card_special": special
                    }
                    if skin_id == "default":
                        if entity_lower not in character_cards:
                            character_cards[entity_lower] = {}
                        character_cards[entity_lower]["default"] = {"normal": normal, "special": special}
                else:
                    if entity_lower not in cameo_skins:
                        cameo_skins[entity_lower] = {}
                    cameo_skins[entity_lower][skin_id] = {
                        "name": skin_info["name"],
                        "price": skin_info["price"],
                        "unlocked": skin_info["unlocked"],
                        "card_normal": normal,
                        "card_special": special
                    }
                    if skin_id == "default":
                        if entity_lower not in cameo_cards:
                            cameo_cards[entity_lower] = {}
                        cameo_cards[entity_lower]["default"] = {"normal": normal, "special": special}

        self.gm.assets["character_skins"] = character_skins
        self.gm.assets["cameo_skins"] = cameo_skins
        self.gm.assets["character_cards"] = character_cards
        self.gm.assets["cameo_cards"] = cameo_cards
        self._loaded_assets += 1
        print(f"✅ Загружены карточки для {len(character_skins)} персонажей и {len(cameo_skins)} камео")

    # ------------------------------------------------------------
    # 7. Карточки для магазина (только платные скины)
    # ------------------------------------------------------------
    def _load_shop_skins(self):
        skins_cards = {}
        for entity, skins in self.gm.assets.get("character_skins", {}).items():
            for skin_id, data in skins.items():
                if data.get("price", 0) > 0 and skin_id != "default":
                    key = f"{entity}_{skin_id}"  # entity уже в нижнем регистре
                    skins_cards[key] = {
                        "normal": data.get("card_normal"),
                        "special": data.get("card_special")
                    }
        for entity, skins in self.gm.assets.get("cameo_skins", {}).items():
            for skin_id, data in skins.items():
                if data.get("price", 0) > 0 and skin_id != "default":
                    key = f"{entity}_{skin_id}"
                    skins_cards[key] = {
                        "normal": data.get("card_normal"),
                        "special": data.get("card_special")
                    }
        self.gm.assets["skins_cards"] = skins_cards
        self._loaded_assets += 1
        print(f"✅ Загружены карточки для {len(skins_cards)} платных скинов в магазин")

    # ------------------------------------------------------------
    # 8. Видео-арты для раздела FIGHT
    # ------------------------------------------------------------
    def _load_video_assets(self):
        art_animations = {}
        entities = ["1x1x1x1", "chara", "steve", "c00lk1d", "papyrus"]
        for entity in entities:
            entity_lower = entity.lower()
            video_path = os.path.join("Sprites", "arts", f"{entity}_default_art.mp4")
            actual_path = resource_path(video_path)
            if os.path.exists(actual_path):
                try:
                    animation = VideoAnimation(video_path, target_size=(self.s(350), self.s(350)), loop=True)
                    art_animations[f"{entity_lower}_default"] = animation
                    print(f"✅ Загружено видео для {entity}")
                except Exception as e:
                    print(f"❌ Ошибка загрузки видео {entity}: {e}")
            else:
                # Пробуем альтернативный путь
                alt_path = os.path.join("Sprites", "arts", f"{entity}_art.mp4")
                if os.path.exists(resource_path(alt_path)):
                    try:
                        animation = VideoAnimation(alt_path, target_size=(self.s(350), self.s(350)), loop=True)
                        art_animations[f"{entity_lower}_default"] = animation
                        print(f"✅ Загружено альтернативное видео для {entity}")
                    except:
                        pass
                else:
                    # Создаём заглушку
                    size = self.s(350)
                    placeholder = pygame.Surface((size, size), pygame.SRCALPHA)
                    placeholder.fill((80, 80, 150, 255))
                    font = pygame.font.SysFont("arial", 30)
                    text = font.render(entity, True, (255,255,255))
                    placeholder.blit(text, (size//2 - text.get_width()//2, size//2 - text.get_height()//2))
                    class DummyAnimation:
                        def __init__(self, frame):
                            self.frames = [frame]
                            self.index = 0
                        def update(self, dt):
                            pass
                        def get_frame(self):
                            return self.frames[0]
                    art_animations[f"{entity_lower}_default"] = DummyAnimation(placeholder)
        self.gm.assets["art_animations"] = art_animations
        self._loaded_assets += 1
        print(f"✅ Загружено {len(art_animations)} артов для раздела FIGHT")


    # ------------------------------------------------------------
    # Отрисовка логотипа и прогресса
    # ------------------------------------------------------------
    def _draw_text_with_outline(self, screen, text, x, y, color, outline_color, size, outline_width=2):
        font = self.get_font(size, bold=True)
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx == 0 and dy == 0:
                    continue
                outline_surf = font.render(text, True, outline_color)
                screen.blit(outline_surf, (x + dx, y + dy))
        text_surf = font.render(text, True, color)
        screen.blit(text_surf, (x, y))

    def update(self, dt):
        # Фаза показа логотипа
        if self.show_logo:
            self.logo_timer += dt
            if self.logo_timer >= self.logo_duration:
                self.show_logo = False
                print("✅ Логотип показан, начинаем загрузку")
                self.gm._logo_shown = True
                self._start_loading()
            return

        # Фаза загрузки
        if self._all_loaded and self._loaded_assets >= self._total_assets:
            print("✅ Загрузка завершена, переход к сцене:", self.target_scene)
            self.gm.set_scene(self.target_scene)

    def draw(self, screen):
        if self.show_logo:
            screen.fill((0, 0, 0))
            if self.logo_image:
                logo_x = screen.get_width() // 2 - self.logo_image.get_width() // 2
                logo_y = screen.get_height() // 2 - self.logo_image.get_height() // 2
                screen.blit(self.logo_image, (logo_x, logo_y))
            else:
                self._draw_text_with_outline(
                    screen,
                    "VillianWar",
                    screen.get_width() // 2 - 200,
                    screen.get_height() // 2 - 50,
                    (255, 255, 255),
                    (0, 0, 0),
                    72,
                    3
                )
            return

        # Основной экран загрузки
        if self.background_art:
            screen.blit(self.background_art, (0, 0))
        else:
            screen.fill((0, 0, 30))

        self._draw_text_with_outline(
            screen,
            "VillianWar",
            self.s(50),
            self.s(50),
            (255, 255, 255),
            (0, 0, 0),
            48,
            2
        )

        bar_width = self.s(600)
        bar_height = self.s(30)
        bar_x = screen.get_width() // 2 - bar_width // 2
        bar_y = screen.get_height() // 2 + self.s(200)

        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        progress = self._loaded_assets / max(1, self._total_assets)
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            pygame.draw.rect(screen, (0, 200, 100), (bar_x, bar_y, fill_width, bar_height))

        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)

        font = self.get_font(24)
        step_text = font.render("Загрузка ресурсов...", True, (200, 200, 200))
        screen.blit(step_text, (screen.get_width() // 2 - step_text.get_width() // 2, bar_y - self.s(40)))

        percent = int(progress * 100)
        percent_text = font.render(f"{percent}%", True, (255, 255, 255))
        screen.blit(percent_text, (screen.get_width() // 2 - percent_text.get_width() // 2, bar_y + bar_height + self.s(20)))

        hint_font = self.get_font(18)
        hint_text = self.gm.settings.get_text("please_wait")
        hint = hint_font.render(hint_text, True, (150, 150, 150))
        screen.blit(hint, (screen.get_width() // 2 - hint.get_width() // 2, bar_y + bar_height + self.s(60)))