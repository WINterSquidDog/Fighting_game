from src.managers.game_manager import GameManager
import pygame
class Image:
    def __init__(self, gm: GameManager, screen, coords: tuple, size: tuple, pic_way: str):
        self.resolution: tuple[int, int] = gm.settings.current_settings["resolution"]
        self.is_fullscreen: bool = gm.settings.current_settings["fullscreen"]
        self.base_coords = coords
        self.base_size = size
        self.pic = pygame.image.load(pic_way).convert_alpha()
        self.screen = screen
        if not self.is_fullscreen:
            self.sizer_nf()
            self.pic = pygame.transform.scale(self.pic, self.base_size)
        else:
            self.sizer_f()
   
    def sizer_nf(self):
        self.coords = [self.base_coords[0] * (self.resolution[0] / 1280), self.base_coords * (self.resolution[1] / 720)]
        self.base_size = (self.base_size[0] * (self.resolution[0] / 1280), self.base_size * (self.resolution[1] / 720))

    def sizer_f(self):
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        self.coords = [self.base_coords[0] * (screen_width / 1280), self.base_coords * (screen_height / 720)]
        self.base_size = (self.base_coords[0] * (self.resolution[0] / 1280), self.base_coords * (self.resolution[1] / 720))

    def draw(self):
        self.screen.blit(self.pic, self.coords)

class Text:
    def __init__(self, gm: GameManager, screen, coords: tuple, size: int, text: str, font):
        self.resolution: tuple[int, int] = gm.settings.current_settings["resolution"]
        self.is_fullscreen: bool = gm.settings.current_settings["fullscreen"]
        self.screen = screen
        self.base_coords = coords
        self.base_size = size
        self.text = text
        self.font = font

    def sizer_nf(self):
        self.coords = [self.base_coords[0] * (self.resolution[0] / 1280), self.base_coords * (self.resolution[1] / 720)]
        self.base_size = (self.base_coords[0] * (self.resolution[0] / 1280), self.base_coords * (self.resolution[1] / 720))

    def sizer_f(self):
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        self.coords = [self.base_coords[0] * (screen_width / 1280), self.base_coords * (screen_height / 720)]
        self.base_size = (self.base_coords[0] * (self.resolution[0] / 1280), self.base_coords * (self.resolution[1] / 720))
