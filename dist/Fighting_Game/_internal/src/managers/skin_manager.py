# src/managers/skin_manager.py
import json
import os

class SkinManager:
    def __init__(self):
        self.skins_data = self._load_skins_data()
    
    def _load_skins_data(self):
        """Загружает данные о скинах"""
        return {
            "characters": {
                "1x1x1x1": {
                    "skins": {
                        "default": {
                            "name": "Timeless",
                            "unlocked": True,
                            "price": 0
                        }
                    },
                    "default_skin": "default"
                },
                "chara": {
                    "skins": {
                        "default": {
                            "name": "Determined", 
                            "unlocked": True,
                            "price": 0
                        }
                    },
                    "default_skin": "default"
                },
                "steve": {
                    "skins": {
                        "default": {
                            "name": "Builder",
                            "unlocked": True, 
                            "price": 0
                        }
                    },
                    "default_skin": "default"
                }
            },
            "cameos": {
                "c00lk1d": {
                    "skins": {
                        "default": {
                            "name": "Hacker",
                            "unlocked": True,
                            "price": 0
                        },
                        "tag_time": {
                            "name": "Tag Time",
                            "unlocked": True,
                            "price": 0
                        }
                    },
                    "default_skin": "default"
                },
                "papyrus": {
                    "skins": {
                        "default": {
                            "name": "The Great",
                            "unlocked": True,
                            "price": 0
                        }
                    },
                    "default_skin": "default"
                },
                "larry": {
                    "skins": {
                        "default": {
                            "name": "Lava Guy", 
                            "unlocked": True,
                            "price": 0
                        }
                    },
                    "default_skin": "default"
                }
            }
        }
    
    def get_character_skins(self, character_name):
        """Возвращает скины для персонажа"""
        return self.skins_data["characters"].get(character_name.lower(), {}).get("skins", {})
    
    def get_cameo_skins(self, cameo_name):
        """Возвращает скины для камео"""
        return self.skins_data["cameos"].get(cameo_name.lower(), {}).get("skins", {})
    
    def get_default_skin(self, character_name, is_cameo=False):
        """Возвращает скин по умолчанию"""
        category = "cameos" if is_cameo else "characters"
        return self.skins_data[category].get(character_name.lower(), {}).get("default_skin", "default")
    
    def is_skin_unlocked(self, character_name, skin_id, is_cameo=False):
        """Проверяет, разблокирован ли скин"""
        skins = self.get_cameo_skins(character_name) if is_cameo else self.get_character_skins(character_name)
        return skins.get(skin_id, {}).get("unlocked", False)