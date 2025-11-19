# src/scenes/shop_scene.py
import pygame
import os
from src.managers.game_manager import BaseScene

class ShopScene(BaseScene):
    def __init__(self, gm):
        super().__init__(gm)
        self.save_manager = gm.save_manager
        
        self.colors = {
            "background": (20, 20, 40),
            "header_bg": (30, 30, 50),
            "card_bg": (50, 50, 80),
            "card_locked": (80, 50, 50),
            "card_unlocked": (50, 80, 50),
            "button_primary": (100, 150, 255),
            "button_secondary": (255, 100, 100),
            "text_light": (255, 255, 255),
            "text_dark": (200, 200, 200),
            "accent": (255, 215, 0),
            "price_color": (255, 200, 100)
        }
        
        # Все доступные скины для продажи
        self.shop_items = [
            # Персонажи
            {"type": "character", "character": "steve", "skin_id": "two_faced", "name": "Two Faced Steve", "price": 500, "unlocked": False},
            # Можно добавить больше скинов здесь
        ]
        
        self.selected_item = 0
        self.back_button = None
        self.buy_button = None
        
    def on_enter(self):
        self._update_items_status()
        
    def _update_items_status(self):
        """Обновляет статус разблокировки скинов"""
        for item in self.shop_items:
            if item["type"] == "character":
                # Проверяем через skin_manager или по сохранениям
                item["unlocked"] = self.gm.skin_manager.is_skin_unlocked(item["character"], item["skin_id"])
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._go_back()
                elif event.key == pygame.K_LEFT:
                    self.selected_item = (self.selected_item - 1) % len(self.shop_items)
                elif event.key == pygame.K_RIGHT:
                    self.selected_item = (self.selected_item + 1) % len(self.shop_items)
                elif event.key == pygame.K_RETURN:
                    self._buy_item()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.back_button and self.back_button.collidepoint(mouse_pos):
                        self._go_back()
                    elif self.buy_button and self.buy_button.collidepoint(mouse_pos):
                        self._buy_item()
    
    def _buy_item(self):
        """Покупка выбранного предмета"""
        if not self.shop_items:
            return
            
        item = self.shop_items[self.selected_item]
        
        if item["unlocked"]:
            print(f"ℹ️ Скин {item['name']} уже разблокирован")
            return
            
        player_coins = self.save_manager.get_coins()
        
        if player_coins >= item["price"]:
            # Списание монет
            self.save_manager.data["coins"] = player_coins - item["price"]
            self.save_manager.save_game()
            
            # Разблокировка скина
            item["unlocked"] = True
            # Здесь нужно также обновить skin_manager
            
            print(f"✅ Куплен скин: {item['name']} за {item['price']} монет")
        else:
            print(f"❌ Недостаточно монет для {item['name']}")
    
    def _go_back(self):
        self.gm.set_scene("menu")
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        self._draw_background(screen)
        self._draw_header(screen)
        self._draw_shop_content(screen)
    
    def _draw_background(self, screen):
        screen.fill(self.colors["background"])
    
    def _draw_header(self, screen):
        header_height = 80
        header_rect = pygame.Rect(0, 0, screen.get_width(), header_height)
        pygame.draw.rect(screen, self.colors["header_bg"], header_rect)
        
        title_font = self.get_font(32, bold=True)
        title = title_font.render("МАГАЗИН", True, self.colors["accent"])
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 25))
        
        # Кнопка назад
        back_font = self.get_font(18, bold=True)
        back_text = back_font.render("НАЗАД", True, self.colors["text_light"])
        back_button_width = max(120, back_text.get_width() + 30)
        self.back_button = pygame.Rect(20, 20, back_button_width, 40)
        
        pygame.draw.rect(screen, self.colors["button_secondary"], self.back_button, border_radius=8)
        pygame.draw.rect(screen, self.colors["text_light"], self.back_button, 2, border_radius=8)
        screen.blit(back_text, (self.back_button.centerx - back_text.get_width() // 2,
                              self.back_button.centery - back_text.get_height() // 2))
        
        # Монеты игрока
        coins_font = self.get_font(20)
        coins_text = coins_font.render(f"Монеты: {self.save_manager.get_coins()}", True, self.colors["accent"])
        screen.blit(coins_text, (screen.get_width() - coins_text.get_width() - 30, 30))
    
    def _draw_shop_content(self, screen):
        if not self.shop_items:
            self._draw_empty_shop(screen)
            return
            
        item = self.shop_items[self.selected_item]
        card_size = self.s(300)
        
        # Карточка товара
        card_rect = pygame.Rect(
            screen.get_width() // 2 - card_size // 2,
            screen.get_height() // 2 - card_size // 2 - 50,
            card_size,
            card_size
        )
        
        # Фон карточки
        card_color = self.colors["card_unlocked"] if item["unlocked"] else self.colors["card_locked"]
        pygame.draw.rect(screen, card_color, card_rect, border_radius=15)
        pygame.draw.rect(screen, self.colors["text_light"], card_rect, 3, border_radius=15)
        
        # Название скина
        name_font = self.get_font(24, bold=True)
        name_text = name_font.render(item["name"], True, self.colors["text_light"])
        screen.blit(name_text, (screen.get_width() // 2 - name_text.get_width() // 2, card_rect.top - 40))
        
        # Цена
        price_font = self.get_font(20)
        if item["unlocked"]:
            price_text = price_font.render("КУПЛЕНО", True, self.colors["text_dark"])
        else:
            price_text = price_font.render(f"Цена: {item['price']} монет", True, self.colors["price_color"])
        screen.blit(price_text, (screen.get_width() // 2 - price_text.get_width() // 2, card_rect.bottom + 20))
        
        # Кнопка покупки
        if not item["unlocked"]:
            btn_width = self.s(200)
            btn_height = self.s(50)
            self.buy_button = pygame.Rect(
                screen.get_width() // 2 - btn_width // 2,
                card_rect.bottom + 60,
                btn_width,
                btn_height
            )
            
            can_afford = self.save_manager.get_coins() >= item["price"]
            btn_color = self.colors["button_primary"] if can_afford else (100, 100, 100)
            
            pygame.draw.rect(screen, btn_color, self.buy_button, border_radius=10)
            pygame.draw.rect(screen, self.colors["text_light"], self.buy_button, 2, border_radius=10)
            
            btn_font = self.get_font(20, bold=True)
            btn_text = btn_font.render("КУПИТЬ", True, self.colors["text_light"])
            screen.blit(btn_text, (self.buy_button.centerx - btn_text.get_width() // 2,
                                 self.buy_button.centery - btn_text.get_height() // 2))
    
    def _draw_empty_shop(self, screen):
        empty_font = self.get_font(24)
        empty_text = empty_font.render("Магазин пуст. Зайдите позже!", True, self.colors["text_dark"])
        screen.blit(empty_text, (screen.get_width() // 2 - empty_text.get_width() // 2,
                               screen.get_height() // 2 - empty_text.get_height() // 2))
    
    def on_enter(self):
        print("🎮 Магазин открыт!")
        self._update_items_status()