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
        
        # НЕ пересоздаем файлы при инициализации
        self.load_language_files()
        
        # Если файлы не загрузились, создаем их в памяти
        if not self.translations.get("ru"):
            print("⚠️ Файлы локалей не найдены, создаем в памяти...")
            self._create_translations_in_memory()
    
    def load_language_files(self):
        """Загружает все файлы переводов из папки locales"""
        self.translations = {}
        locales_dir = "locales"
        
        # Проверяем, существует ли папка locales
        if not os.path.exists(locales_dir):
            print(f"⚠️ Папка локалей не найдена: {locales_dir}")
            return
        
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
    
    def _create_translations_in_memory(self):
        """Создает переводы в памяти, если файлы не найдены"""
        print("📝 Создаем переводы в памяти...")
        
        # Базовые переводы для всех языков
        self.translations = {
            "ru": self._get_russian_translations(),
            "en": self._get_english_translations(),
            "es": self._get_spanish_translations()
        }
    
    def _get_russian_translations(self):
        return {
            # Основные
            "game_title": "BRAWL FIGHTERS",
            "menu_sections": ["БОЙ", "ПЕРСОНАЖИ", "КАМЕО", "СКИНЫ", "МАГАЗИН", "НАСТРОЙКИ", "ВЫХОД"],
            
            # Режимы игры
            "battle_mode": "РЕЖИМЫ БОЯ",
            "vs_bot": "VS BOT",
            "vs_friend": "ПРОТИВ ДРУГА",
            "training": "ТРЕНИРОВКА",
            
            # Выбор персонажей
            "select_character": "ВЫБЕРИ ПЕРСОНАЖА",
            "select_cameo": "ВЫБЕРИ КАМЕО",
            "confirm_selection": "ПОДТВЕРДИТЕ ВЫБОР",
            "selected": "ВЫБРАНО!",
            "select_character_first": "Сначала выберите персонажа и камео!",
            
            # Подсказки
            "start_battle_hint": "Нажмите ENTER или кликните для начала боя",
            "use_arrows": "Используйте A/D, ←→ или кликните стрелки для просмотра",
            "confirm_hint": "Нажмите ENTER или кликните 'Подтвердить' для выбора",
            "returning_to_battle": "Возвращаемся к разделу Бой...",
            
            # Магазин
            "shop": "МАГАЗИН",
            "shop_soon": "🛒 МАГАЗИН СКОРО ОТКРОЕТСЯ",
            "earn_coins": "Зарабатывайте монеты в боях!",
            
            # Настройки
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
            "back": "НАЗАД",
            
            # Выход
            "exit_game": "ВЫХОД ИЗ ИГРЫ",
            "exit_confirm": "Вы уверены, что хотите выйти?",
            "exit": "ВЫЙТИ",
            "exit_hint": "Нажмите ENTER или кликните для выхода",
            
            # Управление
            "navigation": "←→/Клик Навигация",
            "selection": "ENTER/Клик Выбор", 
            "browse": "A/D/←→ Просмотр в разделах",
            "confirm_action": "ENTER Подтвердить выбор",
            "cancel_action": "ESC Отменить выбор",
            
            # Загрузка
            "loading": "Загрузка...",
            "loading_resources": "Загрузка ресурсов...",
            "loading_characters": "Инициализация персонажей...",
            "loading_scenes": "Подготовка сцен...",
            "loading_complete": "Запуск игры...",
            "please_wait": "Идет загрузка, пожалуйста подождите...",
            
            # Статусы выбора
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
            "map_by_characters": "По персонажам",
            "map_description_by_characters": "Карта выбирается по выбранным персонажам",
            
            # Описания персонажей
            "character_1x1x1x1_desc": "Загадочный кубический воин",
            "character_chara_desc": "Решительный боец",
            "character_steve_desc": "Мастер строительства",
            "character_nameless_desc": "Забытый воин без имени",
            "cameo_coolkid_desc": "Хакер-вундеркинд",
            "cameo_papyrus_desc": "Великий Папайрус!",
            
            # Кнопки
            "on": "ВКЛ",
            "off": "ВЫКЛ",
            "yes": "ДА",
            "no": "НЕТ",
            "fight": "FIGHT!",
            
            # Скины
            "skins_section": "СКИНЫ",
            "character_skins": "СКИНЫ ПЕРСОНАЖЕЙ", 
            "cameo_skins": "СКИНЫ КАМЕО",
            "skin_selected": "СКИН ВЫБРАН!",
            "confirm_skin": "ПОДТВЕРДИТЕ ВЫБОР СКИНА",
            "browse_skins": "Используйте A/D, ←→ или кликните стрелки для просмотра скинов",
            "select_skin": "ВЫБРАТЬ",
            "skin_for": "СКИНЫ ДЛЯ",
            "characters_tab": "ПЕРСОНАЖИ",
            "cameos_tab": "КАМЕО",
            
            # Названия скинов
            "skin_default": "Обычный",
            "skin_timeless": "Бессмертный",
            "skin_two_faced": "Бог пустоты",
            "skin_tag_time": "Время тегов",
            "skin_the_great": "Великий",
            
            # Новые для MK1 стиля выбора
            "select_character_title_mk1": "ВЫБОР ПЕРСОНАЖА",
            "select_cameo_title_mk1": "ВЫБОР КАМЕО",
            "select_map_title": "ВЫБОР КАРТЫ",
            
            # Карты
            "map_soul_beach": "Soul Beach",
            "map_hall_of_judgement": "Hall of Judgement", 
            "map_deep_caves": "Deep Caves",
            "map_everlost": "Everlost",
            "map_random": "Случайная",
            "map_description_soul_beach": "Песчаный пляж с древними руинами",
            "map_description_hall_of_judgement": "Заброшенный зал суда",
            "map_description_deep_caves": "Темные пещеры с кристаллами",
            "map_description_everlost": "Забытое измерение",
            
            # Игроки
            "player1": "ИГРОК 1",
            "player2": "ИГРОК 2",
            "confirm_selection_mk1": "ПОДТВЕРДИТЬ ВЫБОР",
            "start_battle_mk1": "НАЧАТЬ БОЙ",
            
            # Подсказки для выбора
            "character_selection_hint": "Выберите персонажа для боя",
            "cameo_selection_hint": "Выберите камео для поддержки",
            "map_selection_hint": "Выберите арену для боя",
            "auto_map_selection": "Автоматический выбор карты",
            "back_to_menu": "НАЗАД В МЕНЮ",
            
            # Дополнительные имена
            "nameless": "Nameless",
            
            # Технические
            "placeholder_card": "ЗАГЛУШКА",
            "special": "SPECIAL",
            "normal": "NORMAL",
            "auto_return": "Автоматический переход...",
            "selection_confirmed": "✅ Выбор подтвержден!"
        }
    
    def _get_english_translations(self):
        return {
            # Main
            "game_title": "BRAWL FIGHTERS",
            "menu_sections": ["FIGHT", "CHARACTERS", "CAMEOS", "SKINS", "SHOP", "SETTINGS", "EXIT"],
            
            # Game modes
            "battle_mode": "BATTLE MODES",
            "vs_bot": "VS BOT",
            "vs_friend": "VS FRIEND",
            "training": "TRAINING",
            
            # Character selection
            "select_character": "SELECT CHARACTER",
            "select_cameo": "SELECT CAMEOS",
            "confirm_selection": "CONFIRM SELECTION",
            "selected": "SELECTED!",
            "select_character_first": "Select character and cameo first!",
            
            # Hints
            "start_battle_hint": "Press ENTER or click to start battle",
            "use_arrows": "Use A/D, ←→ or click arrows to browse",
            "confirm_hint": "Press ENTER or click 'Confirm' to select",
            "returning_to_battle": "Returning to Battle section...",
            
            # Shop
            "shop": "SHOP",
            "shop_soon": "🛒 SHOP OPENING SOON",
            "earn_coins": "Earn coins in battles!",
            
            # Settings
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
            "back": "BACK",
            
            # Exit
            "exit_game": "EXIT GAME",
            "exit_confirm": "Are you sure you want to exit?",
            "exit": "EXIT",
            "exit_hint": "Press ENTER or click to exit",
            
            # Controls
            "navigation": "←→/Click Navigation",
            "selection": "ENTER/Click Selection",
            "browse": "A/D/←→ Browse in sections",
            "confirm_action": "ENTER Confirm selection",
            "cancel_action": "ESC Cancel selection",
            
            # Loading
            "loading": "Loading...",
            "loading_resources": "Loading resources...",
            "loading_characters": "Initializing characters...",
            "loading_scenes": "Preparing scenes...",
            "loading_complete": "Starting game...",
            "please_wait": "Loading, please wait...",
            
            # Selection statuses
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
            "map_by_characters": "By Characters",
            "map_description_by_characters": "Map is selected based on chosen characters",
            
            # Character descriptions
            "character_1x1x1x1_desc": "Mysterious cubic warrior",
            "character_chara_desc": "Determined fighter",
            "character_steve_desc": "Master builder",
            "character_nameless_desc": "Forgotten warrior without name",
            "cameo_coolkid_desc": "Hacker prodigy",
            "cameo_papyrus_desc": "The Great Papyrus!",
            
            # Buttons
            "on": "ON",
            "off": "OFF",
            "yes": "YES",
            "no": "NO",
            "fight": "FIGHT!",
            
            # Skins
            "skins_section": "SKINS",
            "character_skins": "CHARACTER SKINS",
            "cameo_skins": "CAMEOS SKINS",
            "skin_selected": "SKIN SELECTED!",
            "confirm_skin": "CONFIRM SKIN SELECTION",
            "browse_skins": "Use A/D, ←→ or click arrows to browse skins",
            "select_skin": "SELECT",
            "skin_for": "SKINS FOR",
            "characters_tab": "CHARACTERS",
            "cameos_tab": "CAMEOS",
            
            # Skin names
            "skin_default": "Default",
            "skin_timeless": "Timeless",
            "skin_two_faced": "Void God",
            "skin_tag_time": "Tag Time",
            "skin_the_great": "The Great",
            
            # New for MK1 style selection
            "select_character_title_mk1": "SELECT CHARACTER",
            "select_cameo_title_mk1": "SELECT CAMEOS",
            "select_map_title": "SELECT MAP",
            
            # Maps
            "map_soul_beach": "Soul Beach",
            "map_hall_of_judgement": "Hall of Judgement",
            "map_deep_caves": "Deep Caves",
            "map_everlost": "Everlost",
            "map_random": "Random",
            "map_description_soul_beach": "Sandy beach with ancient ruins",
            "map_description_hall_of_judgement": "Abandoned hall of judgement",
            "map_description_deep_caves": "Dark caves with crystals",
            "map_description_everlost": "Forgotten dimension",
            
            # Players
            "player1": "PLAYER 1",
            "player2": "PLAYER 2",
            "confirm_selection_mk1": "CONFIRM SELECTION",
            "start_battle_mk1": "START BATTLE",
            
            # Selection hints
            "character_selection_hint": "Select character for battle",
            "cameo_selection_hint": "Select cameo for support",
            "map_selection_hint": "Select arena for battle",
            "auto_map_selection": "Auto map selection",
            "back_to_menu": "BACK TO MENU",
            
            # Additional names
            "nameless": "Nameless",
            
            # Technical
            "placeholder_card": "PLACEHOLDER",
            "special": "SPECIAL",
            "normal": "NORMAL",
            "auto_return": "Auto-returning...",
            "selection_confirmed": "✅ Selection confirmed!"
        }
    
    def _get_spanish_translations(self):
        return {
            # Principal
            "game_title": "BRAWL FIGHTERS",
            "menu_sections": ["LUCHA", "PERSONAJES", "CAMEO", "SKINS", "TIENDA", "AJUSTES", "SALIR"],
            
            # Modos de juego
            "battle_mode": "MODOS DE LUCHA",
            "vs_bot": "VS BOT",
            "vs_friend": "CONTRA AMIGO",
            "training": "ENTRENAMIENTO",
            
            # Selección de personajes
            "select_character": "SELECCIONAR PERSONAJE",
            "select_cameo": "SELECCIONAR CAMEO",
            "confirm_selection": "CONFIRMAR SELECCIÓN",
            "selected": "¡SELECCIONADO!",
            "select_character_first": "¡Primero selecciona personaje y cameo!",
            
            # Sugerencias
            "start_battle_hint": "Presiona ENTER o haz clic para comenzar",
            "use_arrows": "Usa A/D, ←→ o haz clic en flechas para navegar",
            "confirm_hint": "Presiona ENTER o haz clic 'Confirmar' para seleccionar",
            "returning_to_battle": "Volviendo a sección Lucha...",
            
            # Tienda
            "shop": "TIENDA",
            "shop_soon": "🛒 TIENDA PRONTO",
            "earn_coins": "¡Gana monedas en batallas!",
            
            # Ajustes
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
            "back": "ATRÁS",
            
            # Salir
            "exit_game": "SALIR DEL JUEGO",
            "exit_confirm": "¿Estás seguro de que quieres salir?",
            "exit": "SALIR",
            "exit_hint": "Presiona ENTER o haz clic para salir",
            
            # Controles
            "navigation": "←→/Clic Navegación",
            "selection": "ENTER/Clic Selección",
            "browse": "A/D/←→ Navegar en secciones",
            "confirm_action": "ENTER Confirmar selección",
            "cancel_action": "ESC Cancelar selección",
            
            # Carga
            "loading": "Cargando...",
            "loading_resources": "Cargando recursos...",
            "loading_characters": "Inicializando personajes...",
            "loading_scenes": "Preparando escenas...",
            "loading_complete": "Iniciando juego...",
            "please_wait": "Cargando, por favor espera...",
            
            # Estados de selección
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
            "map_by_characters": "Por Personajes",
            "map_description_by_characters": "El mapa se selecciona según los personajes elegidos",
            
            # Descripciones de personajes
            "character_1x1x1x1_desc": "Guerrero cúbico misterioso",
            "character_chara_desc": "Luchador determinado",
            "character_steve_desc": "Maestro constructor",
            "character_nameless_desc": "Guerrero olvidado sin nombre",
            "cameo_coolkid_desc": "Prodiguio hacker",
            "cameo_papyrus_desc": "¡El Gran Papyrus!",
            
            # Botones
            "on": "ON",
            "off": "OFF",
            "yes": "SÍ",
            "no": "NO",
            "fight": "¡LUCHA!",
            
            # Skins
            "skins_section": "SKINS",
            "character_skins": "SKINS DE PERSONAJES",
            "cameo_skins": "SKINS DE CAMEO",
            "skin_selected": "¡SKIN SELECCIONADO!",
            "confirm_skin": "CONFIRMAR SELECCIÓN DE SKIN",
            "browse_skins": "Usa A/D, ←→ o haz clic en flechas para navegar skins",
            "select_skin": "SELECCIONAR",
            "skin_for": "SKINS PARA",
            "characters_tab": "PERSONAJES",
            "cameos_tab": "CAMEO",
            
            # Nombres de skins
            "skin_default": "Predeterminado",
            "skin_timeless": "Eterno",
            "skin_two_faced": "Dios del Vacío",
            "skin_tag_time": "Tiempo de Etiquetas",
            "skin_the_great": "El Grande",
            
            # Nuevo para selección estilo MK1
            "select_character_title_mk1": "SELECCIONAR PERSONAJE",
            "select_cameo_title_mk1": "SELECCIONAR CAMEO",
            "select_map_title": "SELECCIONAR MAPA",
            
            # Mapas
            "map_soul_beach": "Soul Beach",
            "map_hall_of_judgement": "Hall of Judgement",
            "map_deep_caves": "Deep Caves",
            "map_everlost": "Everlost",
            "map_random": "Aleatorio",
            "map_description_soul_beach": "Playa arenosa con ruinas antiguas",
            "map_description_hall_of_judgement": "Sala del juicio abandonada",
            "map_description_deep_caves": "Cuevas oscuras con cristales",
            "map_description_everlost": "Dimensión olvidada",
            
            # Jugadores
            "player1": "JUGADOR 1",
            "player2": "JUGADOR 2",
            "confirm_selection_mk1": "CONFIRMAR SELECCIÓN",
            "start_battle_mk1": "COMENZAR BATALLA",
            
            # Sugerencias de selección
            "character_selection_hint": "Selecciona personaje para la batalla",
            "cameo_selection_hint": "Selecciona cameo para apoyo",
            "map_selection_hint": "Selecciona arena para la batalla",
            "auto_map_selection": "Selección automática de mapa",
            "back_to_menu": "VOLVER AL MENÚ",
            
            # Nombres adicionales
            "nameless": "Sin Nombre",
            
            # Técnico
            "placeholder_card": "MARCADOR",
            "special": "ESPECIAL",
            "normal": "NORMAL",
            "auto_return": "Volviendo automáticamente...",
            "selection_confirmed": "✅ ¡Selección confirmada!"
        }
    
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