# src/managers/save_manager.py
import json
import os

class SaveManager:
    def __init__(self, save_file="game_save.json"):
        self.save_file = save_file
        self.default_data = {
            "last_character": "1x1x1x1",
            "last_cameo": "C00lK1D", 
            "character_skin": "default",
            "cameo_skin": "default",
            "coins": 1250,
            "trophies": 1850
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
                print("✅ Загрузка сохранения выполнена")
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
            if character:
                self.data["last_character"] = character
            if cameo:
                self.data["last_cameo"] = cameo
            if character_skin:
                self.data["character_skin"] = character_skin
            if cameo_skin:
                self.data["cameo_skin"] = cameo_skin
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print("💾 Прогресс сохранен")
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
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