# src/scenes/menu_scene.py
import pygame
import os
from src.managers.game_manager import BaseScene
from src.managers.save_manager import SaveManager
from src.managers.skin_manager import SkinManager

class MenuScene(BaseScene):
    def __init__(self, gm):
        super().__init__(gm)
        
        # Добавляем менеджер сохранений
        self.save_manager = SaveManager()
        self.save_manager.load_save()
        
        # Добавляем менеджер скинов
        self.skin_manager = SkinManager()
        self.save_manager = SaveManager()
        self.save_manager.load_save()

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
            "selected": (100, 255, 100)
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
                "name": "Chara", 
                "card_normal": None,
                "card_special": None,
                "description": "",
                "selected": False,
                "skin": "default"
            },
            {
                "name": "Steve",
                "card_normal": None,
                "card_special": None,
                "description": "",
                "selected": False,
                "skin": "default"
            }
        ]
        
        # Камео с карточками
        self.selected_cameo = 0
        self.cameos = [
            {
                "name": "C00lK1D",
                "card_normal": None,
                "card_special": None,
                "description": "",
                "selected": False,
                "skin": "default"
            },
            {
                "name": "Papyrus",
                "card_normal": None,
                "card_special": None,
                "description": "",
                "selected": False,
                "skin": "default"
            },
            {
                "name": "Larry",
                "card_normal": None,
                "card_special": None,
                "description": "",
                "selected": False,
                "skin": "default"
            }
        ]
        
        # Кнопки для мыши
        self.tab_buttons = []
        self.char_left_btn = None
        self.char_right_btn = None
        self.char_select_btn = None
        self.cameo_left_btn = None
        self.cameo_right_btn = None
        self.cameo_select_btn = None
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
        
        # Загружаем тексты и карточки
        self._refresh_texts()
        self.music_started = False
        
    def on_enter(self):
        """Загружаем карточки и восстанавливаем последний выбор"""
        self._load_all_cards()
        self._play_background_music()
        self._restore_last_selection()

    def _restore_last_selection(self):
        """Восстанавливает последний выбор персонажей из сохранения"""
        last_char = self.save_manager.get_last_character()
        last_cameo = self.save_manager.get_last_cameo()
        
        print(f"🔍 Восстановление: персонаж='{last_char}', камео='{last_cameo}'")
        
        # Находим индексы последних выбранных персонажей
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
        
        print(f"🎯 Начинаем сохранение персонажа: {selected_char['name']}")
        
        # Сохраняем выбор
        self.save_manager.save_game(
            character=selected_char["name"],  # Сохраняем именно имя
            character_skin=selected_char["skin"]
        )
        
        print(f"✅ Выбран и сохранен персонаж: {selected_char['name']}")
        # ИСПРАВЛЕНО: используем правильное имя метода
        self.selection_confirmed_time = pygame.time.get_ticks()
        self.show_selection_confirmed = True
        self.selecting_mode = False

    def _select_cameo(self):
        """Выбор камео - можно выбирать одного и того же повторно"""
        selected_cameo = self.cameos[self.selected_cameo]
        selected_cameo["selected"] = True
        
        print(f"🎯 Начинаем сохранение камео: {selected_cameo['name']}")
        
        # Сохраняем выбор
        self.save_manager.save_game(
            cameo=selected_cameo["name"],  # Сохраняем именно имя
            cameo_skin=selected_cameo["skin"]
        )
        
        print(f"✅ Выбрано и сохранено камео: {selected_cameo['name']}")
        # ИСПРАВЛЕНО: используем правильное имя метода
        self.selection_confirmed_time = pygame.time.get_ticks()
        self.show_selection_confirmed = True
        self.selecting_mode = False

    def _load_all_cards(self):
        """Загружаем все карточки с учетом скинов"""
        card_size = self._get_card_size()
        
        for character in self.characters:
            # Загружаем карточки с учетом скина
            skin = character["skin"]
            character["card_normal"] = self._load_card_image(
                f"{character['name'].lower()}_{skin}_normal.jpg", False, card_size
            )
            character["card_special"] = self._load_card_image(
                f"{character['name'].lower()}_{skin}_special.jpg", True, card_size
            )
            
        for cameo in self.cameos:
            # Загружаем карточки с учетом скина
            skin = cameo["skin"]
            cameo["card_normal"] = self._load_card_image(
                f"{cameo['name'].lower()}_{skin}_normal.jpg", False, card_size
            )
            cameo["card_special"] = self._load_card_image(
                f"{cameo['name'].lower()}_{skin}_special.jpg", True, card_size
            )
    
    def _get_card_size(self):
        """Определяем размер карточки в зависимости от разрешения"""
        base_size = 280
        
        if self.gm.settings.scale_factor > 1.5:
            return int(base_size * 1.3)
        elif self.gm.settings.scale_factor > 1.2:
            return int(base_size * 1.15)
        return base_size

    def _load_card_image(self, filename, is_special, card_size):
        """Загрузка карточки с указанным размером"""
        card_path = os.path.join("Sprites", "cards", filename)
        
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
        """Воспроизводит фоновую музыку меню если она еще не играет"""
        if self.music_started:
            return
            
        try:
            music_path = os.path.join("Sounds", "Music", "back_music.mp3")
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
        
        # Обновляем описания персонажей
        for char in self.characters:
            char["description"] = self.gm.settings.get_text(f"character_{char['name'].lower()}_desc")
        
        for cameo in self.cameos:
            cameo["description"] = self.gm.settings.get_text(f"cameo_{cameo['name'].lower()}_desc")
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if not self.selecting_mode and not self.show_selection_confirmed:
                    if event.key == pygame.K_LEFT:
                        self.current_section = (self.current_section - 1) % len(self.sections)
                    elif event.key == pygame.K_RIGHT:
                        self.current_section = (self.current_section + 1) % len(self.sections)
                    elif event.key == pygame.K_RETURN:
                        current_section_name = self.sections[self.current_section]
                        if current_section_name == self.gm.settings.get_text("settings"):
                            self._open_settings()
                        elif current_section_name == self.sections[0]:  # БОЙ
                            self._start_battle()
                        elif current_section_name == self.sections[3]:  # МАГАЗИН
                            self._open_shop()
                        elif current_section_name == self.sections[5]:  # ВЫХОД
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
                
                elif self.selecting_mode and not self.show_selection_confirmed:
                    if event.key == pygame.K_RETURN:
                        self._confirm_selection()
                    elif event.key == pygame.K_ESCAPE:
                        self.selecting_mode = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._handle_mouse_click(mouse_pos)
    
    def _handle_mouse_click(self, mouse_pos):
        """Обработка кликов мыши"""
        print(f"🖱️ Клик в позиции: {mouse_pos}")
        
        # Клики по вкладкам
        for i, tab_rect in enumerate(self.tab_buttons):
            if tab_rect.collidepoint(mouse_pos):
                print(f"📌 Клик по вкладке: {self.sections[i]}")
                self.current_section = i
                # ... остальной код ...
        
        if self.show_selection_confirmed:
            return
            
        if not self.selecting_mode:
            # Навигация в секциях CHARACTERS и CAMEOS
            if self.current_section == 1:  # CHARACTERS
                if self.char_left_btn and self.char_left_btn.collidepoint(mouse_pos):
                    print("⬅️ Клик по левой стрелке персонажа")
                    self.selected_character = (self.selected_character - 1) % len(self.characters)
                elif self.char_right_btn and self.char_right_btn.collidepoint(mouse_pos):
                    print("➡️ Клик по правой стрелке персонажа")
                    self.selected_character = (self.selected_character + 1) % len(self.characters)
                elif self.char_select_btn and self.char_select_btn.collidepoint(mouse_pos):
                    print("🎯 Клик по кнопке выбора персонажа")
                    self.selecting_mode = True
                    
            elif self.current_section == 2:  # CAMEOS
                if self.cameo_left_btn and self.cameo_left_btn.collidepoint(mouse_pos):
                    print("⬅️ Клик по левой стрелке камео")
                    self.selected_cameo = (self.selected_cameo - 1) % len(self.cameos)
                elif self.cameo_right_btn and self.cameo_right_btn.collidepoint(mouse_pos):
                    print("➡️ Клик по правой стрелке камео")
                    self.selected_cameo = (self.selected_cameo + 1) % len(self.cameos)
                elif self.cameo_select_btn and self.cameo_select_btn.collidepoint(mouse_pos):
                    print("🎯 Клик по кнопке выбора камео")
                    self.selecting_mode = True
                    
        else:
            # Подтверждение выбора в режиме selecting_mode
            if self.current_section == 1 and self.char_select_btn and self.char_select_btn.collidepoint(mouse_pos):
                print("✅ Подтверждение выбора персонажа")
                self._select_character()
            elif self.current_section == 2 and self.cameo_select_btn and self.cameo_select_btn.collidepoint(mouse_pos):
                print("✅ Подтверждение выбора камео")
                self._select_cameo()
    
    def _confirm_selection(self):
        """Подтверждение выбора персонажа или камео"""
        if self.current_section == 1:  # CHARACTERS
            for char in self.characters:
                char["selected"] = False
            self.characters[self.selected_character]["selected"] = True
            print(f"✅ Выбран персонаж: {self.characters[self.selected_character]['name']}")
            
        elif self.current_section == 2:  # CAMEOS
            for cameo in self.cameos:
                cameo["selected"] = False
            self.cameos[self.selected_cameo]["selected"] = True
            print(f"✅ Выбрано камео: {self.cameos[self.selected_cameo]['name']}")
        
        self.selection_confirmed_time = pygame.time.get_ticks()
        self.show_selection_confirmed = True
        self.selecting_mode = False
    
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
        print(f"🎮 Запуск боя: {char_name} + {cameo_name}")
        self._create_game_scenes(char_name, cameo_name)
        
        from src.scenes.loading_scene import LoadingScene
        loading_scene = LoadingScene(self.gm, "intro")
        self.gm.register_scene("game_loading", loading_scene)
        self.gm.set_scene("game_loading")
    
    def _open_settings(self):
        self.gm.set_scene("settings")

    def _open_shop(self):
        print("Магазин пока не реализован")
    
    def _exit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def _create_game_scenes(self, char_name, cameo_name):
        from src.core.character import Character
        from src.scenes.intro_scene import IntroSequenceScene
        from src.scenes.battle_scene import BattleScene
        from src.scenes.victory_scene import VictoryScene
        
        player_char = Character(char_name, self.gm.resources)
        enemy_char = Character("fighter_right", self.gm.resources)
        player_cameo = Character(cameo_name, self.gm.resources)
        enemy_cameo = Character("cameo_right", self.gm.resources)
        
        self.gm.register_scene("intro", IntroSequenceScene(self.gm, player_char, player_cameo, enemy_char, enemy_cameo))
        self.gm.register_scene("battle", BattleScene(self.gm, player_char, enemy_char))
        self.gm.register_scene("victory", VictoryScene(self.gm, None))
    
    def update(self, dt):
        if self.show_selection_confirmed:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_confirmed_time > 1500:
                self.show_selection_confirmed = False
                # Автоматически возвращаемся на вкладку FIGHT после подтверждения выбора
                self.current_section = 0
    
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
            self._draw_shop_section(screen, content_rect)
        elif self.current_section == 4:
            self._draw_settings_section(screen, content_rect)
        elif self.current_section == 5:
            self._draw_exit_section(screen, content_rect)
        
        self._draw_bottom_bar(screen)
    
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
        
        # Левая группа: FIGHT, CHARACTERS, CAMEOS
        left_tabs = self.sections[:3]
        # Правая группа: SHOP, SETTINGS, EXIT
        right_tabs = self.sections[3:]
        
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
            
            pygame.draw.rect(screen, color, tab_rect, border_radius=self.s(12))  # Увеличил радиус
            pygame.draw.rect(screen, self.colors["text_light"], tab_rect, self.s(2), border_radius=self.s(12))
            
            # ⚡ УВЕЛИЧИЛ ШРИФТ
            max_font_size = self.f(18)  # Было 16 -> 18
            min_font_size = self.f(12)  # Было 11 -> 12
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
            tab_index = i + 3  # Индекс в общем списке
            tab_rect = pygame.Rect(right_x, right_start_y + i * (tab_height + tab_spacing), tab_width, tab_height)
            self.tab_buttons.append(tab_rect)
            
            if section == self.sections[5]:  # ВЫХОД
                color = self.colors["danger"] if tab_index == self.current_section else (150, 80, 80)
            else:
                color = self.colors["button_secondary"] if tab_index == self.current_section else self.colors["header_bg"]
            
            pygame.draw.rect(screen, color, tab_rect, border_radius=self.s(12))  # Увеличил радиус
            pygame.draw.rect(screen, self.colors["text_light"], tab_rect, self.s(2), border_radius=self.s(12))
            
            # ⚡ УВЕЛИЧИЛ ШРИФТ
            max_font_size = self.f(18)  # Было 16 -> 18
            min_font_size = self.f(12)  # Было 11 -> 12
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
        """Секция FIGHT - основной экран"""
        # Показываем выбранные персонаж и камео
        selected_char = next((char for char in self.characters if char["selected"]), None)
        selected_cameo = next((cameo for cameo in self.cameos if cameo["selected"]), None)
        
        # 🎨 ДОБАВЛЯЕМ АРТЫ ПО ЦЕНТРУ (перекрывающиеся)
        art_size = self.s(350)  # Размер артов - МЕНЯЙТЕ ЗДЕСЬ
        
        # Арт персонажа (слева, немного перекрывает камео)
        if selected_char:
            char_art = self._load_art_image(f"{selected_char['name'].lower()}.png", art_size)
            if char_art:
                # 🎨 КООРДИНАТЫ ПЕРСОНАЖА - МЕНЯЙТЕ ЗДЕСЬ
                char_x = rect.centerx - art_size + self.s(40)  # Сдвиг влево от центра
                char_y = rect.centery - art_size // 2  # Центр по вертикали
                screen.blit(char_art, (char_x, char_y))
        
        # Арт камео (справа, перекрывает персонажа)
        if selected_cameo:
            cameo_art = self._load_art_image(f"{selected_cameo['name'].lower()}.png", art_size)
            if cameo_art:
                # 🎨 КООРДИНАТЫ КАМЕО - МЕНЯЙТЕ ЗДЕСЬ
                cameo_x = rect.centerx - self.s(40)  # Сдвиг вправо от центра
                cameo_y = rect.centery - art_size // 2  # Центр по вертикали
                screen.blit(cameo_art, (cameo_x, cameo_y))
        
        # Кнопка выбора режима (нерабочая) - внизу по центру
        # ⚡ УВЕЛИЧИЛ КНОПКУ РЕЖИМА
        mode_btn_width = self.s(220)  # Было 200 -> 220
        mode_btn_height = self.s(60)  # Было 50 -> 60
        self.mode_button = pygame.Rect(
            rect.centerx - mode_btn_width // 2,
            rect.bottom - mode_btn_height - self.s(30),
            mode_btn_width,
            mode_btn_height
        )
        
        pygame.draw.rect(screen, self.colors["button_secondary"], self.mode_button, border_radius=self.s(12))
        pygame.draw.rect(screen, self.colors["text_light"], self.mode_button, self.s(2), border_radius=self.s(12))
        
        mode_font = self.get_font(20, bold=True)  # Увеличил шрифт
        mode_text = mode_font.render("VS BOT", True, self.colors["text_light"])
        screen.blit(mode_text, (self.mode_button.centerx - mode_text.get_width() // 2,
                              self.mode_button.centery - mode_text.get_height() // 2))
        
        # Кнопка начала боя - внизу справа
        # ⚡ УВЕЛИЧИЛ КНОПКУ FIGHT
        btn_width = self.s(200)  # Было 180 -> 200
        btn_height = self.s(60)  # Было 50 -> 60
        self.battle_button = pygame.Rect(
            rect.right - btn_width - self.s(50),
            rect.bottom - btn_height - self.s(30),
            btn_width,
            btn_height
        )
        battle_enabled = selected_char and selected_cameo
        
        if battle_enabled:
            pygame.draw.rect(screen, self.colors["button_primary"], self.battle_button, border_radius=self.s(12))
            pygame.draw.rect(screen, self.colors["accent"], self.battle_button, self.s(3), border_radius=self.s(12))
        else:
            pygame.draw.rect(screen, (100, 100, 100), self.battle_button, border_radius=self.s(12))
            pygame.draw.rect(screen, (150, 150, 150), self.battle_button, self.s(3), border_radius=self.s(12))
        
        btn_font = self.get_font(22, bold=True)  # Увеличил шрифт
        btn_text = btn_font.render("FIGHT!", True, 
                                 self.colors["text_light"] if battle_enabled else self.colors["text_dark"])
        screen.blit(btn_text, (self.battle_button.centerx - btn_text.get_width() // 2,
                             self.battle_button.centery - btn_text.get_height() // 2))

    def _load_art_image(self, filename, art_size):
        """Загрузка арта с указанным размером"""
        art_path = os.path.join("Sprites", "arts", filename)
        
        try:
            if os.path.exists(art_path):
                art = pygame.image.load(art_path).convert_alpha()
                # Масштабируем сохраняя пропорции
                original_width, original_height = art.get_size()
                scale_factor = min(art_size / original_width, art_size / original_height)
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                art = pygame.transform.scale(art, (new_width, new_height))
                return art
            else:
                return self._create_placeholder_art(filename, art_size)
        except Exception as e:
            print(f"❌ Ошибка загрузки арта {art_path}: {e}")
            return self._create_placeholder_art(filename, art_size)

    def _create_placeholder_art(self, filename, art_size):
        """Создание заглушки для арта"""
        art = pygame.Surface((art_size, art_size), pygame.SRCALPHA)
        art.fill((80, 80, 150, 255))
        
        border = max(3, art_size // 40)
        pygame.draw.rect(art, (255, 255, 255), (border, border, art_size-2*border, art_size-2*border), border)
        
        placeholder_font = pygame.font.SysFont("arial", max(20, art_size//15), bold=True)
        placeholder_text = placeholder_font.render("АРТ", True, (255, 255, 255))
        art.blit(placeholder_text, (art_size//2 - placeholder_text.get_width()//2, art_size//3))
        
        name_font = pygame.font.SysFont("arial", max(14, art_size//20))
        name_text = name_font.render(filename, True, (200, 200, 200))
        art.blit(name_text, (art_size//2 - name_text.get_width()//2, art_size//2))
        
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
        card_size = self._get_card_size()
        
        # 🎯 УПРОЩАЕМ: special карточка ТОЛЬКО во время выбора
        if self.selecting_mode or self.show_selection_confirmed:
            card = character["card_special"]
        else:
            card = character["card_normal"]  # Всегда normal, кроме момента выбора
            
        card_rect = pygame.Rect(rect.centerx - card_size//2, rect.centery - card_size//2, card_size, card_size)
        screen.blit(card, card_rect)
        
        name_font = self.get_font(22, bold=True)
        # 🎯 УПРОЩАЕМ: имя всегда одного цвета (не зависит от выбора)
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
        
        # 🎯 УПРОЩАЕМ: кнопка всегда "ВЫБРАТЬ" и всегда активна
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
        
        # 🎯 УПРОЩАЕМ: special карточка ТОЛЬКО во время выбора
        if self.selecting_mode or self.show_selection_confirmed:
            card = cameo["card_special"]
        else:
            card = cameo["card_normal"]  # Всегда normal, кроме момента выбора
            
        card_rect = pygame.Rect(rect.centerx - card_size//2, rect.centery - card_size//2, card_size, card_size)
        screen.blit(card, card_rect)
        
        name_font = self.get_font(20, bold=True)
        # 🎯 УПРОЩАЕМ: имя всегда одного цвета (не зависит от выбора)
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
        
        # 🎯 УПРОЩАЕМ: кнопка всегда "ВЫБРАТЬ" и всегда активна
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
    
    def _draw_shop_section(self, screen, rect):
        """Секция магазина"""
        title_font = self.get_font(26, bold=True)
        title_text = self.gm.settings.get_text("shop")
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width() // 2, rect.y + self.s(25)))
        
        placeholder_font = self.get_font(22)
        placeholder_text = self.gm.settings.get_text("shop_coming_soon")
        placeholder = placeholder_font.render(placeholder_text, True, self.colors["text_dark"])
        screen.blit(placeholder, (rect.centerx - placeholder.get_width() // 2, rect.centery - self.s(15)))
        
        offer_font = self.get_font(18)
        offer_text = self.gm.settings.get_text("earn_coins_hint")
        offer = offer_font.render(offer_text, True, (255, 200, 100))
        screen.blit(offer, (rect.centerx - offer.get_width() // 2, rect.centery + self.s(25)))
    
    def _draw_settings_section(self, screen, rect):
        """Секция настроек"""
        title_font = self.get_font(26, bold=True)
        title_text = self.gm.settings.get_text("settings")
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width() // 2, rect.y + self.s(25)))
        
        settings = [
            self.gm.settings.get_text("sound_effects"),
            self.gm.settings.get_text("music_tracks"), 
            self.gm.settings.get_text("screen_mode"),
            self.gm.settings.get_text("interface_language")
        ]
        
        setting_font = self.get_font(20)
        for i, setting in enumerate(settings):
            text = setting_font.render(setting, True, self.colors["text_light"])
            screen.blit(text, (rect.x + self.s(40), rect.y + self.s(70) + i * self.s(50)))
    
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
        bar_height = self.s(30)  # Уменьшил высоту
        bar_rect = pygame.Rect(0, screen.get_height() - bar_height, screen.get_width(), bar_height)
        pygame.draw.rect(screen, self.colors["header_bg"], bar_rect)
        
        copyright_font = self.get_font(12)
        copyright_text = copyright_font.render("© 2024 Brawl Fighters", True, self.colors["text_dark"])
        screen.blit(copyright_text, (screen.get_width() - copyright_text.get_width() - self.s(25), 
                                   bar_rect.centery - copyright_text.get_height()//2))