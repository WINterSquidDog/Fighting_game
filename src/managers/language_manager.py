# src/managers/language_manager.py
import json
import os
import shutil

class LanguageManager:
    def __init__(self):
        self.current_language = "ru"
        self.translations = {}
        self.available_languages = {
            "ru": "Русский",
            "en": "English", 
            "es": "Español"
        }
        
        # ПЕРЕСОЗДАЕМ файлы переводов принудительно
        self._create_default_locales()
        self.load_language_files()
    
    def load_language_files(self):
        """Загружает все файлы переводов из папки locales"""
        self.translations = {}
        locales_dir = "locales"
        
        for lang_code in self.available_languages.keys():
            file_path = os.path.join(locales_dir, f"{lang_code}.json")
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                    print(f"✅ Загружен язык: {lang_code}")
                except Exception as e:
                    print(f"❌ Ошибка загрузки языка {lang_code}: {e}")
                    self.translations[lang_code] = {}
            else:
                print(f"⚠️ Файл перевода не найден: {file_path}")
                self.translations[lang_code] = {}
    
    def _create_default_locales(self):
        """ПЕРЕСОЗДАЕТ файлы переводов с ВСЕМИ ключами"""
        # Удаляем старую папку locales если есть
        locales_dir = "locales"
        if os.path.exists(locales_dir):
            shutil.rmtree(locales_dir)
        os.makedirs(locales_dir)
        
        default_translations = {
            "ru": {
                "game_title": "BRAWL FIGHTERS",
                "menu_sections": ["БОЙ", "ПЕРСОНАЖИ", "КАМЕО", "МАГАЗИН", "НАСТРОЙКИ", "ВЫХОД"],
                "battle_mode": "РЕЖИМЫ БОЯ",
                "select_character": "ВЫБЕРИ ПЕРСОНАЖА",
                "select_cameo": "ВЫБЕРИ КАМЕО",
                "confirm_selection": "ПОДТВЕРДИТЕ ВЫБОР",
                "selected": "ВЫБРАНО!",
                "fight_vs_bot": "БОЙ ПРОТИВ БОТА",
                "select_character_first": "Сначала выберите персонажа и камео!",
                "start_battle_hint": "Нажмите ENTER или кликните для начала боя",
                "use_arrows": "Используйте A/D, ←→ или кликните стрелки для просмотра",
                "confirm_hint": "Нажмите ENTER или кликните 'Подтвердить' для выбора",
                "returning_to_battle": "Возвращаемся к разделу Бой...",
                "shop": "МАГАЗИН",
                "shop_soon": "🛒 МАГАЗИН СКОРО ОТКРОЕТСЯ",
                "earn_coins": "Зарабатывайте монеты в боях!",
                "settings": "НАСТРОЙКИ",
                "audio_settings": "🎵 АУДИО",
                "graphics_settings": "🎮 ГРАФИКА", 
                "system_settings": "🌐 СИСТЕМА",
                "music_volume": "Громкость музыки:",
                "sound_volume": "Громкость звуков:",
                "fullscreen": "Полноэкранный режим:",
                "resolution": "Разрешение экрана:",
                "language": "Язык интерфейса:",
                "apply": "ПРИМЕНИТЬ",
                "exit_game": "ВЫХОД ИЗ ИГРЫ",
                "exit_confirm": "Вы уверены, что хотите выйти?",
                "exit": "ВЫЙТИ",
                "exit_hint": "Нажмите ENTER или кликните для выхода",
                "navigation": "←→/Клик Навигация",
                "selection": "ENTER/Клик Выбор",
                "browse": "A/D/←→ Просмотр в разделах",
                "confirm_action": "ENTER Подтвердить выбор",
                "cancel_action": "ESC Отменить выбор",
                "auto_return": "Автоматический переход...",
                "loading": "Загрузка...",
                "loading_resources": "Загрузка ресурсов...",
                "loading_characters": "Инициализация персонажей...",
                "loading_scenes": "Подготовка сцен...",
                "loading_complete": "Запуск игры...",
                "please_wait": "Идет загрузка, пожалуйста подождите...",
                "not_selected": "Не выбран",
                "not_selected_female": "Не выбрано",
                "select_character_title": "ВЫБЕРИ ПЕРСОНАЖА",
                "select_cameo_title": "ВЫБЕРИ КАМЕО",
                "confirm_character": "ПОДТВЕРДИТЕ ВЫБОР ПЕРСОНАЖА", 
                "confirm_cameo": "ПОДТВЕРДИТЕ ВЫБОР КАМЕО",
                "character_selected": "ПЕРСОНАЖ ВЫБРАН!",
                "cameo_selected": "КАМЕО ВЫБРАНО!",
                "select_button": "ВЫБРАТЬ",
                "confirm_button": "ПОДТВЕРДИТЬ",
                "selected_button": "ВЫБРАНО",
                "character_1x1x1x1_desc": "Загадочный кубический воин",
                "character_chara_desc": "Решительный боец",
                "character_steve_desc": "Мастер строительства",
                "cameo_coolkid_desc": "Хакер-вундеркинд",
                "cameo_papyrus_desc": "Великий Папайрус!",
                "cameo_larry_desc": "Загадочный лавовый парень",
                "back": "НАЗАД",
                "on": "ВКЛ",
                "off": "ВЫКЛ",
                "select_required": "Сначала выберите персонажа и камео!",
                "exit_confirmation": "Вы уверены, что хотите выйти?",
                "shop_coming_soon": "🛒 МАГАЗИН СКОРО ОТКРОЕТСЯ", 
                "earn_coins_hint": "Зарабатывайте монеты в боях!",
                "apply_restart": "Применить настройки? Игра будет перезапущена.",
                "yes": "ДА",
                "no": "НЕТ",
                "audio": "АУДИО",
                "graphics": "ГРАФИКА",
                "system": "СИСТЕМА",
                "sound_effects": "Громкость звуков:",
                "music_tracks": "Громкость музыки:",
                "screen_mode": "Полноэкранный режим:",
                "screen_resolution": "Разрешение экрана:",
                "interface_language": "Язык интерфейса:",
                "save_settings": "ПРИМЕНИТЬ",
                "character_section": "ПЕРСОНАЖ",
                "cameo_section": "КАМЕО", 
                "actions": "ДЕЙСТВИЯ",
                "fight": "FIGHT!",
                "vs_bot": "VS BOT",
                "menu_controls": "WASD/Стрелки - навигация, ENTER - начать бой",
                "selection_confirmed": "✅ Выбор подтвержден!",
                "placeholder_card": "ЗАГЛУШКА",
                "special": "SPECIAL",
                "normal": "NORMAL",
            },
            "en": {
                "game_title": "BRAWL FIGHTERS",
                "menu_sections": ["FIGHT", "CHARACTERS", "CAMEOS", "SHOP", "SETTINGS", "EXIT"],
                "battle_mode": "BATTLE MODES", 
                "select_character": "SELECT CHARACTER",
                "select_cameo": "SELECT CAMEOS",
                "confirm_selection": "CONFIRM SELECTION",
                "selected": "SELECTED!",
                "fight_vs_bot": "FIGHT VS BOT",
                "select_character_first": "Select character and cameo first!",
                "start_battle_hint": "Press ENTER or click to start battle",
                "use_arrows": "Use A/D, ←→ or click arrows to browse",
                "confirm_hint": "Press ENTER or click 'Confirm' to select",
                "returning_to_battle": "Returning to Battle section...",
                "shop": "SHOP",
                "shop_soon": "🛒 SHOP OPENING SOON",
                "earn_coins": "Earn coins in battles!",
                "settings": "SETTINGS",
                "audio_settings": "🎵 AUDIO",
                "graphics_settings": "🎮 GRAPHICS",
                "system_settings": "🌐 SYSTEM", 
                "music_volume": "Music Volume:",
                "sound_volume": "Sound Volume:", 
                "fullscreen": "Fullscreen Mode:",
                "resolution": "Screen Resolution:",
                "language": "Interface Language:",
                "apply": "APPLY",
                "exit_game": "EXIT GAME",
                "exit_confirm": "Are you sure you want to exit?",
                "exit": "EXIT",
                "exit_hint": "Press ENTER or click to exit",
                "navigation": "←→/Click Navigation",
                "selection": "ENTER/Click Selection", 
                "browse": "A/D/←→ Browse in sections",
                "confirm_action": "ENTER Confirm selection",
                "cancel_action": "ESC Cancel selection",
                "auto_return": "Auto-returning...",
                "loading": "Loading...",
                "loading_resources": "Loading resources...",
                "loading_characters": "Initializing characters...",
                "loading_scenes": "Preparing scenes...",
                "loading_complete": "Starting game...",
                "please_wait": "Loading, please wait...",
                "not_selected": "Not selected",
                "not_selected_female": "Not selected", 
                "select_character_title": "SELECT CHARACTER",
                "select_cameo_title": "SELECT CAMEOS",
                "confirm_character": "CONFIRM CHARACTER SELECTION",
                "confirm_cameo": "CONFIRM CAMEOS SELECTION",
                "character_selected": "CHARACTER SELECTED!",
                "cameo_selected": "CAMEOS SELECTED!",
                "select_button": "SELECT",
                "confirm_button": "CONFIRM",
                "selected_button": "SELECTED",
                "character_1x1x1x1_desc": "Mysterious cubic warrior",
                "character_chara_desc": "Determined fighter", 
                "character_steve_desc": "Master builder",
                "cameo_coolkid_desc": "Hacker prodigy",
                "cameo_papyrus_desc": "The Great Papyrus!",
                "cameo_larry_desc": "Mysterious lava guy",
                "back": "BACK",
                "on": "ON",
                "off": "OFF",
                "select_required": "Select character and cameo first!",
                "exit_confirmation": "Are you sure you want to exit?",
                "shop_coming_soon": "🛒 SHOP OPENING SOON",
                "earn_coins_hint": "Earn coins in battles!",
                "apply_restart": "Apply settings? Game will restart.",
                "yes": "YES", 
                "no": "NO",
                "audio": "AUDIO",
                "graphics": "GRAPHICS",
                "system": "SYSTEM",
                "sound_effects": "Sound Volume:",
                "music_tracks": "Music Volume:",
                "screen_mode": "Fullscreen Mode:",
                "screen_resolution": "Screen Resolution:",
                "interface_language": "Interface Language:",
                "save_settings": "APPLY",
                "character_section": "CHARACTER",
                "cameo_section": "CAMEOS",
                "actions": "ACTIONS", 
                "fight": "FIGHT!",
                "vs_bot": "VS BOT",
                "menu_controls": "WASD/Arrows - navigation, ENTER - start battle",
                "selection_confirmed": "✅ Selection confirmed!",
                "placeholder_card": "PLACEHOLDER",
                "special": "SPECIAL",
                "normal": "NORMAL",
            },
            "es": {
                "game_title": "BRAWL FIGHTERS", 
                "menu_sections": ["LUCHA", "PERSONAJES", "CAMEO", "TIENDA", "AJUSTES", "SALIR"],
                "battle_mode": "MODOS DE LUCHA",
                "select_character": "SELECCIONAR PERSONAJE",
                "select_cameo": "SELECCIONAR CAMEO",
                "confirm_selection": "CONFIRMAR SELECCIÓN",
                "selected": "¡SELECCIONADO!",
                "fight_vs_bot": "LUCHA VS BOT",
                "select_character_first": "¡Primero selecciona personaje y cameo!",
                "start_battle_hint": "Presiona ENTER o haz clic para comenzar",
                "use_arrows": "Usa A/D, ←→ o haz clic en flechas para navegar",
                "confirm_hint": "Presiona ENTER o haz clic 'Confirmar' para seleccionar",
                "returning_to_battle": "Volviendo a sección Lucha...",
                "shop": "TIENDA",
                "shop_soon": "🛒 TIENDA PRONTO",
                "earn_coins": "¡Gana monedas en batallas!",
                "settings": "AJUSTES",
                "audio_settings": "🎵 AUDIO",
                "graphics_settings": "🎮 GRÁFICOS",
                "system_settings": "🌐 SISTEMA",
                "music_volume": "Volumen de música:",
                "sound_volume": "Volumen de sonido:",
                "fullscreen": "Pantalla completa:",
                "resolution": "Resolución de pantalla:",
                "language": "Idioma de interfaz:",
                "apply": "APLICAR",
                "exit_game": "SALIR DEL JUEGO",
                "exit_confirm": "¿Estás seguro de que quieres salir?",
                "exit": "SALIR",
                "exit_hint": "Presiona ENTER o haz clic para salir",
                "navigation": "←→/Clic Navegación",
                "selection": "ENTER/Clic Selección",
                "browse": "A/D/←→ Navegar en secciones",
                "confirm_action": "ENTER Confirmar selección",
                "cancel_action": "ESC Cancelar selección",
                "auto_return": "Volviendo automáticamente...",
                "loading": "Cargando...",
                "loading_resources": "Cargando recursos...",
                "loading_characters": "Inicializando personajes...",
                "loading_scenes": "Preparando escenas...",
                "loading_complete": "Iniciando juego...",
                "please_wait": "Cargando, por favor espera...",
                "not_selected": "No seleccionado",
                "not_selected_female": "No seleccionado",
                "select_character_title": "SELECCIONAR PERSONAJE",
                "select_cameo_title": "SELECCIONAR CAMEO",
                "confirm_character": "CONFIRMAR SELECCIÓN DE PERSONAJE",
                "confirm_cameo": "CONFIRMAR SELECCIÓN DE CAMEO",
                "character_selected": "¡PERSONAJE SELECCIONADO!",
                "cameo_selected": "¡CAMEO SELECCIONADO!",
                "select_button": "SELECCIONAR",
                "confirm_button": "CONFIRMAR",
                "selected_button": "SELECCIONADO",
                "character_1x1x1x1_desc": "Guerrero cúbico misterioso",
                "character_chara_desc": "Luchador determinado",
                "character_steve_desc": "Maestro constructor",
                "cameo_coolkid_desc": "Prodiguio hacker",
                "cameo_papyrus_desc": "¡El Gran Papyrus!",
                "cameo_larry_desc": "Chico de lava misterioso",
                "back": "ATRÁS",
                "on": "ON",
                "off": "OFF",
                "select_required": "¡Primero selecciona personaje y cameo!",
                "exit_confirmation": "¿Estás seguro de que quieres salir?",
                "shop_coming_soon": "🛒 TIENDA PRONTO",
                "earn_coins_hint": "¡Gana monedas en batallas!",
                "apply_restart": "¿Aplicar ajustes? El juego se reiniciará.",
                "yes": "SÍ",
                "no": "NO",
                "audio": "AUDIO",
                "graphics": "GRÁFICOS",
                "system": "SISTEMA",
                "sound_effects": "Volumen de sonido:",
                "music_tracks": "Volumen de música:",
                "screen_mode": "Pantalla completa:",
                "screen_resolution": "Resolución de pantalla:",
                "interface_language": "Idioma de interfaz:",
                "save_settings": "APLICAR",
                "character_section": "PERSONAJE",
                "cameo_section": "CAMEO",
                "actions": "ACCIONES",
                "fight": "¡LUCHA!",
                "vs_bot": "VS BOT", 
                "menu_controls": "WASD/Flechas - navegación, ENTER - comenzar",
                "selection_confirmed": "✅ ¡Selección confirmada!",
                "placeholder_card": "MARCADOR",
                "special": "ESPECIAL",
                "normal": "NORMAL",
            }
        }
        
        for lang_code, translations in default_translations.items():
            file_path = os.path.join("locales", f"{lang_code}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=2)
            print(f"✅ ПЕРЕСОЗДАН файл перевода: {file_path}")
    
    def set_language(self, language_name):
        """Устанавливает язык по названию (Русский, English, etc)"""
        # Находим код языка по названию
        for code, name in self.available_languages.items():
            if name == language_name:
                self.current_language = code
                print(f"🌐 Язык изменен на: {language_name} ({code})")
                return True
        return False
    
    def get(self, key, default=None):
        """Получает перевод по ключу"""
        translation = self.translations.get(self.current_language, {})
        result = translation.get(key, default or key)
        return result
    
    def get_sections(self):
        """Получает переведенные разделы меню"""
        return self.translations.get(self.current_language, {}).get("menu_sections", [])