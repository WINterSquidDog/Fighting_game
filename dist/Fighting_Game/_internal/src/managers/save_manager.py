# src/managers/save_manager.py
import json
import sys
import os
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SaveManager:
    def __init__(self, save_file=None):
        self.save_file = save_file or "game_save.json"
        if not os.path.isabs(self.save_file):
            self.save_file = resource_path(self.save_file)
        self.default_data = {
            "last_character": "1x1x1x1",
            "last_cameo": "C00lK1D", 
            "character_skin": "default",
            "cameo_skin": "default",
            "coins": 1250,
            "trophies": 1850,
            "unlocked_skins": {  # ДОБАВЛЕНО: Храним разблокированные скины
                "character": {},
                "cameo": {}
            }
        }
        self.data = self.default_data.copy()
        
    def load_save(self):
        """Загружает данные сохранения из файла"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    # Обновляем только существующие ключи
                    for key, value in loaded_data.items():
                        if key in self.data:
                            self.data[key] = value
                
                # ДОБАВЛЕНО: Проверяем структуру unlocked_skins
                if "unlocked_skins" not in self.data:
                    self.data["unlocked_skins"] = {"character": {}, "cameo": {}}
                elif "character" not in self.data["unlocked_skins"]:
                    self.data["unlocked_skins"]["character"] = {}
                elif "cameo" not in self.data["unlocked_skins"]:
                    self.data["unlocked_skins"]["cameo"] = {}
                
                print("✅ Загрузка сохранения выполнена")
                print(f"💰 Разблокированные скины: {self.data['unlocked_skins']}")
                return True
            else:
                self.create_default_save()
                return False
        except Exception as e:
            print(f"❌ Ошибка загрузки сохранения: {e}")
            self.create_default_save()
            return False
    
    def create_default_save(self):
        """Создает файл сохранения с настройками по умолчанию"""
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.default_data, f, ensure_ascii=False, indent=2)
            print("✅ Создан файл сохранения по умолчанию")
        except Exception as e:
            print(f"❌ Ошибка создания файла сохранения: {e}")
    
    def save_game(self, character=None, cameo=None, character_skin=None, cameo_skin=None):
        """Сохраняет текущий прогресс"""
        try:
            print(f"💾 Начало сохранения: char={character}, cameo={cameo}")
            
            if character is not None:
                self.data["last_character"] = character
                print(f"💾 Установлен персонаж: {character}")
            if cameo is not None:
                self.data["last_cameo"] = cameo
                print(f"💾 Установлено камео: {cameo}")
            if character_skin is not None:
                self.data["character_skin"] = character_skin
            if cameo_skin is not None:
                self.data["cameo_skin"] = cameo_skin
            
            print(f"💾 Данные перед сохранением: {self.data}")
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print("💾 Файл сохранения записан")
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    # ДОБАВЛЕНО: Методы для работы со скинами
    
    def unlock_character_skin(self, character_name, skin_id):
        """Разблокирует скин персонажа"""
        if "unlocked_skins" not in self.data:
            self.data["unlocked_skins"] = {"character": {}, "cameo": {}}
        
        if character_name not in self.data["unlocked_skins"]["character"]:
            self.data["unlocked_skins"]["character"][character_name] = []
        
        if skin_id not in self.data["unlocked_skins"]["character"][character_name]:
            self.data["unlocked_skins"]["character"][character_name].append(skin_id)
            print(f"✅ Скин разблокирован: {character_name}.{skin_id}")
            self.save_game()  # Сохраняем изменения
            return True
        return False
    
    def unlock_cameo_skin(self, cameo_name, skin_id):
        """Разблокирует скин камео"""
        if "unlocked_skins" not in self.data:
            self.data["unlocked_skins"] = {"character": {}, "cameo": {}}
        
        if cameo_name not in self.data["unlocked_skins"]["cameo"]:
            self.data["unlocked_skins"]["cameo"][cameo_name] = []
        
        if skin_id not in self.data["unlocked_skins"]["cameo"][cameo_name]:
            self.data["unlocked_skins"]["cameo"][cameo_name].append(skin_id)
            print(f"✅ Скин камео разблокирован: {cameo_name}.{skin_id}")
            self.save_game()  # Сохраняем изменения
            return True
        return False
    
    def is_character_skin_unlocked(self, character_name, skin_id):
        """Проверяет, разблокирован ли скин персонажа"""
        if ("unlocked_skins" in self.data and 
            "character" in self.data["unlocked_skins"] and
            character_name in self.data["unlocked_skins"]["character"]):
            return skin_id in self.data["unlocked_skins"]["character"][character_name]
        return False
    
    def is_cameo_skin_unlocked(self, cameo_name, skin_id):
        """Проверяет, разблокирован ли скин камео"""
        if ("unlocked_skins" in self.data and 
            "cameo" in self.data["unlocked_skins"] and
            cameo_name in self.data["unlocked_skins"]["cameo"]):
            return skin_id in self.data["unlocked_skins"]["cameo"][cameo_name]
        return False
    
    def get_all_unlocked_skins(self):
        """Возвращает все разблокированные скины"""
        return self.data.get("unlocked_skins", {"character": {}, "cameo": {}})
    
    # Старые методы остаются без изменений
    
    def get_last_character(self):
        return self.data["last_character"]
    
    def get_last_cameo(self):
        return self.data["last_cameo"]
    
    def get_character_skin(self):
        return self.data["character_skin"]
    
    def get_cameo_skin(self):
        return self.data["cameo_skin"]
    
    def get_coins(self):
        return self.data["coins"]
    
    def get_trophies(self):
        return self.data["trophies"]