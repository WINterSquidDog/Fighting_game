# src/managers/save_manager.py
import json
import os
import sys

# Функция для получения корректного пути к ресурсам в pyinstaller
def resource_path(relative_path):
    """Получает правильный путь к ресурсам для работы как из .py, так и из .exe"""
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class SaveManager:
    def __init__(self):
        self.save_file = resource_path("src\data\game_save.json")  # Используем resource_path
        self.save_data = {}
        self.default_data = {
            "character": "1x1x1x1",
            "cameo": "c00lk1d",
            "character_skin": "default",
            "cameo_skin": "default",
            "game_mode": "vs_bot",  # Новое поле
            "coins": 1000,
            "trophies": 0,
            "character_skins": {},
            "cameo_skins": {},
            "first_launch": True,  # Флаг первого запуска
            "map": "random",  # Выбранная карта
            "character_map": {}  # Карты по умолчанию для персонажей
        }
        self.load_save()
    
    def load_save(self):
        """Загружает сохранение или создает новое"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    self.save_data = json.load(f)
                
                # Проверяем наличие всех необходимых полей
                for key, value in self.default_data.items():
                    if key not in self.save_data:
                        self.save_data[key] = value
                
                print(f"📂 Загружено сохранение: {self.save_file}")
            else:
                self.save_data = self.default_data.copy()
                self.write_save()
                print(f"🆕 Создано новое сохранение: {self.save_file}")
                
        except Exception as e:
            print(f"❌ Ошибка загрузки сохранения {self.save_file}: {e}")
            self.save_data = self.default_data.copy()
    
    def write_save(self):
        """Записывает сохранение в файл"""
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.save_data, f, ensure_ascii=False, indent=2)
            print(f"💾 Сохранение записано: {self.save_file}")
        except Exception as e:
            print(f"❌ Ошибка записи сохранения {self.save_file}: {e}")
    
    def save_game(self, game_mode=None, **kwargs):
        """
        Сохраняет игру с новыми данными
        """
        # Обновляем данные если они переданы
        if game_mode is not None:
            self.save_data["game_mode"] = game_mode
        if "character" in kwargs:
            self.save_data["character"] = kwargs["character"]
        if "cameo" in kwargs:
            self.save_data["cameo"] = kwargs["cameo"]
        if "character_skin" in kwargs:
            self.save_data["character_skin"] = kwargs["character_skin"]
        if "cameo_skin" in kwargs:
            self.save_data["cameo_skin"] = kwargs["cameo_skin"]
        if "coins" in kwargs:
            self.save_data["coins"] = kwargs["coins"]
        if "trophies" in kwargs:
            self.save_data["trophies"] = kwargs["trophies"]
        if "first_launch" in kwargs:
            self.save_data["first_launch"] = kwargs["first_launch"]
        if "map" in kwargs:
            self.save_data["map"] = kwargs["map"]
        
        # Сохраняем в файл
        self.write_save()
        print(f"💾 Игра сохранена")
    
    def get_coins(self):
        return self.save_data.get("coins", 0)
    
    def get_trophies(self):
        return self.save_data.get("trophies", 0)
    
    def get_last_character(self):
        return self.save_data.get("character", "1x1x1x1")
    
    def get_last_cameo(self):
        return self.save_data.get("cameo", "c00lk1d")
    
    def get_character_skin(self):
        return self.save_data.get("character_skin", "default")
    
    def get_cameo_skin(self):
        return self.save_data.get("cameo_skin", "default")
    
    def get_last_game_mode(self):
        """Возвращает последний выбранный режим игры"""
        return self.save_data.get("game_mode", "vs_bot")  # Возвращаем id (строчные)
    
    def is_first_launch(self):
        """Проверяет, первый ли это запуск игры"""
        return self.save_data.get("first_launch", True)
    
    def set_first_launch_false(self):
        """Устанавливает флаг первого запуска в False"""
        self.save_data["first_launch"] = False
        self.write_save()
    
    def get_map(self):
        """Возвращает выбранную карту"""
        return self.save_data.get("map", "random")
    
    def set_map(self, map_name):
        """Устанавливает карту"""
        self.save_data["map"] = map_name
        self.write_save()
    
    def add_coins(self, amount):
        coins = self.get_coins()
        self.save_data["coins"] = coins + amount
        self.write_save()
    
    def add_trophies(self, amount):
        trophies = self.get_trophies()
        self.save_data["trophies"] = trophies + amount
        self.write_save()
    
    def is_character_skin_unlocked(self, character, skin):
        character_key = character.lower()
        skin_key = skin.lower()
        
        if character_key not in self.save_data["character_skins"]:
            return False
        
        character_skins = self.save_data["character_skins"][character_key]
        return skin_key in character_skins and character_skins[skin_key]
    
    def unlock_character_skin(self, character, skin):
        character_key = character.lower()
        skin_key = skin.lower()
        
        if character_key not in self.save_data["character_skins"]:
            self.save_data["character_skins"][character_key] = {}
        
        self.save_data["character_skins"][character_key][skin_key] = True
        self.write_save()
        print(f"🔓 Разблокирован скин {character}.{skin}")
    
    def is_cameo_skin_unlocked(self, cameo, skin):
        cameo_key = cameo.lower()
        skin_key = skin.lower()
        
        if cameo_key not in self.save_data["cameo_skins"]:
            return False
        
        cameo_skins = self.save_data["cameo_skins"][cameo_key]
        return skin_key in cameo_skins and cameo_skins[skin_key]
    
    def unlock_cameo_skin(self, cameo, skin):
        cameo_key = cameo.lower()
        skin_key = skin.lower()
        
        if cameo_key not in self.save_data["cameo_skins"]:
            self.save_data["cameo_skins"][cameo_key] = {}
        
        self.save_data["cameo_skins"][cameo_key][skin_key] = True
        self.write_save()
        print(f"🔓 Разблокирован скин камео {cameo}.{skin}")
    
    def reset_save(self):
        """Сбрасывает сохранение к дефолтным значениям"""
        self.save_data = self.default_data.copy()
        self.write_save()
        print("🔄 Сохранение сброшено")