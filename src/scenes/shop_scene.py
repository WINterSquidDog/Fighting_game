# src/scenes/shop_scene.py
import pygame
import random
from src.managers.game_manager import BaseScene
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

class ShopScene(BaseScene):
    def __init__(self, gm):
        super().__init__(gm)
        
        # Цветовая схема
        self.colors = {
            "background": (20, 20, 40),
            "header_bg": (30, 30, 50),
            "button_primary": (255, 100, 100),
            "button_secondary": (100, 150, 255),
            "button_tertiary": (100, 200, 100),
            "text_light": (255, 255, 255),
            "text_dark": (200, 200, 200),
            "accent": (255, 215, 0),
            "danger": (255, 80, 80),
            "selected": (100, 255, 100),
            "locked": (150, 150, 150),
            "discount": (255, 100, 100)
        }
        
        # Получаем менеджер сохранений
        self.save_manager = gm.save_manager
        self.save_manager.load_save()
        
        # Данные игрока
        self.player_coins = self.save_manager.get_coins()
        self.player_trophies = self.save_manager.get_trophies()
        
        # Вкладки магазина
        self.tabs = ["АКЦИИ", "ПОДАРОК", "СКИНЫ", "ВАЛЮТА"]
        self.current_tab = 2  # По умолчанию открываем скины
        
        # Скины для продажи
        self.skins_for_sale = []
        self.selected_skin_index = 0
        self.load_skins_for_sale()
        
        # Валюта для продажи - ТЕСТОВАЯ ВЕРСИЯ
        self.currency_packs = [
            {"name": "ТЕСТОВЫЙ НАБОР 1", "coins": 100, "price": 0, "icon": "💰", "real_price": 0},
            {"name": "ТЕСТОВЫЙ НАБОР 2", "coins": 500, "price": 0, "icon": "💰💰", "real_price": 0},
            {"name": "ТЕСТОВЫЙ НАБОР 3", "coins": 1000, "price": 0, "icon": "💰💰💰", "real_price": 0},
            {"name": "ТЕСТОВЫЙ НАБОР 4", "coins": 5000, "price": 0, "icon": "👑", "real_price": 0},
        ]
        self.selected_currency_index = 0
        
        # Акции (пока пусто)
        self.sales_items = []
        
        # Ежедневный подарок (пока пусто)
        self.daily_gift = None
        
        # Анимация покупки
        self.purchase_animation = False
        self.purchase_animation_time = 0
        self.purchase_animation_item = None
        
        # Кнопки
        self.tab_buttons = []
        self.buy_button = None
        self.currency_buy_button = None
        self.back_button = None
        
        # Частицы для анимации
        self.particles = []
        
        # Стрелки навигации (фикс для кнопок влево/вправо)
        self.skin_left_btn_rect = None
        self.skin_right_btn_rect = None
        
        # Сообщение о блокировке скина (фикс бага с зависанием)
        self.locked_skin_message = False
        self.locked_skin_message_time = 0
        
    def load_skins_for_sale(self):
        """Загружает все скины, доступные для покупки с учетом сохранений"""
        self.skins_for_sale = []
        
        # Получаем ссылку на menu_scene для доступа к скинам
        menu_scene = self.gm.get_scene("menu")
        
        if menu_scene and hasattr(menu_scene, 'character_skins'):
            # Скины персонажей
            for char_name, skins in menu_scene.character_skins.items():
                for skin_id, skin_data in skins.items():
                    # Пропускаем дефолтные скины и всегда разблокированные
                    if skin_id == "default" or skin_data.get("unlocked", False):
                        continue
                    
                    # Проверяем разблокирован ли скин через save_manager
                    is_unlocked = self.save_manager.is_character_skin_unlocked(char_name, skin_id)
                    
                    # Добавляем только если не разблокирован И цена > 0
                    if not is_unlocked and skin_data.get("price", 0) > 0:
                        # ЗАГРУЖАЕМ КАРТОЧКИ ПРАВИЛЬНО - как в MenuScene
                        card_size = self._get_card_size()
                        
                        # ИСПРАВЛЕНИЕ: Правильные пути к файлам карточек
                        normal_filename = f"{char_name}_{skin_id}_normal.jpg"
                        special_filename = f"{char_name}_{skin_id}_special.jpg"
                        
                        # Используем те же методы загрузки что и в MenuScene
                        card_normal = self._load_card_image(normal_filename, False, card_size)
                        card_special = self._load_card_image(special_filename, True, card_size)
                        
                        print(f"🛍️ Скин для продажи {char_name}.{skin_id}: price={skin_data.get('price', 0)}, unlocked={is_unlocked}")
                        
                        self.skins_for_sale.append({
                            "type": "character",
                            "char_name": char_name,
                            "skin_id": skin_id,
                            "name": skin_data.get("name", f"Скин {skin_id}"),
                            "price": skin_data.get("price", 100),
                            "unlocked": is_unlocked,
                            "card_normal": card_normal,
                            "card_special": card_special
                        })
        
        if menu_scene and hasattr(menu_scene, 'cameo_skins'):
            # Скины камео
            for cameo_name, skins in menu_scene.cameo_skins.items():
                for skin_id, skin_data in skins.items():
                    if skin_id == "default" or skin_data.get("unlocked", False):
                        continue
                    
                    # Проверяем разблокирован ли скин через save_manager
                    is_unlocked = self.save_manager.is_cameo_skin_unlocked(cameo_name, skin_id)
                    
                    # Добавляем только если не разблокирован И цена > 0
                    if not is_unlocked and skin_data.get("price", 0) > 0:
                        card_size = self._get_card_size()
                        
                        # ИСПРАВЛЕНИЕ: Правильные пути к файлам карточек
                        normal_filename = f"{cameo_name}_{skin_id}_normal.jpg"
                        special_filename = f"{cameo_name}_{skin_id}_special.jpg"
                        
                        card_normal = self._load_card_image(normal_filename, False, card_size)
                        card_special = self._load_card_image(special_filename, True, card_size)
                        
                        print(f"🛍️ Камео скин для продажи {cameo_name}.{skin_id}: price={skin_data.get('price', 0)}, unlocked={is_unlocked}")
                        
                        self.skins_for_sale.append({
                            "type": "cameo",
                            "cameo_name": cameo_name,
                            "skin_id": skin_id,
                            "name": skin_data.get("name", f"Скин {skin_id}"),
                            "price": skin_data.get("price", 100),
                            "unlocked": is_unlocked,
                            "card_normal": card_normal,
                            "card_special": card_special
                        })
        
        print(f"🛍️ Загружено {len(self.skins_for_sale)} скинов для продажи")
        
        # Сортируем по цене (от дешевых к дорогим)
        self.skins_for_sale.sort(key=lambda x: x["price"])
    
    def _get_card_size(self):
        """Определяем размер карточки как в MenuScene"""
        base_size = 280
        
        if self.gm.settings.scale_factor > 1.5:
            return int(base_size * 1.3)
        elif self.gm.settings.scale_factor > 1.2:
            return int(base_size * 1.15)
        return base_size
    
    def _load_card_image(self, filename, is_special, card_size):
        """Загрузка карточки с указанным размером - как в MenuScene"""
        # ИСПРАВЛЕНИЕ: Правильный путь к карточкам - Sprites/cards/filename
        card_path = resource_path(os.path.join("Sprites", "cards", filename))
        
        try:
            if os.path.exists(card_path):
                print(f"✅ Загружаем карточку: {card_path}")
                card = pygame.image.load(card_path).convert_alpha()
                card = pygame.transform.scale(card, (card_size, card_size))
                return card
            else:
                print(f"⚠️ Карточка не найдена: {card_path}")
                
                # Пробуем найти в альтернативных местах
                alt_paths = [
                    resource_path(os.path.join("Sprites", "cards", filename.lower())),
                    resource_path(os.path.join("sprites", "cards", filename)),
                    resource_path(os.path.join("sprites", "cards", filename.lower())),
                ]
                
                for alt_path in alt_paths:
                    if os.path.exists(alt_path):
                        print(f"✅ Найдена альтернативная карточка: {alt_path}")
                        card = pygame.image.load(alt_path).convert_alpha()
                        card = pygame.transform.scale(card, (card_size, card_size))
                        return card
                
                # Если нигде не нашли, создаем заглушку
                return self._create_placeholder_card(filename, is_special, card_size)
        except Exception as e:
            print(f"❌ Ошибка загрузки карточки {card_path}: {e}")
            return self._create_placeholder_card(filename, is_special, card_size)
    
    def _create_placeholder_card(self, filename, is_special, card_size):
        """Создание заглушки для карточки - как в MenuScene"""
        card = pygame.Surface((card_size, card_size), pygame.SRCALPHA)
        
        if is_special:
            card.fill((180, 150, 50, 255))
            border = max(3, card_size // 40)
            pygame.draw.rect(card, (255, 215, 0), (card_size//20, card_size//20, card_size*0.9, card_size*0.9), border)
            pygame.draw.rect(card, (100, 255, 100), (card_size//40, card_size//40, card_size*0.95, card_size*0.95), border//2)
        else:
            card.fill((80, 80, 150, 255))
            border = max(3, card_size // 40)
            pygame.draw.rect(card, (255, 255, 255), (card_size//20, card_size//20, card_size*0.9, card_size*0.9), border)
        
        placeholder_text = "ЗАГЛУШКА"
        filename_text = filename
        
        font_size = max(10, card_size // 12)
        font = pygame.font.SysFont("arial", font_size)
        status = "SPECIAL" if is_special else "NORMAL"
        text = font.render(f"{filename_text}", True, (255, 255, 255))
        card.blit(text, (card_size//20, card_size//2))
        
        placeholder_font = pygame.font.SysFont("arial", max(12, card_size//10), bold=True)
        placeholder_render = placeholder_font.render(placeholder_text, True, (255, 255, 255))
        card.blit(placeholder_render, (card_size//2 - placeholder_render.get_width()//2, card_size//3))
        
        return card
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gm.set_scene("menu")
                elif event.key == pygame.K_LEFT:
                    if self.current_tab == 2 and self.skins_for_sale:  # Скины
                        # ФИКС: Должна работать даже во время анимации покупки
                        if not self.purchase_animation:
                            self.selected_skin_index = (self.selected_skin_index - 1) % len(self.skins_for_sale)
                    elif self.current_tab == 3:  # Валюта
                        # ФИКС: Должна работать даже во время анимации покупки
                        if not self.purchase_animation:
                            self.selected_currency_index = (self.selected_currency_index - 1) % len(self.currency_packs)
                elif event.key == pygame.K_RIGHT:
                    if self.current_tab == 2 and self.skins_for_sale:  # Скины
                        # ФИКС: Должна работать даже во время анимации покупки
                        if not self.purchase_animation:
                            self.selected_skin_index = (self.selected_skin_index + 1) % len(self.skins_for_sale)
                    elif self.current_tab == 3:  # Валюта
                        # ФИКС: Должна работать даже во время анимации покупки
                        if not self.purchase_animation:
                            self.selected_currency_index = (self.selected_currency_index + 1) % len(self.currency_packs)
                elif event.key == pygame.K_RETURN:
                    # ФИКС: Не работаем во время анимации покупки
                    if self.purchase_animation:
                        return
                        
                    if self.current_tab == 2 and self.skins_for_sale:  # Скины
                        self.buy_selected_skin()
                    elif self.current_tab == 3:  # Валюта
                        self.buy_selected_currency()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # ФИКС: Не обрабатываем клики во время анимации покупки
                    if self.purchase_animation:
                        return
                    self.handle_mouse_click(mouse_pos)
    
    def handle_mouse_click(self, mouse_pos):
        """Обработка кликов мыши"""
        # Клики по вкладкам
        for i, tab_rect in enumerate(self.tab_buttons):
            if tab_rect.collidepoint(mouse_pos):
                self.current_tab = i
                return
        
        # Кнопка "Купить" для скинов
        if self.current_tab == 2 and self.buy_button and self.buy_button.collidepoint(mouse_pos):
            self.buy_selected_skin()
        
        # Кнопка "Купить" для валюты
        elif self.current_tab == 3 and self.currency_buy_button and self.currency_buy_button.collidepoint(mouse_pos):
            self.buy_selected_currency()
        
        # Кнопка "Назад"
        elif self.back_button and self.back_button.collidepoint(mouse_pos):
            self.gm.set_scene("menu")
        
        # ФИКС: Обработка кликов по стрелкам навигации скинов
        elif self.current_tab == 2 and self.skins_for_sale:
            if self.skin_left_btn_rect and self.skin_left_btn_rect.collidepoint(mouse_pos):
                self.selected_skin_index = (self.selected_skin_index - 1) % len(self.skins_for_sale)
            elif self.skin_right_btn_rect and self.skin_right_btn_rect.collidepoint(mouse_pos):
                self.selected_skin_index = (self.selected_skin_index + 1) % len(self.skins_for_sale)
    
    def buy_selected_skin(self):
        """Покупка выбранного скина - ИСПРАВЛЕНА ДЛЯ СОХРАНЕНИЯ"""
        if not self.skins_for_sale or self.selected_skin_index >= len(self.skins_for_sale):
            return
        
        skin = self.skins_for_sale[self.selected_skin_index]
        
        # Если уже куплен, не покупаем снова
        if skin["unlocked"]:
            print(f"ℹ️ Скин {skin['name']} уже куплен")
            return
        
        # Проверяем достаточно ли денег
        if self.player_coins >= skin["price"]:
            # Списываем деньги
            self.player_coins -= skin["price"]
            
            # Сохраняем новые монеты в менеджер сохранений
            self.save_manager.data["coins"] = self.player_coins
            
            # Разблокируем скин в сохранениях
            if skin["type"] == "character":
                self.save_manager.unlock_character_skin(skin["char_name"], skin["skin_id"])
            else:  # cameo
                self.save_manager.unlock_cameo_skin(skin["cameo_name"], skin["skin_id"])
            
            # Сохраняем изменения
            self.save_manager.save_game()
            
            # Отмечаем скин как купленный в списке магазина
            skin["unlocked"] = True
            
            # Получаем menu_scene для обновления данных
            menu_scene = self.gm.get_scene("menu")
            
            # Обновляем данные в menu_scene
            if menu_scene:
                if skin["type"] == "character":
                    if skin["char_name"] in menu_scene.character_skins:
                        menu_scene.character_skins[skin["char_name"]][skin["skin_id"]]["unlocked"] = True
                        
                        # Обновляем current_skins если мы в меню скинов
                        if hasattr(menu_scene, 'current_section') and menu_scene.current_section == 3:
                            menu_scene._refresh_current_skins()
                else:  # cameo
                    if skin["cameo_name"] in menu_scene.cameo_skins:
                        menu_scene.cameo_skins[skin["cameo_name"]][skin["skin_id"]]["unlocked"] = True
            
            # Обновляем баланс в меню сцене
            if menu_scene:
                menu_scene.player_data["coins"] = self.player_coins
                menu_scene.save_manager.data["coins"] = self.player_coins
            
            # Создаем частицы для анимации
            self.create_particles()
            
            # Запускаем анимацию покупки
            self.purchase_animation = True
            self.purchase_animation_time = pygame.time.get_ticks()
            self.purchase_animation_item = skin
            
            print(f"✅ Куплен скин {skin['name']} за {skin['price']} монет. Баланс: {self.player_coins}")
            print(f"💾 Скин сохранен как разблокированный: {skin['char_name'] if skin['type'] == 'character' else skin['cameo_name']}.{skin['skin_id']}")
        else:
            print(f"❌ Недостаточно монет для покупки скина {skin['name']}")
            # ФИКС: Показываем сообщение о недостатке денег
            self.locked_skin_message = True
            self.locked_skin_message_time = pygame.time.get_ticks()
    
    def buy_selected_currency(self):
        """Покупка выбранного набора валюты - ТЕСТОВАЯ ВЕРСИЯ"""
        currency = self.currency_packs[self.selected_currency_index]
        
        print(f"🛒 Тестовая покупка набора валюты: {currency['name']} за {currency['real_price']} рублей (БЕСПЛАТНО)")
        
        # ТЕСТОВАЯ ВЕРСИЯ: просто добавляем монеты
        self.player_coins += currency["coins"]
        
        # Сохраняем новые монеты
        self.save_manager.data["coins"] = self.player_coins
        self.save_manager.save_game()
        
        # Обновляем данные в меню
        menu_scene = self.gm.get_scene("menu")
        if menu_scene:
            menu_scene.player_data["coins"] = self.player_coins
            menu_scene.save_manager.data["coins"] = self.player_coins
        
        print(f"💰 Получено {currency['coins']} монет. Новый баланс: {self.player_coins}")
        
        # Создаем частицы для анимации
        self.create_particles()
        
        # Запускаем анимацию
        self.purchase_animation = True
        self.purchase_animation_time = pygame.time.get_ticks()
        self.purchase_animation_item = currency
    
    def create_particles(self):
        """Создает частицы для анимации покупки"""
        self.particles = []
        screen = pygame.display.get_surface()  # Получаем текущий экран
        if not screen:
            return
            
        screen_width, screen_height = screen.get_size()
        
        for _ in range(30):  # Создаем 30 частиц
            self.particles.append({
                "x": random.randint(0, screen_width),
                "y": random.randint(0, screen_height),
                "size": random.randint(3, 8),
                "color": random.choice([(255, 215, 0), (255, 100, 100), (100, 255, 100), (100, 150, 255)]),
                "speed_x": random.uniform(-2, 2),
                "speed_y": random.uniform(-2, 2),
                "life": 1.0  # Время жизни частицы (1.0 = 100%)
            })
    
    def update(self, dt):
        """Обновление сцены"""
        # Обновляем частицы
        for particle in self.particles[:]:
            particle["x"] += particle["speed_x"]
            particle["y"] += particle["speed_y"]
            particle["life"] -= 0.02  # Уменьшаем время жизни
            
            if particle["life"] <= 0:
                self.particles.remove(particle)
        
        if self.purchase_animation:
            current_time = pygame.time.get_ticks()
            if current_time - self.purchase_animation_time > 2000:  # 2 секунды
                self.purchase_animation = False
                self.purchase_animation_item = None
                self.particles = []
        
        # ФИКС: Обновление сообщения о блокировке скина
        if self.locked_skin_message:
            current_time = pygame.time.get_ticks()
            if current_time - self.locked_skin_message_time > 1500:
                self.locked_skin_message = False
    
    def draw(self, screen):
        """Отрисовка сцены"""
        self.draw_background(screen)
        self.draw_header(screen)
        self.draw_tabs(screen)
        
        # Отрисовка контента в зависимости от текущей вкладки
        content_rect = pygame.Rect(0, self.s(140), screen.get_width(), screen.get_height() - self.s(180))
        
        if self.current_tab == 0:
            self.draw_sales_tab(screen, content_rect)
        elif self.current_tab == 1:
            self.draw_gift_tab(screen, content_rect)
        elif self.current_tab == 2:
            self.draw_skins_tab(screen, content_rect)
        elif self.current_tab == 3:
            self.draw_currency_tab(screen, content_rect)
        
        self.draw_bottom_bar(screen)
        
        # Отрисовка анимации покупки поверх всего
        if self.purchase_animation:
            self.draw_purchase_animation(screen)
        
        # ФИКС: Отрисовка сообщения о блокировке скина
        if self.locked_skin_message:
            self.draw_locked_skin_message(screen)
    
    def draw_background(self, screen):
        """Отрисовка фона"""
        screen.fill(self.colors["background"])
        
        # Градиентный фон
        for i in range(screen.get_height()):
            color = (20 + i//20, 20 + i//25, 40 + i//15)
            pygame.draw.line(screen, color, (0, i), (screen.get_width(), i))
    
    def draw_header(self, screen):
        """Верхняя панель с названием и ресурсами"""
        header_height = self.s(80)
        header_rect = pygame.Rect(0, 0, screen.get_width(), header_height)
        
        # Градиентный фон хедера
        for i in range(header_height):
            color = (30 + i//3, 30 + i//3, 50 + i//2)
            pygame.draw.line(screen, color, (0, i), (screen.get_width(), i))
        
        # Заголовок
        title_font = self.get_font(36, bold=True)
        title_text = "МАГАЗИН"
        title = title_font.render(title_text, True, self.colors["accent"])
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, self.s(20)))
        
        # Ресурсы игрока
        resource_font = self.get_font(18)
        coins_text = resource_font.render(f"🪙 {self.player_coins}", True, (255, 215, 0))
        trophies_text = resource_font.render(f"🏆 {self.player_trophies}", True, (255, 200, 100))
        
        screen.blit(coins_text, (screen.get_width() - self.s(150), self.s(25)))
        screen.blit(trophies_text, (screen.get_width() - self.s(150), self.s(50)))
    
    def draw_tabs(self, screen):
        """Отрисовка вкладок магазина"""
        self.tab_buttons = []
        
        tab_width = screen.get_width() // len(self.tabs)
        tab_height = self.s(50)
        
        for i, tab_name in enumerate(self.tabs):
            tab_rect = pygame.Rect(i * tab_width, self.s(80), tab_width, tab_height)
            self.tab_buttons.append(tab_rect)
            
            # Цвет вкладки в зависимости от активности
            if i == self.current_tab:
                color = self.colors["button_primary"]
                text_color = self.colors["text_light"]
            else:
                color = self.colors["header_bg"]
                text_color = self.colors["text_dark"]
            
            pygame.draw.rect(screen, color, tab_rect)
            pygame.draw.rect(screen, self.colors["text_light"], tab_rect, self.s(2))
            
            # Текст вкладки
            tab_font = self.get_font(18, bold=True)
            tab_text = tab_font.render(tab_name, True, text_color)
            screen.blit(tab_text, (tab_rect.centerx - tab_text.get_width()//2, 
                                 tab_rect.centery - tab_text.get_height()//2))
    
    def draw_sales_tab(self, screen, rect):
        """Вкладка акций"""
        title_font = self.get_font(26, bold=True)
        title_text = "АКЦИИ"
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width()//2, rect.y + self.s(20)))
        
        # Сообщение о том, что раздел пуст
        message_font = self.get_font(20)
        message_text = "Акций пока нет. Загляните позже!"
        message = message_font.render(message_text, True, self.colors["text_dark"])
        screen.blit(message, (rect.centerx - message.get_width()//2, rect.centery))
    
    def draw_gift_tab(self, screen, rect):
        """Вкладка ежедневного подарка"""
        title_font = self.get_font(26, bold=True)
        title_text = "ЕЖЕДНЕВНЫЙ ПОДАРОК"
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width()//2, rect.y + self.s(20)))
        
        # Сообщение о том, что раздел пуст
        message_font = self.get_font(20)
        message_text = "Заходите завтра за новым подарком!"
        message = message_font.render(message_text, True, self.colors["text_dark"])
        screen.blit(message, (rect.centerx - message.get_width()//2, rect.centery))
    
    def draw_skins_tab(self, screen, rect):
        """Вкладка скинов - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        title_font = self.get_font(26, bold=True)
        title_text = "СКИНЫ"
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width()//2, rect.y + self.s(20)))
        
        if not self.skins_for_sale:
            # Сообщение, если все скины куплены
            message_font = self.get_font(20)
            message_text = "Все скины уже куплены! Загляните позже."
            message = message_font.render(message_text, True, self.colors["text_dark"])
            screen.blit(message, (rect.centerx - message.get_width()//2, rect.centery))
            
            # Добавляем подсказку
            hint_font = self.get_font(16)
            hint_text = "В будущем будут добавлены новые скины!"
            hint = hint_font.render(hint_text, True, self.colors["text_dark"])
            screen.blit(hint, (rect.centerx - hint.get_width()//2, rect.centery + self.s(30)))
            return
        
        skin = self.skins_for_sale[self.selected_skin_index]
        
        # ИСПРАВЛЕНИЕ: Используем тот же размер карточки что и в MenuScene
        card_size = self._get_card_size()
        
        # Карточка скина - используем card_normal как в меню
        card = skin.get("card_normal")
        if card and isinstance(card, pygame.Surface):
            # Карточка уже масштабирована при загрузке
            card_rect = pygame.Rect(rect.centerx - card_size//2, rect.centery - card_size//2, card_size, card_size)
            screen.blit(card, card_rect)
        else:
            # Если карточки нет, создаем заглушку
            filename = f"{skin.get('char_name', skin.get('cameo_name', 'unknown'))}_{skin['skin_id']}_normal.jpg"
            placeholder = self._create_placeholder_card(filename, False, card_size)
            card_rect = pygame.Rect(rect.centerx - card_size//2, rect.centery - card_size//2, card_size, card_size)
            screen.blit(placeholder, card_rect)
        
        # Название скина
        name_font = self.get_font(22, bold=True)
        name_text = name_font.render(skin["name"], True, self.colors["text_light"])
        screen.blit(name_text, (rect.centerx - name_text.get_width()//2, card_rect.bottom + self.s(20)))
        
        # Цена
        price_font = self.get_font(20)
        price_text = price_font.render(f"Цена: {skin['price']} монет", True, (255, 215, 0))
        screen.blit(price_text, (rect.centerx - price_text.get_width()//2, card_rect.bottom + self.s(45)))
        
        # Статус
        status_font = self.get_font(18)
        if skin["unlocked"]:
            status_text = "РАЗБЛОКИРОВАН"
            status_color = self.colors["selected"]
        else:
            status_text = "ЗАБЛОКИРОВАН"
            status_color = self.colors["locked"]
        
        status = status_font.render(status_text, True, status_color)
        screen.blit(status, (rect.centerx - status.get_width()//2, card_rect.bottom + self.s(70)))
        
        # Кнопка покупки
        btn_width = self.s(180)
        btn_height = self.s(45)
        self.buy_button = pygame.Rect(rect.centerx - btn_width//2, card_rect.bottom + self.s(100), btn_width, btn_height)
        
        # Проверяем можно ли купить
        can_afford = self.player_coins >= skin["price"]
        
        if skin["unlocked"]:
            btn_color = self.colors["selected"]
            btn_text = "КУПЛЕНО"
        elif can_afford:
            btn_color = self.colors["button_primary"]
            btn_text = "КУПИТЬ"
        else:
            btn_color = self.colors["locked"]
            btn_text = "НЕДОСТАТОЧНО"
        
        pygame.draw.rect(screen, btn_color, self.buy_button, border_radius=self.s(8))
        pygame.draw.rect(screen, self.colors["text_light"], self.buy_button, self.s(2), border_radius=self.s(8))
        
        btn_font = self.get_font(18, bold=True)
        btn_render = btn_font.render(btn_text, True, self.colors["text_light"])
        screen.blit(btn_render, (self.buy_button.centerx - btn_render.get_width()//2,
                               self.buy_button.centery - btn_render.get_height()//2))
        
        # Подсказка навигации
        hint_font = self.get_font(16)
        hint_text = "Используйте ← → для навигации, ENTER для покупки"
        hint = hint_font.render(hint_text, True, self.colors["text_dark"])
        screen.blit(hint, (rect.centerx - hint.get_width()//2, self.buy_button.bottom + self.s(20)))
        
        # ФИКС: Добавляем стрелки навигации как в меню и сохраняем их прямоугольники
        if len(self.skins_for_sale) > 1:
            arrow_size = self.s(50)
            card_center_y = rect.centery  # Центр по вертикали
            
            # Стрелка влево - ФИКС: сохраняем прямоугольник для обработки кликов
            self.skin_left_btn_rect = pygame.Rect(
                rect.centerx - card_size//2 - arrow_size - self.s(15),
                card_center_y - arrow_size//2,
                arrow_size,
                arrow_size
            )
            
            pygame.draw.rect(screen, self.colors["button_primary"], self.skin_left_btn_rect, border_radius=self.s(10))
            pygame.draw.rect(screen, self.colors["text_light"], self.skin_left_btn_rect, self.s(2), border_radius=self.s(10))
            
            arrow_font = self.get_font(28, bold=True)
            left_arrow = arrow_font.render("⟨", True, self.colors["text_light"])
            screen.blit(left_arrow, (self.skin_left_btn_rect.centerx - left_arrow.get_width()//2,
                                   self.skin_left_btn_rect.centery - left_arrow.get_height()//2))
            
            # Стрелка вправо - ФИКС: сохраняем прямоугольник для обработки кликов
            self.skin_right_btn_rect = pygame.Rect(
                rect.centerx + card_size//2 + self.s(15),
                card_center_y - arrow_size//2,
                arrow_size,
                arrow_size
            )
            
            pygame.draw.rect(screen, self.colors["button_primary"], self.skin_right_btn_rect, border_radius=self.s(10))
            pygame.draw.rect(screen, self.colors["text_light"], self.skin_right_btn_rect, self.s(2), border_radius=self.s(10))
            
            right_arrow = arrow_font.render("⟩", True, self.colors["text_light"])
            screen.blit(right_arrow, (self.skin_right_btn_rect.centerx - right_arrow.get_width()//2,
                                    self.skin_right_btn_rect.centery - right_arrow.get_height()//2))
        else:
            # Если скин один, очищаем ссылки на кнопки
            self.skin_left_btn_rect = None
            self.skin_right_btn_rect = None
    
    def draw_currency_tab(self, screen, rect):
        """Вкладка валюты - ТЕСТОВАЯ ВЕРСИЯ"""
        title_font = self.get_font(26, bold=True)
        title_text = "ВАЛЮТА (ТЕСТ)"
        title = title_font.render(title_text, True, self.colors["text_light"])
        screen.blit(title, (rect.centerx - title.get_width()//2, rect.y + self.s(20)))
        
        currency = self.currency_packs[self.selected_currency_index]
        
        # Отображение набора валюты
        pack_width = self.s(300)
        pack_height = self.s(150)
        pack_rect = pygame.Rect(rect.centerx - pack_width//2, rect.centery - pack_height//2, pack_width, pack_height)
        
        # Фон набора
        pygame.draw.rect(screen, self.colors["header_bg"], pack_rect, border_radius=self.s(12))
        pygame.draw.rect(screen, self.colors["accent"], pack_rect, self.s(3), border_radius=self.s(12))
        
        # Иконка валюты
        icon_font = self.get_font(40)
        icon = icon_font.render(currency["icon"], True, (255, 215, 0))
        screen.blit(icon, (pack_rect.centerx - icon.get_width()//2, pack_rect.top + self.s(20)))
        
        # Название набора
        name_font = self.get_font(20, bold=True)
        name = name_font.render(currency["name"], True, self.colors["text_light"])
        screen.blit(name, (pack_rect.centerx - name.get_width()//2, pack_rect.top + self.s(70)))
        
        # Количество монет
        coins_font = self.get_font(18)
        coins_text = coins_font.render(f"{currency['coins']} монет", True, (255, 215, 0))
        screen.blit(coins_text, (pack_rect.centerx - coins_text.get_width()//2, pack_rect.top + self.s(95)))
        
        # Цена (тестовая версия)
        price_font = self.get_font(16)
        price_text = price_font.render("БЕСПЛАТНО (ТЕСТ)", True, (100, 255, 100))
        screen.blit(price_text, (pack_rect.centerx - price_text.get_width()//2, pack_rect.top + self.s(115)))
        
        # Кнопка покупки
        btn_width = self.s(200)
        btn_height = self.s(45)
        self.currency_buy_button = pygame.Rect(rect.centerx - btn_width//2, pack_rect.bottom + self.s(30), btn_width, btn_height)
        
        pygame.draw.rect(screen, self.colors["button_tertiary"], self.currency_buy_button, border_radius=self.s(8))
        pygame.draw.rect(screen, self.colors["text_light"], self.currency_buy_button, self.s(2), border_radius=self.s(8))
        
        btn_font = self.get_font(18, bold=True)
        btn_text = btn_font.render("ПОЛУЧИТЬ БЕСПЛАТНО", True, self.colors["text_light"])
        screen.blit(btn_text, (self.currency_buy_button.centerx - btn_text.get_width()//2,
                             self.currency_buy_button.centery - btn_text.get_height()//2))
        
        # Подсказка навигации
        hint_font = self.get_font(16)
        hint_text = "Используйте ← → для выбора набора (ТЕСТ - монеты добавляются бесплатно)"
        hint = hint_font.render(hint_text, True, self.colors["text_dark"])
        screen.blit(hint, (rect.centerx - hint.get_width()//2, self.currency_buy_button.bottom + self.s(20)))
    
    def draw_bottom_bar(self, screen):
        """Нижняя панель с кнопкой назад"""
        bar_height = self.s(60)
        bar_rect = pygame.Rect(0, screen.get_height() - bar_height, screen.get_width(), bar_height)
        
        # Фон
        pygame.draw.rect(screen, self.colors["header_bg"], bar_rect)
        
        # Кнопка "Назад"
        btn_width = self.s(120)
        btn_height = self.s(40)
        self.back_button = pygame.Rect(self.s(20), bar_rect.centery - btn_height//2, btn_width, btn_height)
        
        pygame.draw.rect(screen, self.colors["button_secondary"], self.back_button, border_radius=self.s(8))
        pygame.draw.rect(screen, self.colors["text_light"], self.back_button, self.s(2), border_radius=self.s(8))
        
        back_font = self.get_font(18, bold=True)
        back_text = back_font.render("НАЗАД", True, self.colors["text_light"])
        screen.blit(back_text, (self.back_button.centerx - back_text.get_width()//2,
                              self.back_button.centery - back_text.get_height()//2))
    
    def draw_purchase_animation(self, screen):
        """Анимация покупки"""
        if not self.purchase_animation_item:
            return
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.purchase_animation_time
        progress = min(elapsed / 2000, 1.0)  # 2 секунды анимации
        
        # Создаем полупрозрачный черный фон
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(150 * progress)))
        screen.blit(overlay, (0, 0))
        
        # Отрисовываем частицы
        for particle in self.particles:
            if particle["life"] > 0:
                alpha = int(255 * particle["life"])
                particle_color = (*particle["color"], alpha)
                
                # Создаем поверхность для частицы с альфа-каналом
                particle_surface = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, particle_color, 
                                 (particle["size"], particle["size"]), particle["size"])
                screen.blit(particle_surface, (particle["x"] - particle["size"], particle["y"] - particle["size"]))
        
        # Определяем размер карточки с анимации
        base_size = self.s(200)
        animated_size = int(base_size * (1 + progress * 0.5))  # Увеличивается на 50%
        
        # Центрируем карточку
        card_x = screen.get_width() // 2 - animated_size // 2
        card_y = screen.get_height() // 2 - animated_size // 2
        
        # Рисуем карточку
        if "card_special" in self.purchase_animation_item and self.purchase_animation_item["card_special"]:
            # Для скина используем специальную карточку
            card_special = self.purchase_animation_item["card_special"]
            if isinstance(card_special, pygame.Surface):
                card = pygame.transform.scale(card_special, (animated_size, animated_size))
                
                # Добавляем свечение
                glow_size = animated_size + 20
                glow = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.rect(glow, (255, 255, 100, 100), (0, 0, glow_size, glow_size), 
                               border_radius=self.s(10))
                screen.blit(glow, (card_x - 10, card_y - 10))
                
                screen.blit(card, (card_x, card_y))
        else:
            # Для валюты рисуем простую карточку
            card = pygame.Surface((animated_size, animated_size), pygame.SRCALPHA)
            card.fill((100, 100, 255, 200))
            pygame.draw.rect(card, (255, 215, 0), (0, 0, animated_size, animated_size), self.s(5))
            
            # Иконка валюты
            icon_font = pygame.font.SysFont("arial", animated_size // 3)
            icon = icon_font.render("💰", True, (255, 215, 0))
            card.blit(icon, (animated_size//2 - icon.get_width()//2, 
                           animated_size//2 - icon.get_height()//2))
            
            screen.blit(card, (card_x, card_y))
        
        # Текст "ПОЛУЧЕНО!"
        text_size = int(self.s(40) * (1 + progress * 0.3))
        text_font = pygame.font.SysFont("arial", text_size, bold=True)
        
        if "name" in self.purchase_animation_item:
            if "coins" in self.purchase_animation_item:
                text = text_font.render(f"ПОЛУЧЕНО: {self.purchase_animation_item['coins']} монет!", 
                                      True, (100, 255, 100))
            else:
                text = text_font.render(f"КУПЛЕНО: {self.purchase_animation_item['name']}", 
                                      True, (100, 255, 100))
        else:
            text = text_font.render("ПОЛУЧЕНО!", True, (100, 255, 100))
        
        text_x = screen.get_width() // 2 - text.get_width() // 2
        text_y = card_y - text.get_height() - self.s(20)
        screen.blit(text, (text_x, text_y))
    
    def draw_locked_skin_message(self, screen):
        """Сообщение о недостатке денег для покупки скина"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.locked_skin_message_time
        progress = min(elapsed / 1500, 1.0)
        
        if progress >= 1.0:
            return
        
        # Создаем полупрозрачный фон
        overlay = pygame.Surface((screen.get_width(), self.s(100)), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(200 * progress)))
        
        overlay_y = screen.get_height() // 2 - self.s(50)
        screen.blit(overlay, (0, overlay_y))
        
        # Текст сообщения
        text_font = self.get_font(24, bold=True)
        text = text_font.render("НЕДОСТАТОЧНО МОНЕТ!", True, self.colors["danger"])
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 
                         overlay_y + self.s(20)))
        
        # Подсказка
        hint_font = self.get_font(18)
        hint = hint_font.render("Купите монеты в разделе ВАЛЮТА", True, self.colors["text_light"])
        screen.blit(hint, (screen.get_width() // 2 - hint.get_width() // 2, 
                          overlay_y + self.s(60)))