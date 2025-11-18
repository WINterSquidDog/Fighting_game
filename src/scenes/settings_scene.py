# src/scenes/settings_scene.py
import pygame
import os
from src.managers.game_manager import BaseScene

class SettingsScene(BaseScene):
    def __init__(self, gm):
        super().__init__(gm)
        self.settings_manager = self.gm.settings
        
        self.resolutions = [
            [1280, 720],
            [1366, 768], 
            [1920, 1080],
            [2560, 1440]
        ]
        
        self.languages = list(self.gm.settings.language_manager.available_languages.values())
        
        self.colors = {
            "background": (40, 40, 60),
            "header_bg": (30, 30, 50),
            "button_primary": (100, 150, 255),
            "button_secondary": (255, 100, 100),
            "text_light": (255, 255, 255),
            "text_dark": (200, 200, 200),
            "accent": (255, 215, 0),
            "slider_track": (80, 80, 100),
            "slider_fill": (100, 200, 255),
            "slider_thumb": (255, 255, 255),
            "selected": (100, 255, 100)
        }
        
        self.back_button = None
        self.slider_music = None
        self.slider_sound = None
        self.fullscreen_toggle = None
        self.resolution_buttons = []
        self.language_buttons = []
        self.apply_button = None
        
        self.dragging_music = False
        self.dragging_sound = False
        
        # Убрали диалог подтверждения
        self.show_confirm_dialog = False
    
    def on_enter(self):
        """При входе в настройки просто обновляем громкость"""
        # ✅ Музыка продолжает играть, просто обновляем громкость
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.settings_manager.current_settings["music_volume"])
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._go_back()
                elif event.key == pygame.K_RETURN:
                    self._apply_settings()  # Теперь сразу применяем
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._handle_mouse_click(mouse_pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging_music = False
                    self.dragging_sound = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_music and self.slider_music:
                    self._update_music_volume(mouse_pos)
                elif self.dragging_sound and self.slider_sound:
                    self._update_sound_volume(mouse_pos)
    
    def _handle_mouse_click(self, mouse_pos):
        if self.back_button and self.back_button.collidepoint(mouse_pos):
            self._go_back()
            return
        
        if self.slider_music and self.slider_music.collidepoint(mouse_pos):
            self.dragging_music = True
            self._update_music_volume(mouse_pos)
        
        if self.slider_sound and self.slider_sound.collidepoint(mouse_pos):
            self.dragging_sound = True
            self._update_sound_volume(mouse_pos)
        
        if self.fullscreen_toggle and self.fullscreen_toggle.collidepoint(mouse_pos):
            self.settings_manager.current_settings["fullscreen"] = not self.settings_manager.current_settings["fullscreen"]
        
        for i, res_button in enumerate(self.resolution_buttons):
            if res_button.collidepoint(mouse_pos):
                self.settings_manager.current_settings["resolution"] = self.resolutions[i]
        
        for i, lang_button in enumerate(self.language_buttons):
            if lang_button.collidepoint(mouse_pos):
                self.settings_manager.current_settings["language"] = self.languages[i]
        
        if self.apply_button and self.apply_button.collidepoint(mouse_pos):
            self._apply_settings()  # Теперь сразу применяем
    
    def on_enter(self):
        """При входе в настройки просто обновляем громкость"""
        # ✅ Музыка продолжает играть, просто обновляем громкость
        self.gm.update_music_volume()

    def on_exit(self):
        """Убираем on_exit - музыка продолжает играть"""
        pass  # ✅ Музыка НЕ останавливается при выходе из настроек

    def _update_music_volume(self, mouse_pos):
        if not self.slider_music:
            return
        
        x = max(self.slider_music.left, min(mouse_pos[0], self.slider_music.right))
        progress = (x - self.slider_music.left) / self.slider_music.width
        
        self.settings_manager.current_settings["music_volume"] = max(0.0, min(1.0, progress))
        pygame.mixer.music.set_volume(self.settings_manager.current_settings["music_volume"])
        
        x = max(self.slider_music.left, min(mouse_pos[0], self.slider_music.right))
        progress = (x - self.slider_music.left) / self.slider_music.width
        
        self.settings_manager.current_settings["music_volume"] = max(0.0, min(1.0, progress))
        pygame.mixer.music.set_volume(self.settings_manager.current_settings["music_volume"])
    
    def _update_sound_volume(self, mouse_pos):
        if not self.slider_sound:
            return
        
        x = max(self.slider_sound.left, min(mouse_pos[0], self.slider_sound.right))
        progress = (x - self.slider_sound.left) / self.slider_sound.width
        
        self.settings_manager.current_settings["sound_volume"] = max(0.0, min(1.0, progress))
    
    def _apply_settings(self):
        """Применяет настройки без перезагрузки"""
        new_screen = self.settings_manager.apply_graphics_settings()
        if new_screen:
            self.gm.screen = new_screen
        
        # Устанавливаем язык
        self.settings_manager.set_language(self.settings_manager.current_settings["language"])
        
        self.settings_manager.save_settings()
        print("✅ Настройки применены")
        
        # НЕ перезагружаем игру, просто остаемся в настройках
    
    def _go_back(self):
        self.gm.set_scene("menu")
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        self._draw_background(screen)
        self._draw_header(screen)
        self._draw_settings_content(screen)
    
    def _draw_background(self, screen):
        screen.fill(self.colors["background"])
    
    def _draw_header(self, screen):
        header_height = 80
        header_rect = pygame.Rect(0, 0, screen.get_width(), header_height)
        pygame.draw.rect(screen, self.colors["header_bg"], header_rect)
        
        title_font = self.get_font(32, bold=True)
        title = title_font.render(self.gm.settings.get_text("settings"), True, self.colors["accent"])
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 25))
        
        # Кнопка назад
        back_font = self.get_font(18, bold=True)
        back_text = back_font.render(self.gm.settings.get_text("back"), True, self.colors["text_light"])
        back_button_width = max(120, back_text.get_width() + 30)
        back_button_height = 40
        self.back_button = pygame.Rect(20, 20, back_button_width, back_button_height)
        
        pygame.draw.rect(screen, self.colors["button_secondary"], self.back_button, border_radius=8)
        pygame.draw.rect(screen, self.colors["text_light"], self.back_button, 2, border_radius=8)
        screen.blit(back_text, (self.back_button.centerx - back_text.get_width() // 2,
                              self.back_button.centery - back_text.get_height() // 2))
    
    def _draw_settings_content(self, screen):
        margin = min(100, screen.get_width() * 0.08)
        content_rect = pygame.Rect(
            margin, 
            100,
            screen.get_width() - 2 * margin, 
            screen.get_height() - 180
        )
        
        sections = [
            (self.gm.settings.get_text("audio_settings"), self._draw_audio_settings, 120),
            (self.gm.settings.get_text("graphics_settings"), self._draw_graphics_settings, 150),
            (self.gm.settings.get_text("system_settings"), self._draw_system_settings, 120)
        ]
        
        total_fixed_height = sum(height for _, _, height in sections)
        remaining_height = content_rect.height - total_fixed_height
        extra_per_section = remaining_height // len(sections) if remaining_height > 0 else 0
        
        current_y = content_rect.y
        for i, (section_name, draw_function, base_height) in enumerate(sections):
            section_height = base_height + extra_per_section
            
            section_rect = pygame.Rect(
                content_rect.x,
                current_y,
                content_rect.width,
                section_height
            )
            
            pygame.draw.rect(screen, (50, 50, 70), section_rect, border_radius=10)
            pygame.draw.rect(screen, self.colors["text_light"], section_rect, 2, border_radius=10)
            
            section_font = self.get_font(24, bold=True)
            section_title = section_font.render(section_name, True, self.colors["text_light"])
            screen.blit(section_title, (section_rect.x + 20, section_rect.y + 15))
            
            draw_function(screen, section_rect)
            current_y += section_height + 10
    
    def _draw_audio_settings(self, screen, rect):
        y_offset = rect.y + 60
        
        # Левая колонка - тексты
        music_font = self.get_font(20)
        music_text = music_font.render(self.gm.settings.get_text("music_volume"), True, self.colors["text_light"])
        screen.blit(music_text, (rect.x + 30, y_offset))
        
        sound_font = self.get_font(20)
        sound_text = sound_font.render(self.gm.settings.get_text("sound_volume"), True, self.colors["text_light"])
        screen.blit(sound_text, (rect.x + 30, y_offset + 50))
        
        # Правая колонка - контролы
        controls_start_x = rect.x + rect.width * 0.6
        slider_width = rect.width * 0.3
        slider_height = 20
        
        # Слайдер музыки
        slider_y = y_offset - (slider_height - music_font.get_height()) // 2
        slider_rect = pygame.Rect(controls_start_x, slider_y, slider_width, slider_height)
        self.slider_music = slider_rect
        self._draw_slider(screen, slider_rect, self.settings_manager.current_settings["music_volume"])
        
        percent_font = self.get_font(18)
        percent_text = percent_font.render(f"{int(self.settings_manager.current_settings['music_volume'] * 100)}%", 
                                         True, self.colors["text_dark"])
        screen.blit(percent_text, (slider_rect.right + 15, slider_y))
        
        # Слайдер звуков
        sound_slider_y = y_offset + 50 - (slider_height - sound_font.get_height()) // 2
        sound_slider_rect = pygame.Rect(controls_start_x, sound_slider_y, slider_width, slider_height)
        self.slider_sound = sound_slider_rect
        self._draw_slider(screen, sound_slider_rect, self.settings_manager.current_settings["sound_volume"])
        
        sound_percent_text = percent_font.render(f"{int(self.settings_manager.current_settings['sound_volume'] * 100)}%", 
                                               True, self.colors["text_dark"])
        screen.blit(sound_percent_text, (sound_slider_rect.right + 15, sound_slider_y))
    
    def _draw_graphics_settings(self, screen, rect):
        y_offset = rect.y + 60
        
        # Левая колонка - тексты
        fullscreen_font = self.get_font(20)
        fullscreen_text = fullscreen_font.render(self.gm.settings.get_text("fullscreen"), True, self.colors["text_light"])
        screen.blit(fullscreen_text, (rect.x + 30, y_offset))
        
        resolution_font = self.get_font(20)
        resolution_text = resolution_font.render(self.gm.settings.get_text("resolution"), True, self.colors["text_light"])
        screen.blit(resolution_text, (rect.x + 30, y_offset + 50))
        
        # Правая колонка - контролы
        controls_start_x = rect.x + rect.width * 0.6
        
        # Переключатель полноэкранного режима
        toggle_height = 30
        toggle_y = y_offset - (toggle_height - fullscreen_font.get_height()) // 2
        toggle_width = 80
        toggle_rect = pygame.Rect(controls_start_x, toggle_y, toggle_width, toggle_height)
        self.fullscreen_toggle = toggle_rect
        
        if self.settings_manager.current_settings["fullscreen"]:
            pygame.draw.rect(screen, self.colors["button_primary"], toggle_rect, border_radius=15)
            toggle_text = self.gm.settings.get_text("on")
        else:
            pygame.draw.rect(screen, (100, 100, 100), toggle_rect, border_radius=15)
            toggle_text = self.gm.settings.get_text("off")
        
        pygame.draw.rect(screen, self.colors["text_light"], toggle_rect, 2, border_radius=15)
        
        toggle_font = self.get_font(16, bold=True)
        toggle_label = toggle_font.render(toggle_text, True, self.colors["text_light"])
        screen.blit(toggle_label, (toggle_rect.centerx - toggle_label.get_width() // 2,
                                toggle_rect.centery - toggle_label.get_height() // 2))
        
        # Кнопки разрешений
        self.resolution_buttons = []
        available_width = rect.width - (controls_start_x - rect.x) - 20
        button_spacing = 8
        
        button_width = (available_width - button_spacing) // 2
        button_height = 28
        
        resolution_start_y = y_offset + 50
        
        for i, resolution in enumerate(self.resolutions):
            row = i // 2
            col = i % 2
            
            btn_rect = pygame.Rect(
                controls_start_x + col * (button_width + button_spacing), 
                resolution_start_y + row * (button_height + button_spacing), 
                button_width, 
                button_height
            )
            
            self.resolution_buttons.append(btn_rect)
            
            is_selected = self.settings_manager.current_settings["resolution"] == resolution
            color = self.colors["button_primary"] if is_selected else (80, 80, 100)
            
            pygame.draw.rect(screen, color, btn_rect, border_radius=4)
            pygame.draw.rect(screen, self.colors["text_light"], btn_rect, 2, border_radius=4)
            
            res_text = self._get_resolution_text(resolution, button_width - 10)
            screen.blit(res_text, (btn_rect.centerx - res_text.get_width() // 2,
                                btn_rect.centery - res_text.get_height() // 2))

    def _get_resolution_text(self, resolution, max_width):
        base_text = f"{resolution[0]}x{resolution[1]}"
        font = self.get_font(12)
        text_surface = font.render(base_text, True, self.colors["text_light"])
        
        if text_surface.get_width() <= max_width:
            return text_surface
        
        short_text = f"{resolution[0]//1000}Kx{resolution[1]//1000}K" if resolution[0] >= 2000 else base_text
        short_surface = font.render(short_text, True, self.colors["text_light"])
        
        if short_surface.get_width() <= max_width:
            return short_surface
        
        small_font = self.get_font(10)
        return small_font.render(base_text, True, self.colors["text_light"])
    
    def _draw_system_settings(self, screen, rect):
        y_offset = rect.y + 60
        
        # Левая колонка - тексты
        language_font = self.get_font(20)
        language_text = language_font.render(self.gm.settings.get_text("language"), True, self.colors["text_light"])
        screen.blit(language_text, (rect.x + 30, y_offset))
        
        # Правая колонка - кнопки языков
        controls_start_x = rect.x + rect.width * 0.6
        button_width = 120
        button_height = 30
        button_spacing = 10
        
        self.language_buttons = []
        for i, language in enumerate(self.languages):
            btn_rect = pygame.Rect(
                controls_start_x + i * (button_width + button_spacing), 
                y_offset, 
                button_width, 
                button_height
            )
            self.language_buttons.append(btn_rect)
            
            is_selected = self.settings_manager.current_settings["language"] == language
            color = self.colors["button_primary"] if is_selected else (80, 80, 100)
            
            pygame.draw.rect(screen, color, btn_rect, border_radius=5)
            pygame.draw.rect(screen, self.colors["text_light"], btn_rect, 2, border_radius=5)
            
            lang_font = self.get_font(16)
            lang_text = lang_font.render(language, True, self.colors["text_light"])
            screen.blit(lang_text, (btn_rect.centerx - lang_text.get_width() // 2,
                                  btn_rect.centery - lang_text.get_height() // 2))
        
        # Кнопка применения
        apply_font = self.get_font(18, bold=True)
        apply_text = apply_font.render(self.gm.settings.get_text("apply"), True, self.colors["text_light"])
        apply_button_width = max(150, apply_text.get_width() + 40)
        apply_button_height = 40
        
        self.apply_button = pygame.Rect(
            rect.centerx - apply_button_width // 2, 
            y_offset + 80, 
            apply_button_width, 
            apply_button_height
        )
        
        pygame.draw.rect(screen, self.colors["button_primary"], self.apply_button, border_radius=8)
        pygame.draw.rect(screen, self.colors["text_light"], self.apply_button, 2, border_radius=8)
        screen.blit(apply_text, (self.apply_button.centerx - apply_text.get_width() // 2,
                               self.apply_button.centery - apply_text.get_height() // 2))
    
    def _draw_slider(self, screen, rect, progress):
        pygame.draw.rect(screen, self.colors["slider_track"], rect, border_radius=10)
        
        if progress > 0:
            fill_rect = pygame.Rect(rect.left, rect.top, int(rect.width * progress), rect.height)
            pygame.draw.rect(screen, self.colors["slider_fill"], fill_rect, border_radius=10)
        
        thumb_x = rect.left + int(rect.width * progress)
        thumb_rect = pygame.Rect(thumb_x - 6, rect.top - 5, 12, rect.height + 10)
        pygame.draw.rect(screen, self.colors["slider_thumb"], thumb_rect, border_radius=6)
        pygame.draw.rect(screen, self.colors["text_light"], thumb_rect, 2, border_radius=6)
        
        pygame.draw.rect(screen, self.colors["text_light"], rect, 2, border_radius=10)