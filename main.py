# main.py
import pygame
from src.managers.game_manager import GameManager
from src.managers.settings_manager import SettingsManager
from src.scenes.loading_scene import LoadingScene
from src.scenes.menu_scene import MenuScene
from src.scenes.settings_scene import SettingsScene
from src.scenes.battle_scene import BattleScene
from src.scenes.intro_scene import IntroSequenceScene
from src.scenes.victory_scene import VictoryScene
from src.core.character import Character
from src.managers.resource_manager import ResourceManager
from src.core.input_handler import InputHandler
from src.managers.language_manager import LanguageManager
from src.managers.save_manager import SaveManager
from src.scenes.shop_scene import ShopScene
from src.managers.skin_manager import SkinManager
from src.scenes.shop_scene import ShopScene
import sys
import os

# Определяем, запущено ли приложение из .exe
def resource_path(relative_path):
    """ Получает правильный путь к ресурсам для .exe """
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def main():
    pygame.init()
    pygame.mixer.init()
    print("🔧 Запуск игры...")
    # Сначала загружаем настройки
    settings_manager = SettingsManager()
    print("🎮 Загруженные настройки:")
    print(f"  Разрешение: {settings_manager.current_settings['resolution']}")
    print(f"  Полный экран: {settings_manager.current_settings['fullscreen']}")
    print(f"  Громкость музыки: {settings_manager.current_settings['music_volume']}")
    print("🌐 Доступные языки:", settings_manager.language_manager.available_languages)
    print("🌐 Текущий язык:", settings_manager.current_settings["language"])
    # Создаем экран с настройками
    screen = settings_manager.apply_graphics_settings()
    if not screen:
        print("❌ Не удалось применить настройки графики, используем по умолчанию")
        screen = pygame.display.set_mode(settings_manager.base_resolution)
        settings_manager.update_scale_factor(settings_manager.base_resolution[0])
    
    print(f"🖥️ Создан экран: {screen.get_size()}")
    
    pygame.display.set_caption("Fighting Game")
    clock = pygame.time.Clock()

    # Core systems с настройками
    resources = ResourceManager()
    input_handler = InputHandler()
    save_manager = SaveManager()
    skin_manager = SkinManager()

    # Game manager с настройками
    gm = GameManager(resources, input_handler)
    gm.settings = settings_manager
    gm.screen = screen
    gm.save_manager = save_manager
    gm.skin_manager = skin_manager
    # Регистрируем сцены
    gm.register_scene("loading", LoadingScene(gm))
    gm.register_scene("menu", MenuScene(gm))
    gm.register_scene("settings", SettingsScene(gm))
    gm.register_scene("intro", None)
    gm.register_scene("battle", None)
    gm.register_scene("victory", None)
    gm.register_scene("shop", ShopScene(gm))

    # Начинаем с загрузки
    gm.set_scene("loading")

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        gm.handle_events(events)
        gm.update(dt)

        screen.fill((0, 0, 0))
        gm.draw(screen)
        pygame.display.flip()

    # Сохраняем настройки при выходе
    settings_manager.save_settings()
    pygame.quit()

if __name__ == "__main__":
    main()