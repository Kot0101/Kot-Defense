import pygame, math
from config import *
from classes import Sprite

# Managers
class WidgetManager:
    def __init__(self):
        self.game_inited = False
        self.widgets = []
        self.touched = False
        self.visible = False
        
        # Настройки умного каскадного спавна
        self.spawn_x = 50
        self.spawn_y = 50
        self.step_x = 30  # Сдвиг по горизонтали для следующего окна
        self.step_y = 30  # Сдвиг по вертикали для следующего окна
    
    def init_game(self, game):
        self.game_inited = True
        self.game = game
        for w in self.widgets:
            w.game = game

    def add(self, widget):
        self.widgets.append(widget)
        if self.game_inited:
            widget.game = self.game

        # --- УМНОЕ ПОЗИЦИОНИРОВАНИЕ ---
        if hasattr(widget, 'rect'):
            # Задаем окну текущие координаты спавна
            widget.rect.x = self.spawn_x
            widget.rect.y = self.spawn_y
            
            # Ограничиваем окно (clamp), чтобы оно гарантированно не вылезало за экран
            # WIDTH и HEIGHT импортируются из config
            if widget.rect.right > WIDTH:
                widget.rect.x = max(0, WIDTH - widget.rect.w - 10)
            if widget.rect.bottom > HEIGHT:
                widget.rect.y = max(0, HEIGHT - widget.rect.h - 10)
                
            # Обновляем все внутренние ректы окна (кнопки закрытия, хедеры и т.д.)
            widget.update_rects()

            # Считаем координаты для СЛЕДУЮЩЕГО окна
            self.spawn_x += self.step_x
            self.spawn_y += self.step_y

            # Если следующий спавн упирается в правый или нижний край экрана, сбрасываем цикл
            if self.spawn_x + 150 > WIDTH or self.spawn_y + 150 > HEIGHT:
                self.spawn_x = 50
                self.spawn_y = 50

    def bring_to_front(self, widget):
        self.widgets.remove(widget)
        self.widgets.append(widget)

    def update(self):
        if self.game.input.scancode_pressed(CONSOLE_TOGGLE_SCANCODE):
            self.visible = not self.visible
        if self.visible == True:
            self.touched = False
            
            # Приоритетный ввод от UI Visualizer (элементы поверх всех виджетов)
            for w in self.widgets:
                if isinstance(w, UIVisualizer) and not w.closed:
                    if w.handle_element_input():
                        self.touched = True
                        break
            
            for w in reversed(self.widgets):
                w.update()
                if not self.touched and w.visible:
                    self.touched = w.window_input()
            
    def draw(self):
        if self.visible == True:
            self.widgets = [w for w in self.widgets if w.closed == False]
            for w in self.widgets:
                if w.visible:
                    w.draw()
            # UI элементы поверх всех виджетов (пока WidgetManager видим)
            for w in self.widgets:
                if isinstance(w, UIVisualizer) and w.visible:
                    w.draw_elements()
                    break

class ProgramManager:
    def __init__(self):
        self.programs = {}
    
    def init(self, name, cls):
        self.programs[name] = cls
    
    def get(self, name):
        if name in self.list():
            return self.programs[name]
        else:
            return None
    
    def remove(self, name):
        if name in self.list():
            self.programs.pop(name)
        else:
            return None
    
    def list(self):
       return self.programs.keys()

# Classes
class DebugWidget:
    def __init__(self, title, rect=pygame.Rect(0, 0, 200, 150)):
        self.title = title
        self.title_color = (255, 255, 255)
        self.rect = rect
        self.font = pygame.font.SysFont("Arial", 16)
        
        self.close_button = True
        self.drag_offset = (0, 0)
        
        self.visible = True
        self.dragging = False
        self.closed = False
        
        self.update_rects()
    
    def update_rects(self):
        self.header = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, 30)
        self.close_btn = pygame.Rect(self.rect.right - 25, self.rect.y+5, 20, 20)
    
    def close(self):
        self.closed = True
    
    def window_input(self):
        im = self.game.input
        touched = False
        if self.close_button and self.close_btn.collidepoint(im.mouse_pos):
            self.game.cursorManager.set_state('hovered')
        if im.mouse_pressed(1):
            
            if self.close_button and self.close_btn.collidepoint(im.mouse_pos):
                self.close()
            elif self.header.collidepoint(im.mouse_pos):
                self.dragging = True
                self.drag_offset = (im.mouse_pos[0] - self.rect.x, im.mouse_pos[1] - self.rect.y)
            if self.rect.collidepoint(im.mouse_pos):
                self.game.widgetManager.bring_to_front(self)
                touched = True
        if self.dragging:
            if self.game.input.mouse_released(1):
                self.dragging = False
            else:
                self.rect.x, self.rect.y = min(max(im.mouse_pos[0] - self.drag_offset[0], 0), WIDTH-5), min(max(im.mouse_pos[1] - self.drag_offset[1], 0), HEIGHT-5)
                self.update_rects()
                touched = True
        return touched
    
    def update(self):
        pass
    
    def draw(self):
        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        pygame.draw.rect(screen, (100, 100, 100), self.header)
        if self.close_button == True:
            pygame.draw.rect(screen, (237, 69, 69) if self.close_btn.collidepoint(self.game.input.mouse_pos) else (200, 50, 50), self.close_btn)
        screen.blit(self.font.render(self.title, True, self.title_color,), (self.rect.x+5, self.rect.y+5))

# Programs
class Explorer(DebugWidget):
    def __init__(self):
        super().__init__("Explorer", rect=pygame.Rect(100, 80, 580, 480))
        self.close_button = True
        self.root_obj = None
        self.current_obj = None
        self.path_history = [] 
        
        self.items = []
        self.scroll_offset = 0
        self.max_visible_items = 14
        self.item_height = 24
        
        self.search_query = ""
        self.input_focus = None  
        self.input_buffer = ""
        self.selected_item = None
        
        self.last_click_time = 0
        self.last_clicked_name = None

    def refresh_items(self):
        if self.current_obj is None:
            return
        self.items = []
        obj = self.current_obj
        
        try:
            attrs = dir(obj)
        except Exception:
            attrs = []

        for attr in attrs:
            if attr.startswith('_'): 
                continue
            try:
                val = getattr(obj, attr)
            except Exception:
                continue
                
            if self.search_query and self.search_query.lower() not in attr.lower():
                continue
                
            if callable(val):
                item_type = 'method'
            elif isinstance(val, (int, float, str, bool, type(None))):
                item_type = 'value'
            elif hasattr(val, 'value') and hasattr(val, 'base'):
                item_type = 'stat'
            else:
                item_type = 'folder'
                
            self.items.append({
                'name': attr,
                'value': val,
                'type': item_type
            })
            
        self.items.sort(key=lambda x: ('folder', 'value', 'stat', 'method').index(x['type']))

    def get_current_path_str(self):
        if not self.path_history:
            return "game"
        return "game." + ".".join([p[0] for p in self.path_history])

    def window_input(self):
        im = self.game.input
        touched = False
        
        if self.current_obj is None:
            self.root_obj = self.game
            self.current_obj = self.game
            self.refresh_items()

        btn_back_rect = pygame.Rect(self.rect.x + 15, self.rect.y + 35, 60, 22)
        search_rect = pygame.Rect(self.rect.x + 310, self.rect.y + 35, 215, 22)
        btn_clear_search = pygame.Rect(self.rect.x + 530, self.rect.y + 35, 20, 22)
        
        scroll_up_rect = pygame.Rect(self.rect.right - 30, self.rect.y + 70, 20, 25)
        scroll_down_rect = pygame.Rect(self.rect.right - 30, self.rect.bottom - 60, 20, 25)

        # Обработка смены курсора при наведении
        if btn_back_rect.collidepoint(im.mouse_pos) or search_rect.collidepoint(im.mouse_pos) or \
           btn_clear_search.collidepoint(im.mouse_pos) or scroll_up_rect.collidepoint(im.mouse_pos) or \
           scroll_down_rect.collidepoint(im.mouse_pos):
            self.game.cursorManager.set_state('hovered')

        if im.mouse_pressed(1):
            if btn_back_rect.collidepoint(im.mouse_pos) and self.path_history:
                _, prev_obj = self.path_history.pop()
                self.current_obj = prev_obj
                self.scroll_offset = 0
                self.refresh_items()
                touched = True
            
            elif search_rect.collidepoint(im.mouse_pos):
                self.input_focus = 'search'
                self.input_buffer = self.search_query
                touched = True
                
            elif btn_clear_search.collidepoint(im.mouse_pos):
                self.search_query = ""
                self.refresh_items()
                touched = True
                
            elif scroll_up_rect.collidepoint(im.mouse_pos):
                self.scroll_offset = max(0, self.scroll_offset - 1)
                touched = True
                
            elif scroll_down_rect.collidepoint(im.mouse_pos):
                max_scroll = max(0, len(self.items) - self.max_visible_items)
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
                touched = True
                
            else:
                list_start_y = self.rect.y + 70
                for i in range(min(self.max_visible_items, len(self.items))):
                    idx = self.scroll_offset + i
                    if idx >= len(self.items): break
                    
                    item_rect = pygame.Rect(self.rect.x + 15, list_start_y + (i * self.item_height), self.rect.w - 50, self.item_height)
                    if item_rect.collidepoint(im.mouse_pos):
                        item = self.items[idx]
                        now = pygame.time.get_ticks()
                        if now - self.last_click_time < 300 and self.last_clicked_name == item['name']:
                            self.handle_double_click(item)
                        else:
                            self.last_click_time = now
                            self.last_clicked_name = item['name']
                        touched = True
                        break
                        
            if self.input_focus and not search_rect.collidepoint(im.mouse_pos):
                if self.input_focus != 'edit' and self.input_focus != 'invoke':
                    self.input_focus = None

        # Проверка ховера для элементов списка (курсор)
        list_start_y = self.rect.y + 70
        for i in range(min(self.max_visible_items, len(self.items))):
            item_rect = pygame.Rect(self.rect.x + 15, list_start_y + (i * self.item_height), self.rect.w - 50, self.item_height)
            if item_rect.collidepoint(im.mouse_pos):
                self.game.cursorManager.set_state('hovered')
                break

        if self.dragging:
            touched = True

        base_touched = super().window_input()
        return touched or base_touched

    def handle_double_click(self, item):
        if item['type'] == 'folder':
            self.path_history.append((item['name'], self.current_obj))
            self.current_obj = item['value']
            self.scroll_offset = 0
            self.search_query = ""
            self.refresh_items()
            
        elif item['type'] in ('value', 'stat'):
            self.selected_item = item
            self.input_focus = 'edit'
            if item['type'] == 'stat':
                self.input_buffer = str(item['value'].base)
            else:
                self.input_buffer = str(item['value'])
            
        elif item['type'] == 'method':
            self.selected_item = item
            self.input_focus = 'invoke'
            self.input_buffer = ""

    def update(self):
        im = self.game.input
        if not self.input_focus: 
            return
            
        for char in im.text_queue:
            self.input_buffer += char
            
        if im.key_backspace:
            self.input_buffer = self.input_buffer[:-1]
            
        if im.key_enter:
            if self.input_focus == 'search':
                self.search_query = self.input_buffer
                self.scroll_offset = 0
                self.refresh_items()
                self.input_focus = None
                
            elif self.input_focus == 'edit':
                attr_name = self.selected_item['name']
                raw_val = self.input_buffer.strip()
                try:
                    parsed_val = eval(raw_val, {"__builtins__": None}, {})
                except Exception:
                    parsed_val = raw_val
                    
                try:
                    if self.selected_item['type'] == 'stat':
                        stat_obj = getattr(self.current_obj, attr_name)
                        stat_obj.base = parsed_val
                    else:
                        setattr(self.current_obj, attr_name, parsed_val)
                except Exception as e:
                    if hasattr(self.game, 'console'):
                        self.game.console.log(f"[Explorer Error] Failed to change {attr_name}: {e}")
                    
                self.refresh_items()
                self.input_focus = None
                self.selected_item = None
                
            elif self.input_focus == 'invoke':
                method_obj = self.selected_item['value']
                args_str = self.input_buffer.strip()
                try:
                    if args_str:
                        parsed_args = eval(f"({args_str},)", {"__builtins__": None}, {})
                    else:
                        parsed_args = ()
                    
                    result = method_obj(*parsed_args)
                    if hasattr(self.game, 'console'):
                        self.game.console.log(f"[Explorer] Successful call {self.selected_item['name']}(). Result: {result}")
                except Exception as e:
                    if hasattr(self.game, 'console'):
                        self.game.console.log(f"[Explorer Error] Error calling function: {e}")
                    
                self.refresh_items()
                self.input_focus = None
                self.selected_item = None

    def draw(self):
        super().draw()
        list_start_y = self.rect.y + 70
        im_pos = self.game.input.mouse_pos
        
        scroll_up_rect = pygame.Rect(self.rect.right - 30, self.rect.y + 70, 20, 25)
        scroll_down_rect = pygame.Rect(self.rect.right - 30, self.rect.bottom - 60, 20, 25)
        
        # Кнопка назад
        btn_back_rect = pygame.Rect(self.rect.x + 15, self.rect.y + 35, 60, 22)
        hover_back = btn_back_rect.collidepoint(im_pos)
        back_color = (80, 85, 90) if hover_back and self.path_history else ((60, 65, 70) if self.path_history else (30, 32, 35))
        pygame.draw.rect(screen, back_color, btn_back_rect)
        pygame.draw.rect(screen, (110, 115, 120) if hover_back else (90, 95, 100), btn_back_rect, 1)
        screen.blit(self.font.render(" <- Back", True, (255, 255, 255) if hover_back and self.path_history else ((240, 240, 240) if self.path_history else (100, 105, 110))), (btn_back_rect.x + 2, btn_back_rect.y + 2))

        path_str = self.get_current_path_str()
        if len(path_str) > 22: 
            path_str = "..." + path_str[-22:]
        path_surf = self.font.render(path_str, True, (130, 200, 245))
        screen.blit(path_surf, (self.rect.x + 85, self.rect.y + 37))

        # Поиск
        search_rect = pygame.Rect(self.rect.x + 310, self.rect.y + 35, 215, 22)
        hover_search = search_rect.collidepoint(im_pos)
        search_bg = (35, 37, 39) if hover_search or self.input_focus == 'search' else (45, 48, 52)
        pygame.draw.rect(screen, search_bg, search_rect)
        pygame.draw.rect(screen, (245, 170, 60) if self.input_focus == 'search' else ((120, 125, 130) if hover_search else (80, 85, 90)), search_rect, 1)
        
        s_text = self.input_buffer if self.input_focus == 'search' else (self.search_query if self.search_query else "Search...")
        s_color = (255, 255, 255) if self.input_focus == 'search' or self.search_query else (120, 125, 130)
        screen.blit(self.font.render(s_text, True, s_color), (search_rect.x + 5, search_rect.y + 2))
        
        btn_x = pygame.Rect(self.rect.x + 530, self.rect.y + 35, 20, 22)
        hover_x = btn_x.collidepoint(im_pos)
        pygame.draw.rect(screen, (100, 50, 50) if hover_x else (70, 40, 40), btn_x)
        screen.blit(self.font.render("X", True, (255, 130, 130) if hover_x else (240, 100, 100)), (btn_x.x + 5, btn_x.y + 2))

        pygame.draw.line(screen, (70, 75, 80), (self.rect.x + 10, self.rect.y + 64), (self.rect.right - 10, self.rect.y + 64), 2)

        visible_items = self.items[self.scroll_offset : self.scroll_offset + self.max_visible_items]
        
        if not self.items:
            empty_surf = self.font.render("[Object is empty or nothing was found]", True, (130, 135, 140))
            screen.blit(empty_surf, (self.rect.x + 30, list_start_y + 10))

        for i, item in enumerate(visible_items):
            item_y = list_start_y + (i * self.item_height)
            item_rect = pygame.Rect(self.rect.x + 15, item_y, self.rect.w - 50, self.item_height)
            
            if item_rect.collidepoint(im_pos):
                pygame.draw.rect(screen, (65, 70, 75), item_rect) # Подсветка строки
            
            if item['type'] == 'folder':
                prefix, p_color = "[DIR] ", (100, 180, 245)
                display_text = f"{item['name']}"
            elif item['type'] == 'method':
                prefix, p_color = "[FX]  ", (160, 230, 100)
                display_text = f"{item['name']}()"
            else:
                prefix, p_color = "[VAL] ", (245, 170, 60)
                if item['type'] == 'stat':
                    val_str = str(item['value'].value)
                else:
                    val_str = str(item['value'])
                if len(val_str) > 35: val_str = val_str[:32] + "..."
                display_text = f"{item['name']} = {val_str}"
            
            screen.blit(self.font.render(prefix, True, p_color), (self.rect.x + 20, item_y + 2))
            screen.blit(self.font.render(display_text, True, (230, 235, 240)), (self.rect.x + 75, item_y + 2))
            
            pygame.draw.line(screen, (48, 50, 52), (self.rect.x + 15, item_y + self.item_height), (self.rect.right - 35, item_y + self.item_height), 1)

        # Скролл
        pygame.draw.rect(screen, (70, 75, 80) if scroll_up_rect.collidepoint(im_pos) else (50, 53, 56), scroll_up_rect)
        screen.blit(self.font.render("^", True, (255, 255, 255) if scroll_up_rect.collidepoint(im_pos) else (200, 205, 210)), (scroll_up_rect.x + 6, scroll_up_rect.y + 2))
        
        pygame.draw.rect(screen, (70, 75, 80) if scroll_down_rect.collidepoint(im_pos) else (50, 53, 56), scroll_down_rect)
        screen.blit(self.font.render("v", True, (255, 255, 255) if scroll_down_rect.collidepoint(im_pos) else (200, 205, 210)), (scroll_down_rect.x + 6, scroll_down_rect.y + 4))

        if self.input_focus in ('edit', 'invoke'):
            panel_rect = pygame.Rect(self.rect.x + 10, self.rect.bottom - 32, self.rect.w - 20, 24)
            pygame.draw.rect(screen, (20, 22, 24), panel_rect)
            pygame.draw.rect(screen, (245, 170, 60), panel_rect, 1)
            
            if self.input_focus == 'edit':
                prompt = f"Edit {self.selected_item['name']}: {self.input_buffer}"
            else:
                prompt = f"Run {self.selected_item['name']}({self.input_buffer})"
                
            screen.blit(self.font.render(prompt, True, (255, 255, 255)), (panel_rect.x + 10, panel_rect.y + 2))

class DogInspector(DebugWidget):
    def __init__(self, dog, enemy_manager):
        self.is_class = isinstance(dog, type)
        name = dog.__name__ if self.is_class else dog.__class__.__name__
        super().__init__(f"Inspector: {name}", rect=pygame.Rect(0, 0, 260, 410))
        
        self.dog = dog
        self.enemy_manager = enemy_manager
        self.close_button = True
        self.preview_image = None
        self.spawn_btn_rect = pygame.Rect(self.rect.x + 15, self.rect.y + 350, self.rect.w - 30, 45)
        
        try:
            if self.is_class:
                temp_dog = dog((0, 0))
                self.preview_image = temp_dog.sprite.image
                del temp_dog
            else:
                self.preview_image = dog.sprite.image
        except Exception as e:
            print(f"[Debug Error] Failed to extract sprite: {e}")
            self.preview_image = None

    def window_input(self):
        im = self.game.input
        touched = False
        self.spawn_btn_rect.topleft = (self.rect.x + 15, self.rect.y + 350)

        if self.spawn_btn_rect.collidepoint(im.mouse_pos):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                enemy_class = self.dog if self.is_class else self.dog.__class__
                self.enemy_manager.spawn_specific(enemy_class)
                if hasattr(self.game, 'console'):
                    self.game.console.log(f"[Debug] Spawned dog: {enemy_class.__name__}", (96, 227, 73))
                touched = True

        base_touched = super().window_input()
        return touched or base_touched

    def draw(self):
        super().draw()
        def _v(obj): return obj.value if hasattr(obj, 'value') else obj
        
        hp_val = _v(self.dog.max_hp) if self.is_class else f"{round(_v(self.dog.hp), 1)}/{_v(self.dog.max_hp)}"
        
        stats = [
            f"HP:        {hp_val}",
            f"SPEED:     {_v(self.dog.speed)}",
            f"STRENGTH:  {_v(self.dog.strength)}",
            f"BUDGET:    {_v(self.dog.budget)}",
            f"COST:      {_v(self.dog.cost)}",
            f"PRIORITY:  {_v(self.dog.priority)}",
            f"REQ WAVE:  {_v(self.dog.req_wave)}"
        ]
        
        for i, line in enumerate(stats):
            surf = self.font.render(line, True, (200, 205, 210))
            screen.blit(surf, (self.rect.x + 15, self.rect.y + 40 + (i * 20)))
            
        pygame.draw.line(screen, (58, 62, 65), (self.rect.x + 10, self.rect.y + 190), (self.rect.right - 10, self.rect.y + 190))
        
        preview_rect = pygame.Rect(self.rect.x + 15, self.rect.y + 205, self.rect.w - 30, 130)
        pygame.draw.rect(screen, (22, 24, 25), preview_rect)
        pygame.draw.rect(screen, (48, 52, 55), preview_rect, 1)
        
        if self.preview_image:
            img = self.preview_image
            img_w, img_h = img.get_size()
            if img_w > preview_rect.w - 10 or img_h > preview_rect.h - 10:
                scale = min((preview_rect.w - 10) / img_w, (preview_rect.h - 10) / img_h)
                img = pygame.transform.scale(img, (int(img_w * scale), int(img_h * scale)))
            img_rect = img.get_rect(center=preview_rect.center)
            screen.blit(img, img_rect.topleft)
        else:
            no_img_txt = self.font.render("[ NO PREVIEW ]", True, (100, 105, 110))
            txt_rect = no_img_txt.get_rect(center=preview_rect.center)
            screen.blit(no_img_txt, txt_rect.topleft)

        im_pos = self.game.input.mouse_pos
        if self.spawn_btn_rect.collidepoint(im_pos):
            btn_color = (46, 139, 87) 
        else:
            btn_color = (34, 110, 68) 
            
        pygame.draw.rect(screen, btn_color, self.spawn_btn_rect, border_radius=6)
        pygame.draw.rect(screen, (80, 180, 120) if self.spawn_btn_rect.collidepoint(im_pos) else (50, 140, 90), self.spawn_btn_rect, 1, border_radius=6)
        
        btn_text = self.font.render("SPAWN DOG", True, (255, 255, 255) if self.spawn_btn_rect.collidepoint(im_pos) else (240, 245, 250))
        btn_text_rect = btn_text.get_rect(center=self.spawn_btn_rect.center)
        screen.blit(btn_text, btn_text_rect.topleft)

class DogViewer(DebugWidget):
    def __init__(self):
        super().__init__("Dog Manager", rect=pygame.Rect(100, 100, 340, 460))
        self.close_button = True
        self.mode = "registered"
        
        self.tab_reg = pygame.Rect(0, 0, 0, 0)
        self.tab_act = pygame.Rect(0, 0, 0, 0)
        self.update_rects()

    def update_rects(self):
        super().update_rects()
        self.tab_reg = pygame.Rect(self.rect.x + 10, self.rect.y + 35, 155, 24)
        self.tab_act = pygame.Rect(self.rect.x + 175, self.rect.y + 35, 155, 24)

    def window_input(self):
        im = self.game.input
        touched = False
        
        # Курсор и клик по вкладкам (ЛКМ)
        if self.tab_reg.collidepoint(im.mouse_pos):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                self.mode = "registered"
                touched = True
        elif self.tab_act.collidepoint(im.mouse_pos):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                self.mode = "active"
                touched = True
                
        if hasattr(self.game, 'enemyManager'):
            line_height = 20
            start_y = self.rect.y + 75
            
            if self.mode == "registered":
                types = list(self.game.enemyManager.initEnemies.keys())
                for i, name in enumerate(types):
                    line_rect = pygame.Rect(self.rect.x + 10, start_y + (i * line_height), self.rect.w - 20, line_height)
                    if line_rect.collidepoint(im.mouse_pos):
                        self.game.cursorManager.set_state('hovered')
                        # ЛКМ для списков
                        if im.mouse_pressed(1):
                            enemy_cls = self.game.enemyManager.initEnemies[name]
                            self.game.widgetManager.add(DogInspector(enemy_cls, self.game.enemyManager))
                            touched = True
                            break
                            
            elif self.mode == "active":
                dogs = self.game.enemyManager.enemies
                for i, dog in enumerate(dogs):
                    line_rect = pygame.Rect(self.rect.x + 10, start_y + (i * line_height), self.rect.w - 20, line_height)
                    
                    if line_rect.collidepoint(im.mouse_pos):
                        self.game.cursorManager.set_state('hovered')
                        # ЛКМ для списков
                        if im.mouse_pressed(1):
                            self.game.widgetManager.add(DogInspector(dog, self.game.enemyManager))
                            touched = True
                            break
                            
                    # Колесико (Средняя кнопка) для клика по объектам НА САМОМ ПОЛЕ
                    if dog.rect.collidepoint(im.mouse_pos):
                        if im.mouse_pressed(2):
                            self.game.widgetManager.add(DogInspector(dog, self.game.enemyManager))
                            touched = True
                            break

        if self.dragging:
            self.update_rects()

        base_touched = super().window_input()
        return touched or base_touched

    def draw(self):
        super().draw()
        im_pos = self.game.input.mouse_pos
        
        color_reg = (46, 48, 50) if self.tab_reg.collidepoint(im_pos) else ((36, 38, 40) if self.mode == "registered" else (26, 28, 30))
        color_act = (46, 48, 50) if self.tab_act.collidepoint(im_pos) else ((36, 38, 40) if self.mode == "active" else (26, 28, 30))
        
        pygame.draw.rect(screen, color_reg, self.tab_reg)
        pygame.draw.rect(screen, (80, 85, 90) if self.tab_reg.collidepoint(im_pos) else (58, 62, 65), self.tab_reg, 1)
        pygame.draw.rect(screen, color_act, self.tab_act)
        pygame.draw.rect(screen, (80, 85, 90) if self.tab_act.collidepoint(im_pos) else (58, 62, 65), self.tab_act, 1)
        
        txt_reg = self.font.render("REGISTERED", True, (255, 200, 100) if self.mode == "registered" else (160, 165, 170))
        txt_act = self.font.render("ACTIVE ON FIELD", True, (255, 200, 100) if self.mode == "active" else (160, 165, 170))
        screen.blit(txt_reg, (self.tab_reg.x + 35, self.tab_reg.y + 5))
        screen.blit(txt_act, (self.tab_act.x + 20, self.tab_act.y + 5))
        
        if not hasattr(self.game, 'enemyManager'):
            error_surf = self.font.render("ERROR: NO ENEMY_MANAGER", True, (232, 58, 49))
            screen.blit(error_surf, (self.rect.x + 15, self.rect.y + 75))
            return

        line_height = 20
        start_y = self.rect.y + 75
        
        if self.mode == "registered":
            types = list(self.game.enemyManager.initEnemies.keys())
            for i, name in enumerate(types):
                line_rect = pygame.Rect(self.rect.x + 10, start_y + (i * line_height), self.rect.w - 20, line_height)
                if line_rect.collidepoint(im_pos):
                    pygame.draw.rect(screen, (52, 56, 60), line_rect) # Подсветка строки
                    
                enemy_cls = self.game.enemyManager.initEnemies[name]
                budget = getattr(enemy_cls, 'budget', 0)
                budget_val = budget.value if hasattr(budget, 'value') else budget
                
                line_text = f" [{i+1:02d}] {name:<12} | BUDGET: {budget_val}"
                surf = self.font.render(line_text, True, (240, 245, 250) if line_rect.collidepoint(im_pos) else (200, 205, 210))
                screen.blit(surf, (self.rect.x + 15, start_y + (i * line_height)))
                
        elif self.mode == "active":
            dogs = self.game.enemyManager.enemies
            if not dogs:
                empty_surf = self.font.render(" NO ACTIVE ENEMIES IN FIELD.", True, (120, 125, 130))
                screen.blit(empty_surf, (self.rect.x + 15, start_y))
            else:
                for i, dog in enumerate(dogs):
                    line_rect = pygame.Rect(self.rect.x + 10, start_y + (i * line_height), self.rect.w - 20, line_height)
                    if line_rect.collidepoint(im_pos):
                        pygame.draw.rect(screen, (52, 56, 60), line_rect) # Подсветка строки
                        
                    name = dog.__class__.__name__
                    hp_val = dog.hp.value if hasattr(dog.hp, 'value') else dog.hp
                    max_hp_val = dog.max_hp.value if hasattr(dog.max_hp, 'value') else dog.max_hp
                    hp_percent = int((hp_val / max_hp_val) * 100) if max_hp_val > 0 else 0
                    
                    line_text = f" [{i+1:02d}] {name:<12} | HP: {hp_percent:3d}% | X: {dog.rect.x}"
                    base_color = (96, 227, 73) if hp_val > 0 else (232, 58, 49)
                    # Если наведены — чуть высветляем
                    color = (min(base_color[0]+30, 255), min(base_color[1]+30, 255), min(base_color[2]+30, 255)) if line_rect.collidepoint(im_pos) else base_color 
                    
                    surf = self.font.render(line_text, True, color)
                    screen.blit(surf, (self.rect.x + 15, start_y + (i * line_height)))

class CatInspector(DebugWidget):
    def __init__(self, cat, game_obj):
        self.is_class = isinstance(cat, type)
        name = cat.__name__ if self.is_class else cat.__class__.__name__
        super().__init__(f"Inspector: {name}", rect=pygame.Rect(0, 0, 260, 350))
        
        self.cat = cat
        self.game = game_obj 
        self.close_button = True
        self.preview_image = None
        
        def _get_val(obj): return obj.value if hasattr(obj, 'value') else obj

        try:
            if self.is_class:
                class DummyParent:
                    def __init__(self, game_ref):
                        self.cost = 0
                        self.game = game_ref

                temp_cat = cat(DummyParent(self.game), (0, 0))
                temp_cat.game = self.game
                
                self.preview_image = temp_cat.sprite.image
                self.max_hp = _get_val(temp_cat.max_hp)
                self.rate = _get_val(temp_cat.rate)
                self.range = _get_val(temp_cat.range)
                self.strength = _get_val(temp_cat.strength)
                self.count = _get_val(temp_cat.count)
                
                self.cost = 0
                if hasattr(self.game, 'storeManager'):
                    for p in self.game.storeManager.products:
                        if getattr(p, 'tower', None) == name:
                            self.cost = _get_val(p.cost)
                            break
                del temp_cat
            else:
                self.preview_image = cat.sprite.image
                self.max_hp = _get_val(cat.max_hp)
                self.rate = _get_val(cat.rate)
                self.range = _get_val(cat.range)
                self.strength = _get_val(cat.strength)
                self.count = _get_val(cat.count)
                self.cost = _get_val(cat.cost)
        except Exception as e:
            print(f"[Debug Error] Failed to extract sprite: {e}")
            self.preview_image = None
            self.max_hp = 0
            self.rate = 0
            self.range = 0
            self.strength = 0
            self.count = 0
            self.cost = 0

    def draw(self):
        super().draw()
        
        def _get_val(obj): return obj.value if hasattr(obj, 'value') else obj
        hp_val = self.max_hp if self.is_class else f"{round(_get_val(self.cat.hp), 1)}/{self.max_hp}"
        
        stats = [
            f"HP:        {hp_val}",
            f"RATE:      {self.rate}",
            f"RANGE:     {self.range}",
            f"STRENGTH:  {self.strength}",
            f"TARGETS:   {self.count}",
            f"COST:      {self.cost}$"
        ]
        
        for i, line in enumerate(stats):
            surf = self.font.render(line, True, (200, 205, 210))
            screen.blit(surf, (self.rect.x + 15, self.rect.y + 40 + (i * 20)))
            
        pygame.draw.line(screen, (58, 62, 65), (self.rect.x + 10, self.rect.y + 190), (self.rect.right - 10, self.rect.y + 190))
        
        preview_rect = pygame.Rect(self.rect.x + 15, self.rect.y + 205, self.rect.w - 30, 130)
        pygame.draw.rect(screen, (22, 24, 25), preview_rect)
        pygame.draw.rect(screen, (48, 52, 55), preview_rect, 1)
        
        if self.preview_image:
            img = self.preview_image
            img_w, img_h = img.get_size()
            
            if img_w > preview_rect.w - 10 or img_h > preview_rect.h - 10:
                scale = min((preview_rect.w - 10) / img_w, (preview_rect.h - 10) / img_h)
                img = pygame.transform.scale(img, (int(img_w * scale), int(img_h * scale)))

            img_rect = img.get_rect(center=preview_rect.center)
            screen.blit(img, img_rect.topleft)
        else:
            no_img_txt = self.font.render("[ NO PREVIEW ]", True, (100, 105, 110))
            txt_rect = no_img_txt.get_rect(center=preview_rect.center)
            screen.blit(no_img_txt, txt_rect.topleft)

class CatViewer(DebugWidget):
    def __init__(self):
        super().__init__("Cat Manager", rect=pygame.Rect(100, 100, 340, 460))
        self.close_button = True
        self.mode = "registered"
        
        self.tab_reg = pygame.Rect(0, 0, 0, 0)
        self.tab_act = pygame.Rect(0, 0, 0, 0)
        self.update_rects()

    def update_rects(self):
        super().update_rects()
        self.tab_reg = pygame.Rect(self.rect.x + 10, self.rect.y + 35, 155, 24)
        self.tab_act = pygame.Rect(self.rect.x + 175, self.rect.y + 35, 155, 24)

    def window_input(self):
        im = self.game.input
        touched = False
        
        if self.tab_reg.collidepoint(im.mouse_pos):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                self.mode = "registered"
                touched = True
        elif self.tab_act.collidepoint(im.mouse_pos):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                self.mode = "active"
                touched = True
                
        if hasattr(self.game, 'towerManager'):
            line_height = 20
            start_y = self.rect.y + 75
            
            if self.mode == "registered":
                types = list(self.game.towerManager.initTowers.keys())
                for i, name in enumerate(types):
                    line_rect = pygame.Rect(self.rect.x + 10, start_y + (i * line_height), self.rect.w - 20, line_height)
                    if line_rect.collidepoint(im.mouse_pos):
                        self.game.cursorManager.set_state('hovered')
                        # ЛКМ для списков
                        if im.mouse_pressed(1):
                            cat_cls = self.game.towerManager.initTowers[name]
                            inspector = CatInspector(cat_cls, self.game)
                            self.game.widgetManager.add(inspector)
                            touched = True
                            break
                            
            elif self.mode == "active":
                cats = self.game.towerManager.towers
                for i, cat in enumerate(cats):
                    line_rect = pygame.Rect(self.rect.x + 10, start_y + (i * line_height), self.rect.w - 20, line_height)
                    if line_rect.collidepoint(im.mouse_pos):
                        self.game.cursorManager.set_state('hovered')
                        # ЛКМ для списков
                        if im.mouse_pressed(1):
                            inspector = CatInspector(cat, self.game)
                            self.game.widgetManager.add(inspector)
                            touched = True
                            break
                            
                    # Колесико мыши для клика по башням на ПОЛЕ
                    if cat.rect.collidepoint(im.mouse_pos):
                        if im.mouse_pressed(2):
                            inspector = CatInspector(cat, self.game)
                            self.game.widgetManager.add(inspector)
                            touched = True
                            break

        if self.dragging:
            self.update_rects()

        base_touched = super().window_input()
        return touched or base_touched

    def draw(self):
        super().draw()
        im_pos = self.game.input.mouse_pos
        
        color_reg = (46, 48, 50) if self.tab_reg.collidepoint(im_pos) else ((36, 38, 40) if self.mode == "registered" else (26, 28, 30))
        color_act = (46, 48, 50) if self.tab_act.collidepoint(im_pos) else ((36, 38, 40) if self.mode == "active" else (26, 28, 30))
        
        pygame.draw.rect(screen, color_reg, self.tab_reg)
        pygame.draw.rect(screen, (80, 85, 90) if self.tab_reg.collidepoint(im_pos) else (58, 62, 65), self.tab_reg, 1)
        pygame.draw.rect(screen, color_act, self.tab_act)
        pygame.draw.rect(screen, (80, 85, 90) if self.tab_act.collidepoint(im_pos) else (58, 62, 65), self.tab_act, 1)
        
        txt_reg = self.font.render("REGISTERED", True, (245, 170, 60) if self.mode == "registered" else (130, 135, 140))
        txt_act = self.font.render("ACTIVE ON FIELD", True, (245, 170, 60) if self.mode == "active" else (130, 135, 140))
        screen.blit(txt_reg, (self.tab_reg.x + 35, self.tab_reg.y + 5))
        screen.blit(txt_act, (self.tab_act.x + 20, self.tab_act.y + 5))
        
        if not hasattr(self.game, 'towerManager'):
            error_surf = self.font.render("ERROR: NO TOWER_MANAGER", True, (232, 58, 49))
            screen.blit(error_surf, (self.rect.x + 15, self.rect.y + 75))
            return

        line_height = 20
        start_y = self.rect.y + 75
        
        if self.mode == "registered":
            types = list(self.game.towerManager.initTowers.keys())
            for i, name in enumerate(types):
                line_rect = pygame.Rect(self.rect.x + 10, start_y + (i * line_height), self.rect.w - 20, line_height)
                if line_rect.collidepoint(im_pos):
                    pygame.draw.rect(screen, (52, 56, 60), line_rect)
                
                cost = 0
                if hasattr(self.game, 'storeManager'):
                    for p in self.game.storeManager.products:
                        if getattr(p, 'tower', None) == name:
                            cost = p.cost.value if hasattr(p.cost, 'value') else p.cost
                            break
                
                line_text = f" [{i+1:02d}] {name:<12} | COST: {cost}$"
                surf = self.font.render(line_text, True, (240, 245, 250) if line_rect.collidepoint(im_pos) else (200, 205, 210))
                screen.blit(surf, (self.rect.x + 15, start_y + (i * line_height)))
                
        elif self.mode == "active":
            cats = self.game.towerManager.towers
            if not cats:
                empty_surf = self.font.render(" NO ACTIVE TOWERS IN FIELD.", True, (120, 125, 130))
                screen.blit(empty_surf, (self.rect.x + 15, start_y))
            else:
                for i, cat in enumerate(cats):
                    line_rect = pygame.Rect(self.rect.x + 10, start_y + (i * line_height), self.rect.w - 20, line_height)
                    if line_rect.collidepoint(im_pos):
                        pygame.draw.rect(screen, (52, 56, 60), line_rect)
                        
                    name = cat.__class__.__name__
                    hp_val = cat.hp.value if hasattr(cat.hp, 'value') else cat.hp
                    max_hp_val = cat.max_hp.value if hasattr(cat.max_hp, 'value') else cat.max_hp
                    hp_percent = int((hp_val / max_hp_val) * 100) if max_hp_val > 0 else 0
                    
                    line_text = f" [{i+1:02d}] {name:<12} | HP: {hp_percent:3d}% | X: {cat.rect.x} | Y: {cat.rect.y}"
                    base_color = (96, 227, 73) if hp_val > 0 else (232, 58, 49)
                    color = (min(base_color[0]+30, 255), min(base_color[1]+30, 255), min(base_color[2]+30, 255)) if line_rect.collidepoint(im_pos) else base_color 
                    
                    surf = self.font.render(line_text, True, color)
                    screen.blit(surf, (self.rect.x + 15, start_y + (i * line_height)))

class PlayerEditor(DebugWidget):
    def __init__(self):
        super().__init__("Player Editor", rect=pygame.Rect(0, 0, 260, 320))
        self.close_button = True
        
        # Определим кнопки (текст, тип действия, значение)
        # Типы: 'mod' - изменение числа, 'action' - выполнение
        self.controls = [
            ("Health", "health", 1),
            ("Money", "money", 1),
            ("Strength", "strength", 0.1),
            ("Farm Mult", "farm_muiltipiler", 1),
        ]

    def window_input(self):
        touched = super().window_input()
        player = getattr(self.game, 'player', None)
        if not player: return touched

        im = self.game.input
        m = im.mouse_pos
        
        # Определяем множитель (Shift = x10, Ctrl = x100)
        keys = pygame.key.get_pressed()
        mod = 1
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]: mod = 1000
        elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]: mod = 10
        
        # Кнопка Next Wave
        nw_rect = pygame.Rect(self.rect.x + 20, self.rect.y + 260, self.rect.w - 40, 40)
        if nw_rect.collidepoint(m):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                self.game.waveManager.next_wave()
                touched = True

        # Кнопки изменения параметров
        for i, (name, attr, delta) in enumerate(self.controls):
            y = self.rect.y + 50 + (i * 45)
            btn_minus = pygame.Rect(self.rect.x + 150, y, 30, 25)
            btn_plus = pygame.Rect(self.rect.x + 190, y, 30, 25)
            
            if btn_minus.collidepoint(m) or btn_plus.collidepoint(m):
                self.game.cursorManager.set_state('hovered')
                if im.mouse_pressed(1):
                    # Применяем модификатор
                    step = delta * mod
                    
                    stat_obj = getattr(player, attr)
                    val = stat_obj.value if hasattr(stat_obj, 'value') else stat_obj
                    
                    if btn_minus.collidepoint(m):
                        new_val = round(val - step, 2) if isinstance(delta, float) else val - step
                    else:
                        new_val = round(val + step, 2) if isinstance(delta, float) else val + step
                        
                    if hasattr(stat_obj, 'base'):
                        stat_obj.base = new_val
                    else:
                        setattr(player, attr, new_val)
                    touched = True
                    
        return touched

    def draw(self):
        super().draw()
        im_pos = self.game.input.mouse_pos
        player = getattr(self.game, 'player', None)

        # Если игрока нет, рисуем заглушку
        if not player:
            txt = self.font.render("Player not initialized!", True, (255, 100, 100))
            screen.blit(txt, (self.rect.x + 15, self.rect.y + 50))
            return

        # Иначе рисуем обычный интерфейс
        for i, (name, attr, delta) in enumerate(self.controls):
            y = self.rect.y + 50 + (i * 45)
            stat_obj = getattr(player, attr)
            val = stat_obj.value if hasattr(stat_obj, 'value') else stat_obj
            
            txt = self.font.render(f"{name}: {val}", True, (220, 220, 220))
            screen.blit(txt, (self.rect.x + 15, y + 5))
            
            for btn_rect, label in [(pygame.Rect(self.rect.x + 150, y, 30, 25), "-"), 
                                    (pygame.Rect(self.rect.x + 190, y, 30, 25), "+")]:
                color = (70, 70, 70) if not btn_rect.collidepoint(im_pos) else (90, 90, 90)
                pygame.draw.rect(screen, color, btn_rect)
                pygame.draw.rect(screen, (120, 120, 120), btn_rect, 1)
                lbl = self.font.render(label, True, (255, 255, 255))
                screen.blit(lbl, (btn_rect.x + 10, btn_rect.y + 3))

        nw_rect = pygame.Rect(self.rect.x + 20, self.rect.y + 260, self.rect.w - 40, 40)
        color = (34, 110, 68) if not nw_rect.collidepoint(im_pos) else (46, 139, 87)
        pygame.draw.rect(screen, color, nw_rect, border_radius=5)
        txt = self.font.render("FORCE NEXT WAVE", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=nw_rect.center))

class ProgramHub(DebugWidget):
    def __init__(self):
        # Инициализируем с временным размером, он пересчитается, как только появится доступ к self.game
        super().__init__("Program Hub", rect=pygame.Rect(50, 50, 100, 100))
        self.close_button = True
        
        # Настройки сетки и кнопок
        self.btn_w = 150
        self.btn_h = 35
        self.pad = 10
        self.margin = 15
        self.header_h = 30
        self.pagination_h = 40  # Высота панели страниц
        
        self.cols = 1
        self.rows = 1
        self.pages = 1
        self.current_page = 0
        self.max_per_page = 24
        
        # Флаг для ленивой инициализации (пока менеджер не прокинул self.game)
        self.layout_initialized = False

    def recalculate_layout(self):
        """Динамически рассчитывает идеальные пропорции окна и пагинацию"""
        # Берем список всех программ, кроме самого Хаба (чтобы не открывать Хаб внутри Хаба)
        programs = [p for p in self.game.programManager.list() if p != "ProgramHub"]
        N = len(programs)
        
        if N == 0:
            self.cols = 1
            self.rows = 1
            self.pages = 1
            self.current_page = 0
            self.update_window_size()
            return

        # Максимальные ограничения для одной страницы
        MAX_COLS = 4
        MAX_ROWS = 6
        MAX_PER_PAGE = MAX_COLS * MAX_ROWS  # 24 программы на страницу

        if N <= MAX_PER_PAGE:
            self.pages = 1
            self.current_page = 0
            self.max_per_page = MAX_PER_PAGE
            
            # Ищем комбинацию (колонок и строк), которая ближе всего к пропорции 1.4
            best_cols, best_rows = 1, N
            best_deviation = float('inf')
            target_ratio = 1.4
            
            for c in range(1, min(N, MAX_COLS) + 1):
                r = math.ceil(N / c)
                if r > MAX_ROWS:
                    continue
                
                # Рассчитываем гипотетические размеры окна
                w = 2 * self.margin + c * self.btn_w + (c - 1) * self.pad
                h = self.header_h + self.margin + r * self.btn_h + (r - 1) * self.pad + self.margin
                ratio = w / h
                deviation = abs(ratio - target_ratio)
                
                # Выбираем вариант с наименьшим отклонением от идеальных пропорций
                if deviation < best_deviation:
                    best_deviation = deviation
                    best_cols, best_rows = c, r
            
            self.cols = best_cols
            self.rows = best_rows
        else:
            # Если программ слишком много, включаем максимальную сетку и пагинацию
            self.cols = MAX_COLS
            self.rows = MAX_ROWS
            self.max_per_page = MAX_PER_PAGE
            self.pages = math.ceil(N / MAX_PER_PAGE)
            self.current_page = min(self.current_page, self.pages - 1)
            
        self.update_window_size()

    def update_window_size(self):
        """Пересчитывает физические размеры pygame.Rect окна"""
        w = 2 * self.margin + self.cols * self.btn_w + (self.cols - 1) * self.pad
        h = self.header_h + self.margin + self.rows * self.btn_h + (self.rows - 1) * self.pad + self.margin
        
        # Если страниц больше одной, резервируем место под нижнюю панель навигации
        if self.pages > 1:
            h += self.pagination_h
            
        self.rect.w = w
        self.rect.h = h
        self.update_rects()

    def window_input(self):
        # Инициализируем размеры при первом кадре ввода, когда self.game уже точно существует
        if not self.layout_initialized:
            self.recalculate_layout()
            self.layout_initialized = True
            
        im = self.game.input
        m = im.mouse_pos
        touched = False
        
        programs = [p for p in self.game.programManager.list() if p != "ProgramHub"]
        N = len(programs)
        
        # Срез программ для текущей страницы
        start_idx = self.current_page * self.max_per_page
        end_idx = min(start_idx + self.max_per_page, N)
        page_programs = programs[start_idx:end_idx]
        
        if im.mouse_pressed(1):
            # 1. Проверяем клики по кнопкам программ
            for idx, name in enumerate(page_programs):
                col = idx % self.cols
                row = idx // self.cols
                
                bx = self.rect.x + self.margin + col * (self.btn_w + self.pad)
                by = self.rect.y + self.header_h + self.margin + row * (self.btn_h + self.pad)
                btn_rect = pygame.Rect(bx, by, self.btn_w, self.btn_h)
                
                if btn_rect.collidepoint(m):
                    cls = self.game.programManager.get(name)
                    if cls:
                        # Инстанцируем класс без аргументов (как в DebugConsole)
                        widget = cls()
                        self.game.widgetManager.add(widget)
                        touched = True
                        break
                        
            # 2. Проверяем клики по кнопкам страниц (если они активны)
            if self.pages > 1:
                pag_y = self.rect.bottom - self.pagination_h + 5
                pag_h = self.pagination_h - 10
                prev_btn = pygame.Rect(self.rect.x + self.margin, pag_y, 40, pag_h)
                next_btn = pygame.Rect(self.rect.right - self.margin - 40, pag_y, 40, pag_h)
                
                if prev_btn.collidepoint(m):
                    self.current_page = (self.current_page - 1) % self.pages
                    touched = True
                elif next_btn.collidepoint(m):
                    self.current_page = (self.current_page + 1) % self.pages
                    touched = True

        # Смена состояния курсора при наведении
        for idx, name in enumerate(page_programs):
            col = idx % self.cols
            row = idx // self.cols
            bx = self.rect.x + self.margin + col * (self.btn_w + self.pad)
            by = self.rect.y + self.header_h + self.margin + row * (self.btn_h + self.pad)
            btn_rect = pygame.Rect(bx, by, self.btn_w, self.btn_h)
            if btn_rect.collidepoint(m):
                self.game.cursorManager.set_state('hovered')
                
        if self.pages > 1:
            pag_y = self.rect.bottom - self.pagination_h + 5
            pag_h = self.pagination_h - 10
            prev_btn = pygame.Rect(self.rect.x + self.margin, pag_y, 40, pag_h)
            next_btn = pygame.Rect(self.rect.right - self.margin - 40, pag_y, 40, pag_h)
            if prev_btn.collidepoint(m) or next_btn.collidepoint(m):
                self.game.cursorManager.set_state('hovered')
                
        base_touched = super().window_input()
        if self.dragging:
            self.update_rects()
            
        return touched or base_touched

    def draw(self):
        if not self.layout_initialized:
            return
            
        super().draw()
        
        programs = [p for p in self.game.programManager.list() if p != "ProgramHub"]
        N = len(programs)
        
        start_idx = self.current_page * self.max_per_page
        end_idx = min(start_idx + self.max_per_page, N)
        page_programs = programs[start_idx:end_idx]
        
        m_pos = self.game.input.mouse_pos
        
        # Рисуем кнопки программ
        for idx, name in enumerate(page_programs):
            col = idx % self.cols
            row = idx // self.cols
            
            bx = self.rect.x + self.margin + col * (self.btn_w + self.pad)
            by = self.rect.y + self.header_h + self.margin + row * (self.btn_h + self.pad)
            btn_rect = pygame.Rect(bx, by, self.btn_w, self.btn_h)
            
            # Подсветка при наведении
            color = (60, 60, 60) if not btn_rect.collidepoint(m_pos) else (80, 80, 80)
            
            pygame.draw.rect(screen, color, btn_rect, border_radius=4)
            pygame.draw.rect(screen, (100, 100, 100), btn_rect, 1, border_radius=4)
            
            # Текст по центру кнопки
            txt_surf = self.font.render(name, True, (255, 255, 255))
            txt_rect = txt_surf.get_rect(center=btn_rect.center)
            screen.blit(txt_surf, txt_rect.topleft)
            
        # Рисуем панель страниц (только если страниц действительно больше 1)
        if self.pages > 1:
            pag_y = self.rect.bottom - self.pagination_h + 5
            pag_h = self.pagination_h - 10
            
            prev_btn = pygame.Rect(self.rect.x + self.margin, pag_y, 40, pag_h)
            next_btn = pygame.Rect(self.rect.right - self.margin - 40, pag_y, 40, pag_h)
            
            # Кнопка НАЗАД [<]
            prev_color = (60, 60, 60) if not prev_btn.collidepoint(m_pos) else (80, 80, 80)
            pygame.draw.rect(screen, prev_color, prev_btn, border_radius=4)
            pygame.draw.rect(screen, (100, 100, 100), prev_btn, 1, border_radius=4)
            prev_txt = self.font.render("<", True, (255, 255, 255))
            screen.blit(prev_txt, prev_txt.get_rect(center=prev_btn.center))
            
            # Кнопка ВПЕРЕД [>]
            next_color = (60, 60, 60) if not next_btn.collidepoint(m_pos) else (80, 80, 80)
            pygame.draw.rect(screen, next_color, next_btn, border_radius=4)
            pygame.draw.rect(screen, (100, 100, 100), next_btn, 1, border_radius=4)
            next_txt = self.font.render(">", True, (255, 255, 255))
            screen.blit(next_txt, next_txt.get_rect(center=next_btn.center))
            
            # Номер страницы "Текущая / Всего"
            page_str = f"{self.current_page + 1} / {self.pages}"
            page_surf = self.font.render(page_str, True, (200, 200, 200))
            center_x = (prev_btn.right + next_btn.left) // 2
            page_rect = page_surf.get_rect(center=(center_x, prev_btn.centery))
            screen.blit(page_surf, page_rect.topleft)

# =====================================================================
#                        UI VISUALIZER
# =====================================================================
# Утилита для визуальной расстановки UI-элементов (спрайтов).
# - Создание элементов по имени файла из Data/textures
# - Список всех элементов
# - Редактор X / Y / Scale X / Scale Y / Z / Anchor
# - Визуальное редактирование (drag / resize) только одного элемента за раз
# - Экспорт в Python-код в Data/Logs/UI_MAKER.txt
# =====================================================================

# Глобальный список UI-элементов (общий для всех инстансов UIVisualizer)
_ui_elements = []

# Глобальное состояние визуального редактирования.
_ui_editor_state = {
    'visual_edit_target': None,
    'drag_mode': None,          # 'move' | 'scale_x' | 'scale_y' | None
    'drag_start_mouse': None,   # (x, y)
    'drag_start_scale': None,   # [sx, sy]
    'drag_start_pos': None,     # [x, y]
}


def _blur_all_other_inputs(game, current_widget):
    """
    Снимает фокус текстового ввода со ВСЕХ виджетов, кроме указанного.
    Работает для UIElementEditor (_focused_field), UICreateWindow / Explorer
    (input_focus) и DebugConsole (worded).
    """
    for w in game.widgetManager.widgets:
        if w is current_widget:
            continue
        if hasattr(w, '_focused_field'):
            w._focused_field = None
        if hasattr(w, 'input_focus'):
            w.input_focus = None
        if hasattr(w, 'worded'):
            w.worded = False


def _write_export_file(game, content, mode="w"):
    """
    Записывает строку в Data/Logs/UI_MAKER.txt.
    mode='w' - перезапись, mode='a' - дозапись.
    Возвращает путь (Path) при успехе или None при ошибке.
    """
    try:
        log_dir = game.pathManager.DATA / "Logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        file_path = log_dir / "UI_MAKER.txt"
        with open(file_path, mode, encoding="utf-8") as f:
            f.write(content)
        return file_path
    except Exception as e:
        if hasattr(game, 'console') and game.console:
            game.console.log(f"[UI Visualizer] Ошибка записи файла: {e}", (232, 58, 49))
        return None


class UIElement:
    """Один визуальный элемент. Не имеет функционала, только спрайт + rect."""
    _next_id = 1

    def __init__(self, game, name, pos=(WIDTH // 2, HEIGHT // 2),
                 scale=(64, 64), anchor="center", z=1):
        self.game = game
        self.id = UIElement._next_id
        UIElement._next_id += 1

        self.name = name
        self.scale = [max(1, int(scale[0])), max(1, int(scale[1]))]
        self.anchor = anchor
        self.z = int(z)
        self.pos = [int(pos[0]), int(pos[1])]

        self._build_sprite()

    # ---------- внутреннее ----------
    def _resolve_path(self):
        """Полный путь до картинки. Если файла нет - placeholder.png."""
        base = self.game.pathManager.TEXTURES
        try:
            candidate = base / self.name
            if candidate.exists():
                return candidate
        except Exception:
            pass
        if hasattr(self.game, 'console') and self.game.console:
            self.game.console.log(
                f'[UI Visualizer] Файл не найден: {self.name} -> placeholder.png',
                (255, 200, 100)
            )
        return base / "placeholder.png"

    def _build_sprite(self):
        path = self._resolve_path()
        self.sprite = Sprite(path, scale=tuple(self.scale))
        self.rect = self.sprite.image.get_rect()
        setattr(self.rect, self.anchor, self.pos)

    # ---------- публичное ----------
    def reload_sprite(self):
        anchor_pos = list(getattr(self.rect, self.anchor)) if hasattr(self, 'rect') else list(self.pos)
        self._build_sprite()
        setattr(self.rect, self.anchor, anchor_pos)
        self.pos = list(anchor_pos)

    def set_pos(self, x, y):
        self.pos = [int(x), int(y)]
        setattr(self.rect, self.anchor, self.pos)

    def set_scale(self, sx, sy):
        sx = max(1, min(int(sx), 4096))
        sy = max(1, min(int(sy), 4096))
        if sx == self.scale[0] and sy == self.scale[1]:
            return
        anchor_pos = list(getattr(self.rect, self.anchor))
        self.scale = [sx, sy]
        self.sprite.set_scale((sx, sy))
        self.rect = self.sprite.image.get_rect()
        setattr(self.rect, self.anchor, anchor_pos)
        self.pos = list(anchor_pos)

    def set_anchor(self, new_anchor):
        topleft = self.rect.topleft
        self.anchor = new_anchor
        self.rect = self.sprite.image.get_rect()
        self.rect.topleft = topleft
        self.pos = list(getattr(self.rect, self.anchor))

    def set_z(self, z):
        self.z = int(z)

    def set_name(self, name):
        self.name = name
        self.reload_sprite()

    def draw(self, surface):
        surface.blit(self.sprite.image, self.rect)

    def to_code(self):
        """Python-код, как если бы объект создавался через ObjectManager."""
        return (
            f'obj = objectManager.new_object(\n'
            f'    Sprite(pathManager.TEXTURES / "{self.name}", scale=({self.scale[0]}, {self.scale[1]})),\n'
            f'    ({self.pos[0]}, {self.pos[1]}),\n'
            f'    "{self.anchor}"\n'
            f')\n'
            f'obj.z = {self.z}'
        )


class UIVisualizer(DebugWidget):
    """Главное окно: список элементов + кнопки Create / Export All."""

    def __init__(self):
        super().__init__("UI Visualizer", rect=pygame.Rect(80, 80, 360, 500))
        self.close_button = True

        self.scroll_offset = 0
        self.max_visible_items = 13
        self.item_height = 22

        self._last_click_times = {}

        self.update_rects()

    # ---------------- rects ----------------
    def update_rects(self):
        super().update_rects()
        y = self.rect.y + 35
        self.btn_create = pygame.Rect(self.rect.x + 10, y, 165, 24)
        self.btn_export_all = pygame.Rect(self.rect.x + 185, y, 165, 24)

    # ---------------- ввод по элементам ----------------
    def handle_element_input(self):
        im = self.game.input
        m = im.mouse_pos

        target = _ui_editor_state['visual_edit_target']

        # Режим визуального редактирования
        if target is not None:
            if target not in _ui_elements:
                _ui_editor_state['visual_edit_target'] = None
                _ui_editor_state['drag_mode'] = None
            else:
                if self._process_visual_edit_drag(target):
                    return True

        # Клики по элементам (детект двойного клика)
        if im.mouse_pressed(1):
            sorted_els = sorted(enumerate(_ui_elements),
                                key=lambda x: (x[1].z, x[0]), reverse=True)
            for _, el in sorted_els:
                if el.rect.collidepoint(m):
                    now = pygame.time.get_ticks()
                    last = self._last_click_times.get(el.id, 0)
                    if now - last < 300:
                        self._open_editor(el)
                        self._last_click_times[el.id] = 0
                    else:
                        self._last_click_times[el.id] = now
                    return True

        return False

    # ---------------- визуальное редактирование ----------------
    def _process_visual_edit_drag(self, el):
        im = self.game.input
        m = im.mouse_pos
        state = _ui_editor_state

        # Активный drag
        if state['drag_mode'] is not None:
            if im.mouse_released(1):
                state['drag_mode'] = None
                state['drag_start_mouse'] = None
                state['drag_start_scale'] = None
                state['drag_start_pos'] = None
                return True

            if im.mouse_down(1) and state['drag_start_mouse'] is not None:
                dx = m[0] - state['drag_start_mouse'][0]
                dy = m[1] - state['drag_start_mouse'][1]

                if state['drag_mode'] == 'move':
                    new_x = state['drag_start_pos'][0] + dx
                    new_y = state['drag_start_pos'][1] + dy

                    keys = pygame.key.get_pressed()
                    ctrl = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
                    shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

                    if ctrl and not shift:
                        new_y = state['drag_start_pos'][1]
                    elif shift and not ctrl:
                        new_x = state['drag_start_pos'][0]

                    el.set_pos(new_x, new_y)

                elif state['drag_mode'] == 'scale_x':
                    new_sx = max(1, state['drag_start_scale'][0] + dx)
                    el.set_scale(new_sx, el.scale[1])

                elif state['drag_mode'] == 'scale_y':
                    new_sy = max(1, state['drag_start_scale'][1] - dy)
                    el.set_scale(el.scale[0], new_sy)

                return True

        # Начало нового drag
        if im.mouse_pressed(1):
            right_handle = self._get_right_handle_rect(el)
            top_handle = self._get_top_handle_rect(el)

            if right_handle.collidepoint(m):
                state['drag_mode'] = 'scale_x'
                state['drag_start_mouse'] = m
                state['drag_start_scale'] = el.scale.copy()
                return True
            if top_handle.collidepoint(m):
                state['drag_mode'] = 'scale_y'
                state['drag_start_mouse'] = m
                state['drag_start_scale'] = el.scale.copy()
                return True
            if el.rect.collidepoint(m):
                state['drag_mode'] = 'move'
                state['drag_start_mouse'] = m
                state['drag_start_pos'] = list(el.pos)
                return True

        return False

    def _get_right_handle_rect(self, el):
        s = 10
        return pygame.Rect(el.rect.right - s // 2, el.rect.centery - s // 2, s, s)

    def _get_top_handle_rect(self, el):
        s = 10
        return pygame.Rect(el.rect.centerx - s // 2, el.rect.top - s // 2, s, s)

    # ---------------- прочее ----------------
    def toggle_visual_edit(self, el):
        if _ui_editor_state['visual_edit_target'] is el:
            _ui_editor_state['visual_edit_target'] = None
            _ui_editor_state['drag_mode'] = None
        else:
            _ui_editor_state['visual_edit_target'] = el
            _ui_editor_state['drag_mode'] = None

    def _open_editor(self, el):
        for w in self.game.widgetManager.widgets:
            if isinstance(w, UIElementEditor) and w.element is el and not w.closed:
                self.game.widgetManager.bring_to_front(w)
                return
        self.game.widgetManager.add(UIElementEditor(el))

    def _export_all(self):
        from datetime import datetime

        if not _ui_elements:
            self.game.console.log("[UI Visualizer] Нет элементов для экспорта.", (255, 200, 100))
            return

        lines = []
        lines.append("# " + "=" * 50)
        lines.append("# UI Layout Export")
        lines.append(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"# Elements: {len(_ui_elements)}")
        lines.append("# " + "=" * 50)
        lines.append("")
        lines.append("# context: objectManager, pathManager, Sprite")
        lines.append("")

        for el in _ui_elements:
            lines.append(f"# --- [{el.id:02d}] {el.name} ---")
            lines.append(el.to_code())
            lines.append("")

        content = "\n".join(lines)
        result = _write_export_file(self.game, content, mode="w")

        self.game.console.log("=" * 42, (255, 200, 100))
        self.game.console.log(f"# Экспортировано элементов: {len(_ui_elements)}", (255, 200, 100))
        if result:
            self.game.console.log(f"# Записано в: {result}", (96, 227, 73))
        else:
            self.game.console.log("# Ошибка записи файла", (232, 58, 49))
        self.game.console.log("=" * 42, (255, 200, 100))

    # ---------------- ввод окна ----------------
    def window_input(self):
        im = self.game.input
        m = im.mouse_pos
        touched = False

        if self.btn_create.collidepoint(m):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                w = UICreateWindow()
                self.game.widgetManager.add(w)
                _blur_all_other_inputs(self.game, w)
                touched = True
        elif self.btn_export_all.collidepoint(m):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                self._export_all()
                touched = True

        list_start_y = self.rect.y + 70
        visible_count = min(self.max_visible_items,
                            max(0, len(_ui_elements) - self.scroll_offset))
        for i in range(visible_count):
            idx = self.scroll_offset + i
            item_rect = pygame.Rect(self.rect.x + 10,
                                    list_start_y + i * self.item_height,
                                    self.rect.w - 20, self.item_height)
            if item_rect.collidepoint(m):
                self.game.cursorManager.set_state('hovered')
                if im.mouse_pressed(1):
                    self._open_editor(_ui_elements[idx])
                    touched = True
                    break

        # Скролл колёсиком
        if self.rect.collidepoint(m):
            if im.mouse_pressed(4):
                self.scroll_offset = max(0, self.scroll_offset - 1)
            if im.mouse_pressed(5):
                max_scroll = max(0, len(_ui_elements) - self.max_visible_items)
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)

        base = super().window_input()
        return touched or base

    # ---------------- отрисовка ----------------
    def draw_elements(self):
        if not _ui_elements:
            return

        sorted_els = sorted(enumerate(_ui_elements), key=lambda x: (x[1].z, x[0]))
        for _, el in sorted_els:
            el.draw(screen)

        target = _ui_editor_state['visual_edit_target']
        if target is not None and target in _ui_elements:
            outline = target.rect.inflate(2, 2)
            pygame.draw.rect(screen, (255, 200, 60), outline, 2)

            rh = self._get_right_handle_rect(target)
            th = self._get_top_handle_rect(target)
            mp = self.game.input.mouse_pos

            pygame.draw.rect(screen, (255, 240, 100) if rh.collidepoint(mp) else (255, 200, 60), rh)
            pygame.draw.rect(screen, (0, 0, 0), rh, 1)
            pygame.draw.rect(screen, (255, 240, 100) if th.collidepoint(mp) else (255, 200, 60), th)
            pygame.draw.rect(screen, (0, 0, 0), th, 1)

    def draw(self):
        super().draw()
        im_pos = self.game.input.mouse_pos

        # Кнопки
        for btn, label, base_color in [
            (self.btn_create, "+ Create New", (46, 139, 87)),
            (self.btn_export_all, "Export All", (60, 80, 120)),
        ]:
            hover = btn.collidepoint(im_pos)
            color = tuple(min(255, c + 25) for c in base_color) if hover else base_color
            pygame.draw.rect(screen, color, btn, border_radius=4)
            pygame.draw.rect(screen, (120, 120, 120), btn, 1, border_radius=4)
            t = self.font.render(label, True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=btn.center))

        pygame.draw.line(screen, (70, 75, 80),
                         (self.rect.x + 10, self.rect.y + 66),
                         (self.rect.right - 10, self.rect.y + 66), 1)

        # Список
        list_start_y = self.rect.y + 70
        if not _ui_elements:
            empty = self.font.render("Нет элементов. Нажми [+ Create New]", True, (130, 135, 140))
            screen.blit(empty, (self.rect.x + 15, list_start_y + 5))
            return

        visible_count = min(self.max_visible_items,
                            max(0, len(_ui_elements) - self.scroll_offset))

        for i in range(visible_count):
            idx = self.scroll_offset + i
            el = _ui_elements[idx]
            item_rect = pygame.Rect(self.rect.x + 10,
                                    list_start_y + i * self.item_height,
                                    self.rect.w - 20, self.item_height)
            hover = item_rect.collidepoint(im_pos)
            is_editing = (_ui_editor_state['visual_edit_target'] is el)

            if is_editing:
                pygame.draw.rect(screen, (90, 130, 70), item_rect)
            elif hover:
                pygame.draw.rect(screen, (52, 56, 60), item_rect)

            text = f"[{el.id:02d}] {el.name}"
            info = f"({el.pos[0]},{el.pos[1]}) z={el.z}"

            info_surf = self.font.render(info, True, (150, 160, 170))
            info_x = item_rect.right - info_surf.get_width() - 4

            max_name_w = info_x - item_rect.x - 8
            name_surf = self.font.render(text, True,
                                         (240, 245, 250) if (hover or is_editing) else (200, 205, 210))
            while name_surf.get_width() > max_name_w and len(text) > 4:
                text = text[:-2] + ".."
                name_surf = self.font.render(text, True,
                                             (240, 245, 250) if (hover or is_editing) else (200, 205, 210))

            screen.blit(name_surf, (item_rect.x + 4, item_rect.y + 2))
            screen.blit(info_surf, (info_x, item_rect.y + 2))


class UICreateWindow(DebugWidget):
    """Маленькое окно для ввода имени файла и создания UIElement."""

    def __init__(self):
        super().__init__("Create UI Element", rect=pygame.Rect(0, 0, 320, 130))
        self.close_button = True

        self.input_text = ""
        self.input_focus = True
        self.cursor_timer = 0

        self.update_rects()

    def update_rects(self):
        super().update_rects()
        self.input_rect = pygame.Rect(self.rect.x + 15, self.rect.y + 45,
                                      self.rect.w - 30, 26)
        self.btn_create = pygame.Rect(self.rect.x + 15, self.rect.y + 85, 140, 28)
        self.btn_cancel = pygame.Rect(self.rect.x + 165, self.rect.y + 85, 140, 28)

    # ---------------- ввод ----------------
    def window_input(self):
        im = self.game.input
        m = im.mouse_pos
        touched = False

        # Клик вне окна - снимаем свой фокус
        if im.mouse_pressed(1) and not self.rect.collidepoint(m):
            if self.input_focus:
                self.input_focus = False

        if self.input_rect.collidepoint(m):
            self.game.cursorManager.set_state('text')
            if im.mouse_pressed(1):
                if not self.input_focus:
                    self.input_focus = True
                    _blur_all_other_inputs(self.game, self)
                touched = True

        if self.btn_create.collidepoint(m):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                self._do_create()
                touched = True
        elif self.btn_cancel.collidepoint(m):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                self.close()
                touched = True

        base = super().window_input()
        return touched or base

    def _do_create(self):
        name = self.input_text.strip()
        if not name:
            name = "placeholder.png"
        if '.' not in name:
            name = name + ".png"

        el = UIElement(self.game, name,
                       pos=(WIDTH // 2, HEIGHT // 2),
                       scale=(64, 64), anchor="center", z=1)
        _ui_elements.append(el)

        self.game.console.log(
            f'[UI Visualizer] Создан элемент id={el.id}: {name}',
            (96, 227, 73)
        )
        self.close()

    def update(self):
        im = self.game.input
        if not self.input_focus:
            return

        for char in im.text_queue:
            if len(self.input_text) < 60:
                self.input_text += char
        if im.key_backspace:
            self.input_text = self.input_text[:-1]
        if im.key_enter:
            self._do_create()

    def draw(self):
        super().draw()
        im_pos = self.game.input.mouse_pos

        lbl = self.font.render("Имя файла (напр. cat.png):", True, (200, 200, 200))
        screen.blit(lbl, (self.rect.x + 15, self.rect.y + 24))

        hover = self.input_rect.collidepoint(im_pos)
        pygame.draw.rect(screen, (35, 37, 39), self.input_rect)
        border = (245, 170, 60) if self.input_focus else \
                 ((100, 110, 120) if hover else (80, 85, 90))
        pygame.draw.rect(screen, border, self.input_rect, 1)

        blink = (pygame.time.get_ticks() // 500) % 2 == 0
        cursor = "|" if (self.input_focus and blink) else ""
        txt = self.font.render(self.input_text + cursor, True, (255, 255, 255))
        screen.blit(txt, (self.input_rect.x + 5, self.input_rect.y + 4))

        for btn, label, base_color in [
            (self.btn_create, "Create", (46, 139, 87)),
            (self.btn_cancel, "Cancel", (139, 60, 60)),
        ]:
            h = btn.collidepoint(im_pos)
            color = tuple(min(255, c + 25) for c in base_color) if h else base_color
            pygame.draw.rect(screen, color, btn, border_radius=4)
            pygame.draw.rect(screen, (200, 200, 200), btn, 1, border_radius=4)
            t = self.font.render(label, True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=btn.center))


class UIElementEditor(DebugWidget):
    """Редактор одного UI-элемента: поля + anchor-сетка + Visual Edit + Export/Delete."""

    def __init__(self, element):
        super().__init__(f"Edit: {element.name}", rect=pygame.Rect(0, 0, 300, 430))
        self.close_button = True
        self.element = element

        self._focused_field = None
        self._field_buffers = {}
        self._field_rects = {}
        self._anchor_rects = {}

        self.update_rects()

    # ---------------- геометрия ----------------
    def update_rects(self):
        super().update_rects()

        fields = ['name', 'x', 'y', 'scale_x', 'scale_y', 'z']
        x = self.rect.x + 15
        y = self.rect.y + 40

        self._field_rects = {}
        for i, f in enumerate(fields):
            self._field_rects[f] = pygame.Rect(x + 85, y + i * 26,
                                               self.rect.w - 105, 22)

        grid_size = 24
        gap = 2
        grid_x = x + 85
        grid_y = y + len(fields) * 26 + 14

        anchors = [
            ['topleft', 'midtop', 'topright'],
            ['midleft', 'center', 'midright'],
            ['bottomleft', 'midbottom', 'bottomright'],
        ]
        self._anchor_rects = {}
        for row, names in enumerate(anchors):
            for col, a in enumerate(names):
                rect = pygame.Rect(
                    grid_x + col * (grid_size + gap),
                    grid_y + row * (grid_size + gap),
                    grid_size, grid_size
                )
                self._anchor_rects[a] = rect

        btn_y = grid_y + 3 * (grid_size + gap) + 18
        self.btn_visual_edit = pygame.Rect(x, btn_y, self.rect.w - 30, 32)
        bw = (self.rect.w - 40) // 2
        self.btn_export = pygame.Rect(x, btn_y + 40, bw, 30)
        self.btn_delete = pygame.Rect(x + bw + 10, btn_y + 40, bw, 30)

    # ---------------- значения полей ----------------
    def _get_field_value(self, field):
        el = self.element
        if field == 'name':    return el.name
        if field == 'x':       return str(el.pos[0])
        if field == 'y':       return str(el.pos[1])
        if field == 'scale_x': return str(el.scale[0])
        if field == 'scale_y': return str(el.scale[1])
        if field == 'z':       return str(el.z)
        return ""

    def _apply_name(self, text):
        text = text.strip()
        if not text:
            return
        self.element.set_name(text)
        self.title = f"Edit: {self.element.name}"

    def _try_apply_numeric(self, field, text):
        text = text.strip()
        if text == "" or text == "-":
            return
        try:
            v = int(text)
        except ValueError:
            return
        el = self.element
        if field == 'x':       el.set_pos(v, el.pos[1])
        elif field == 'y':     el.set_pos(el.pos[0], v)
        elif field == 'scale_x': el.set_scale(v, el.scale[1])
        elif field == 'scale_y': el.set_scale(el.scale[0], v)
        elif field == 'z':     el.set_z(v)

    # ---------------- ввод ----------------
    def window_input(self):
        im = self.game.input
        m = im.mouse_pos
        touched = False

        # Клик вне окна - снимаем свой фокус
        if im.mouse_pressed(1) and not self.rect.collidepoint(m):
            if self._focused_field is not None:
                self._focused_field = None

        # Клик по полям
        for field, rect in self._field_rects.items():
            if rect.collidepoint(m):
                self.game.cursorManager.set_state('text')
                if im.mouse_pressed(1):
                    if self._focused_field == 'name' and self._focused_field != field:
                        self._apply_name(self._field_buffers.get('name', ''))
                    if self._focused_field != field:
                        _blur_all_other_inputs(self.game, self)
                    self._focused_field = field
                    self._field_buffers[field] = self._get_field_value(field)
                    touched = True
                    break

        # Anchor
        for anchor, rect in self._anchor_rects.items():
            if rect.collidepoint(m):
                self.game.cursorManager.set_state('hovered')
                if im.mouse_pressed(1):
                    self.element.set_anchor(anchor)
                    touched = True
                    break

        # Кнопки
        if self.btn_visual_edit.collidepoint(m):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                visualizer = self._find_visualizer()
                if visualizer:
                    visualizer.toggle_visual_edit(self.element)
                touched = True
        elif self.btn_export.collidepoint(m):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                content = "\n" + f"# --- [{self.element.id:02d}] {self.element.name} ---" + "\n" \
                          + self.element.to_code() + "\n"
                result = _write_export_file(self.game, content, mode="a")
                for line in self.element.to_code().split('\n'):
                    self.game.console.log(line, (200, 220, 255))
                if result:
                    self.game.console.log(f"# Append to {result}", (96, 227, 73))
                touched = True
        elif self.btn_delete.collidepoint(m):
            self.game.cursorManager.set_state('hovered')
            if im.mouse_pressed(1):
                self._delete()
                touched = True

        base = super().window_input()
        return touched or base

    def _find_visualizer(self):
        for w in self.game.widgetManager.widgets:
            if isinstance(w, UIVisualizer) and not w.closed:
                return w
        v = UIVisualizer()
        self.game.widgetManager.add(v)
        return v

    def _delete(self):
        if _ui_editor_state['visual_edit_target'] is self.element:
            _ui_editor_state['visual_edit_target'] = None
            _ui_editor_state['drag_mode'] = None

        if self.element in _ui_elements:
            _ui_elements.remove(self.element)
        self.close()

    # ---------------- update ----------------
    def update(self):
        if self.element not in _ui_elements:
            self.close()
            return

        im = self.game.input
        if self._focused_field is None:
            return

        field = self._focused_field
        buf = self._field_buffers.get(field, "")

        for char in im.text_queue:
            buf += char
        if im.key_backspace:
            buf = buf[:-1]
        self._field_buffers[field] = buf

        if field == 'name':
            if im.key_enter:
                self._apply_name(buf)
                self._focused_field = None
        else:
            self._try_apply_numeric(field, buf)
            if im.key_enter:
                self._focused_field = None

    # ---------------- отрисовка ----------------
    def draw(self):
        super().draw()
        im_pos = self.game.input.mouse_pos
        el = self.element

        labels = [
            ('name', 'Name:'),
            ('x', 'X:'),
            ('y', 'Y:'),
            ('scale_x', 'Scale X:'),
            ('scale_y', 'Scale Y:'),
            ('z', 'Z:'),
        ]
        for field, label in labels:
            rect = self._field_rects[field]

            lbl = self.font.render(label, True, (200, 205, 210))
            screen.blit(lbl, (self.rect.x + 15, rect.y + 3))

            focused = (self._focused_field == field)
            hover = rect.collidepoint(im_pos)

            pygame.draw.rect(screen, (35, 37, 39), rect)
            border = (245, 170, 60) if focused else \
                     ((100, 110, 120) if hover else (80, 85, 90))
            pygame.draw.rect(screen, border, rect, 1)

            if focused:
                value = self._field_buffers.get(field, '')
            else:
                value = self._get_field_value(field)

            if self.font.size(value)[0] > rect.w - 10:
                value = value[:22] + ".."

            blink = (pygame.time.get_ticks() // 500) % 2 == 0
            cursor = "|" if (focused and blink) else ""
            surf = self.font.render(value + cursor, True, (255, 255, 255))
            screen.blit(surf, (rect.x + 5, rect.y + 3))

        # Лейбл Anchor
        anchor_lbl = self.font.render("Anchor:", True, (200, 205, 210))
        first_anchor_rect = self._anchor_rects['topleft']
        screen.blit(anchor_lbl, (self.rect.x + 15, first_anchor_rect.y + 4))

        for anchor, rect in self._anchor_rects.items():
            selected = (el.anchor == anchor)
            hover = rect.collidepoint(im_pos)
            if selected:
                color = (245, 170, 60)
            elif hover:
                color = (90, 90, 90)
            else:
                color = (55, 58, 60)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (110, 115, 120), rect, 1)
            if selected:
                pygame.draw.circle(screen, (255, 255, 255), rect.center, 3)

        # Кнопка Visual Edit
        is_editing = (_ui_editor_state['visual_edit_target'] is el)
        hover = self.btn_visual_edit.collidepoint(im_pos)
        if is_editing:
            base_color = (46, 139, 87) if hover else (34, 110, 68)
            label = "Visual Edit: ON"
        else:
            base_color = (60, 60, 110) if hover else (45, 45, 80)
            label = "Visual Edit: OFF"
        pygame.draw.rect(screen, base_color, self.btn_visual_edit, border_radius=4)
        pygame.draw.rect(screen, (150, 150, 150), self.btn_visual_edit, 1, border_radius=4)
        t = self.font.render(label, True, (255, 255, 255))
        screen.blit(t, t.get_rect(center=self.btn_visual_edit.center))

        # Export
        hover = self.btn_export.collidepoint(im_pos)
        color = (70, 100, 140) if hover else (50, 70, 100)
        pygame.draw.rect(screen, color, self.btn_export, border_radius=4)
        pygame.draw.rect(screen, (150, 150, 150), self.btn_export, 1, border_radius=4)
        t = self.font.render("Export", True, (255, 255, 255))
        screen.blit(t, t.get_rect(center=self.btn_export.center))

        # Delete
        hover = self.btn_delete.collidepoint(im_pos)
        color = (180, 60, 60) if hover else (140, 40, 40)
        pygame.draw.rect(screen, color, self.btn_delete, border_radius=4)
        pygame.draw.rect(screen, (200, 200, 200), self.btn_delete, 1, border_radius=4)
        t = self.font.render("Delete", True, (255, 255, 255))
        screen.blit(t, t.get_rect(center=self.btn_delete.center))

# Console
class DebugConsole(DebugWidget):
    def __init__(self):
        super().__init__("console", rect=pygame.Rect(WIDTH//2, HEIGHT//2, 500, 350))
        self.close_button = True
        self.visible = True
        
        self.cursor_visible = False
        self.cursor_timer = 0
        self.cursor_blink_speed = 500
        
        self.colors = {
            "error": (232, 58, 49),
            "success": (96, 227, 73)
        }
        
        # Используем список вместо словаря, чтобы одинаковые логи не заменяли друг друга
        self.logs = []
        self.current_input = ""
        self.worded = False

        # --- ПЕРЕМЕННЫЕ ДЛЯ ИСТОРИИ И ВВОДА ---
        self.history = []            # Список для хранения истории команд
        self.history_index = 0       # Текущий индекс в истории
        self.saved_input = ""        # Буфер для сохранения недописанного текста пользователя
        self.prev_up_pressed = False # Флаг удержания стрелочки Вверх
        self.prev_down_pressed = False # Флаг удержания стрелочки Вниз

        # --- ПЕРЕМЕННЫЕ ДЛЯ ИЗМЕНЕНИЯ РАЗМЕРА (РЕСАЙЗА) ---
        self.resizing = False
        self.min_w = 300             # Минимальная ширина консоли
        self.min_h = 200             # Минимальная высота консоли
        
    def update_rects(self):
        super().update_rects()
        
        left_offset = 100
        self.down_board = 6
        y_down_scale = 35
        y_down_bar = self.rect.y+self.rect.h-y_down_scale
        
        self.down_bar = pygame.Rect(self.rect.x, y_down_bar, self.rect.w-left_offset, y_down_scale)
        self.right_down_bar = pygame.Rect(self.rect.x+self.rect.w-left_offset, y_down_bar, left_offset, y_down_scale)
        
        self.button = pygame.Rect(self.rect.x+self.rect.w-left_offset, y_down_bar+self.down_board, left_offset-self.down_board, y_down_scale-self.down_board*2)
    
    def log(self, text, color = (255, 255, 255)):
        # Добавляем кортеж (текст, цвет) в конец списка логов
        self.logs.append((text, color))
    
    def execute_command(self, command):
        self.log("> " + command)
        
        # --- ЗАПИСЬ В ИСТОРИЮ ---
        if command.strip():
            if not self.history or self.history[-1] != command:
                self.history.append(command)
            self.history_index = len(self.history) # Сбрасываем указатель в конец истории

        command_split = command.split()
        if len(command_split) > 0:
            if command_split[0]=="help":
                self.log("clear - clear logs") 
                self.log("restart <arg1> - reboots the arg1")
                self.log("program <name> - opens the program")
                self.log("program list - full list of programs")
            elif command_split[0]=="clear":
                self.logs = []
            elif command_split[0]=="restart":
                if len(command_split) > 1:
                    if command_split[1]=="game":
                        self.game.running = False
                        Game = self.game.__class__()
                    elif command_split[1]=="console":
                        console = DebugConsole()
                        self.game.widgetManager.add(console)
                        self.game.console = console
                        self.closed = True
                    else:
                        self.log("Invalid argument", self.colors["error"])
                else:
                    self.log("restart game - reboots the game")
                    self.log("restart console - reboots the console")
            elif command_split[0]=="program":
                if len(command_split) > 1:
                    if command_split[1]=="list":
                        programs = self.game.programManager.list()
                        self.log("Full list programs:")
                        for p in programs:
                            self.log("- " + p)
                    else:
                        program = self.game.programManager.get(command_split[1])
                        if program == None:
                            self.log('Invalid program', self.colors["error"])
                        else:
                            p=program()
                            self.game.widgetManager.add(p)
                            self.log('Success', self.colors["success"])
                else:
                    self.log('No argument "name"', self.colors["error"])
            elif command_split[0]=="kill":
                if len(command_split) > 1:
                    if command_split[1]=="all":
                        for dog in self.game.enemyManager.enemies:
                            dog.alive = False
                        for cat in self.game.towerManager.towers:
                            cat.alive = False
                        self.log('Success', self.colors["success"])
                    elif command_split[1]=="dogs":
                        for dog in self.game.enemyManager.enemies:
                            dog.alive = False
                        self.log('Success', self.colors["success"])
                    elif command_split[1]=="cats":
                        for cat in self.game.towerManager.towers:
                            cat.alive = False
                        self.log('Success', self.colors["success"])
                    else:
                        self.log('Invalid argument, try: "dogs/cats/all"', self.colors["error"])
                else:
                    self.log('No argument "dogs/cats/all"', self.colors["error"])
            elif command_split[0]=="unlock": # Не работает
                self.game.storeManager.unlock_all()
            # elif command_split[0]=="object": В пизду, мне лень
                # if len(command_split) > 1 and self.game:
                    # obj_manager = self.game.sceneManager.current.objects
                    # bro = self.objects.new_object(command_split[1], [0, 0], 'center')
                # else:
                    # self.log('Nahui idi', self.colors["error"])
            else:
                self.log("Invalid command", self.colors["error"])
    
    def window_input(self):
        im = self.game.input
        touched = False

        # Зона изменения размера (уголок 15х15 пикселей в правом нижнем углу)
        resize_rect = pygame.Rect(self.rect.right - 15, self.rect.bottom - 15, 15, 15)
        
        if resize_rect.collidepoint(im.mouse_pos):
            self.game.cursorManager.set_state('hovered')
        elif self.down_bar.collidepoint(im.mouse_pos):
            self.game.cursorManager.set_state('text')
            if not self.worded and im.mouse_pressed(1):
                self.worded = True
                self.cursor_visible = False
                self.cursor_timer = 0
                self.cursor_blink_speed = 500

        if self.close_button and self.close_btn.collidepoint(im.mouse_pos):
            self.game.cursorManager.set_state('hovered')
        if self.button.collidepoint(im.mouse_pos) and not resize_rect.collidepoint(im.mouse_pos):
            self.game.cursorManager.set_state('hovered')

        if im.mouse_pressed(1):
            if resize_rect.collidepoint(im.mouse_pos):
                self.resizing = True
                touched = True
            elif self.close_button and self.close_btn.collidepoint(im.mouse_pos):
                self.close()
            elif self.button.collidepoint(im.mouse_pos) and self.current_input:
                command = self.current_input
                self.current_input = ""
                self.execute_command(command)
            elif self.header.collidepoint(im.mouse_pos):
                self.dragging = True
                self.drag_offset = (im.mouse_pos[0] - self.rect.x, im.mouse_pos[1] - self.rect.y)
            if self.rect.collidepoint(im.mouse_pos):
                self.game.widgetManager.bring_to_front(self)
                touched = True

        # Логика перетаскивания (Drag)
        if self.dragging:
            if im.mouse_released(1):
                self.dragging = False
            else:
                self.rect.x, self.rect.y = min(max(im.mouse_pos[0] - self.drag_offset[0], 0), WIDTH-5), min(max(im.mouse_pos[1] - self.drag_offset[1], 0), HEIGHT-5)
                self.update_rects()
                touched = True

        # Логика изменения размера (Resize)
        if self.resizing:
            if im.mouse_released(1):
                self.resizing = False
            else:
                self.rect.w = min(max(im.mouse_pos[0] - self.rect.x, self.min_w), WIDTH - self.rect.x)
                self.rect.h = min(max(im.mouse_pos[1] - self.rect.y, self.min_h), HEIGHT - self.rect.y)
                self.update_rects()
                touched = True

        return touched
    
    def update(self):
        im = self.game.input
        
        # Cursor
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_timer > self.cursor_blink_speed:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time
        
        # Select word input
        if (im.mouse_pressed(1) or im.mouse_pressed(2) or im.mouse_pressed(3)) and not self.down_bar.collidepoint(im.mouse_pos):
            self.worded = False
            
        # Input
        if self.worded:
            for char in im.text_queue:
                self.current_input += char
            
            # --- ОБРАБОТКА BACKSPACE (ОБЫЧНЫЙ И С CTRL) ---
            if im.key_backspace:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    s = self.current_input.rstrip()
                    idx = s.rfind(' ')
                    if idx == -1:
                        self.current_input = ""
                    else:
                        self.current_input = s[:idx + 1]
                else:
                    self.current_input = self.current_input[:-1]
            
            if im.key_enter and self.current_input:
                input_val = self.current_input
                self.current_input = ""
                self.execute_command(input_val)

            # --- ОБРАБОТКА СТРЕЛОЧЕК ---
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_UP]:
                if not self.prev_up_pressed:
                    if self.history:
                        if self.history_index == len(self.history):
                            self.saved_input = self.current_input
                        
                        self.history_index = max(0, self.history_index - 1)
                        self.current_input = self.history[self.history_index]
                self.prev_up_pressed = True
            else:
                self.prev_up_pressed = False
                
            if keys[pygame.K_DOWN]:
                if not self.prev_down_pressed:
                    if self.history:
                        self.history_index = min(len(self.history), self.history_index + 1)
                        
                        if self.history_index == len(self.history):
                            self.current_input = self.saved_input
                        else:
                            self.current_input = self.history[self.history_index]
                self.prev_down_pressed = True
            else:
                self.prev_down_pressed = False
    
    def close(self):
        self.game.widgetManager.visible = False
    
    def draw(self):
        super().draw()
        # Down Bar
        db = self.down_bar
        pygame.draw.rect(screen, (40, 40, 40), db)
        pygame.draw.rect(screen, (100, 100, 100), db, self.down_board)
        pygame.draw.line(screen, (153, 153, 153), (db.x+self.down_board, db.y+db.h-self.down_board), (db.x+db.w-self.down_board, db.y+db.h-self.down_board))
        pygame.draw.line(screen, (153, 153, 153), (db.x+db.w-self.down_board, db.y+db.h-self.down_board), (db.x+db.w-self.down_board, db.y+self.down_board))
        
        pygame.draw.rect(screen, (100, 100, 100), self.right_down_bar)
        
        # Button
        b = self.button
        pygame.draw.rect(screen, (117, 117, 117) if self.button.collidepoint(self.game.input.mouse_pos) else (100, 100, 100), b)
        pygame.draw.line(screen, (40, 40, 40), (b.x, b.y), (b.x, b.y+b.h-2))
        pygame.draw.line(screen, (40, 40, 40), (b.x, b.y), (b.x+b.w-2, b.y))
        pygame.draw.line(screen, (153, 153, 153), (b.x+1, b.y+1), (b.x+1, b.y+b.h-2+1))
        pygame.draw.line(screen, (153, 153, 153), (b.x+1, b.y+1), (b.x+b.w-2+1, b.y+1))
        pygame.draw.line(screen, (40, 40, 40), (b.x, b.y+b.h-2), (b.x+b.w-1, b.y+b.h-2), 2)
        pygame.draw.line(screen, (40, 40, 40), (b.x+b.w-2, b.y+b.h-2), (b.x+b.w-2, b.y), 2)
        
        submit_surf = self.font.render("Submit", True, (255, 255, 255))
        submit_rect = submit_surf.get_rect(center=b.center)
        screen.blit(submit_surf, submit_rect)
        
        # --- ИЗМЕНЕНО: Динамический расчет высоты и ширины для логов ---
        line_height = self.font.get_height() + 2
        available_height = (self.down_bar.y) - (self.rect.y + 35)
        max_lines = max(1, available_height // line_height)
        max_width = self.rect.w - 20 # 10px отступы слева и справа
        
        # Список для хранения уже перенесенных строк
        all_wrapped_lines = []
        
        # Алгоритм Word Wrap (Перенос строк)
        for text, color in self.logs:
            # На случай, если в самом тексте есть явные символы \n
            paragraphs = text.split('\n')
            for paragraph in paragraphs:
                words = paragraph.split(' ')
                current_line = ""
                for word in words:
                    # Если само по себе слово шире, чем окно консоли (например, длинный путь или спам букв)
                    if self.font.size(word)[0] > max_width:
                        if current_line:
                            all_wrapped_lines.append((current_line, color))
                            current_line = ""
                        # Бьем это длинное слово посимвольно
                        for char in word:
                            test_line = current_line + char
                            if self.font.size(test_line)[0] <= max_width:
                                current_line = test_line
                            else:
                                if current_line:
                                    all_wrapped_lines.append((current_line, color))
                                current_line = char
                    else:
                        test_line = current_line + " " + word if current_line else word
                        if self.font.size(test_line)[0] <= max_width:
                            current_line = test_line
                        else:
                            if current_line:
                                all_wrapped_lines.append((current_line, color))
                            current_line = word
                if current_line:
                    all_wrapped_lines.append((current_line, color))
        
        # Берем только те последние строки, которые физически помещаются на экране
        visible_lines = all_wrapped_lines[-max_lines:]
        
        # Отрисовка логов
        for i, (line_text, line_color) in enumerate(visible_lines):
            text_surf = self.font.render(line_text, True, line_color)
            screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 35 + (i * line_height)))
            
        cursor = "|" if self.cursor_visible and self.worded else ""
        input_surf = self.font.render(" > " + self.current_input + cursor, True, (255, 255, 0))
        screen.blit(input_surf, (self.down_bar.x + 5, self.down_bar.y + 7))

        # Визуальный индикатор изменения размера
        br_x, br_y = self.rect.right, self.rect.bottom
        pygame.draw.line(screen, (50, 50, 50), (br_x - 3, br_y - 10), (br_x - 10, br_y - 3), 1)
        pygame.draw.line(screen, (50, 50, 50), (br_x - 3, br_y - 6), (br_x - 6, br_y - 3), 1)
        
programManager = ProgramManager()
programManager.init("DogViewer", DogViewer)
programManager.init("CatViewer", CatViewer)
programManager.init("Explorer", Explorer)
programManager.init("Player", PlayerEditor)
programManager.init("UIVisualizer", UIVisualizer)
programManager.init("hub", ProgramHub)