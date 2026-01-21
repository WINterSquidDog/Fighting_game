# src/scenes/menu_scene.py
import pygame
import os
import sys
from src.managers.game_manager import BaseScene
from src.managers.save_manager import SaveManager
from src.managers.skin_manager import SkinManager
from src.core.animations import VideoAnimation, resource_path

# Функция для получения корректного пути к ресурсам в pyinstaller
def resource_path(relative_path):
    """Получает правильный путь к ресурсам для работы как из .py, так и из .exe"""
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class MenuScene(BaseScene):
    def __init__(self, gm):
        super().__init__(gm)
        
        # Добавляем менеджер сохранений
        self.save_manager = SaveManager()
        self.save_manager.load_save()
        
        # Добавляем менеджер скинов
        self.skin_manager = SkinManager()

        # Цветовая схема
        self.colors = {
            "background": (20, 20, 40),
            "header_bg": (30, 30, 50),
            "button_primary": (255, 100, 100),
            "button_secondary": (100, 150, 255),
            "button_tertiary": (100, 200, 100),
            "text_light": (255, 255, 255),
            "text_dark": (200, 200, 200),
            "accent": (255, 215, 0),
            "danger": (255, 80, 80),
            "selected": (100, 255, 100),
            "training": (180, 100, 255)  # Новый цвет для режима тренировки
        }
        
        # Данные игрока из сохранения
        self.player_data = {
            "coins": self.save_manager.get_coins(),
            "trophies": self.save_manager.get_trophies()
        }
        
        # Персонажи с карточками
        self.selected_character = 0
        self.characters = [
            {
                "name": "1x1x1x1",
                "card_normal": None,
                "card_special": None,
                "description": "",
                "selected": False,
                "skin": "default"
            },
            {
                "name": "chara",  # строчными буквами для единообразия
                "card_normal": None,
                "card_special": None,
                "description": "",
                "selected": False,
                "skin": "default"
            },
            {
                "name": "steve",  # строчными буквами для единообразия
                "card_normal": None,
                "card_special": None,
                "description": "",
                "selected": False,
                "skin": "default"
            }
        ]
        
        # Камео с карточками (все строчными буквами)
        self.selected_cameo = 0
        self.cameos = [
            {
                "name": "c00lk1d",  # строчными буквами
                "description": "",
                "selected": False,
                "skin": "default",
                "card_normal": None,
                "card_special": None
            },
            {
                "name": "papyrus",  # строчными буквами
                "description": "",
                "selected": False,
                "skin": "default",
                "card_normal": None,
                "card_special": None
            },
        ]

        # Данные скинов - ОБНОВЛЕННАЯ СТРУКТУРА с учетом сохранений И ЦЕН
        self.character_skins = {
            "1x1x1x1": {
                "default": {"name": self.gm.settings.get_text("skin_default"), "unlocked": True, "price": 0, "card_normal": None, "card_special": None},
                "timeless": {"name": self.gm.settings.get_text("skin_timeless"), "unlocked": True, "price": 0, "card_normal": None, "card_special": None}  # Всегда разблокирован
            },
            "chara": {
                "default": {"name": self.gm.settings.get_text("skin_default"), "unlocked": True, "price": 0, "card_normal": None, "card_special": None},
                "second_time": {"name": "Second Time", "unlocked": self.save_manager.is_character_skin_unlocked("chara", "second_time"), "price": 500, "card_normal": None, "card_special": None}
            },
            "steve": {
                "default": {"name": self.gm.settings.get_text("skin_default"), "unlocked": True, "price": 0, "card_normal": None, "card_special": None},
                "void_god": {"name": self.gm.settings.get_text("skin_two_faced"), "unlocked": self.save_manager.is_character_skin_unlocked("steve", "void_god"), "price": 500, "card_normal": None, "card_special": None}
            }
        }

        # ОБНОВЛЕННАЯ СТРУКТУРА ДЛЯ КАМЕО (все строчными буквами) с учетом сохранений И ЦЕН
        self.cameo_skins = {
            "c00lk1d": {
                "default": {"name": self.gm.settings.get_text("skin_default"), "unlocked": True, "price": 0, "card_normal": None, "card_special": None},
                "tag_time": {"name": self.gm.settings.get_text("skin_tag_time"), "unlocked": self.save_manager.is_cameo_skin_unlocked("c00lk1d", "tag_time"), "price": 100, "card_normal": None, "card_special": None}
            },
            "papyrus": {
                "default": {"name": self.gm.settings.get_text("skin_default"), "unlocked": True, "price": 0, "card_normal": None, "card_special": None},
                "withered": {"name": "Withered", "unlocked": self.save_manager.is_cameo_skin_unlocked("papyrus", "withered"), "price": 200, "card_normal": None, "card_special": None}
            },
        }

        # Состояние выбора скинов
        self.selected_skin_tab = 0  # 0 - персонажи, 1 - камео
        self.selected_skin_index = 0
        self.skin_selecting_mode = False
        self.current_skins = []
        
        # Кнопки для мыши
        self.tab_buttons = []
        self.char_left_btn = None
        self.char_right_btn = None
        self.char_select_btn = None
        self.cameo_left_btn = None
        self.cameo_right_btn = None
        self.cameo_select_btn = None
        self.skin_tab_left = None
        self.skin_tab_right = None
        self.skin_left_btn = None
        self.skin_right_btn = None
        self.skin_select_btn = None
        self.battle_button = None
        self.mode_button = None
        self.shop_button = None
        self.settings_button = None
        self.exit_button = None
        
        # Состояние выбора
        self.current_section = 0
        self.selecting_mode = False
        self.selection_confirmed_time = 0
        self.show_selection_confirmed = False
        
        # 🎮 ДОБАВЛЕНО: Режимы игры
        self.game_modes = [
            {"id": "vs_bot", "name": "VS BOT"},
            {"id": "training", "name": "ТРЕНИРОВКА"}
        ]  # Режимы игры как массив словарей
        self.selected_game_mode = 0  # 0 - VS BOT, 1 - Тренировка
        self.mode_selecting = False  # Режим выбора режима игры
        
        # Загружаем тексты и карточки
        self._refresh_texts()
        self.music_started = False
        
        # Переменные для анимации
        self.unlock_animation = False
        self.unlock_animation_time = 0
        self.unlock_animation_skin = None
        
        # Сообщение о блокировке скина
        self.locked_skin_message = False
        self.locked_skin_message_time = 0
        
        # 🎬 ДОБАВЛЕНО: Кэш для анимаций артов
        self.art_animations = {}  # Ключ: (имя, скин, размер) -> VideoAnimation
        self.playing_animations = []  # Список активных анимаций для обновления
        
    def on_enter(self):
        """Загружаем карточки и восстанавливаем последний выбор"""
        self._load_all_cards()
        self._play_background_music()
        self._restore_last_selection()
        
        # ОБНОВЛЯЕМ ДАННЫЕ ИГРОКА ИЗ СОХРАНЕНИЙ
        self.save_manager.load_save()  # Перезагружаем сохранения
        self.player_data["coins"] = self.save_manager.get_coins()
        self.player_data["trophies"] = self.save_manager.get_trophies()
        
        last_mode_id = self.save_manager.get_last_game_mode()  # Теперь получаем id
        print(f"🎮 Восстанавливаем режим игры по id: {last_mode_id}")
        
        # Находим индекс восстановленного режима по id
        mode_found = False
        for i, mode in enumerate(self.game_modes):
            if mode["id"] == last_mode_id:  # Сравниваем по id
                self.selected_game_mode = i
                print(f"✅ Восстановлен режим: {mode['name']} (id: {mode['id']})")
                mode_found = True
                break
        
        if not mode_found:
            # Если режим не найден, выбираем первый
            self.selected_game_mode = 0
            print(f"⚠️ Режим с id '{last_mode_id}' не найден, используем первый")
        
        # ОБНОВЛЯЕМ СТАТУС РАЗБЛОКИРОВКИ СКИНОВ ИЗ СОХРАНЕНИЙ
        print("🔄 Обновление статуса скинов из сохранений...")
        
        # Обновляем character_skins
        for char_name, skins in self.character_skins.items():
            for skin_id in skins.keys():
                if skin_id != "default":
                    is_unlocked = self.save_manager.is_character_skin_unlocked(char_name, skin_id)
                    self.character_skins[char_name][skin_id]["unlocked"] = is_unlocked
                    print(f"  {char_name}.{skin_id}: unlocked={is_unlocked}")
        
        # Обновляем cameo_skins
        for cameo_name, skins in self.cameo_skins.items():
            for skin_id in skins.keys():
                if skin_id != "default":
                    is_unlocked = self.save_manager.is_cameo_skin_unlocked(cameo_name, skin_id)
                    self.cameo_skins[cameo_name][skin_id]["unlocked"] = is_unlocked
                    print(f"  {cameo_name}.{skin_id}: unlocked={is_unlocked}")
        
        print(f"💰 Данные игрока обновлены: {self.player_data['coins']} монет, {self.player_data['trophies']} трофеев")

    def _restore_last_selection(self):
        """Восстанавливает последний выбор персонажей из сохранения"""
        last_char = self.save_manager.get_last_character()
        last_cameo = self.save_manager.get_last_cameo()
        
        print(f"🔍 Восстановление: персонаж='{last_char}', камео='{last_cameo}'")
        
        # Находим индексы последних выбранных персонажей (все в нижнем регистре для сравнения)
        char_found = False
        for i, char in enumerate(self.characters):
            if char["name"].lower() == last_char.lower():
                self.selected_character = i
                char["selected"] = True
                char["skin"] = self.save_manager.get_character_skin()
                print(f"✅ Восстановлен персонаж: {char['name']} (индекс {i})")
                char_found = True
                break
        
        if not char_found:
            print(f"⚠️ Персонаж '{last_char}' не найден, используем первого")
            self.selected_character = 0
            self.characters[0]["selected"] = True
        
        cameo_found = False
        for i, cameo in enumerate(self.cameos):
            if cameo["name"].lower() == last_cameo.lower():
                self.selected_cameo = i
                cameo["selected"] = True
                cameo["skin"] = self.save_manager.get_cameo_skin()
                print(f"✅ Восстановлено камео: {cameo['name']} (индекс {i})")
                cameo_found = True
                break
        
        if not cameo_found:
            print(f"⚠️ Камео '{last_cameo}' не найден, используем первого")
            self.selected_cameo = 0
            self.cameos[0]["selected"] = True

    def _select_character(self):
        """Выбор персонажа - можно выбирать одного и того же повторно"""
        selected_char = self.characters[self.selected_character]
        selected_char["selected"] = True
        for char in self.characters:
            if char != self.characters[self.selected_character]:
                char["selected"] = False
        print(f"🎯 Начинаем сохранение персонажа: {selected_char['name']}")
        
        # Сохраняем выбор
        self.save_manager.save_game(
            character=selected_char["name"],  # Сохраняем именно имя
            character_skin=selected_char["skin"]
        )
        
        print(f"✅ Выбран и сохранен персонаж: {selected_char['name']}")
        print(self.characters)
        self.selection_confirmed_time = pygame.time.get_ticks()
        self.show_selection_confirmed = True
        self.selecting_mode = False

    def _select_cameo(self):
        """Выбор камео - можно выбирать одного и того же повторно"""
        selected_cameo = self.cameos[self.selected_cameo]
        selected_cameo["selected"] = True
        
        print(f"🎯 Начинаем сохранение камео: {selected_cameo['name']}")
        for char in self.cameos:
            if char != self.cameos[self.selected_cameo]:
                char["selected"] = False
        # Сохраняем выбор
        self.save_manager.save_game(
            cameo=selected_cameo["name"],  # Сохраняем именно имя
            cameo_skin=selected_cameo["skin"]
        )
        
        print(f"✅ Выбрано и сохранено камео: {selected_cameo['name']}")
        self.selection_confirmed_time = pygame.time.get_ticks()
        self.show_selection_confirmed = True
        self.selecting_mode = False

    def _load_all_cards(self):
        """Загружаем все карточки с учетом скинов"""
        card_size = self._get_card_size()
        
        # Загружаем карточки персонажей
        for char_name in self.character_skins.keys():
            for skin_id in self.character_skins[char_name].keys():
                skin_data = self.character_skins[char_name][skin_id]
                skin_data["card_normal"] = self._load_card_image(
                    f"{char_name}_{skin_id}_normal.jpg", False, card_size
                )
                skin_data["card_special"] = self._load_card_image(
                    f"{char_name}_{skin_id}_special.jpg", True, card_size
                )
        print(self.character_skins)
        
        # Загружаем карточки камео - ИСПРАВЛЕННЫЙ КОД
        for cameo_name in self.cameo_skins.keys():
            for skin_id in self.cameo_skins[cameo_name].keys():
                skin_data = self.cameo_skins[cameo_name][skin_id]
                skin_data["card_normal"] = self._load_card_image(
                    f"{cameo_name}_{skin_id}_normal.jpg", False, card_size
                )
                skin_data["card_special"] = self._load_card_image(
                    f"{cameo_name}_{skin_id}_special.jpg", True, card_size
                )
        
        # Также загружаем дефолтные карточки для cameos (для совместимости)
        for cameo in self.cameos:
            cameo_key = cameo['name'].lower()
            if cameo_key in self.cameo_skins:
                default_skin = "default"
                if default_skin in self.cameo_skins[cameo_key]:
                    cameo["card_normal"] = self.cameo_skins[cameo_key][default_skin]["card_normal"]
                    cameo["card_special"] = self.cameo_skins[cameo_key][default_skin]["card_special"]
    
    def _load_character_cards(self, character):
        """Перезагружает карточки для персонажа с учетом скина"""
        char_key = character['name'].lower()
        skin_id = character["skin"]
        
        if char_key in self.character_skins and skin_id in self.character_skins[char_key]:
            skin_data = self.character_skins[char_key][skin_id]
            
            # Просто присваиваем уже загруженные карточки
            character["card_normal"] = skin_data["card_normal"]
            character["card_special"] = skin_data["card_special"]
            print(f"🔄 Перезагружены карточки для {character['name']} с скином {skin_id}")
        else:
            print(f"⚠️ Не найден скин {skin_id} для персонажа {character['name']}")

    def _load_cameo_cards(self, cameo):
        """Перезагружает карточки для камео с учетом скина"""
        cameo_key = cameo['name'].lower()
        skin_id = cameo["skin"]
        
        if cameo_key in self.cameo_skins and skin_id in self.cameo_skins[cameo_key]:
            skin_data = self.cameo_skins[cameo_key][skin_id]
            
            # Просто присваиваем уже загруженные карточки
            cameo["card_normal"] = skin_data["card_normal"]
            cameo["card_special"] = skin_data["card_special"]
            print(f"🔄 Перезагружены карточки для {cameo['name']} с скином {skin_id}")
        else:
            print(f"⚠️ Не найден скин {skin_id} для камео {cameo['name']}")
    
    def _get_card_size(self):
        """Определяем размер карточки в зависимости от разрешения"""
        base_size = 280
        
        if self.gm.settings.scale_factor > 1.5:
            return int(base_size * 1.3)
        elif self.gm.settings.scale_factor > 1.2:
            return int(base_size * 1.15)
        return base_size

    def _load_card_image(self, filename, is_special, card_size):
        """Загрузка карточки с указанным размером - ИСПРАВЛЕНО ДЛЯ PYINSTALLER"""
        # Используем resource_path для корректной работы в .exe
        card_path = resource_path(os.path.join("Sprites", "cards", filename))
        
        try:
            if os.path.exists(card_path):
                card = pygame.image.load(card_path).convert_alpha()
                card = pygame.transform.scale(card, (card_size, card_size))
                return card
            else:
                print(f"⚠️ Карточка не найдена: {card_path}")
                return self._create_placeholder_card(filename, is_special, card_size)
        except Exception as e:
            print(f"❌ Ошибка загрузки карточки {card_path}: {e}")
            return self._create_placeholder_card(filename, is_special, card_size)

    def _create_placeholder_card(self, filename, is_special, card_size):
        """Создание заглушки для карточки"""
        card = pygame.Surface((card_size, card_size), pygame.SRCALPHA)
        
        if is_special:
            card.fill((180, 150, 50, 255))
            border = max(3, card_size // 40)
            pygame.draw.rect(card, (255, 215, 0), (card_size//20, card_size//20, card_size*0.9, card_size*0.9), border)
            pygame.draw.rect(card, (100, 255, 100), (card_size//40, card_size//40, card_size*0.95, card_size*0.95), border//2)
        else:
            card.fill((80, 80, 150, 255))
            border = max(3, card_size // 40)
            pygame.draw.rect(card, (255, 255, 255), (card_size//20, card_size//20, card_size*0.9, card_size*0.9), border)
        
        placeholder_text = self.gm.settings.get_text("placeholder_card", "ЗАГЛУШКА")
        filename_text = filename
        
        font_size = max(10, card_size // 12)
        font = pygame.font.SysFont("arial", font_size)
        status = self.gm.settings.get_text("special") if is_special else self.gm.settings.get_text("normal")
        text = font.render(f"{filename_text}", True, (255, 255, 255))
        card.blit(text, (card_size//20, card_size//2))
        
        placeholder_font = pygame.font.SysFont("arial", max(12, card_size//10), bold=True)
        placeholder_render = placeholder_font.render(placeholder_text, True, (255, 255, 255))
        card.blit(placeholder_render, (card_size//2 - placeholder_render.get_width()//2, card_size//3))
        
        return card

    def _play_background_music(self):
        """Воспроизводит фоновую музыку меню если она еще не играет - ИСПРАВЛЕНО ДЛЯ PYINSTALLER"""
        if self.music_started:
            return
            
        try:
            # Используем resource_path для корректной работы в .exe
            music_path = resource_path(os.path.join("Sounds", "Music", "back_music.mp3"))
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.gm.settings.current_settings["music_volume"])
                pygame.mixer.music.play(-1)
                self.music_started = True
                print("🎵 Фоновая музыка меню запущена")
            else:
                print(f"⚠️ Файл музыки не найден: {music_path}")
        except Exception as e:
            print(f"❌ Ошибка загрузки музыки: {e}")
    
    def on_language_change(self):
        """Вызывается при смене языка"""
        print("🔄 Обновление текстов меню...")
        self._refresh_texts()
    
    def _refresh_texts(self):
        """Обновляет все тексты в меню"""
        if not self.gm.settings:
            return
            
        self.sections = self.gm.settings.get_text("menu_sections")
        # Добавляем вкладку скинов если ее нет
        if len(self.sections) == 6:  # Если стандартные 6 вкладок
            self.sections.insert(3, "SKINS")  # Добавляем после CAMEOS
        
        # Обновляем описания персонажей
        for char in self.characters:
            char["description"] = self.gm.settings.get_text(f"character_{char['name'].lower()}_desc")
        
        for cameo in self.cameos:
            cameo["description"] = self.gm.settings.get_text(f"cameo_{cameo['name'].lower()}_desc")
        
        # 🎮 Обновляем названия режимов игры
        self.game_modes = [
            {"id": "vs_bot", "name": self.gm.settings.get_text("vs_bot", "VS BOT")},
            {"id": "training", "name": self.gm.settings.get_text("training", "ТРЕНИРОВКА")}
        ]
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                # ФИКС: ESC должен выходить из любого режима
                if event.key == pygame.K_ESCAPE:
                    if self.mode_selecting:
                        self.mode_selecting = False
                        print("🚪 Выход из режима выбора режима игры (ESC)")
                    elif self.skin_selecting_mode:
                        self.skin_selecting_mode = False
                        print("🚪 Выход из режима выбора скина (ESC)")
                    elif self.selecting_mode:
                        self.selecting_mode = False
                        print("🚪 Выход из режима выбора персонажа/камео (ESC)")
                    elif self.current_section == 6:  # Если в разделе EXIT
                        self._exit_game()
                    return
                
                if not self.selecting_mode and not self.show_selection_confirmed and not self.skin_selecting_mode and not self.mode_selecting:
                    if event.key == pygame.K_LEFT:
                        self.current_section = (self.current_section - 1) % len(self.sections)
                        if self.current_section == 3:  # SKINS
                            self._refresh_current_skins()
                    elif event.key == pygame.K_RIGHT:
                        self.current_section = (self.current_section + 1) % len(self.sections)
                        if self.current_section == 3:  # SKINS
                            self._refresh_current_skins()
                    elif event.key == pygame.K_RETURN:
                        current_section_name = self.sections[self.current_section]
                        if current_section_name == self.gm.settings.get_text("settings"):
                            self._open_settings()
                        elif current_section_name == self.sections[0]:  # БОЙ
                            self._start_battle()
                        elif current_section_name == self.sections[4]:  # МАГАЗИН
                            self._open_shop()
                        elif current_section_name == self.sections[6]:  # ВЫХОД
                            self._exit_game()
                            
                    elif self.current_section == 1:  # CHARACTERS
                        if event.key in [pygame.K_a, pygame.K_LEFT]:
                            self.selected_character = (self.selected_character - 1) % len(self.characters)
                        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                            self.selected_character = (self.selected_character + 1) % len(self.characters)
                        elif event.key == pygame.K_RETURN:
                            if not self.selecting_mode:
                                self.selecting_mode = True
                    elif self.current_section == 2:  # CAMEOS
                        if event.key in [pygame.K_a, pygame.K_LEFT]:
                            self.selected_cameo = (self.selected_cameo - 1) % len(self.cameos)
                        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                            self.selected_cameo = (self.selected_cameo + 1) % len(self.cameos)
                        elif event.key == pygame.K_RETURN:
                            if not self.selecting_mode:
                                self.selecting_mode = True
                    elif self.current_section == 3:  # SKINS
                        if event.key in [pygame.K_a, pygame.K_LEFT]:
                            self.selected_skin_tab = (self.selected_skin_tab - 1) % 2
                            self._refresh_current_skins()
                        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                            self.selected_skin_tab = (self.selected_skin_tab + 1) % 2
                            self._refresh_current_skins()
                        elif event.key == pygame.K_RETURN:
                            if not self.skin_selecting_mode:
                                self.skin_selecting_mode = True
                                print("🎯 Вход в режим выбора скина")
                
                # 🎮 Обработка режима выбора режима игры
                elif self.mode_selecting and not self.show_selection_confirmed:
                    if event.key == pygame.K_RETURN:
                        self._select_game_mode()
                    elif event.key == pygame.K_ESCAPE:
                        self.mode_selecting = False
                        print("🚪 Выход из режима выбора режима игры")
                    elif event.key in [pygame.K_a, pygame.K_LEFT, pygame.K_UP]:
                        self.selected_game_mode = (self.selected_game_mode - 1) % len(self.game_modes)
                        print(f"⬅️ Смена режима: {self.game_modes[self.selected_game_mode]['name']}")
                    elif event.key in [pygame.K_d, pygame.K_RIGHT, pygame.K_DOWN]:
                        self.selected_game_mode = (self.selected_game_mode + 1) % len(self.game_modes)
                        print(f"➡️ Смена режима: {self.game_modes[self.selected_game_mode]['name']}")
                
                # ФИКС: В режиме выбора скина должны работать стрелки навигации и ESC
                elif self.skin_selecting_mode and not self.show_selection_confirmed:
                    if event.key == pygame.K_RETURN:
                        self._select_skin()
                    elif event.key == pygame.K_ESCAPE:
                        self.skin_selecting_mode = False
                        print("🚪 Выход из режима выбора скина")
                    elif event.key in [pygame.K_a, pygame.K_LEFT]:
                        self.selected_skin_index = (self.selected_skin_index - 1) % len(self.current_skins)
                        print(f"⬅️ Навигация по скинам: индекс {self.selected_skin_index}")
                    elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                        self.selected_skin_index = (self.selected_skin_index + 1) % len(self.current_skins)
                        print(f"➡️ Навигация по скинам: индекс {self.selected_skin_index}")
                    elif event.key == pygame.K_TAB:  # Дополнительная кнопка для смены таба
                        self.selected_skin_tab = (self.selected_skin_tab + 1) % 2
                        self._refresh_current_skins()
                        print(f"🔄 Смена таба скинов: {self.selected_skin_tab}")
                
                elif self.selecting_mode and not self.show_selection_confirmed:
                    if event.key == pygame.K_RETURN:
                        if self.current_section == 1:
                            self._select_character()
                        elif self.current_section == 2:
                            self._select_cameo()
                    elif event.key == pygame.K_ESCAPE:
                        self.selecting_mode = False
                        print("🚪 Выход из режима подтверждения выбора")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # ФИКС: Если показывается сообщение о блокировке скина, игнорируем клики
                    if self.locked_skin_message:
                        return
                    self._handle_mouse_click(mouse_pos)
                    
    def _handle_mouse_click(self, mouse_pos):
        """Обработка кликов мыши"""
        if self.show_selection_confirmed:
            return
            
        if not self.selecting_mode and not self.skin_selecting_mode and not self.mode_selecting:
            # Клики по вкладкам
            for i, tab_rect in enumerate(self.tab_buttons):
                if tab_rect.collidepoint(mouse_pos):
                    self.current_section = i
                    if i == 3:  # SKINS
                        print(f"🎯 Открываем скины для секции: {i}")
                        self._refresh_current_skins()
                    elif i == 4:  # SHOP
                        self._open_shop()
                        return
                    elif i == 5:  # SETTINGS
                        self._open_settings()
                        return
                    elif i == 6:  # EXIT
                        self._exit_game()
                        return
            
            # Навигация в секциях
            if self.current_section == 1:  # CHARACTERS
                if self.char_left_btn and self.char_left_btn.collidepoint(mouse_pos):
                    self.selected_character = (self.selected_character - 1) % len(self.characters)
                elif self.char_right_btn and self.char_right_btn.collidepoint(mouse_pos):
                    self.selected_character = (self.selected_character + 1) % len(self.characters)
                elif self.char_select_btn and self.char_select_btn.collidepoint(mouse_pos):
                    self.selecting_mode = True
                    
            elif self.current_section == 2:  # CAMEOS
                if self.cameo_left_btn and self.cameo_left_btn.collidepoint(mouse_pos):
                    self.selected_cameo = (self.selected_cameo - 1) % len(self.cameos)
                elif self.cameo_right_btn and self.cameo_right_btn.collidepoint(mouse_pos):
                    self.selected_cameo = (self.selected_cameo + 1) % len(self.cameos)
                elif self.cameo_select_btn and self.cameo_select_btn.collidepoint(mouse_pos):
                    self.selecting_mode = True
            
            elif self.current_section == 3:  # SKINS
                if self.skin_tab_left and self.skin_tab_left.collidepoint(mouse_pos):
                    self.selected_skin_tab = (self.selected_skin_tab - 1) % 2
                    self._refresh_current_skins()
                elif self.skin_tab_right and self.skin_tab_right.collidepoint(mouse_pos):
                    self.selected_skin_tab = (self.selected_skin_tab + 1) % 2
                    self._refresh_current_skins()
                elif self.skin_left_btn and self.skin_left_btn.collidepoint(mouse_pos):
                    self.selected_skin_index = (self.selected_skin_index - 1) % len(self.current_skins)
                elif self.skin_right_btn and self.skin_right_btn.collidepoint(mouse_pos):
                    self.selected_skin_index = (self.selected_skin_index + 1) % len(self.current_skins)
                elif self.skin_select_btn and self.skin_select_btn.collidepoint(mouse_pos):
                    self.skin_selecting_mode = True
            
            # 🎮 Обработка кнопки выбора режима игры
            elif self.current_section == 0 and self.mode_button and self.mode_button.collidepoint(mouse_pos):
                self.mode_selecting = True
                print(f"🎮 Вход в режим выбора режима игры")
            
            # Обработка кнопок в секции FIGHT
            elif self.current_section == 0 and self.battle_button and self.battle_button.collidepoint(mouse_pos):
                self._start_battle()
                    
        elif self.selecting_mode:
            # Подтверждение выбора в режиме selecting_mode
            if self.current_section == 1 and self.char_select_btn and self.char_select_btn.collidepoint(mouse_pos):
                self._select_character()
            elif self.current_section == 2 and self.cameo_select_btn and self.cameo_select_btn.collidepoint(mouse_pos):
                self._select_cameo()
        
        elif self.skin_selecting_mode:
            # Подтверждение выбора скина
            if self.current_section == 3 and self.skin_select_btn and self.skin_select_btn.collidepoint(mouse_pos):
                self._select_skin()
        
        elif self.mode_selecting:
            # Подтверждение выбора режима игры
            if self.current_section == 0 and self.mode_button and self.mode_button.collidepoint(mouse_pos):
                self._select_game_mode()
    
    def _refresh_current_skins(self):
        """Обновляет список текущих скинов при смене таба"""
        self.current_skins = []
        
        if self.selected_skin_tab == 0:  # Персонажи
            selected_char = next((char for char in self.characters if char["selected"]), None)
            if selected_char:
                char_key = selected_char['name'].lower().strip()
                print(f"🔍 Ищем скины для: '{char_key}' в {list(self.character_skins.keys())}")
                
                if char_key in self.character_skins:
                    # Преобразуем словарь в список для единообразия
                    skins_dict = self.character_skins[char_key]
                    for skin_id, skin_data in skins_dict.items():
                        self.current_skins.append({
                            "id": skin_id,
                            "name": skin_data["name"],
                            "unlocked": skin_data["unlocked"],
                            "card_normal": skin_data["card_normal"],
                            "card_special": skin_data["card_special"]
                        })
                    print(f"✅ Найдено {len(self.current_skins)} скинов для {selected_char['name']}")
                else:
                    print(f"❌ Не найдено скинов для {char_key}")
            else:
                print("❌ Не выбран персонаж")
        else:  # Камео
            selected_cameo = next((cameo for cameo in self.cameos if cameo["selected"]), None)
            if selected_cameo:
                cameo_key = selected_cameo['name'].lower().strip()
                print(f"🔍 Ищем скины для камео: '{cameo_key}' в {list(self.cameo_skins.keys())}")
                
                if cameo_key in self.cameo_skins:
                    skins_dict = self.cameo_skins[cameo_key]
                    for skin_id, skin_data in skins_dict.items():
                        self.current_skins.append({
                            "id": skin_id,
                            "name": skin_data["name"],
                            "unlocked": skin_data["unlocked"],
                            "card_normal": skin_data["card_normal"],
                            "card_special": skin_data["card_special"]
                        })
                    print(f"✅ Найдено {len(self.current_skins)} скинов для камео {selected_cameo['name']}")
                else:
                    print(f"❌ Не найдено скинов для камео {cameo_key}")
            else:
                print("❌ Не выбрано камео")
        
        # Находим индекс текущего активного скина
        selected_entity = None
        if self.selected_skin_tab == 0:
            selected_entity = next((char for char in self.characters if char["selected"]), None)
        else:
            selected_entity = next((cameo for cameo in self.cameos if cameo["selected"]), None)
            
        if selected_entity:
            current_skin_id = selected_entity["skin"]
            for i, skin in enumerate(self.current_skins):
                if skin["id"] == current_skin_id:
                    self.selected_skin_index = i
                    print(f"🎯 Найден текущий скин '{current_skin_id}' на позиции {i}")
                    break
            else:
                self.selected_skin_index = 0  # fallback
                print(f"⚠️ Текущий скин '{current_skin_id}' не найден в списке, сбрасываем на индекс 0")
        
        print(f"🎯 Текущий индекс скина: {self.selected_skin_index}, всего скинов: {len(self.current_skins)}")

    def _select_skin(self):
        """Применяет выбранный скин - ИСПРАВЛЕН БАГ С ЗАВИСАНИЕМ"""
        if not self.current_skins or self.selected_skin_index >= len(self.current_skins):
            print(f"❌ Нет скинов для выбора: {len(self.current_skins)} доступно, индекс {self.selected_skin_index}")
            return
            
        skin = self.current_skins[self.selected_skin_index]
        
        print(f"🎯 Выбран скин: {skin['name']} (id: {skin['id']})")
        
        # ИСПРАВЛЕНИЕ БАГА: Проверка разблокировки - не выходим из режима, просто показываем сообщение
        if not skin["unlocked"]:
            print(f"❌ Скин {skin['name']} заблокирован! Показываем сообщение...")
            self.locked_skin_message = True
            self.locked_skin_message_time = pygame.time.get_ticks()
            # ФИКС: Не блокируем управление, пользователь может нажать ESC или выбрать другой скин
            # skin_selecting_mode остается True, чтобы можно было выбрать другой скин
            return
        
        # Если скин разблокирован, применяем его
        if self.selected_skin_tab == 0:  # Персонажи
            selected_char = next((char for char in self.characters if char["selected"]), None)
            if selected_char:
                selected_char["skin"] = skin["id"]
                # Сохраняем в сохранения
                self.save_manager.save_game(character_skin=skin["id"])
                print(f"✅ Применен скин персонажа: {skin['name']}")
                
                # ПЕРЕЗАГРУЖАЕМ КАРТОЧКИ С НОВЫМ СКИНОМ
                self._load_character_cards(selected_char)
        else:  # Камео
            selected_cameo = next((cameo for cameo in self.cameos if cameo["selected"]), None)
            if selected_cameo:
                selected_cameo["skin"] = skin["id"]
                # Сохраняем в сохранения
                self.save_manager.save_game(cameo_skin=skin["id"])
                print(f"✅ Применен скин камео: {skin['name']}")
                
                # ПЕРЕЗАГРУЖАЕМ КАРТОЧКИ С НОВЫМ СКИНОМ
                self._load_cameo_cards(selected_cameo)
        
        self.selection_confirmed_time = pygame.time.get_ticks()
        self.show_selection_confirmed = True
        self.skin_selecting_mode = False  # Выходим из режима выбора

    def _select_game_mode(self):
        """🎮 Сохраняет выбранный режим игры"""
        selected_mode = self.game_modes[self.selected_game_mode]
        print(f"🎮 Выбран режим игры: {selected_mode['name']}")
        
        # Сохраняем в сохранения ID режима (строчные)
        self.save_manager.save_game(game_mode=selected_mode["id"])  # Используем id
        
        self.selection_confirmed_time = pygame.time.get_ticks()
        self.show_selection_confirmed = True
        self.mode_selecting = False
        print(f"✅ Режим '{selected_mode['name']}' сохранен (id: {selected_mode['id']})")

    def _start_battle(self):
        selected_char = next((char for char in self.characters if char["selected"]), None)
        selected_cameo = next((cameo for cameo in self.cameos if cameo["selected"]), None)
        
        if not selected_char:
            print("❌ Выберите персонажа перед началом боя!")
            return
        if not selected_cameo:
            print("❌ Выберите камео перед началом боя!")
            return
            
        char_name = selected_char["name"]
        cameo_name = selected_cameo["name"]
        game_mode = self.game_modes[self.selected_game_mode]
        
        print(f"🎮 Запуск боя: {char_name} + {cameo_name} | Режим: {game_mode['name']}")
        
        # 🎮 Передаем выбранный режим в игровые сцены
        self._create_game_scenes(char_name, cameo_name, game_mode)
        
        from src.scenes.loading_scene import LoadingScene
        loading_scene = LoadingScene(self.gm, "intro")
        self.gm.register_scene("game_loading", loading_scene)
        self.gm.set_scene("game_loading")
    
    def _open_settings(self):
        self.gm.set_scene("settings")

    def _open_shop(self):
        """Открывает магазин"""
        print("🛒 Открываем магазин...")
        self.gm.set_scene("shop")
    
    def _exit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def _create_game_scenes(self, char_name, cameo_name, game_mode):
        from src.core.character import Character
        from src.scenes.intro_scene import IntroSequenceScene
        from src.scenes.battle_scene import BattleScene
        from src.scenes.victory_scene import VictoryScene
        
        player_char = Character(char_name, self.gm.resources)
        enemy_char = Character("fighter_right", self.gm.resources)
        player_cameo = Character(cameo_name, self.gm.resources)
        enemy_cameo = Character("cameo_right", self.gm.resources)
        
        # 🎮 Создаем интро сцену с передачей режима игры
        self.gm.register_scene("intro", IntroSequenceScene(
            self.gm, player_char, player_cameo, enemy_char, enemy_cameo, game_mode
        ))
        self.gm.register_scene("battle", BattleScene(self.gm, player_char, enemy_char, game_mode))
        self.gm.register_scene("victory", VictoryScene(self.gm, None, game_mode))
    
    def update(self, dt):
        """Обновление сцены"""
        # 🎬 ОБНОВЛЯЕМ ВСЕ АКТИВНЫЕ АНИМАЦИИ
        for animation in self.playing_animations:
            animation.update(dt)
        
        # Очищаем список анимаций (будет заполнен заново при отрисовке)
        self.playing_animations = []
        
        if self.show_selection_confirmed:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_confirmed_time > 1500:
                self.show_selection_confirmed = False
                self.selecting_mode = False
                self.skin_selecting_mode = False
                self.mode_selecting = False  # 🎮 Сбрасываем режим выбора режима
                # Автоматически возвращаемся на вкладку FIGHT после подтверждения выбора
                self.current_section = 0
        
        # Обновление анимации разблокировки
        if self.unlock_animation:
            current_time = pygame.time.get_ticks()
            if current_time - self.unlock_animation_time > 2000:
                self.unlock_animation = False
                self.unlock_animation_skin = None
        
        # ФИКС: Обновление сообщения о блокировке скина
        if self.locked_skin_message:
            current_time = pygame.time.get_ticks()
            if current_time - self.locked_skin_message_time > 1500:
                self.locked_skin_message = False
    
    def draw(self, screen):
        self._draw_background(screen)
        self._draw_header(screen)
        self._draw_section_tabs(screen)
        
        # Рисуем контент в зависимости от текущей секции
        content_rect = pygame.Rect(0, self.s(140), screen.get_width(), screen.get_height() - self.s(200))
        
        if self.current_section == 0:
            self._draw_fight_section(screen, content_rect)
        elif self.current_section == 1:
            self._draw_characters_section(screen, content_rect)
        elif self.current_section == 2:
            self._draw_cameo_section(screen, content_rect)
        elif self.current_section == 3:
            self._draw_skins_section(screen, content_rect)
        elif self.current_section == 4:
            self._draw_shop_section(screen, content_rect)
        elif self.current_section == 5:
            self._draw_settings_section(screen, content_rect)
        elif self.current_section == 6:
            self._draw_exit_section(screen, content_rect)
        
        self._draw_bottom_bar(screen)
        
        # Рисуем анимацию разблокировки поверх всего
        if self.unlock_animation:
            self._draw_unlock_animation(screen)
        
        # Рисуем сообщение о блокировке скина
        if self.locked_skin_message:
            self._draw_locked_skin_message(screen)
    
    def _draw_background(self, screen):
        """Отрисовка фона с градиентом"""
        screen.fill(self.colors["background"])
        
        # Градиентный фон
        for i in range(screen.get_height()):
            color = (20 + i//20, 20 + i//25, 40 + i//15)
            pygame.draw.line(screen, color, (0, i), (screen.get_width(), i))
    
    def _draw_header(self, screen):
        """Верхняя панель с названием и ресурсами"""
        header_height = self.s(80)
        header_rect = pygame.Rect(0, 0, screen.get_width(), header_height)
        
        # Градиентный фон хедера
        for i in range(header_height):
            color = (30 + i//3, 30 + i//3, 50 + i//2)
            pygame.draw.line(screen, color, (0, i), (screen.get_width(), i))
        
        # Заголовок
        title_font = self.get_font(36, bold=True)
        title_text = self.gm.settings.get_text("game_title")
        title = title_font.render(title_text, True, self.colors["accent"])
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, self.s(20)))
        
        # Ресурсы игрока
        resource_font = self.get_font(18)
        coins_text = resource_font.render(f"🪙 {self.player_data['coins']}", True, (255, 215, 0))
        trophies_text = resource_font.render(f"🏆 {self.player_data['trophies']}", True, (255, 200, 100))
        
        screen.blit(coins_text, (screen.get_width() - self.s(150), self.s(25)))
        screen.blit(trophies_text, (screen.get_width() - self.s(150), self.s(50)))
    
    def _draw_section_tabs(self, screen):
        """Отрисовка вертикальных вкладок меню слева и справа, центрированных по Y - увеличенные"""
        self.tab_buttons = []
        
        # ⚡ УВЕЛИЧИЛ РАЗМЕРЫ КНОПОК
        tab_width = self.s(180)  # Было 160 -> 180
        tab_height = self.s(55)  # Было 50 -> 55
        tab_spacing = self.s(15)  # Было 12 -> 15
        
        # Левая группа: FIGHT, CHARACTERS, CAMEOS, SKINS
        left_tabs = self.sections[:4]
        # Правая группа: SHOP, SETTINGS, EXIT
        right_tabs = self.sections[4:]
        
        # Центрируем обе группы по вертикали
        left_total_height = len(left_tabs) * tab_height + (len(left_tabs) - 1) * tab_spacing
        right_total_height = len(right_tabs) * tab_height + (len(right_tabs) - 1) * tab_spacing
        
        left_start_y = (screen.get_height() - left_total_height) // 2
        right_start_y = (screen.get_height() - right_total_height) // 2
        
        # Левые вкладки
        left_x = self.s(30)
        for i, section in enumerate(left_tabs):
            tab_rect = pygame.Rect(left_x, left_start_y + i * (tab_height + tab_spacing), tab_width, tab_height)
            self.tab_buttons.append(tab_rect)
            
            color = self.colors["button_primary"] if i == self.current_section else self.colors["header_bg"]
            
            pygame.draw.rect(screen, color, tab_rect, border_radius=self.s(12))
            pygame.draw.rect(screen, self.colors["text_light"], tab_rect, self.s(2), border_radius=self.s(12))
            
            # ⚡ УВЕЛИЧИЛ ШРИФТ
            max_font_size = self.f(18)
            min_font_size = self.f(12)
            font_size = max_font_size
            
            while font_size >= min_font_size:
                font = pygame.font.SysFont("arial", int(font_size), bold=True)
                text_surface = font.render(section, True, self.colors["text_light"])
                
                if text_surface.get_width() <= tab_width - self.s(15):
                    break
                font_size -= 1
            
            final_font = pygame.font.SysFont("arial", int(font_size), bold=True)
            final_text = final_font.render(section, True, self.colors["text_light"])
            
            screen.blit(final_text, (tab_rect.centerx - final_text.get_width() // 2, 
                                   tab_rect.centery - final_text.get_height() // 2))
        
        # Правые вкладки
        right_x = screen.get_width() - tab_width - self.s(30)
        for i, section in enumerate(right_tabs):
            tab_index = i + 4  # Индекс в общем списке
            tab_rect = pygame.Rect(right_x, right_start_y + i * (tab_height + tab_spacing), tab_width, tab_height)
            self.tab_buttons.append(tab_rect)
            
            if section == self.sections[6]:  # ВЫХОД
                color = self.colors["danger"] if tab_index == self.current_section else (150, 80, 80)
            else:
                color = self.colors["button_secondary"] if tab_index == self.current_section else self.colors["header_bg"]
            
            pygame.draw.rect(screen, color, tab_rect, border_radius=self.s(12))
            pygame.draw.rect(screen, self.colors["text_light"], tab_rect, self.s(2), border_radius=self.s(12))
            
            # ⚡ УВЕЛИЧИЛ ШРИФТ
            max_font_size = self.f(18)
            min_font_size = self.f(12)
            font_size = max_font_size
            
            while font_size >= min_font_size:
                font = pygame.font.SysFont("arial", int(font_size), bold=True)
                text_surface = font.render(section, True, self.colors["text_light"])
                
                if text_surface.get_width() <= tab_width - self.s(15):
                    break
                font_size -= 1
            
            final_font = pygame.font.SysFont("arial", int(font_size), bold=True)
            final_text = final_font.render(section, True, self.colors["text_light"])
            
            screen.blit(final_text, (tab_rect.centerx - final_text.get_width() // 2, 
                                   tab_rect.centery - final_text.get_height() // 2))

    def _draw_fight_section(self, screen, rect):
        """Секция FIGHT - основной экран с АНИМИРОВАННЫМИ АРТАМИ и выбором режима"""
        # Показываем выбранные персонаж и камео
        selected_char = next((char for char in self.characters if char["selected"]), None)
        selected_cameo = next((cameo for cameo in self.cameos if cameo["selected"]), None)
        
        # 🎬 АНИМИРОВАННЫЕ АРТЫ ПО ЦЕНТРУ
        art_size = self.s(350)
        
        # Арт персонажа с учетом ВЫБРАННОГО СКИНА (анимированный)
        if selected_char:
            char_animation = self._load_art_animation(selected_char["name"], selected_char["skin"], art_size)
            if char_animation:
                char_x = rect.centerx - art_size + self.s(40)
                char_y = rect.centery - art_size // 2
                
                # Отрисовываем текущий кадр анимации
                frame = char_animation.get_frame()
                if frame:
                    screen.blit(frame, (char_x, char_y))
                
                # Добавляем анимацию в список для обновления, если ее там еще нет
                if char_animation not in self.playing_animations:
                    self.playing_animations.append(char_animation)
        
        # Арт камео с учетом ВЫБРАННОГО СКИНА (анимированный)
        if selected_cameo:
            cameo_animation = self._load_art_animation(selected_cameo["name"], selected_cameo["skin"], art_size)
            if cameo_animation:
                cameo_x = rect.centerx - self.s(40)
                cameo_y = rect.centery - art_size // 2
                
                # Отрисовываем текущий кадр анимации
                frame = cameo_animation.get_frame()
                if frame:
                    screen.blit(frame, (cameo_x, cameo_y))
                
                # Добавляем анимацию в список для обновления, если ее там еще нет
                if cameo_animation not in self.playing_animations:
                    self.playing_animations.append(cameo_animation)
        
        # 🎮 Кнопка выбора режима - внизу по центру
        mode_btn_width = self.s(220)
        mode_btn_height = self.s(60)
        self.mode_button = pygame.Rect(
            rect.centerx - mode_btn_width // 2,
            rect.bottom - mode_btn_height - self.s(30),
            mode_btn_width,
            mode_btn_height
        )
        
        # Определяем цвет кнопки в зависимости от выбранного режима и состояния
        if self.mode_selecting:
            btn_color = self.colors["selected"]
        elif self.selected_game_mode == 1:  # Тренировка
            btn_color = self.colors["training"]
        else:  # VS BOT
            btn_color = self.colors["button_secondary"]
        
        pygame.draw.rect(screen, btn_color, self.mode_button, border_radius=self.s(12))
        pygame.draw.rect(screen, self.colors["text_light"], self.mode_button, self.s(2), border_radius=self.s(12))
        
        mode_font = self.get_font(20, bold=True)
        mode_text = mode_font.render(self.game_modes[self.selected_game_mode]["name"], True, self.colors["text_light"])
        screen.blit(mode_text, (self.mode_button.centerx - mode_text.get_width() // 2,
                              self.mode_button.centery - mode_text.get_height() // 2))
        
        # 🎮 Подсказка для выбора режима (если мы в режиме выбора)
        if self.mode_selecting:
            hint_font = self.get_font(15)
            hint_text = "Используйте ←→ или кликните для выбора режима"
            hint = hint_font.render(hint_text, True, self.colors["text_dark"])
            screen.blit(hint, (rect.centerx - hint.get_width() // 2, 
                             self.mode_button.top - self.s(25)))
        
        # Кнопка начала боя - внизу справа
        btn_width = self.s(200)
        btn_height = self.s(60)
        self.battle_button = pygame.Rect(
            rect.right - btn_width - self.s(50),
            rect.bottom - btn_height - self.s(30),
            btn_width,
            btn_height
        )
        battle_enabled = selected_char and selected_cameo
        
        if battle_enabled:
            # 🎮 Меняем текст кнопки в зависимости от режима
            btn_text = "НАЧАТЬ!" if self.selected_game_mode == 0 else "ТРЕНИРОВАТЬСЯ!"
            pygame.draw.rect(screen, self.colors["button_primary"], self.battle_button, border_radius=self.s(12))
            pygame.draw.rect(screen, self.colors["accent"], self.battle_button, self.s(3), border_radius=self.s(12))
        else:
            btn_text = "FIGHT!"
            pygame.draw.rect(screen, (100, 100, 100), self.battle_button, border_radius=self.s(12))
            pygame.draw.rect(screen, (150, 150, 150), self.battle_button, self.s(3), border_radius=self.s(12))
        
        btn_font = self.get_font(22, bold=True)
        btn_render = btn_font.render(btn_text, True, 
                                   self.colors["text_light"] if battle_enabled else self.colors["text_dark"])
        screen.blit(btn_render, (self.battle_button.centerx - btn_render.get_width() // 2,
                               self.battle_button.centery - btn_render.get_height() // 2))

    def _load_art_animation(self, entity_name, skin_id, art_size):
        """🎬 Загружает видео-анимацию арта с учетом скина"""
        cache_key = f"{entity_name.lower()}_{skin_id}_{art_size}"
        
        # Проверяем кэш
        if cache_key in self.art_animations:
            return self.art_animations[cache_key]
        
        # Основной путь к видео: Sprites/arts/{имя}_{скин}_art.mp4
        video_path = os.path.join("Sprites", "arts", f"{entity_name.lower()}_{skin_id}_art.mp4")
        
        animation = None
        
        try:
            # Используем resource_path для корректной работы в .exe
            actual_path = resource_path(video_path)
            if os.path.exists(actual_path):
                print(f"🎬 Загружаем видео арт: {video_path}")
                
                # Рассчитываем целевой размер с сохранением пропорций 704x1280
                # Пропорции: 704 / 1280 ≈ 0.55 (ширина/высота)
                original_width = 704   # Ширина оригинала
                original_height = 1280 # Высота оригинала
                
                # Сохраняем пропорции видео (портретный формат)
                # Подгоняем под квадрат art_size
                if art_size > 0:
                    # Вычисляем масштаб по высоте (лимитирующая сторона)
                    scale_factor = art_size / original_height
                    target_width = int(original_width * scale_factor)
                    target_height = art_size  # Высота равна art_size
                    
                    # Видео будет уже чем квадрат, поэтому центрируем
                    target_size = (target_width, target_height)
                else:
                    target_size = None
                
                print(f"📐 Масштабирование: {original_width}x{original_height} -> {target_size}")
                
                animation = VideoAnimation(
                    video_path=video_path,
                    target_size=target_size,
                    loop=True,  # Зацикленное воспроизведение
                    fps=30  # Можно не указывать, будет взято из видео
                )
                print(f"✅ Видео загружено: {len(animation.frames)} кадров, FPS: {animation.fps}")
            else:
                print(f"❌ Видео не найдено: {actual_path}")
                # Пробуем альтернативные пути (для обратной совместимости)
                alternative_paths = [
                    os.path.join("Sprites", "arts", f"{entity_name.lower()}_art.mp4"),
                    os.path.join("Sprites", "arts", entity_name.lower(), f"{skin_id}_art.mp4"),
                    os.path.join("Sprites", "arts", entity_name.lower(), "default_art.mp4"),
                ]
                
                for alt_path in alternative_paths:
                    alt_actual_path = resource_path(alt_path)
                    if os.path.exists(alt_actual_path):
                        print(f"🎬 Найдено альтернативное видео: {alt_path}")
                        # Используем то же масштабирование
                        if art_size > 0:
                            scale_factor = art_size / 1280
                            target_width = int(704 * scale_factor)
                            target_height = art_size
                            target_size = (target_width, target_height)
                        else:
                            target_size = None
                        
                        animation = VideoAnimation(
                            video_path=alt_path,
                            target_size=target_size,
                            loop=True,
                            fps=30
                        )
                        print(f"✅ Альтернативное видео загружено")
                        break
                
        except Exception as e:
            print(f"⚠️ Ошибка загрузки видео {video_path}: {e}")
        
        # Если видео не найдено, создаем анимацию из статичного изображения
        if animation is None:
            print(f"⚠️ Видео для {entity_name}_{skin_id} не найдено, используем статичный арт")
            static_image = self._load_static_art_image(entity_name, skin_id, art_size)
            if static_image:
                # Рассчитываем размер для статичного изображения с теми же пропорциями
                if art_size > 0:
                    # Сохраняем пропорции оригинала
                    original_width, original_height = static_image.get_size()
                    scale_factor = art_size / original_height
                    target_width = int(original_width * scale_factor)
                    target_height = art_size
                    
                    # Масштабируем изображение
                    static_image = pygame.transform.scale(static_image, (target_width, target_height))
                
                # Создаем анимацию из одного кадра
                animation = VideoAnimation(
                    video_path="",  # Пустой путь
                    target_size=(target_width, target_height) if art_size > 0 else None,
                    loop=True,
                    fps=1
                )
                # Заменяем кадры на статичное изображение
                animation.frames = [static_image] * 30  # 30 одинаковых кадров для плавности
                animation.fps = 30
                print(f"🖼️ Используем статичный арт: {entity_name}/{skin_id} ({target_width}x{target_height})")
            else:
                # Создаем заглушку с пропорциями 704x1280
                if art_size > 0:
                    scale_factor = art_size / 1280
                    placeholder_width = int(704 * scale_factor)
                    placeholder_height = art_size
                else:
                    placeholder_width = 704
                    placeholder_height = 1280
                
                placeholder = self._create_placeholder_art(entity_name, placeholder_width, placeholder_height)
                animation = VideoAnimation(
                    video_path="",
                    target_size=(placeholder_width, placeholder_height) if art_size > 0 else None,
                    loop=True,
                    fps=1
                )
                animation.frames = [placeholder] * 30
                animation.fps = 30
                print(f"⚠️ Создана заглушка для: {entity_name}/{skin_id} ({placeholder_width}x{placeholder_height})")
        
        # Сохраняем в кэш
        self.art_animations[cache_key] = animation
        return animation
    
    def _load_static_art_image(self, entity_name, skin_id, art_size):
        """Загружает статичное изображение арта (для обратной совместимости)"""
        # Пробуем разные пути к изображениям
        image_paths = [
            os.path.join("Sprites", "arts", f"{entity_name.lower()}_{skin_id}.png"),
            os.path.join("Sprites", "arts", f"{entity_name.lower()}_{skin_id}.jpg"),
            os.path.join("Sprites", "arts", f"{entity_name.lower()}.png"),
            os.path.join("Sprites", "arts", f"{entity_name.lower()}.jpg"),
            os.path.join("Sprites", "arts", entity_name.lower(), f"{skin_id}.png"),
            os.path.join("Sprites", "arts", entity_name.lower(), "default.png"),
        ]
        
        for img_path in image_paths:
            try:
                actual_path = resource_path(img_path)
                if os.path.exists(actual_path):
                    print(f"🖼️ Загружаем статичный арт: {img_path}")
                    image = pygame.image.load(actual_path).convert_alpha()
                    
                    # Масштабируем с сохранением пропорций как у видео 704x1280
                    if art_size > 0:
                        original_width, original_height = image.get_size()
                        
                        # Сохраняем пропорции как у видео (портретный формат)
                        # Высота фиксированная = art_size, ширина пропорциональная
                        scale_factor = art_size / max(original_height, 1)  # избегаем деления на 0
                        target_width = int(original_width * scale_factor)
                        target_height = art_size
                        
                        image = pygame.transform.scale(image, (target_width, target_height))
                        print(f"✅ Статичный арт загружен и масштабирован: {target_width}x{target_height}")
                    
                    return image
            except Exception as e:
                print(f"⚠️ Ошибка загрузки изображения {img_path}: {e}")
                continue
        
        return None

    def _create_placeholder_art(self, filename, width, height):
        """Создание заглушки для арта с указанными размерами"""
        art = pygame.Surface((width, height), pygame.SRCALPHA)
        art.fill((80, 80, 150, 255))
        
        border = max(3, min(width, height) // 40)
        pygame.draw.rect(art, (255, 255, 255), (border, border, width-2*border, height-2*border), border)
        
        placeholder_font = pygame.font.SysFont("arial", max(20, min(width, height)//15), bold=True)
        placeholder_text = placeholder_font.render("АРТ", True, (255, 255, 255))
        art.blit(placeholder_text, (width//2 - placeholder_text.get_width()//2, height//3))
        
        name_font = pygame.font.SysFont("arial", max(14, min(width, height)//20))
        name_text = name_font.render(filename, True, (200, 200, 200))
        art.blit(name_text, (width//2 - name_text.get_width()//2, height//2))
        
        # Добавляем информацию о пропорциях
        ratio_font = pygame.font.SysFont("arial", max(12, min(width, height)//25))
        ratio_text = ratio_font.render(f"{width}x{height}", True, (150, 150, 200))
        art.blit(ratio_text, (width//2 - ratio_text.get_width()//2, height*2//3))
        
        return art
    
    def _draw_characters_section(self, screen, rect):
        """Секция выбора персонажей - упрощенная логика карточек"""
        title_font = self.get_font(26, bold=True)
        if self.show_selection_confirmed:
            title_text = self.gm.settings.get_text("character_selected")
        elif self.selecting_mode:
            title_text = self.gm.settings.get_text("confirm_character")
        else:
            title_text = self.gm.settings.get_text("select_character_title")
            
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width() // 2, rect.y + self.s(25)))
        
        character = self.characters[self.selected_character]
        char_key = character["name"].lower()
        
        # Получаем правильный скин
        if char_key in self.character_skins and "default" in self.character_skins[char_key]:
            skin = self.character_skins[char_key]["default"]
        else:
            skin = {"card_normal": None, "card_special": None}
            
        card_size = self._get_card_size()
        
        # 🎯 УПРОЩАЕМ: special карточка ТОЛЬКО во время выбора
        if self.selecting_mode or self.show_selection_confirmed:
            card = skin["card_special"]
        else:
            card = skin["card_normal"]
            
        if card:
            card_rect = pygame.Rect(rect.centerx - card_size//2, rect.centery - card_size//2, card_size, card_size)
            screen.blit(card, card_rect)
        else:
            # Если карточки нет, показываем заглушку
            error_font = self.get_font(18)
            error_text = error_font.render("Карточка не найдена", True, self.colors["danger"])
            screen.blit(error_text, (rect.centerx - error_text.get_width() // 2, rect.centery - self.s(10)))
            card_rect = pygame.Rect(rect.centerx - card_size//2, rect.centery - card_size//2, card_size, card_size)
        
        name_font = self.get_font(22, bold=True)
        name_text = name_font.render(character["name"], True, self.colors["text_light"])
        screen.blit(name_text, (rect.centerx - name_text.get_width() // 2, card_rect.bottom + self.s(15)))
        
        desc_font = self.get_font(16)
        desc_text = desc_font.render(character["description"], True, self.colors["text_dark"])
        screen.blit(desc_text, (rect.centerx - desc_text.get_width() // 2, card_rect.bottom + self.s(40)))
        
        if not self.selecting_mode and not self.show_selection_confirmed:
            arrow_size = self.s(50)
            self.char_left_btn = pygame.Rect(card_rect.left - arrow_size - self.s(15), card_rect.centery - arrow_size//2, arrow_size, arrow_size)
            self.char_right_btn = pygame.Rect(card_rect.right + self.s(15), card_rect.centery - arrow_size//2, arrow_size, arrow_size)
            
            pygame.draw.rect(screen, self.colors["button_primary"], self.char_left_btn, border_radius=self.s(10))
            pygame.draw.rect(screen, self.colors["text_light"], self.char_left_btn, self.s(2), border_radius=self.s(10))
            arrow_font = self.get_font(28, bold=True)
            left_arrow = arrow_font.render("⟨", True, self.colors["text_light"])
            screen.blit(left_arrow, (self.char_left_btn.centerx - left_arrow.get_width() // 2,
                                self.char_left_btn.centery - left_arrow.get_height() // 2))
            
            pygame.draw.rect(screen, self.colors["button_primary"], self.char_right_btn, border_radius=self.s(10))
            pygame.draw.rect(screen, self.colors["text_light"], self.char_right_btn, self.s(2), border_radius=self.s(10))
            right_arrow = arrow_font.render("⟩", True, self.colors["text_light"])
            screen.blit(right_arrow, (self.char_right_btn.centerx - right_arrow.get_width() // 2,
                                    self.char_right_btn.centery - right_arrow.get_height() // 2))
        
        btn_width = min(self.s(180), rect.width * 0.4)
        btn_height = self.s(45)
        self.char_select_btn = pygame.Rect(rect.centerx - btn_width//2, card_rect.bottom + self.s(60), btn_width, btn_height)
        
        if self.show_selection_confirmed:
            btn_color = self.colors["selected"]
            btn_text = self.gm.settings.get_text("selected_button")
        elif self.selecting_mode:
            btn_color = self.colors["selected"]
            btn_text = self.gm.settings.get_text("confirm_button")
        else:
            btn_color = self.colors["button_primary"]
            btn_text = self.gm.settings.get_text("select_button")
            
        pygame.draw.rect(screen, btn_color, self.char_select_btn, border_radius=self.s(8))
        pygame.draw.rect(screen, self.colors["text_light"], self.char_select_btn, self.s(2), border_radius=self.s(8))
        
        select_font = self.get_font(18, bold=True)
        select_text = select_font.render(btn_text, True, self.colors["text_light"])
        screen.blit(select_text, (self.char_select_btn.centerx - select_text.get_width() // 2,
                                self.char_select_btn.centery - select_text.get_height() // 2))
        
        hint_font = self.get_font(15)
        if self.show_selection_confirmed:
            hint_text = self.gm.settings.get_text("returning_to_battle")
        elif self.selecting_mode:
            hint_text = self.gm.settings.get_text("confirm_hint")
        else:
            hint_text = self.gm.settings.get_text("use_arrows")
            
        hint = hint_font.render(hint_text, True, self.colors["text_dark"])
        screen.blit(hint, (rect.centerx - hint.get_width() // 2, self.char_select_btn.bottom + self.s(15)))
    
    def _draw_cameo_section(self, screen, rect):
        """Секция выбора камео - упрощенная логика карточек"""
        title_font = self.get_font(26, bold=True)
        if self.show_selection_confirmed:
            title_text = self.gm.settings.get_text("cameo_selected")
        elif self.selecting_mode:
            title_text = self.gm.settings.get_text("confirm_cameo")
        else:
            title_text = self.gm.settings.get_text("select_cameo_title")
            
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width() // 2, rect.y + self.s(25)))
        
        cameo = self.cameos[self.selected_cameo]
        card_size = self._get_card_size()
        
        if self.selecting_mode or self.show_selection_confirmed:
            card = cameo["card_special"]
        else:
            card = cameo["card_normal"]
            
        if card:
            card_rect = pygame.Rect(rect.centerx - card_size//2, rect.centery - card_size//2, card_size, card_size)
            screen.blit(card, card_rect)
        else:
            # Если карточки нет, показываем заглушку
            error_font = self.get_font(18)
            error_text = error_font.render("Карточка не найдена", True, self.colors["danger"])
            screen.blit(error_text, (rect.centerx - error_text.get_width() // 2, rect.centery - self.s(10)))
            card_rect = pygame.Rect(rect.centerx - card_size//2, rect.centery - card_size//2, card_size, card_size)
        
        name_font = self.get_font(20, bold=True)
        name_text = name_font.render(cameo["name"], True, self.colors["text_light"])
        screen.blit(name_text, (rect.centerx - name_text.get_width() // 2, card_rect.bottom + self.s(15)))
        
        desc_font = self.get_font(16)
        desc_text = desc_font.render(cameo["description"], True, self.colors["text_dark"])
        screen.blit(desc_text, (rect.centerx - desc_text.get_width() // 2, card_rect.bottom + self.s(40)))
        
        if not self.selecting_mode and not self.show_selection_confirmed:
            arrow_size = self.s(50)
            self.cameo_left_btn = pygame.Rect(card_rect.left - arrow_size - self.s(15), card_rect.centery - arrow_size//2, arrow_size, arrow_size)
            self.cameo_right_btn = pygame.Rect(card_rect.right + self.s(15), card_rect.centery - arrow_size//2, arrow_size, arrow_size)
            
            pygame.draw.rect(screen, self.colors["button_secondary"], self.cameo_left_btn, border_radius=self.s(10))
            pygame.draw.rect(screen, self.colors["text_light"], self.cameo_left_btn, self.s(2), border_radius=self.s(10))
            arrow_font = self.get_font(28, bold=True)
            left_arrow = arrow_font.render("⟨", True, self.colors["text_light"])
            screen.blit(left_arrow, (self.cameo_left_btn.centerx - left_arrow.get_width() // 2,
                                self.cameo_left_btn.centery - left_arrow.get_height() // 2))
            
            pygame.draw.rect(screen, self.colors["button_secondary"], self.cameo_right_btn, border_radius=self.s(10))
            pygame.draw.rect(screen, self.colors["text_light"], self.cameo_right_btn, self.s(2), border_radius=self.s(10))
            right_arrow = arrow_font.render("⟩", True, self.colors["text_light"])
            screen.blit(right_arrow, (self.cameo_right_btn.centerx - right_arrow.get_width() // 2,
                                    self.cameo_right_btn.centery - right_arrow.get_height() // 2))
        
        btn_width = min(self.s(180), rect.width * 0.4)
        btn_height = self.s(45)
        self.cameo_select_btn = pygame.Rect(rect.centerx - btn_width//2, card_rect.bottom + self.s(60), btn_width, btn_height)
        
        if self.show_selection_confirmed:
            btn_color = self.colors["selected"]
            btn_text = self.gm.settings.get_text("selected_button")
        elif self.selecting_mode:
            btn_color = self.colors["selected"]
            btn_text = self.gm.settings.get_text("confirm_button")
        else:
            btn_color = self.colors["button_secondary"]
            btn_text = self.gm.settings.get_text("select_button")
            
        pygame.draw.rect(screen, btn_color, self.cameo_select_btn, border_radius=self.s(8))
        pygame.draw.rect(screen, self.colors["text_light"], self.cameo_select_btn, self.s(2), border_radius=self.s(8))
        
        select_font = self.get_font(18, bold=True)
        select_text = select_font.render(btn_text, True, self.colors["text_light"])
        screen.blit(select_text, (self.cameo_select_btn.centerx - select_text.get_width() // 2,
                                self.cameo_select_btn.centery - select_text.get_height() // 2))
        
        hint_font = self.get_font(15)
        if self.show_selection_confirmed:
            hint_text = self.gm.settings.get_text("returning_to_battle")
        elif self.selecting_mode:
            hint_text = self.gm.settings.get_text("confirm_hint")
        else:
            hint_text = self.gm.settings.get_text("use_arrows")
            
        hint = hint_font.render(hint_text, True, self.colors["text_dark"])
        screen.blit(hint, (rect.centerx - hint.get_width() // 2, self.cameo_select_btn.bottom + self.s(15)))
    
    def _draw_skins_section(self, screen, rect):
        """Секция выбора скинов"""
        # Определяем текущий выбранный персонаж/камео
        if self.selected_skin_tab == 0:  # Персонажи
            selected_entity = next((char for char in self.characters if char["selected"]), None)
            entity_name = selected_entity['name'] if selected_entity else "NONE"
            title_base = self.gm.settings.get_text('skin_for')
        else:  # Камео
            selected_entity = next((cameo for cameo in self.cameos if cameo["selected"]), None)
            entity_name = selected_entity['name'] if selected_entity else "NONE" 
            title_base = self.gm.settings.get_text('skin_for')
        
        title_font = self.get_font(26, bold=True)
        if self.show_selection_confirmed:
            title_text = self.gm.settings.get_text("skin_selected")
        elif self.skin_selecting_mode:
            title_text = self.gm.settings.get_text("confirm_skin")
        else:
            title_text = f"{title_base}: {entity_name}"
            
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width() // 2, rect.y + self.s(25)))
        
        # Таб-переключатель персонаж/камео
        tab_font = self.get_font(20, bold=True)
        char_tab_text = tab_font.render(self.gm.settings.get_text("characters_tab"), True, self.colors["text_light"])
        cameo_tab_text = tab_font.render(self.gm.settings.get_text("cameos_tab"), True, self.colors["text_light"])
        
        tab_width = self.s(150)
        tab_height = self.s(40)
        tab_spacing = self.s(20)
        
        total_tabs_width = tab_width * 2 + tab_spacing
        tabs_start_x = rect.centerx - total_tabs_width // 2
        
        # Таб персонажей
        char_tab_rect = pygame.Rect(tabs_start_x, rect.y + self.s(70), tab_width, tab_height)
        char_color = self.colors["button_primary"] if self.selected_skin_tab == 0 else self.colors["header_bg"]
        pygame.draw.rect(screen, char_color, char_tab_rect, border_radius=self.s(8))
        pygame.draw.rect(screen, self.colors["text_light"], char_tab_rect, self.s(2), border_radius=self.s(8))
        
        screen.blit(char_tab_text, (char_tab_rect.centerx - char_tab_text.get_width() // 2,
                          char_tab_rect.centery - char_tab_text.get_height() // 2))
        self.skin_tab_left = char_tab_rect
        
        # Таб камео
        cameo_tab_rect = pygame.Rect(tabs_start_x + tab_width + tab_spacing, rect.y + self.s(70), tab_width, tab_height)
        cameo_color = self.colors["button_secondary"] if self.selected_skin_tab == 1 else self.colors["header_bg"]
        pygame.draw.rect(screen, cameo_color, cameo_tab_rect, border_radius=self.s(8))
        pygame.draw.rect(screen, self.colors["text_light"], cameo_tab_rect, self.s(2), border_radius=self.s(8))
        screen.blit(cameo_tab_text, (cameo_tab_rect.centerx - cameo_tab_text.get_width() // 2,
                           cameo_tab_rect.centery - cameo_tab_text.get_height() // 2))
        self.skin_tab_right = cameo_tab_rect
        
        # Отображение скинов
        if self.current_skins and self.selected_skin_index < len(self.current_skins):
            skin = self.current_skins[self.selected_skin_index]
            card_size = self._get_card_size()
            
            # ВЫБИРАЕМ ПРАВИЛЬНУЮ КАРТОЧКУ
            if self.skin_selecting_mode or self.show_selection_confirmed:
                card = skin["card_special"]
            else:
                card = skin["card_normal"]
                
            if card:  # Убедимся что карточка существует
                card_rect = pygame.Rect(rect.centerx - card_size//2, rect.centery - card_size//2, card_size, card_size)
                screen.blit(card, card_rect)
                
                name_font = self.get_font(22, bold=True)
                name_text = name_font.render(skin["name"], True, self.colors["text_light"])
                screen.blit(name_text, (rect.centerx - name_text.get_width() // 2, card_rect.bottom + self.s(15)))
                
                # Статус разблокировки
                status_font = self.get_font(18)
                status_text = "🔓 РАЗБЛОКИРОВАН" if skin["unlocked"] else "🔒 ЗАБЛОКИРОВАН"
                status_color = self.colors["selected"] if skin["unlocked"] else self.colors["danger"]
                status = status_font.render(status_text, True, status_color)
                screen.blit(status, (rect.centerx - status.get_width() // 2, card_rect.bottom + self.s(40)))
            else:
                # Если карточки нет, показываем заглушку
                error_font = self.get_font(18)
                error_text = error_font.render("Карточка не найдена", True, self.colors["danger"])
                screen.blit(error_text, (rect.centerx - error_text.get_width() // 2, rect.centery - self.s(10)))
        else:
            # Если скинов нет
            error_font = self.get_font(18)
            error_text = error_font.render("Нет доступных скинов", True, self.colors["text_dark"])
            screen.blit(error_text, (rect.centerx - error_text.get_width() // 2, rect.centery - self.s(10)))
        
        # Стрелки навигации
        if self.current_skins and len(self.current_skins) > 1:
            if not self.skin_selecting_mode and not self.show_selection_confirmed:
                arrow_size = self.s(50)
                card_rect_center = rect.centery  # Примерная позиция
                
                self.skin_left_btn = pygame.Rect(rect.centerx - card_size//2 - arrow_size - self.s(15), 
                                               card_rect_center - arrow_size//2, arrow_size, arrow_size)
                self.skin_right_btn = pygame.Rect(rect.centerx + card_size//2 + self.s(15), 
                                                card_rect_center - arrow_size//2, arrow_size, arrow_size)
                
                pygame.draw.rect(screen, self.colors["button_primary"], self.skin_left_btn, border_radius=self.s(10))
                pygame.draw.rect(screen, self.colors["text_light"], self.skin_left_btn, self.s(2), border_radius=self.s(10))
                arrow_font = self.get_font(28, bold=True)
                left_arrow = arrow_font.render("⟨", True, self.colors["text_light"])
                screen.blit(left_arrow, (self.skin_left_btn.centerx - left_arrow.get_width() // 2,
                                    self.skin_left_btn.centery - left_arrow.get_height() // 2))
                
                pygame.draw.rect(screen, self.colors["button_primary"], self.skin_right_btn, border_radius=self.s(10))
                pygame.draw.rect(screen, self.colors["text_light"], self.skin_right_btn, self.s(2), border_radius=self.s(10))
                right_arrow = arrow_font.render("⟩", True, self.colors["text_light"])
                screen.blit(right_arrow, (self.skin_right_btn.centerx - right_arrow.get_width() // 2,
                                        self.skin_right_btn.centery - right_arrow.get_height() // 2))
        
        # Кнопка выбора
        btn_width = min(self.s(180), rect.width * 0.4)
        btn_height = self.s(45)
        self.skin_select_btn = pygame.Rect(rect.centerx - btn_width//2, rect.bottom - self.s(80), btn_width, btn_height)
        
        # Проверяем можно ли выбрать скин
        can_select = (self.current_skins and 
                     self.selected_skin_index < len(self.current_skins) and 
                     self.current_skins[self.selected_skin_index]["unlocked"])
        
        if self.show_selection_confirmed:
            btn_color = self.colors["selected"]
            btn_text = "ВЫБРАНО!"
        elif self.skin_selecting_mode:
            btn_color = self.colors["selected"]
            btn_text = "ПОДТВЕРДИТЬ"
        elif can_select:
            btn_color = self.colors["button_primary"]
            btn_text = "ВЫБРАТЬ"
        else:
            btn_color = (100, 100, 100)  # Серый для заблокированных
            btn_text = "ЗАБЛОКИРОВАНО"
            
        pygame.draw.rect(screen, btn_color, self.skin_select_btn, border_radius=self.s(8))
        pygame.draw.rect(screen, self.colors["text_light"], self.skin_select_btn, self.s(2), border_radius=self.s(8))
        
        select_font = self.get_font(18, bold=True)
        select_text = select_font.render(btn_text, True, self.colors["text_light"])
        screen.blit(select_text, (self.skin_select_btn.centerx - select_text.get_width() // 2,
                                self.skin_select_btn.centery - select_text.get_height() // 2))
        
        hint_font = self.get_font(15)
        if self.show_selection_confirmed:
            hint_text = "Возврат в раздел FIGHT..."
        elif self.skin_selecting_mode:
            hint_text = "Нажмите ENTER или 'Подтвердить' для выбора"
        elif not can_select:
            hint_text = "Этот скин заблокирован. Купите его в магазине!"
        else:
            hint_text = "Используйте A/D, ←→ или кликните на стрелки для просмотра скинов"
            
        hint = hint_font.render(hint_text, True, self.colors["text_dark"])
        screen.blit(hint, (rect.centerx - hint.get_width() // 2, self.skin_select_btn.bottom + self.s(15)))
    
    def _draw_shop_section(self, screen, rect):
        """Секция магазина"""
        title_font = self.get_font(26, bold=True)
        title_text = self.gm.settings.get_text("shop")
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width() // 2, rect.y + self.s(25)))
        
        # Кнопка открытия магазина
        btn_width = self.s(200)
        btn_height = self.s(60)
        self.shop_button = pygame.Rect(
            rect.centerx - btn_width // 2,
            rect.centery - btn_height // 2,
            btn_width,
            btn_height
        )
        
        pygame.draw.rect(screen, self.colors["button_primary"], self.shop_button, border_radius=self.s(12))
        pygame.draw.rect(screen, self.colors["text_light"], self.shop_button, self.s(2), border_radius=self.s(12))
        
        btn_font = self.get_font(20, bold=True)
        btn_text = btn_font.render("ОТКРЫТЬ МАГАЗИН", True, self.colors["text_light"])
        screen.blit(btn_text, (self.shop_button.centerx - btn_text.get_width() // 2,
                         self.shop_button.centery - btn_text.get_height() // 2))
        
        # Подсказка
        hint_font = self.get_font(16)
        hint_text = "Кликните чтобы открыть магазин"
        hint = hint_font.render(hint_text, True, self.colors["text_dark"])
        screen.blit(hint, (rect.centerx - hint.get_width() // 2, self.shop_button.bottom + self.s(20)))
    
    def _draw_settings_section(self, screen, rect):
        """Секция настроек"""
        title_font = self.get_font(26, bold=True)
        title_text = self.gm.settings.get_text("settings")
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width() // 2, rect.y + self.s(25)))
        
        # Кнопка открытия настроек
        btn_width = self.s(200)
        btn_height = self.s(60)
        self.settings_button = pygame.Rect(
            rect.centerx - btn_width // 2,
            rect.centery - btn_height // 2,
            btn_width,
            btn_height
        )
        
        pygame.draw.rect(screen, self.colors["button_secondary"], self.settings_button, border_radius=self.s(12))
        pygame.draw.rect(screen, self.colors["text_light"], self.settings_button, self.s(2), border_radius=self.s(12))
        
        btn_font = self.get_font(20, bold=True)
        btn_text = btn_font.render("ОТКРЫТЬ НАСТРОЙКИ", True, self.colors["text_light"])
        screen.blit(btn_text, (self.settings_button.centerx - btn_text.get_width() // 2,
                         self.settings_button.centery - btn_text.get_height() // 2))
    
    def _draw_exit_section(self, screen, rect):
        """Секция выхода"""
        title_font = self.get_font(26, bold=True)
        title_text = self.gm.settings.get_text("exit_game")
        title = title_font.render(title_text, True, self.colors["danger"])
        screen.blit(title, (rect.centerx - title.get_width() // 2, rect.y + self.s(35)))
        
        warning_font = self.get_font(20)
        warning_text = self.gm.settings.get_text("exit_confirmation")
        warning = warning_font.render(warning_text, True, self.colors["text_light"])
        screen.blit(warning, (rect.centerx - warning.get_width() // 2, rect.centery - self.s(25)))
        
        btn_width = min(self.s(220), rect.width * 0.5)
        btn_height = self.s(55)
        self.exit_button = pygame.Rect(rect.centerx - btn_width//2, rect.centery + self.s(15), btn_width, btn_height)
        pygame.draw.rect(screen, self.colors["danger"], self.exit_button, border_radius=self.s(10))
        pygame.draw.rect(screen, self.colors["text_light"], self.exit_button, self.s(3), border_radius=self.s(10))
        
        btn_font = self.get_font(20, bold=True)
        btn_text = btn_font.render(self.gm.settings.get_text("exit"), True, self.colors["text_light"])
        screen.blit(btn_text, (self.exit_button.centerx - btn_text.get_width() // 2,
                             self.exit_button.centery - btn_text.get_height() // 2))
        
        hint_font = self.get_font(16)
        hint_text = self.gm.settings.get_text("exit_hint")
        hint = hint_font.render(hint_text, True, self.colors["text_dark"])
        screen.blit(hint, (rect.centerx - hint.get_width() // 2, self.exit_button.bottom + self.s(20)))
    
    def _draw_bottom_bar(self, screen):
        """Нижняя панель - УДАЛЕНА навигация, оставим только копирайт"""
        bar_height = self.s(30)
        bar_rect = pygame.Rect(0, screen.get_height() - bar_height, screen.get_width(), bar_height)
        pygame.draw.rect(screen, self.colors["header_bg"], bar_rect)
        
        copyright_font = self.get_font(12)
        copyright_text = copyright_font.render("© 2024 Brawl Fighters", True, self.colors["text_dark"])
        screen.blit(copyright_text, (screen.get_width() - copyright_text.get_width() - self.s(25), 
                                   bar_rect.centery - copyright_text.get_height()//2))
    
    def _draw_unlock_animation(self, screen):
        """Анимация разблокировки скина"""
        if not self.unlock_animation_skin:
            return
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.unlock_animation_time
        progress = min(elapsed / 2000, 1.0)  # 2 секунды анимации
        
        # Создаем полупрозрачный черный фон
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(150 * progress)))
        screen.blit(overlay, (0, 0))
        
        # Определяем размер карточки с анимации
        base_size = self.s(200)
        animated_size = int(base_size * (1 + progress * 0.5))  # Увеличивается на 50%
        
        # Центрируем карточку
        card_x = screen.get_width() // 2 - animated_size // 2
        card_y = screen.get_height() // 2 - animated_size // 2
        
        # Рисуем увеличенную карточку
        card = pygame.Surface((animated_size, animated_size), pygame.SRCALPHA)
        card.fill((255, 255, 255, int(200 * progress)))
        pygame.draw.rect(card, (100, 255, 100, int(255 * progress)), 
                        (0, 0, animated_size, animated_size), self.s(5))
        
        # Добавляем свечение
        glow = pygame.Surface((animated_size + 20, animated_size + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow, (100, 255, 100, int(100 * progress)), 
                        (0, 0, animated_size + 20, animated_size + 20), 
                        border_radius=self.s(10))
        screen.blit(glow, (card_x - 10, card_y - 10))
        
        screen.blit(card, (card_x, card_y))
        
        # Текст "РАЗБЛОКИРОВАНО!"
        text_size = int(self.s(40) * (1 + progress * 0.3))
        text_font = pygame.font.SysFont("arial", text_size, bold=True)
        text = text_font.render("РАЗБЛОКИРОВАНО!", True, (100, 255, 100))
        
        text_x = screen.get_width() // 2 - text.get_width() // 2
        text_y = card_y - text.get_height() - self.s(20)
        screen.blit(text, (text_x, text_y))
    
    def _draw_locked_skin_message(self, screen):
        """Сообщение о заблокированном скине"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.locked_skin_message_time
        progress = min(elapsed / 1500, 1.0)
        
        if progress >= 1.0:
            return
        
        # Создаем полупрозрачный фон
        overlay = pygame.Surface((screen.get_width(), self.s(100)), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(200 * progress)))
        
        overlay_y = screen.get_height() // 2 - self.s(50)
        screen.blit(overlay, (0, overlay_y))
        
        # Текст сообщения
        text_font = self.get_font(24, bold=True)
        text = text_font.render("СКИН ЗАБЛОКИРОВАН!", True, self.colors["danger"])
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 
                         overlay_y + self.s(20)))
        
        # Подсказка
        hint_font = self.get_font(18)
        hint = hint_font.render("Купите скин в магазине", True, self.colors["text_light"])
        screen.blit(hint, (screen.get_width() // 2 - hint.get_width() // 2, 
                          overlay_y + self.s(60)))