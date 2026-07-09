# src/scenes/menu_scene.py
import pygame
import os
import sys
from src.managers.game_manager import BaseScene
from src.managers.save_manager import SaveManager
from src.managers.skin_manager import SkinManager
from src.core.animations import VideoAnimation, resource_path
import random

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
            "training": (180, 100, 255)
        }
        
        # Данные игрока из сохранения
        self.player_data = {
            "coins": self.save_manager.get_coins(),
            "trophies": self.save_manager.get_trophies()
        }
        
        # Персонажи с карточками (данные, карточки загружены в LoadingScene)
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
                "name": "chara",
                "card_normal": None,
                "card_special": None,
                "description": "",
                "selected": False,
                "skin": "default"
            },
            {
                "name": "steve",
                "card_normal": None,
                "card_special": None,
                "description": "",
                "selected": False,
                "skin": "default"
            }
        ]
        
        # Камео
        self.selected_cameo = 0
        self.cameos = [
            {
                "name": "c00lk1d",
                "description": "",
                "selected": False,
                "skin": "default",
                "card_normal": None,
                "card_special": None
            },
            {
                "name": "papyrus",
                "description": "",
                "selected": False,
                "skin": "default",
                "card_normal": None,
                "card_special": None
            },
        ]

        # Данные скинов - теперь берутся из gm.assets, но структура сохраняется
        self.character_skins = self.gm.assets.get("character_skins", {})
        self.cameo_skins = self.gm.assets.get("cameo_skins", {})

        # Состояние выбора скинов
        self.selected_skin_tab = 0
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
        
        # Режимы игры
        self.game_modes = [
            {"id": "vs_bot", "name": "VS BOT"},
            {"id": "training", "name": "ТРЕНИРОВКА"},
            {"id": "vs_friend", "name": "ПРОТИВ ДРУГА"}
        ]
        self.selected_game_mode = 0
        self.mode_selecting = False
        
        # Загружаем тексты
        self._refresh_texts()
        
        # Переменные для анимации
        self.unlock_animation = False
        self.unlock_animation_time = 0
        self.unlock_animation_skin = None
        
        # Сообщение о блокировке скина
        self.locked_skin_message = False
        self.locked_skin_message_time = 0
        
        # Кэш для анимаций артов - из gm.assets
        self.art_animations = self.gm.assets.get("art_animations", {})
        self.playing_animations = []
        
        # Иконки из gm.assets
        self.icons = self.gm.assets.get("icons", {})

    def on_enter(self):
        """Инициализация при входе в сцену"""
        # Обновляем ресурсы из gm.assets (они загружены после создания объекта)
        self.character_skins = self.gm.assets.get("character_skins", {})
        self.cameo_skins = self.gm.assets.get("cameo_skins", {})
        self.icons = self.gm.assets.get("icons", {})
        self.art_animations = self.gm.assets.get("art_animations", {})

        # Применяем загруженные карточки к объектам
        self._apply_cards_from_assets()
        
        # Восстанавливаем последний выбор
        self._restore_last_selection()
        
        # Обновляем данные игрока из сохранений
        self.save_manager.load_save()
        self.player_data["coins"] = self.save_manager.get_coins()
        self.player_data["trophies"] = self.save_manager.get_trophies()
        
        if not pygame.mixer.music.get_busy():
            music_path = self.gm.assets.get("music_path")
            if music_path and os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.gm.settings.current_settings["music_volume"])
                pygame.mixer.music.play(-1)
                print("🎵 Музыка запущена")

        last_mode_id = self.save_manager.get_last_game_mode()
        mode_found = False
        for i, mode in enumerate(self.game_modes):
            if mode["id"] == last_mode_id:
                self.selected_game_mode = i
                mode_found = True
                break
        if not mode_found:
            self.selected_game_mode = 0
        
        # Обновляем статус разблокировки скинов из сохранений
        for char_name, skins in self.character_skins.items():
            for skin_id in skins.keys():
                if skin_id != "default":
                    is_unlocked = self.save_manager.is_character_skin_unlocked(char_name, skin_id)
                    self.character_skins[char_name][skin_id]["unlocked"] = is_unlocked
        for cameo_name, skins in self.cameo_skins.items():
            for skin_id in skins.keys():
                if skin_id != "default":
                    is_unlocked = self.save_manager.is_cameo_skin_unlocked(cameo_name, skin_id)
                    self.cameo_skins[cameo_name][skin_id]["unlocked"] = is_unlocked

    def _apply_cards_from_assets(self):
        """Применяет загруженные карточки к объектам персонажей и камео."""
        character_cards = self.gm.assets.get("character_cards", {})
        cameo_cards = self.gm.assets.get("cameo_cards", {})
        
        for char in self.characters:
            char_name = char["name"].lower()
            if char_name in character_cards:
                skin_data = character_cards[char_name].get("default", {})
                char["card_normal"] = skin_data.get("normal")
                char["card_special"] = skin_data.get("special")
        
        for cameo in self.cameos:
            cameo_name = cameo["name"].lower()
            if cameo_name in cameo_cards:
                skin_data = cameo_cards[cameo_name].get("default", {})
                cameo["card_normal"] = skin_data.get("normal")
                cameo["card_special"] = skin_data.get("special")

    def _restore_last_selection(self):
        last_char = self.save_manager.get_last_character()
        last_cameo = self.save_manager.get_last_cameo()
        
        char_found = False
        for i, char in enumerate(self.characters):
            if char["name"].lower() == last_char.lower():
                self.selected_character = i
                char["selected"] = True
                char["skin"] = self.save_manager.get_character_skin()
                char_found = True
                break
        if not char_found:
            self.selected_character = 0
            self.characters[0]["selected"] = True
        
        cameo_found = False
        for i, cameo in enumerate(self.cameos):
            if cameo["name"].lower() == last_cameo.lower():
                self.selected_cameo = i
                cameo["selected"] = True
                cameo["skin"] = self.save_manager.get_cameo_skin()
                cameo_found = True
                break
        if not cameo_found:
            self.selected_cameo = 0
            self.cameos[0]["selected"] = True

    def _select_character(self):
        selected_char = self.characters[self.selected_character]
        selected_char["selected"] = True
        for char in self.characters:
            if char != self.characters[self.selected_character]:
                char["selected"] = False
        self.save_manager.save_game(
            character=selected_char["name"],
            character_skin=selected_char["skin"]
        )
        self.selection_confirmed_time = pygame.time.get_ticks()
        self.show_selection_confirmed = True
        self.selecting_mode = False

    def _select_cameo(self):
        selected_cameo = self.cameos[self.selected_cameo]
        selected_cameo["selected"] = True
        for char in self.cameos:
            if char != self.cameos[self.selected_cameo]:
                char["selected"] = False
        self.save_manager.save_game(
            cameo=selected_cameo["name"],
            cameo_skin=selected_cameo["skin"]
        )
        self.selection_confirmed_time = pygame.time.get_ticks()
        self.show_selection_confirmed = True
        self.selecting_mode = False

    def _refresh_current_skins(self):
        self.current_skins = []
        if self.selected_skin_tab == 0:
            selected_char = next((char for char in self.characters if char["selected"]), None)
            if selected_char:
                char_key = selected_char['name'].lower().strip()
                if char_key in self.character_skins:
                    for skin_id, skin_data in self.character_skins[char_key].items():
                        self.current_skins.append({
                            "id": skin_id,
                            "name": skin_data.get("name", skin_id),
                            "unlocked": skin_data.get("unlocked", False),
                            "card_normal": skin_data.get("card_normal"),
                            "card_special": skin_data.get("card_special")
                        })
        else:
            selected_cameo = next((cameo for cameo in self.cameos if cameo["selected"]), None)
            if selected_cameo:
                cameo_key = selected_cameo['name'].lower().strip()
                if cameo_key in self.cameo_skins:
                    for skin_id, skin_data in self.cameo_skins[cameo_key].items():
                        self.current_skins.append({
                            "id": skin_id,
                            "name": skin_data.get("name", skin_id),
                            "unlocked": skin_data.get("unlocked", False),
                            "card_normal": skin_data.get("card_normal"),
                            "card_special": skin_data.get("card_special")
                        })
        
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
                    break
            else:
                self.selected_skin_index = 0

    def _select_skin(self):
        if not self.current_skins or self.selected_skin_index >= len(self.current_skins):
            return
        skin = self.current_skins[self.selected_skin_index]
        if not skin["unlocked"]:
            self.locked_skin_message = True
            self.locked_skin_message_time = pygame.time.get_ticks()
            return
        if self.selected_skin_tab == 0:
            selected_char = next((char for char in self.characters if char["selected"]), None)
            if selected_char:
                selected_char["skin"] = skin["id"]
                self.save_manager.save_game(character_skin=skin["id"])
                selected_char["card_normal"] = skin.get("card_normal")
                selected_char["card_special"] = skin.get("card_special")
        else:
            selected_cameo = next((cameo for cameo in self.cameos if cameo["selected"]), None)
            if selected_cameo:
                selected_cameo["skin"] = skin["id"]
                self.save_manager.save_game(cameo_skin=skin["id"])
                selected_cameo["card_normal"] = skin.get("card_normal")
                selected_cameo["card_special"] = skin.get("card_special")
        self.selection_confirmed_time = pygame.time.get_ticks()
        self.show_selection_confirmed = True
        self.skin_selecting_mode = False

    def _select_game_mode(self):
        selected_mode = self.game_modes[self.selected_game_mode]
        self.save_manager.save_game(game_mode=selected_mode["id"])
        self.selection_confirmed_time = pygame.time.get_ticks()
        self.show_selection_confirmed = True
        self.mode_selecting = False

    def _start_battle(self):
        selected_char = next((char for char in self.characters if char["selected"]), None)
        selected_cameo = next((cameo for cameo in self.cameos if cameo["selected"]), None)
        if not selected_char or not selected_cameo:
            return
        char_name = selected_char["name"]
        cameo_name = selected_cameo["name"]
        game_mode = self.game_modes[self.selected_game_mode]
        if game_mode["id"] == "training":
            self._create_game_scenes(char_name, cameo_name, game_mode)
            from src.scenes.loading_scene import LoadingScene
            loading_scene = LoadingScene(self.gm, "intro")
            self.gm.register_scene("game_loading", loading_scene)
            self.gm.set_scene("game_loading")
        else:
            from src.scenes.character_selection_scene import CharacterSelectionScene
            character_selection = CharacterSelectionScene(self.gm, game_mode["id"], is_training=False)
            self.gm.register_scene("character_selection", character_selection)
            self.gm.set_scene("character_selection")

    def _open_settings(self):
        self.gm.set_scene("settings")

    def _open_shop(self):
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
        game_mode_data = {
            "id": game_mode["id"],
            "name": game_mode["name"],
            "map": "random",
            "is_training": game_mode["id"] == "training"
        }
        self.gm.register_scene("intro", IntroSequenceScene(
            self.gm, player_char, player_cameo, enemy_char, enemy_cameo, game_mode_data
        ))
        self.gm.register_scene("battle", BattleScene(
            self.gm, player_char, enemy_char, game_mode_data
        ))
        self.gm.register_scene("victory", VictoryScene(
            self.gm, None, game_mode_data
        ))

    def on_language_change(self):
        self._refresh_texts()
    
    def _refresh_texts(self):
        if not self.gm.settings:
            return
        self.sections = self.gm.settings.get_text("menu_sections")
        if len(self.sections) == 6:
            self.sections.insert(3, "SKINS")
        for char in self.characters:
            char["description"] = self.gm.settings.get_text(f"character_{char['name'].lower()}_desc")
        for cameo in self.cameos:
            cameo["description"] = self.gm.settings.get_text(f"cameo_{cameo['name'].lower()}_desc")
        self.game_modes = [
            {"id": "vs_bot", "name": self.gm.settings.get_text("vs_bot", "VS BOT")},
            {"id": "vs_friend", "name": self.gm.settings.get_text("vs_friend", "ПРОТИВ ДРУГА")},
            {"id": "training", "name": self.gm.settings.get_text("training", "ТРЕНИРОВКА")}
        ]

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.mode_selecting:
                        self.mode_selecting = False
                    elif self.skin_selecting_mode:
                        self.skin_selecting_mode = False
                    elif self.selecting_mode:
                        self.selecting_mode = False
                    elif self.current_section == 6:
                        self._exit_game()
                    return
                
                if not self.selecting_mode and not self.show_selection_confirmed and not self.skin_selecting_mode and not self.mode_selecting:
                    if event.key == pygame.K_LEFT:
                        self.current_section = (self.current_section - 1) % len(self.sections)
                        if self.current_section == 3:
                            self._refresh_current_skins()
                    elif event.key == pygame.K_RIGHT:
                        self.current_section = (self.current_section + 1) % len(self.sections)
                        if self.current_section == 3:
                            self._refresh_current_skins()
                    elif event.key == pygame.K_RETURN:
                        current_section_name = self.sections[self.current_section]
                        if current_section_name == self.gm.settings.get_text("settings"):
                            self._open_settings()
                        elif current_section_name == self.sections[0]:
                            self._start_battle()
                        elif current_section_name == self.sections[4]:
                            self._open_shop()
                        elif current_section_name == self.sections[6]:
                            self._exit_game()
                    elif self.current_section == 1:
                        if event.key in [pygame.K_a, pygame.K_LEFT]:
                            self.selected_character = (self.selected_character - 1) % len(self.characters)
                        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                            self.selected_character = (self.selected_character + 1) % len(self.characters)
                        elif event.key == pygame.K_RETURN:
                            if not self.selecting_mode:
                                self.selecting_mode = True
                    elif self.current_section == 2:
                        if event.key in [pygame.K_a, pygame.K_LEFT]:
                            self.selected_cameo = (self.selected_cameo - 1) % len(self.cameos)
                        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                            self.selected_cameo = (self.selected_cameo + 1) % len(self.cameos)
                        elif event.key == pygame.K_RETURN:
                            if not self.selecting_mode:
                                self.selecting_mode = True
                    elif self.current_section == 3:
                        if event.key in [pygame.K_a, pygame.K_LEFT]:
                            self.selected_skin_tab = (self.selected_skin_tab - 1) % 2
                            self._refresh_current_skins()
                        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                            self.selected_skin_tab = (self.selected_skin_tab + 1) % 2
                            self._refresh_current_skins()
                        elif event.key == pygame.K_RETURN:
                            if not self.skin_selecting_mode:
                                self.skin_selecting_mode = True
                elif self.mode_selecting and not self.show_selection_confirmed:
                    if event.key == pygame.K_RETURN:
                        self._select_game_mode()
                    elif event.key == pygame.K_ESCAPE:
                        self.mode_selecting = False
                    elif event.key in [pygame.K_a, pygame.K_LEFT, pygame.K_UP]:
                        self.selected_game_mode = (self.selected_game_mode - 1) % len(self.game_modes)
                    elif event.key in [pygame.K_d, pygame.K_RIGHT, pygame.K_DOWN]:
                        self.selected_game_mode = (self.selected_game_mode + 1) % len(self.game_modes)
                elif self.skin_selecting_mode and not self.show_selection_confirmed:
                    if event.key == pygame.K_RETURN:
                        self._select_skin()
                    elif event.key == pygame.K_ESCAPE:
                        self.skin_selecting_mode = False
                    elif event.key in [pygame.K_a, pygame.K_LEFT]:
                        self.selected_skin_index = (self.selected_skin_index - 1) % len(self.current_skins) if self.current_skins else 0
                    elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                        self.selected_skin_index = (self.selected_skin_index + 1) % len(self.current_skins) if self.current_skins else 0
                    elif event.key == pygame.K_TAB:
                        self.selected_skin_tab = (self.selected_skin_tab + 1) % 2
                        self._refresh_current_skins()
                elif self.selecting_mode and not self.show_selection_confirmed:
                    if event.key == pygame.K_RETURN:
                        if self.current_section == 1:
                            self._select_character()
                        elif self.current_section == 2:
                            self._select_cameo()
                    elif event.key == pygame.K_ESCAPE:
                        self.selecting_mode = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.locked_skin_message:
                        return
                    self._handle_mouse_click(mouse_pos)

    def _handle_mouse_click(self, mouse_pos):
        if self.show_selection_confirmed:
            return
        if not self.selecting_mode and not self.skin_selecting_mode and not self.mode_selecting:
            for i, tab_rect in enumerate(self.tab_buttons):
                if tab_rect.collidepoint(mouse_pos):
                    self.current_section = i
                    if i == 3:
                        self._refresh_current_skins()
                    elif i == 4:
                        self._open_shop()
                        return
                    elif i == 5:
                        self._open_settings()
                        return
                    elif i == 6:
                        self._exit_game()
                        return
            if self.current_section == 1:
                if self.char_left_btn and self.char_left_btn.collidepoint(mouse_pos):
                    self.selected_character = (self.selected_character - 1) % len(self.characters)
                elif self.char_right_btn and self.char_right_btn.collidepoint(mouse_pos):
                    self.selected_character = (self.selected_character + 1) % len(self.characters)
                elif self.char_select_btn and self.char_select_btn.collidepoint(mouse_pos):
                    self.selecting_mode = True
            elif self.current_section == 2:
                if self.cameo_left_btn and self.cameo_left_btn.collidepoint(mouse_pos):
                    self.selected_cameo = (self.selected_cameo - 1) % len(self.cameos)
                elif self.cameo_right_btn and self.cameo_right_btn.collidepoint(mouse_pos):
                    self.selected_cameo = (self.selected_cameo + 1) % len(self.cameos)
                elif self.cameo_select_btn and self.cameo_select_btn.collidepoint(mouse_pos):
                    self.selecting_mode = True
            elif self.current_section == 3:
                if self.skin_tab_left and self.skin_tab_left.collidepoint(mouse_pos):
                    self.selected_skin_tab = (self.selected_skin_tab - 1) % 2
                    self._refresh_current_skins()
                elif self.skin_tab_right and self.skin_tab_right.collidepoint(mouse_pos):
                    self.selected_skin_tab = (self.selected_skin_tab + 1) % 2
                    self._refresh_current_skins()
                elif self.skin_left_btn and self.skin_left_btn.collidepoint(mouse_pos):
                    self.selected_skin_index = (self.selected_skin_index - 1) % len(self.current_skins) if self.current_skins else 0
                elif self.skin_right_btn and self.skin_right_btn.collidepoint(mouse_pos):
                    self.selected_skin_index = (self.selected_skin_index + 1) % len(self.current_skins) if self.current_skins else 0
                elif self.skin_select_btn and self.skin_select_btn.collidepoint(mouse_pos):
                    self.skin_selecting_mode = True
            elif self.current_section == 0 and self.mode_button and self.mode_button.collidepoint(mouse_pos):
                self.mode_selecting = True
            elif self.current_section == 0 and self.battle_button and self.battle_button.collidepoint(mouse_pos):
                self._start_battle()
        elif self.selecting_mode:
            if self.current_section == 1 and self.char_select_btn and self.char_select_btn.collidepoint(mouse_pos):
                self._select_character()
            elif self.current_section == 2 and self.cameo_select_btn and self.cameo_select_btn.collidepoint(mouse_pos):
                self._select_cameo()
        elif self.skin_selecting_mode:
            if self.current_section == 3 and self.skin_select_btn and self.skin_select_btn.collidepoint(mouse_pos):
                self._select_skin()
        elif self.mode_selecting:
            if self.current_section == 0 and self.mode_button and self.mode_button.collidepoint(mouse_pos):
                self._select_game_mode()

    def update(self, dt):
        for animation in self.playing_animations:
            animation.update(dt)
        self.playing_animations = []
        if self.show_selection_confirmed:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_confirmed_time > 1500:
                self.show_selection_confirmed = False
                self.selecting_mode = False
                self.skin_selecting_mode = False
                self.mode_selecting = False
                self.current_section = 0
        if self.unlock_animation:
            current_time = pygame.time.get_ticks()
            if current_time - self.unlock_animation_time > 2000:
                self.unlock_animation = False
                self.unlock_animation_skin = None
        if self.locked_skin_message:
            current_time = pygame.time.get_ticks()
            if current_time - self.locked_skin_message_time > 1500:
                self.locked_skin_message = False

    def draw(self, screen):
        self._draw_background(screen)
        self._draw_header(screen)
        self._draw_section_tabs(screen)
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
        if self.unlock_animation:
            self._draw_unlock_animation(screen)
        if self.locked_skin_message:
            self._draw_locked_skin_message(screen)

    def _draw_background(self, screen):
        screen.fill(self.colors["background"])
        for i in range(screen.get_height()):
            color = (20 + i//20, 20 + i//25, 40 + i//15)
            pygame.draw.line(screen, color, (0, i), (screen.get_width(), i))

    def _draw_header(self, screen):
        header_height = self.s(80)
        for i in range(header_height):
            color = (30 + i//3, 30 + i//3, 50 + i//2)
            pygame.draw.line(screen, color, (0, i), (screen.get_width(), i))
        title_font = self.get_font(36, bold=True)
        title_text = self.gm.settings.get_text("game_title")
        title = title_font.render(title_text, True, self.colors["accent"])
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, self.s(20)))
        resource_font = self.get_font(18)
        coins_icon = self.icons.get("coin")
        if coins_icon:
            screen.blit(coins_icon, (screen.get_width() - self.s(150), self.s(25)))
        coins_text = resource_font.render(f"{self.player_data['coins']}", True, (255, 215, 0))
        screen.blit(coins_text, (screen.get_width() - self.s(150) + (coins_icon.get_width() if coins_icon else 0) + 5, self.s(25)))
        trophy_icon = self.icons.get("trophy")
        if trophy_icon:
            screen.blit(trophy_icon, (screen.get_width() - self.s(150), self.s(50)))
        trophies_text = resource_font.render(f"{self.player_data['trophies']}", True, (255, 200, 100))
        screen.blit(trophies_text, (screen.get_width() - self.s(150) + (trophy_icon.get_width() if trophy_icon else 0) + 5, self.s(50)))

    def _draw_section_tabs(self, screen):
        self.tab_buttons = []
        tab_width = self.s(180)
        tab_height = self.s(55)
        tab_spacing = self.s(15)
        left_tabs = self.sections[:4]
        right_tabs = self.sections[4:]
        left_total_height = len(left_tabs) * tab_height + (len(left_tabs) - 1) * tab_spacing
        right_total_height = len(right_tabs) * tab_height + (len(right_tabs) - 1) * tab_spacing
        left_start_y = (screen.get_height() - left_total_height) // 2
        right_start_y = (screen.get_height() - right_total_height) // 2
        left_x = self.s(30)
        for i, section in enumerate(left_tabs):
            tab_rect = pygame.Rect(left_x, left_start_y + i * (tab_height + tab_spacing), tab_width, tab_height)
            self.tab_buttons.append(tab_rect)
            color = self.colors["button_primary"] if i == self.current_section else self.colors["header_bg"]
            pygame.draw.rect(screen, color, tab_rect, border_radius=self.s(12))
            pygame.draw.rect(screen, self.colors["text_light"], tab_rect, self.s(2), border_radius=self.s(12))
            font_size = self.f(18)
            final_font = pygame.font.SysFont("arial", int(font_size), bold=True)
            final_text = final_font.render(section, True, self.colors["text_light"])
            screen.blit(final_text, (tab_rect.centerx - final_text.get_width() // 2, 
                                   tab_rect.centery - final_text.get_height() // 2))
        right_x = screen.get_width() - tab_width - self.s(30)
        for i, section in enumerate(right_tabs):
            tab_index = i + 4
            tab_rect = pygame.Rect(right_x, right_start_y + i * (tab_height + tab_spacing), tab_width, tab_height)
            self.tab_buttons.append(tab_rect)
            if section == self.sections[6]:
                color = self.colors["danger"] if tab_index == self.current_section else (150, 80, 80)
            else:
                color = self.colors["button_secondary"] if tab_index == self.current_section else self.colors["header_bg"]
            pygame.draw.rect(screen, color, tab_rect, border_radius=self.s(12))
            pygame.draw.rect(screen, self.colors["text_light"], tab_rect, self.s(2), border_radius=self.s(12))
            font_size = self.f(18)
            final_font = pygame.font.SysFont("arial", int(font_size), bold=True)
            final_text = final_font.render(section, True, self.colors["text_light"])
            screen.blit(final_text, (tab_rect.centerx - final_text.get_width() // 2, 
                                   tab_rect.centery - final_text.get_height() // 2))

    def _draw_fight_section(self, screen, rect):
        selected_char = next((char for char in self.characters if char["selected"]), None)
        selected_cameo = next((cameo for cameo in self.cameos if cameo["selected"]), None)
        art_size = self.s(350)
        if selected_char:
            char_key = f"{selected_char['name'].lower()}_{selected_char['skin']}"
            char_animation = self.art_animations.get(char_key)
            if char_animation:
                char_x = rect.centerx - art_size + self.s(40)
                char_y = rect.centery - art_size // 2
                frame = char_animation.get_frame()
                if frame:
                    screen.blit(frame, (char_x, char_y))
                if char_animation not in self.playing_animations:
                    self.playing_animations.append(char_animation)
        if selected_cameo:
            cameo_key = f"{selected_cameo['name'].lower()}_{selected_cameo['skin']}"
            cameo_animation = self.art_animations.get(cameo_key)
            if cameo_animation:
                cameo_x = rect.centerx - self.s(40)
                cameo_y = rect.centery - art_size // 2
                frame = cameo_animation.get_frame()
                if frame:
                    screen.blit(frame, (cameo_x, cameo_y))
                if cameo_animation not in self.playing_animations:
                    self.playing_animations.append(cameo_animation)
        mode_btn_width = self.s(220)
        mode_btn_height = self.s(60)
        self.mode_button = pygame.Rect(
            rect.centerx - mode_btn_width // 2,
            rect.bottom - mode_btn_height - self.s(30),
            mode_btn_width,
            mode_btn_height
        )
        btn_color = self.colors["selected"] if self.mode_selecting else (
            self.colors["training"] if self.selected_game_mode == 1 else self.colors["button_secondary"]
        )
        pygame.draw.rect(screen, btn_color, self.mode_button, border_radius=self.s(12))
        pygame.draw.rect(screen, self.colors["text_light"], self.mode_button, self.s(2), border_radius=self.s(12))
        mode_font = self.get_font(20, bold=True)
        mode_text = mode_font.render(self.game_modes[self.selected_game_mode]["name"], True, self.colors["text_light"])
        screen.blit(mode_text, (self.mode_button.centerx - mode_text.get_width() // 2,
                              self.mode_button.centery - mode_text.get_height() // 2))
        if self.mode_selecting:
            hint_font = self.get_font(15)
            hint_text = "Используйте ←→ или кликните для выбора режима"
            hint = hint_font.render(hint_text, True, self.colors["text_dark"])
            screen.blit(hint, (rect.centerx - hint.get_width() // 2, 
                             self.mode_button.top - self.s(25)))
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
            btn_text = "НАЧАТЬ!" if self.selected_game_mode == 0 else "ТРЕНИРОВАТЬСЯ!"
            pygame.draw.rect(screen, self.colors["button_primary"], self.battle_button, border_radius=self.s(12))
            pygame.draw.rect(screen, self.colors["accent"], self.battle_button, self.s(3), border_radius=self.s(12))
        else:
            btn_text = "FIGHT!"
            pygame.draw.rect(screen, (100, 100, 100), self.battle_button, border_radius=self.s(12))
            pygame.draw.rect(screen, (150, 150, 150), self.battle_button, self.s(3), border_radius=self.s(12))
        btn_font = self.get_font(22, bold=True)
        btn_render = btn_font.render(btn_text, True, self.colors["text_light"] if battle_enabled else self.colors["text_dark"])
        screen.blit(btn_render, (self.battle_button.centerx - btn_render.get_width() // 2,
                               self.battle_button.centery - btn_render.get_height() // 2))

    def _draw_characters_section(self, screen, rect):
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
        if char_key in self.character_skins and "default" in self.character_skins[char_key]:
            skin = self.character_skins[char_key]["default"]
        else:
            skin = {"card_normal": None, "card_special": None}
        card_size = self._get_card_size()
        if self.selecting_mode or self.show_selection_confirmed:
            card = skin["card_special"]
        else:
            card = skin["card_normal"]
        if card:
            card_rect = pygame.Rect(rect.centerx - card_size//2, rect.centery - card_size//2, card_size, card_size)
            screen.blit(card, card_rect)
        else:
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
            left_arrow_icon = self.icons.get("arrow_left")
            if left_arrow_icon:
                screen.blit(left_arrow_icon, (self.char_left_btn.centerx - left_arrow_icon.get_width() // 2,
                                            self.char_left_btn.centery - left_arrow_icon.get_height() // 2))
            pygame.draw.rect(screen, self.colors["button_primary"], self.char_right_btn, border_radius=self.s(10))
            pygame.draw.rect(screen, self.colors["button_primary"], self.char_right_btn, self.s(2), border_radius=self.s(10))
            right_arrow_icon = self.icons.get("arrow_right")
            if right_arrow_icon:
                screen.blit(right_arrow_icon, (self.char_right_btn.centerx - right_arrow_icon.get_width() // 2,
                                             self.char_right_btn.centery - right_arrow_icon.get_height() // 2))
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
            left_arrow_icon = self.icons.get("arrow_left")
            if left_arrow_icon:
                screen.blit(left_arrow_icon, (self.cameo_left_btn.centerx - left_arrow_icon.get_width() // 2,
                                            self.cameo_left_btn.centery - left_arrow_icon.get_height() // 2))
            pygame.draw.rect(screen, self.colors["button_secondary"], self.cameo_right_btn, border_radius=self.s(10))
            pygame.draw.rect(screen, self.colors["text_light"], self.cameo_right_btn, self.s(2), border_radius=self.s(10))
            right_arrow_icon = self.icons.get("arrow_right")
            if right_arrow_icon:
                screen.blit(right_arrow_icon, (self.cameo_right_btn.centerx - right_arrow_icon.get_width() // 2,
                                             self.cameo_right_btn.centery - right_arrow_icon.get_height() // 2))
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
        if self.selected_skin_tab == 0:
            selected_entity = next((char for char in self.characters if char["selected"]), None)
            entity_name = selected_entity['name'] if selected_entity else "NONE"
            title_base = self.gm.settings.get_text('skin_for')
        else:
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
        tab_font = self.get_font(20, bold=True)
        char_tab_text = tab_font.render(self.gm.settings.get_text("characters_tab"), True, self.colors["text_light"])
        cameo_tab_text = tab_font.render(self.gm.settings.get_text("cameos_tab"), True, self.colors["text_light"])
        tab_width = self.s(150)
        tab_height = self.s(40)
        tab_spacing = self.s(20)
        total_tabs_width = tab_width * 2 + tab_spacing
        tabs_start_x = rect.centerx - total_tabs_width // 2
        char_tab_rect = pygame.Rect(tabs_start_x, rect.y + self.s(70), tab_width, tab_height)
        char_color = self.colors["button_primary"] if self.selected_skin_tab == 0 else self.colors["header_bg"]
        pygame.draw.rect(screen, char_color, char_tab_rect, border_radius=self.s(8))
        pygame.draw.rect(screen, self.colors["text_light"], char_tab_rect, self.s(2), border_radius=self.s(8))
        screen.blit(char_tab_text, (char_tab_rect.centerx - char_tab_text.get_width() // 2,
                          char_tab_rect.centery - char_tab_text.get_height() // 2))
        self.skin_tab_left = char_tab_rect
        cameo_tab_rect = pygame.Rect(tabs_start_x + tab_width + tab_spacing, rect.y + self.s(70), tab_width, tab_height)
        cameo_color = self.colors["button_secondary"] if self.selected_skin_tab == 1 else self.colors["header_bg"]
        pygame.draw.rect(screen, cameo_color, cameo_tab_rect, border_radius=self.s(8))
        pygame.draw.rect(screen, self.colors["text_light"], cameo_tab_rect, self.s(2), border_radius=self.s(8))
        screen.blit(cameo_tab_text, (cameo_tab_rect.centerx - cameo_tab_text.get_width() // 2,
                           cameo_tab_rect.centery - cameo_tab_text.get_height() // 2))
        self.skin_tab_right = cameo_tab_rect
        if self.current_skins and self.selected_skin_index < len(self.current_skins):
            skin = self.current_skins[self.selected_skin_index]
            card_size = self._get_card_size()
            if self.skin_selecting_mode or self.show_selection_confirmed:
                card = skin["card_special"]
            else:
                card = skin["card_normal"]
            if card:
                card_rect = pygame.Rect(rect.centerx - card_size//2, rect.centery - card_size//2, card_size, card_size)
                screen.blit(card, card_rect)
                name_font = self.get_font(22, bold=True)
                name_text = name_font.render(skin["name"], True, self.colors["text_light"])
                screen.blit(name_text, (rect.centerx - name_text.get_width() // 2, card_rect.bottom + self.s(15)))
                status_font = self.get_font(18)
                if skin["unlocked"]:
                    status_text = "РАЗБЛОКИРОВАН"
                    status_color = self.colors["selected"]
                    status_icon = self.icons.get("unlocked")
                else:
                    status_text = "ЗАБЛОКИРОВАН"
                    status_color = self.colors["danger"]
                    status_icon = self.icons.get("locked")
                status = status_font.render(status_text, True, status_color)
                if status_icon:
                    icon_x = rect.centerx - status.get_width() // 2 - status_icon.get_width() - 5
                    icon_y = card_rect.bottom + self.s(40) + (status.get_height() - status_icon.get_height()) // 2
                    screen.blit(status_icon, (icon_x, icon_y))
                screen.blit(status, (rect.centerx - status.get_width() // 2, card_rect.bottom + self.s(40)))
            else:
                error_font = self.get_font(18)
                error_text = error_font.render("Карточка не найдена", True, self.colors["danger"])
                screen.blit(error_text, (rect.centerx - error_text.get_width() // 2, rect.centery - self.s(10)))
        else:
            error_font = self.get_font(18)
            error_text = error_font.render("Нет доступных скинов", True, self.colors["text_dark"])
            screen.blit(error_text, (rect.centerx - error_text.get_width() // 2, rect.centery - self.s(10)))
        if self.current_skins and len(self.current_skins) > 1:
            if not self.skin_selecting_mode and not self.show_selection_confirmed:
                arrow_size = self.s(50)
                card_rect_center = rect.centery
                self.skin_left_btn = pygame.Rect(rect.centerx - card_size//2 - arrow_size - self.s(15), 
                                               card_rect_center - arrow_size//2, arrow_size, arrow_size)
                self.skin_right_btn = pygame.Rect(rect.centerx + card_size//2 + self.s(15), 
                                                card_rect_center - arrow_size//2, arrow_size, arrow_size)
                pygame.draw.rect(screen, self.colors["button_primary"], self.skin_left_btn, border_radius=self.s(10))
                pygame.draw.rect(screen, self.colors["text_light"], self.skin_left_btn, self.s(2), border_radius=self.s(10))
                left_arrow_icon = self.icons.get("arrow_left")
                if left_arrow_icon:
                    screen.blit(left_arrow_icon, (self.skin_left_btn.centerx - left_arrow_icon.get_width() // 2,
                                                self.skin_left_btn.centery - left_arrow_icon.get_height() // 2))
                pygame.draw.rect(screen, self.colors["button_primary"], self.skin_right_btn, border_radius=self.s(10))
                pygame.draw.rect(screen, self.colors["text_light"], self.skin_right_btn, self.s(2), border_radius=self.s(10))
                right_arrow_icon = self.icons.get("arrow_right")
                if right_arrow_icon:
                    screen.blit(right_arrow_icon, (self.skin_right_btn.centerx - right_arrow_icon.get_width() // 2,
                                                 self.skin_right_btn.centery - right_arrow_icon.get_height() // 2))
        btn_width = min(self.s(180), rect.width * 0.4)
        btn_height = self.s(45)
        self.skin_select_btn = pygame.Rect(rect.centerx - btn_width//2, rect.bottom - self.s(80), btn_width, btn_height)
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
            btn_color = (100, 100, 100)
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
        title_font = self.get_font(26, bold=True)
        title_text = self.gm.settings.get_text("shop")
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width() // 2, rect.y + self.s(25)))
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
        hint_font = self.get_font(16)
        hint_text = "Кликните чтобы открыть магазин"
        hint = hint_font.render(hint_text, True, self.colors["text_dark"])
        screen.blit(hint, (rect.centerx - hint.get_width() // 2, self.shop_button.bottom + self.s(20)))

    def _draw_settings_section(self, screen, rect):
        title_font = self.get_font(26, bold=True)
        title_text = self.gm.settings.get_text("settings")
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width() // 2, rect.y + self.s(25)))
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
        bar_height = self.s(30)
        bar_rect = pygame.Rect(0, screen.get_height() - bar_height, screen.get_width(), bar_height)
        pygame.draw.rect(screen, self.colors["header_bg"], bar_rect)
        copyright_font = self.get_font(12)
        copyright_text = copyright_font.render("© 2024 Brawl Fighters", True, self.colors["text_dark"])
        screen.blit(copyright_text, (screen.get_width() - copyright_text.get_width() - self.s(25), 
                                   bar_rect.centery - copyright_text.get_height()//2))

    def _draw_unlock_animation(self, screen):
        if not self.unlock_animation_skin:
            return
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.unlock_animation_time
        progress = min(elapsed / 2000, 1.0)
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(150 * progress)))
        screen.blit(overlay, (0, 0))
        base_size = self.s(200)
        animated_size = int(base_size * (1 + progress * 0.5))
        card_x = screen.get_width() // 2 - animated_size // 2
        card_y = screen.get_height() // 2 - animated_size // 2
        card = pygame.Surface((animated_size, animated_size), pygame.SRCALPHA)
        card.fill((255, 255, 255, int(200 * progress)))
        pygame.draw.rect(card, (100, 255, 100, int(255 * progress)), 
                        (0, 0, animated_size, animated_size), self.s(5))
        glow = pygame.Surface((animated_size + 20, animated_size + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow, (100, 255, 100, int(100 * progress)), 
                        (0, 0, animated_size + 20, animated_size + 20), 
                        border_radius=self.s(10))
        screen.blit(glow, (card_x - 10, card_y - 10))
        screen.blit(card, (card_x, card_y))
        text_size = int(self.s(40) * (1 + progress * 0.3))
        text_font = pygame.font.SysFont("arial", text_size, bold=True)
        text = text_font.render("РАЗБЛОКИРОВАНО!", True, (100, 255, 100))
        text_x = screen.get_width() // 2 - text.get_width() // 2
        text_y = card_y - text.get_height() - self.s(20)
        screen.blit(text, (text_x, text_y))

    def _draw_locked_skin_message(self, screen):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.locked_skin_message_time
        progress = min(elapsed / 1500, 1.0)
        if progress >= 1.0:
            return
        overlay = pygame.Surface((screen.get_width(), self.s(100)), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(200 * progress)))
        overlay_y = screen.get_height() // 2 - self.s(50)
        screen.blit(overlay, (0, overlay_y))
        text_font = self.get_font(24, bold=True)
        text = text_font.render("СКИН ЗАБЛОКИРОВАН!", True, self.colors["danger"])
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 
                         overlay_y + self.s(20)))
        hint_font = self.get_font(18)
        hint = hint_font.render("Купите скин в магазине", True, self.colors["text_light"])
        screen.blit(hint, (screen.get_width() // 2 - hint.get_width() // 2, 
                          overlay_y + self.s(60)))