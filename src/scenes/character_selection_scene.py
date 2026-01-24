# src/scenes/character_selection_scene.py
import pygame
import os
import sys
from src.managers.game_manager import BaseScene
from src.managers.save_manager import SaveManager
import random

def resource_path(relative_path):
    """Получает правильный путь к ресурсам для работы как из .py, так и из .exe"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class CharacterSelectionScene(BaseScene):
    def __init__(self, gm, game_mode, is_training=False):
        super().__init__(gm)
        self.game_mode = game_mode  # "vs_bot", "vs_friend", "training"
        self.is_training = is_training
        
        # Цветовая схема
        self.colors = {
            "background": (20, 20, 40),
            "header_bg": (30, 30, 50),
            "button_primary": (255, 100, 100),
            "button_secondary": (100, 150, 255),
            "text_light": (255, 255, 255),
            "text_dark": (200, 200, 200),
            "accent": (255, 215, 0),
            "player1_color": (100, 200, 255),  # Синий для P1
            "player2_color": (255, 100, 100),  # Красный для P2
            "selected": (100, 255, 100),
        }
        
        # Состояние выбора
        self.selection_phase = 0  # 0 - выбор персонажей, 1 - выбор камео, 2 - выбор карты
        self.current_player = 0  # 0 - P1, 1 - P2 (для режима vs_friend)
        
        # Персонажи
        self.characters = [
            {"name": "1x1x1x1", "display_name": "1x1x1x1", "map": "soul_beach"},
            {"name": "chara", "display_name": "Chara", "map": "hall_of_judgement"},
            {"name": "steve", "display_name": "Steve", "map": "deep_caves"},
            {"name": "nameless", "display_name": "Nameless", "map": "everlost"}
        ]
        
        # Камео
        self.cameos = [
            {"name": "c00lk1d", "display_name": "Cool Kid", "map": "soul_beach"},
            {"name": "papyrus", "display_name": "Papyrus", "map": "hall_of_judgement"}
        ]
        
        # Карты (инициализируем без переводов, обновим в on_enter)
        self.maps = [
            {"id": "by_characters", "name": "По персонажам", "description": "Карта выбирается по выбранным персонажам"},
            {"id": "random", "name": "Random", "description": "Случайная карта из всех доступных"},
            {"id": "soul_beach", "name": "Soul Beach", "description": "Песчаный пляж с древними руинами"},
            {"id": "hall_of_judgement", "name": "Hall of Judgement", "description": "Заброшенный зал суда"},
            {"id": "deep_caves", "name": "Deep Caves", "description": "Темные пещеры с кристаллами"},
            {"id": "everlost", "name": "Everlost", "description": "Забытое измерение"}
        ]
        
        # Выборы игроков
        self.selections = {
            "p1": {
                "character": None,
                "cameo": None,
                "character_index": 0,
                "cameo_index": 0
            },
            "p2": {
                "character": None,
                "cameo": None,
                "character_index": 0,
                "cameo_index": 0
            }
        }
        
        # Текущие индексы
        self.current_character_index = 0
        self.current_cameo_index = 0
        self.current_map_index = 0
        
        # Подтверждения
        self.character_confirmed = False
        self.cameo_confirmed = False
        self.map_confirmed = False
        
        # Кнопки для мыши
        self.character_left_btn = None
        self.character_right_btn = None
        self.character_confirm_btn = None
        self.cameo_left_btn = None
        self.cameo_right_btn = None
        self.cameo_confirm_btn = None
        self.map_left_btn = None
        self.map_right_btn = None
        self.map_confirm_btn = None
        self.back_btn = None
        
        # Загружаем карточки
        self.character_cards = {}
        self.cameo_cards = {}
        self._load_cards()
        
        # Для режима VS BOT автоматически выбираем случайных для P2
        if self.game_mode == "vs_bot":
            self._select_random_for_bot()
        # Для тренировки P1 vs P1 (тренировка на себе)
        elif self.is_training:
            self.selections["p2"]["character"] = self.selections["p1"]["character"]
            self.selections["p2"]["cameo"] = self.selections["p1"]["cameo"]
        
        # Начинаем с выбора карты для VS BOT и тренировки
        if self.game_mode in ["vs_bot", "training"]:
            self.selection_phase = 2  # Пропускаем выбор, сразу к карте
            print(f"⏩ Пропускаем выбор для {self.game_mode}, сразу к карте")
    
    def _load_cards(self):
        """Загружает карточки персонажей и камео"""
        card_size = self._get_card_size()
        
        # Загружаем карточки персонажей
        for char in self.characters:
            try:
                card_path = resource_path(os.path.join("Sprites", "cards", f"{char['name']}_default_normal.jpg"))
                if os.path.exists(card_path):
                    card = pygame.image.load(card_path).convert_alpha()
                    card = pygame.transform.scale(card, (card_size, card_size))
                    self.character_cards[char["name"]] = card
                else:
                    self.character_cards[char["name"]] = self._create_placeholder_card(char["display_name"], card_size, False)
            except:
                self.character_cards[char["name"]] = self._create_placeholder_card(char["display_name"], card_size, False)
        
        # Загружаем карточки камео
        for cameo in self.cameos:
            try:
                card_path = resource_path(os.path.join("Sprites", "cards", f"{cameo['name']}_default_normal.jpg"))
                if os.path.exists(card_path):
                    card = pygame.image.load(card_path).convert_alpha()
                    card = pygame.transform.scale(card, (card_size, card_size))
                    self.cameo_cards[cameo["name"]] = card
                else:
                    self.cameo_cards[cameo["name"]] = self._create_placeholder_card(cameo["display_name"], card_size, False)
            except:
                self.cameo_cards[cameo["name"]] = self._create_placeholder_card(cameo["display_name"], card_size, False)
    
    def _get_card_size(self):
        """Определяет размер карточки"""
        return self.s(280)
    
    def _create_placeholder_card(self, name, size, is_special=False):
        """Создает заглушку для карточки"""
        card = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if is_special:
            card.fill((180, 150, 50, 255))
        else:
            card.fill((80, 80, 150, 255))
        
        # Добавляем текст
        font = pygame.font.SysFont("arial", max(20, size // 10))
        text = font.render(name, True, (255, 255, 255))
        card.blit(text, (size//2 - text.get_width()//2, size//2 - text.get_height()//2))
        
        return card
    
    def on_enter(self):
        """Инициализация при входе в сцену"""
        print(f"🎮 Режим игры: {self.game_mode}")
        print(f"🏋️ Тренировка: {self.is_training}")
        
        # Обновляем переводы карт
        self._update_map_translations()
        
        # Инициализируем выбор P1 из сохранений
        self._init_player1_from_save()
        
        # Устанавливаем начальный индекс для P1
        if self.selections["p1"]["character"]:
            char_name = self.selections["p1"]["character"]
            for i, char in enumerate(self.characters):
                if char["name"] == char_name:
                    self.current_character_index = i
                    break
        
        if self.selections["p1"]["cameo"]:
            cameo_name = self.selections["p1"]["cameo"]
            for i, cameo in enumerate(self.cameos):
                if cameo["name"] == cameo_name:
                    self.current_cameo_index = i
                    break
        
        print(f"📊 Текущая фаза: {self.selection_phase}")
        print(f"🎮 Выборы: P1={self.selections['p1']}, P2={self.selections['p2']}")
    
    def _update_map_translations(self):
        """Обновляет переводы для карт"""
        if hasattr(self.gm, 'settings') and self.gm.settings:
            # Обновляем названия и описания карт из локализации
            for map_data in self.maps:
                map_id = map_data["id"]
                
                # Получаем название
                name_key = f"map_{map_id}"
                translated_name = self.gm.settings.get_text(name_key)
                if translated_name and translated_name != name_key:  # Проверяем что перевод существует
                    map_data["name"] = translated_name
                
                # Получаем описание
                desc_key = f"map_description_{map_id}"
                translated_desc = self.gm.settings.get_text(desc_key)
                if translated_desc and translated_desc != desc_key:  # Проверяем что перевод существует
                    map_data["description"] = translated_desc
            
            print("✅ Переводы карт обновлены")
        else:
            print("⚠️ Настройки не найдены, используем дефолтные названия карт")
    
    def _init_player1_from_save(self):
        """Инициализирует выбор P1 из сохранений"""
        if hasattr(self.gm, 'save_manager') and self.gm.save_manager:
            # Берем последнего выбранного персонажа и камео
            last_char = self.gm.save_manager.get_last_character()
            last_cameo = self.gm.save_manager.get_last_cameo()
            
            # Устанавливаем для P1
            self.selections["p1"]["character"] = last_char
            self.selections["p1"]["cameo"] = last_cameo
            
            print(f"📂 P1 из сохранений: {last_char} + {last_cameo}")
        else:
            # По умолчанию
            self.selections["p1"]["character"] = "1x1x1x1"
            self.selections["p1"]["cameo"] = "c00lk1d"
    
    def _select_random_for_bot(self):
        """Выбирает случайные значения для бота (VS BOT)"""
        # Сначала инициализируем P1 если не инициализирован
        if not self.selections["p1"]["character"]:
            self.selections["p1"]["character"] = "1x1x1x1"
        if not self.selections["p1"]["cameo"]:
            self.selections["p1"]["cameo"] = "c00lk1d"
        
        # Случайный персонаж для бота (исключая выбранного P1)
        available_chars = [c for c in self.characters if c["name"] != self.selections["p1"]["character"]]
        if available_chars:
            bot_char = random.choice(available_chars)
            self.selections["p2"]["character"] = bot_char["name"]
            print(f"🤖 Бот выбрал персонажа: {bot_char['name']}")
        else:
            # Если только один персонаж, берем его
            bot_char = random.choice(self.characters)
            self.selections["p2"]["character"] = bot_char["name"]
        
        # Случайное камео для бота (исключая выбранное P1)
        available_cameos = [c for c in self.cameos if c["name"] != self.selections["p1"]["cameo"]]
        if available_cameos:
            bot_cameo = random.choice(available_cameos)
            self.selections["p2"]["cameo"] = bot_cameo["name"]
            print(f"🤖 Бот выбрал камео: {bot_cameo['name']}")
        else:
            # Если только одно камео, берем его
            bot_cameo = random.choice(self.cameos)
            self.selections["p2"]["cameo"] = bot_cameo["name"]
        
        print(f"🤖 Бот выбрал: {self.selections['p2']['character']} + {self.selections['p2']['cameo']}")
    
    def _calculate_map_by_characters(self):
        """
        Определяет карту на основе выбранных персонажей и камео
        по стандартным правилам
        """
        # Считаем количество персонажей для каждой карты
        map_counts = {
            "soul_beach": 0,
            "hall_of_judgement": 0,
            "deep_caves": 0,
            "everlost": 0
        }
        
        # Проверяем всех выбранных персонажей и камео
        for player in ["p1", "p2"]:
            if self.selections[player]["character"]:
                char_name = self.selections[player]["character"]
                char = next((c for c in self.characters if c["name"] == char_name), None)
                if char and char["map"] in map_counts:
                    map_counts[char["map"]] += 1
            
            if self.selections[player]["cameo"]:
                cameo_name = self.selections[player]["cameo"]
                cameo = next((c for c in self.cameos if c["name"] == cameo_name), None)
                if cameo and cameo["map"] in map_counts:
                    map_counts[cameo["map"]] += 1
        
        print(f"📊 Подсчет карт (стандартные правила): {map_counts}")
        
        # Находим максимальное количество
        max_count = max(map_counts.values())
        
        # Находим все карты с максимальным количеством
        winning_maps = [map_id for map_id, count in map_counts.items() if count == max_count]
        
        # Если есть явный победитель (только одна карта)
        if len(winning_maps) == 1:
            selected_map = winning_maps[0]
            print(f"🎯 Выбрана карта: {selected_map} (явный победитель)")
        else:
            # Выбираем случайную из карт с максимальным количеством
            selected_map = random.choice(winning_maps)
            print(f"🎲 Выбрана карта: {selected_map} (случайно из {winning_maps} - стандартные правила)")
        
        return selected_map
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Возвращаемся в меню
                    self.gm.set_scene("menu")
                    return
                
                if self.selection_phase == 0:  # Выбор персонажей
                    self._handle_character_selection(event, mouse_pos)
                elif self.selection_phase == 1:  # Выбор камео
                    self._handle_cameo_selection(event, mouse_pos)
                elif self.selection_phase == 2:  # Выбор карты
                    self._handle_map_selection(event, mouse_pos)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._handle_mouse_click(mouse_pos)
    
    def _handle_character_selection(self, event, mouse_pos):
        """Обработка выбора персонажа"""
        player_key = "p1" if self.current_player == 0 else "p2"
        
        if event.key in [pygame.K_a, pygame.K_LEFT]:
            self.current_character_index = (self.current_character_index - 1) % len(self.characters)
            self.selections[player_key]["character_index"] = self.current_character_index
        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
            self.current_character_index = (self.current_character_index + 1) % len(self.characters)
            self.selections[player_key]["character_index"] = self.current_character_index
        elif event.key == pygame.K_RETURN:
            self._confirm_character_selection()
    
    def _handle_cameo_selection(self, event, mouse_pos):
        """Обработка выбора камео"""
        player_key = "p1" if self.current_player == 0 else "p2"
        
        if event.key in [pygame.K_a, pygame.K_LEFT]:
            self.current_cameo_index = (self.current_cameo_index - 1) % len(self.cameos)
            self.selections[player_key]["cameo_index"] = self.current_cameo_index
        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
            self.current_cameo_index = (self.current_cameo_index + 1) % len(self.cameos)
            self.selections[player_key]["cameo_index"] = self.current_cameo_index
        elif event.key == pygame.K_RETURN:
            self._confirm_cameo_selection()
    
    def _handle_map_selection(self, event, mouse_pos):
        """Обработка выбора карты"""
        if event.key in [pygame.K_a, pygame.K_LEFT]:
            self.current_map_index = (self.current_map_index - 1) % len(self.maps)
        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
            self.current_map_index = (self.current_map_index + 1) % len(self.maps)
        elif event.key == pygame.K_RETURN:
            self._confirm_map_selection()
    
    def _handle_mouse_click(self, mouse_pos):
        """Обработка кликов мыши"""
        if self.back_btn and self.back_btn.collidepoint(mouse_pos):
            self.gm.set_scene("menu")
            return
        
        if self.selection_phase == 0:  # Персонажи
            if self.character_left_btn and self.character_left_btn.collidepoint(mouse_pos):
                self._handle_character_selection(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT), mouse_pos)
            elif self.character_right_btn and self.character_right_btn.collidepoint(mouse_pos):
                self._handle_character_selection(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT), mouse_pos)
            elif self.character_confirm_btn and self.character_confirm_btn.collidepoint(mouse_pos):
                self._confirm_character_selection()
        
        elif self.selection_phase == 1:  # Камео
            if self.cameo_left_btn and self.cameo_left_btn.collidepoint(mouse_pos):
                self._handle_cameo_selection(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT), mouse_pos)
            elif self.cameo_right_btn and self.cameo_right_btn.collidepoint(mouse_pos):
                self._handle_cameo_selection(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT), mouse_pos)
            elif self.cameo_confirm_btn and self.cameo_confirm_btn.collidepoint(mouse_pos):
                self._confirm_cameo_selection()
        
        elif self.selection_phase == 2:  # Карта
            if self.map_left_btn and self.map_left_btn.collidepoint(mouse_pos):
                self._handle_map_selection(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT), mouse_pos)
            elif self.map_right_btn and self.map_right_btn.collidepoint(mouse_pos):
                self._handle_map_selection(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT), mouse_pos)
            elif self.map_confirm_btn and self.map_confirm_btn.collidepoint(mouse_pos):
                self._confirm_map_selection()
    
    def _confirm_character_selection(self):
        """Подтверждение выбора персонажа"""
        player_key = "p1" if self.current_player == 0 else "p2"
        selected_char = self.characters[self.current_character_index]
        
        self.selections[player_key]["character"] = selected_char["name"]
        print(f"🎯 {player_key} выбрал персонажа: {selected_char['name']}")
        
        # Только для режима против друга переключаем игроков
        if self.game_mode == "vs_friend" and self.current_player == 0:
            self.current_player = 1
            self.current_character_index = 0
            print("🔄 Переключение на выбор персонажа для P2")
        else:
            # Для VS BOT и тренировки переходим к камео
            self.selection_phase = 1
            self.current_cameo_index = 0
            print("➡️ Переход к выбору камео")
    
    def _confirm_cameo_selection(self):
        """Подтверждение выбора камео"""
        player_key = "p1" if self.current_player == 0 else "p2"
        selected_cameo = self.cameos[self.current_cameo_index]
        
        self.selections[player_key]["cameo"] = selected_cameo["name"]
        print(f"🎯 {player_key} выбрал камео: {selected_cameo['name']}")
        
        # Только для режима против друга переключаем игроков
        if self.game_mode == "vs_friend" and self.current_player == 0:
            self.current_player = 1
            self.current_cameo_index = 0
            self.selection_phase = 0  # Возвращаемся к выбору персонажа для P2
            print("🔄 Переключение на выбор персонажа для P2")
        else:
            # Переходим к выбору карты
            self.selection_phase = 2
            
            # Для тренировки автоматически выбираем карту по персонажам
            if self.is_training:
                selected_map = self._calculate_map_by_characters()
                print(f"🏞️ Автоматически выбрана карта для тренировки: {selected_map}")
                self._confirm_map_selection()
            else:
                print("➡️ Переход к выбору карты")
    
    def _confirm_map_selection(self):
        """Подтверждение выбора карты"""
        selected_map = self.maps[self.current_map_index]
        
        # Определяем какую карту выбрать
        if selected_map["id"] == "by_characters":
            # Стандартные правила (по персонажам)
            selected_map_id = self._calculate_map_by_characters()
            print(f"🗺️ Выбор карты по персонажам: {selected_map_id}")
        elif selected_map["id"] == "random":
            # Случайный выбор из всех конкретных карт (кроме "by_characters" и "random")
            available_maps = [m for m in self.maps if m["id"] not in ["by_characters", "random"]]
            selected_map_data = random.choice(available_maps)
            selected_map_id = selected_map_data["id"]
            print(f"🎲 Случайный выбор карты: {selected_map_id}")
        else:
            # Конкретная карта выбрана напрямую
            selected_map_id = selected_map["id"]
            print(f"🗺️ Выбрана конкретная карта: {selected_map_id}")
        
        print(f"🎯 Финальная карта: {selected_map_id}")
        
        # Сохраняем карту
        if hasattr(self.gm, 'save_manager') and self.gm.save_manager:
            self.gm.save_manager.set_map(selected_map_id)
        
        # Переходим к созданию игровой сессии
        self._create_game_session(selected_map_id)
    
    def _create_game_session(self, map_id):
        """Создает игровую сессию с выбранными параметрами"""
        print(f"🎮 Создание игровой сессии...")
        print(f"  Режим: {self.game_mode}")
        print(f"  Карта: {map_id}")
        print(f"  P1: {self.selections['p1']['character']} + {self.selections['p1']['cameo']}")
        print(f"  P2: {self.selections['p2']['character']} + {self.selections['p2']['cameo']}")
        
        # Создаем персонажей
        from src.core.character import Character
        from src.scenes.intro_scene import IntroSequenceScene
        from src.scenes.battle_scene import BattleScene
        from src.scenes.victory_scene import VictoryScene
        
        # Игрок 1
        player_char = Character(self.selections['p1']['character'], self.gm.resources)
        player_cameo = Character(self.selections['p1']['cameo'], self.gm.resources)
        
        # Игрок 2 (бот или второй игрок)
        enemy_char = Character(self.selections['p2']['character'], self.gm.resources)
        enemy_cameo = Character(self.selections['p2']['cameo'], self.gm.resources)
        
        # Определяем режим для передачи в сцены
        game_mode_data = {
            "id": self.game_mode,
            "name": self.game_mode.upper(),
            "map": map_id,
            "is_training": self.is_training
        }
        
        # Создаем сцены с передачей параметров
        self.gm.register_scene("intro", IntroSequenceScene(
            self.gm, player_char, player_cameo, enemy_char, enemy_cameo, game_mode_data
        ))
        self.gm.register_scene("battle", BattleScene(
            self.gm, player_char, enemy_char, game_mode_data
        ))
        self.gm.register_scene("victory", VictoryScene(
            self.gm, None, game_mode_data
        ))
        
        # Переходим к загрузке
        from src.scenes.loading_scene import LoadingScene
        loading_scene = LoadingScene(self.gm, "intro", skip_logo=True)
        self.gm.register_scene("game_loading", loading_scene)
        self.gm.set_scene("game_loading")
    
    def update(self, dt):
        """Обновление сцены"""
        pass
    
    def draw(self, screen):
        """Отрисовка сцены"""
        screen.fill(self.colors["background"])
        
        # Рисуем заголовок
        self._draw_header(screen)
        
        # Рисуем контент в зависимости от фазы выбора
        if self.selection_phase == 0:
            self._draw_character_selection(screen)
        elif self.selection_phase == 1:
            self._draw_cameo_selection(screen)
        elif self.selection_phase == 2:
            self._draw_map_selection(screen)
        
        # Рисуем кнопку назад
        self._draw_back_button(screen)
    
    def _draw_header(self, screen):
        """Отрисовка заголовка"""
        header_height = self.s(80)
        header_rect = pygame.Rect(0, 0, screen.get_width(), header_height)
        
        # Градиентный фон хедера
        for i in range(header_height):
            color = (30 + i//3, 30 + i//3, 50 + i//2)
            pygame.draw.line(screen, color, (0, i), (screen.get_width(), i))
        
        # Заголовок в зависимости от фазы
        title_font = self.get_font(32, bold=True)
        
        if self.selection_phase == 0:
            player_text = "P1" if self.current_player == 0 else "P2"
            title = title_font.render(f"ВЫБОР ПЕРСОНАЖА - {player_text}", True, self.colors["accent"])
        elif self.selection_phase == 1:
            player_text = "P1" if self.current_player == 0 else "P2"
            title = title_font.render(f"ВЫБОР КАМЕО - {player_text}", True, self.colors["accent"])
        elif self.selection_phase == 2:
            title = title_font.render("ВЫБОР КАРТЫ", True, self.colors["accent"])
        
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, self.s(20)))
        
        # Информация о режиме
        mode_font = self.get_font(18)
        mode_text = f"Режим: {self.game_mode.upper()}"
        if self.is_training:
            mode_text += " (Тренировка)"
        mode = mode_font.render(mode_text, True, self.colors["text_dark"])
        screen.blit(mode, (self.s(20), self.s(50)))
        
        # Показываем выбранных игроков
        if self.selections["p1"]["character"]:
            p1_text = f"P1: {self.selections['p1']['character']}"
            if self.selections["p1"]["cameo"]:
                p1_text += f" + {self.selections['p1']['cameo']}"
            p1 = mode_font.render(p1_text, True, self.colors["player1_color"])
            screen.blit(p1, (screen.get_width() - p1.get_width() - self.s(20), self.s(50)))
    
    def _draw_character_selection(self, screen):
        """Отрисовка выбора персонажа"""
        player_key = "p1" if self.current_player == 0 else "p2"
        player_color = self.colors["player1_color"] if self.current_player == 0 else self.colors["player2_color"]
        
        # Текущий выбранный персонаж
        char_index = self.selections[player_key]["character_index"]
        selected_char = self.characters[char_index]
        
        # Карточка персонажа
        card_size = self._get_card_size()
        card_x = screen.get_width() // 2 - card_size // 2
        card_y = screen.get_height() // 2 - card_size // 2
        
        if selected_char["name"] in self.character_cards:
            card = self.character_cards[selected_char["name"]]
            screen.blit(card, (card_x, card_y))
        
        # Имя персонажа
        name_font = self.get_font(28, bold=True)
        name_text = name_font.render(selected_char["display_name"], True, player_color)
        screen.blit(name_text, (screen.get_width()//2 - name_text.get_width()//2, card_y + card_size + self.s(20)))
        
        # Карта персонажа
        map_font = self.get_font(18)
        map_text = map_font.render(f"Карта: {selected_char['map']}", True, self.colors["text_dark"])
        screen.blit(map_text, (screen.get_width()//2 - map_text.get_width()//2, card_y + card_size + self.s(50)))
        
        # Стрелки навигации
        arrow_size = self.s(50)
        self.character_left_btn = pygame.Rect(card_x - arrow_size - self.s(20), card_y + card_size//2 - arrow_size//2, arrow_size, arrow_size)
        self.character_right_btn = pygame.Rect(card_x + card_size + self.s(20), card_y + card_size//2 - arrow_size//2, arrow_size, arrow_size)
        
        pygame.draw.rect(screen, player_color, self.character_left_btn, border_radius=self.s(10))
        pygame.draw.rect(screen, self.colors["text_light"], self.character_left_btn, self.s(2), border_radius=self.s(10))
        
        left_font = self.get_font(24, bold=True)
        left_text = left_font.render("←", True, self.colors["text_light"])
        screen.blit(left_text, (self.character_left_btn.centerx - left_text.get_width()//2, 
                              self.character_left_btn.centery - left_text.get_height()//2))
        
        pygame.draw.rect(screen, player_color, self.character_right_btn, border_radius=self.s(10))
        pygame.draw.rect(screen, self.colors["text_light"], self.character_right_btn, self.s(2), border_radius=self.s(10))
        
        right_text = left_font.render("→", True, self.colors["text_light"])
        screen.blit(right_text, (self.character_right_btn.centerx - right_text.get_width()//2, 
                               self.character_right_btn.centery - right_text.get_height()//2))
        
        # Кнопка подтверждения
        btn_width = self.s(200)
        btn_height = self.s(50)
        self.character_confirm_btn = pygame.Rect(screen.get_width()//2 - btn_width//2, card_y + card_size + self.s(100), btn_width, btn_height)
        
        pygame.draw.rect(screen, self.colors["selected"], self.character_confirm_btn, border_radius=self.s(10))
        pygame.draw.rect(screen, self.colors["text_light"], self.character_confirm_btn, self.s(2), border_radius=self.s(10))
        
        confirm_font = self.get_font(20, bold=True)
        confirm_text = confirm_font.render("ПОДТВЕРДИТЬ", True, self.colors["text_light"])
        screen.blit(confirm_text, (self.character_confirm_btn.centerx - confirm_text.get_width()//2,
                                 self.character_confirm_btn.centery - confirm_text.get_height()//2))
        
        # Подсказка
        hint_font = self.get_font(16)
        hint_text = "Используйте ←→ для навигации, ENTER для подтверждения"
        hint = hint_font.render(hint_text, True, self.colors["text_dark"])
        screen.blit(hint, (screen.get_width()//2 - hint.get_width()//2, self.character_confirm_btn.bottom + self.s(20)))
    
    def _draw_cameo_selection(self, screen):
        """Отрисовка выбора камео"""
        player_key = "p1" if self.current_player == 0 else "p2"
        player_color = self.colors["player1_color"] if self.current_player == 0 else self.colors["player2_color"]
        
        # Текущий выбранный камео
        cameo_index = self.selections[player_key]["cameo_index"]
        selected_cameo = self.cameos[cameo_index]
        
        # Карточка камео
        card_size = self._get_card_size()
        card_x = screen.get_width() // 2 - card_size // 2
        card_y = screen.get_height() // 2 - card_size // 2
        
        if selected_cameo["name"] in self.cameo_cards:
            card = self.cameo_cards[selected_cameo["name"]]
            screen.blit(card, (card_x, card_y))
        
        # Имя камео
        name_font = self.get_font(28, bold=True)
        name_text = name_font.render(selected_cameo["display_name"], True, player_color)
        screen.blit(name_text, (screen.get_width()//2 - name_text.get_width()//2, card_y + card_size + self.s(20)))
        
        # Карта камео
        map_font = self.get_font(18)
        map_text = map_font.render(f"Карта: {selected_cameo['map']}", True, self.colors["text_dark"])
        screen.blit(map_text, (screen.get_width()//2 - map_text.get_width()//2, card_y + card_size + self.s(50)))
        
        # Стрелки навигации
        arrow_size = self.s(50)
        self.cameo_left_btn = pygame.Rect(card_x - arrow_size - self.s(20), card_y + card_size//2 - arrow_size//2, arrow_size, arrow_size)
        self.cameo_right_btn = pygame.Rect(card_x + card_size + self.s(20), card_y + card_size//2 - arrow_size//2, arrow_size, arrow_size)
        
        pygame.draw.rect(screen, player_color, self.cameo_left_btn, border_radius=self.s(10))
        pygame.draw.rect(screen, self.colors["text_light"], self.cameo_left_btn, self.s(2), border_radius=self.s(10))
        
        left_font = self.get_font(24, bold=True)
        left_text = left_font.render("←", True, self.colors["text_light"])
        screen.blit(left_text, (self.cameo_left_btn.centerx - left_text.get_width()//2, 
                              self.cameo_left_btn.centery - left_text.get_height()//2))
        
        pygame.draw.rect(screen, player_color, self.cameo_right_btn, border_radius=self.s(10))
        pygame.draw.rect(screen, self.colors["text_light"], self.cameo_right_btn, self.s(2), border_radius=self.s(10))
        
        right_text = left_font.render("→", True, self.colors["text_light"])
        screen.blit(right_text, (self.cameo_right_btn.centerx - right_text.get_width()//2, 
                               self.cameo_right_btn.centery - right_text.get_height()//2))
        
        # Кнопка подтверждения
        btn_width = self.s(200)
        btn_height = self.s(50)
        self.cameo_confirm_btn = pygame.Rect(screen.get_width()//2 - btn_width//2, card_y + card_size + self.s(100), btn_width, btn_height)
        
        pygame.draw.rect(screen, self.colors["selected"], self.cameo_confirm_btn, border_radius=self.s(10))
        pygame.draw.rect(screen, self.colors["text_light"], self.cameo_confirm_btn, self.s(2), border_radius=self.s(10))
        
        confirm_font = self.get_font(20, bold=True)
        confirm_text = confirm_font.render("ПОДТВЕРДИТЬ", True, self.colors["text_light"])
        screen.blit(confirm_text, (self.cameo_confirm_btn.centerx - confirm_text.get_width()//2,
                                 self.cameo_confirm_btn.centery - confirm_text.get_height()//2))
        
        # Подсказка
        hint_font = self.get_font(16)
        hint_text = "Используйте ←→ для навигации, ENTER для подтверждения"
        hint = hint_font.render(hint_text, True, self.colors["text_dark"])
        screen.blit(hint, (screen.get_width()//2 - hint.get_width()//2, self.cameo_confirm_btn.bottom + self.s(20)))
    
    def _draw_map_selection(self, screen):
        """Отрисовка выбора карты"""
        selected_map = self.maps[self.current_map_index]
        
        # Прямоугольник для карты
        map_width = self.s(400)
        map_height = self.s(250)
        map_x = screen.get_width() // 2 - map_width // 2
        map_y = screen.get_height() // 2 - map_height // 2
        
        # Фон карты
        pygame.draw.rect(screen, (40, 40, 60), (map_x, map_y, map_width, map_height), border_radius=self.s(10))
        pygame.draw.rect(screen, self.colors["accent"], (map_x, map_y, map_width, map_height), self.s(3), border_radius=self.s(10))
        
        # Название карты
        name_font = self.get_font(32, bold=True)
        name_text = name_font.render(selected_map["name"], True, self.colors["text_light"])
        screen.blit(name_text, (screen.get_width()//2 - name_text.get_width()//2, map_y + self.s(20)))
        
        # Описание карты
        desc_font = self.get_font(18)
        # Разбиваем длинное описание на несколько строк
        description = selected_map["description"]
        max_chars_per_line = 40  # Максимальное количество символов в строке
        if len(description) > max_chars_per_line:
            # Простой перенос строки
            words = description.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line) + len(word) + 1 <= max_chars_per_line:
                    current_line += (" " if current_line else "") + word
                else:
                    lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # Рисуем каждую строку
            for i, line in enumerate(lines):
                desc_text = desc_font.render(line, True, self.colors["text_dark"])
                screen.blit(desc_text, (screen.get_width()//2 - desc_text.get_width()//2, 
                                       map_y + self.s(70) + i * desc_font.get_height()))
        else:
            desc_text = desc_font.render(description, True, self.colors["text_dark"])
            screen.blit(desc_text, (screen.get_width()//2 - desc_text.get_width()//2, map_y + self.s(70)))
        
        # Информация о выбранных персонажах
        info_font = self.get_font(16)
        info_y = map_y + self.s(120)
        
        # P1
        p1_char = self.selections["p1"]["character"] or "Не выбран"
        p1_cameo = self.selections["p1"]["cameo"] or "Не выбрано"
        p1_text = info_font.render(f"P1: {p1_char} + {p1_cameo}", True, self.colors["player1_color"])
        screen.blit(p1_text, (screen.get_width()//2 - p1_text.get_width()//2, info_y))
        
        # P2
        p2_char = self.selections["p2"]["character"] or "Не выбран"
        p2_cameo = self.selections["p2"]["cameo"] or "Не выбрано"
        p2_text = info_font.render(f"P2: {p2_char} + {p2_cameo}", True, self.colors["player2_color"])
        screen.blit(p2_text, (screen.get_width()//2 - p2_text.get_width()//2, info_y + self.s(30)))
        
        # Стрелки навигации
        arrow_size = self.s(50)
        self.map_left_btn = pygame.Rect(map_x - arrow_size - self.s(20), map_y + map_height//2 - arrow_size//2, arrow_size, arrow_size)
        self.map_right_btn = pygame.Rect(map_x + map_width + self.s(20), map_y + map_height//2 - arrow_size//2, arrow_size, arrow_size)
        
        pygame.draw.rect(screen, self.colors["button_primary"], self.map_left_btn, border_radius=self.s(10))
        pygame.draw.rect(screen, self.colors["text_light"], self.map_left_btn, self.s(2), border_radius=self.s(10))
        
        left_font = self.get_font(24, bold=True)
        left_text = left_font.render("←", True, self.colors["text_light"])
        screen.blit(left_text, (self.map_left_btn.centerx - left_text.get_width()//2, 
                              self.map_left_btn.centery - left_text.get_height()//2))
        
        pygame.draw.rect(screen, self.colors["button_primary"], self.map_right_btn, border_radius=self.s(10))
        pygame.draw.rect(screen, self.colors["text_light"], self.map_right_btn, self.s(2), border_radius=self.s(10))
        
        right_text = left_font.render("→", True, self.colors["text_light"])
        screen.blit(right_text, (self.map_right_btn.centerx - right_text.get_width()//2, 
                               self.map_right_btn.centery - right_text.get_height()//2))
        
        # Кнопка подтверждения
        btn_width = self.s(200)
        btn_height = self.s(50)
        self.map_confirm_btn = pygame.Rect(screen.get_width()//2 - btn_width//2, map_y + map_height + self.s(50), btn_width, btn_height)
        
        pygame.draw.rect(screen, self.colors["selected"], self.map_confirm_btn, border_radius=self.s(10))
        pygame.draw.rect(screen, self.colors["text_light"], self.map_confirm_btn, self.s(2), border_radius=self.s(10))
        
        confirm_font = self.get_font(20, bold=True)
        confirm_text = confirm_font.render("НАЧАТЬ БОЙ", True, self.colors["text_light"])
        screen.blit(confirm_text, (self.map_confirm_btn.centerx - confirm_text.get_width()//2,
                                 self.map_confirm_btn.centery - confirm_text.get_height()//2))
        
        # Подсказка
        hint_font = self.get_font(16)
        if selected_map["id"] == "by_characters":
            hint_text = "Карта будет выбрана на основе выбранных персонажей (стандартные правила)"
        elif selected_map["id"] == "random":
            hint_text = "Карта будет выбрана СЛУЧАЙНО из всех доступных карт"
        else:
            hint_text = "Используйте ←→ для навигации, ENTER для начала боя"
        
        hint = hint_font.render(hint_text, True, self.colors["text_dark"])
        screen.blit(hint, (screen.get_width()//2 - hint.get_width()//2, self.map_confirm_btn.bottom + self.s(20)))
    
    def _draw_back_button(self, screen):
        """Отрисовка кнопки назад"""
        btn_width = self.s(120)
        btn_height = self.s(40)
        self.back_btn = pygame.Rect(self.s(20), screen.get_height() - btn_height - self.s(20), btn_width, btn_height)
        
        pygame.draw.rect(screen, (100, 100, 100), self.back_btn, border_radius=self.s(8))
        pygame.draw.rect(screen, self.colors["text_light"], self.back_btn, self.s(2), border_radius=self.s(8))
        
        back_font = self.get_font(18)
        back_text = back_font.render("НАЗАД", True, self.colors["text_light"])
        screen.blit(back_text, (self.back_btn.centerx - back_text.get_width()//2,
                              self.back_btn.centery - back_text.get_height()//2))