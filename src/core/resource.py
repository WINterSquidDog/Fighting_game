import sys
import os
def resource_path(relative_path):
    """ Получает правильный путь к ресурсам для .exe """
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)