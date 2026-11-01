import pygame, copy, math, time
from config import *
from pygame import gfxdraw

# Funk
def radius(pos=(0,0), color=(255, 255, 255), rad=0):
    if rad >0:
        gfxdraw.aacircle(screen, pos[0], pos[1], round(rad), color)

# Math
class Modifier:
    def __init__(self, name, value, mode="add"): # add; multiply; precent
        self.name = name
        self.value = value
        self.mode = mode

class Stat:
    def __init__(self, base):
        self.base = base
        self.mods = []
    
    def add(self, mod):
        if mod not in self.mods:
            self.mods.append(mod)
    
    def remove(self, mod):
        if mod in self.mods:
            self.mods.remove(mod)
    
    def clear(self):
        self.mods = []
    
    @property
    def value(self):
        value = self.base 
        for mod in self.mods:
            if mod.mode == "add":
                value += mod.value
            elif mod.mode == "multiply":
                value += self.base*mod.value
            elif mod.mode == "precent":
                value += self.base / 100 * mod.value
        return value

class Event:
    def __init__(self, event, func):
        self.event = event
        self.func = func
        self.canceled = False
    
    def trigger(self):
        self.func()
    
    def cancel(self):
        self.canceled = True

# Player
class Player:
    def __init__(self, game):
        self.game = game
        self.health = Stat(9)
        self.money = Stat(30)
        self.farm_muiltipiler = Stat(3) # Когда собаки дохнут множитель фарма
        self.strength = Stat(0.1)
    
    def cheak_death(self):
        return self.health.value <= 0
    
    def death(self):
        print("Gay over")
        self.game.sceneManager.go("death")

class PlayerOffside:
    def __init__(self, game, data):
        self.game = game
        self.version = data.get("version", version)
        # self.xp = data.get("xp", 0)
        # self.level = data.get("level", 1)
        # self.points = data.get("points", 0)
        self.coins = data.get("coins", 0)
        self.upgrades = data.get("upgrades", [])
        self.record = data.get("record", 0)
        self.EntryTime = time.time()
        self.ExitTime = time.time()
        self.time = data.get("time", 0)

    def entry_to_game(self):
        self.time = self.time+round(self.ExitTime-self.EntryTime)
        self.EntryTime = time.time()
        self.ExitTime = time.time()
        self.game.saveManager.save_game()

    def give_money(self, amount):
        self.coins += amount
        self.game.saveManager.save_game()

    def to_dict(self):
        return {
            "version": self.version,
            "coins": self.coins,
            "upgrades": self.upgrades,
            "record": self.record,
            
            "time": self.time,
            "EntryTime": self.EntryTime,
            "ExitTime": self.ExitTime
        }

# Classes
class Sprite:
    _image_cache = {}
    _surface_cache = {}
    _original_images = {}  # Кеш для оригинальных изображений

    def __init__(self, path=None, scale=None, color=None, size=(100, 100), alpha=255, flip_x=False, flip_y=False, angle=0, mode="Stretch"):
        self.path = datapackM.get(path)
        self.scale = [int(scale[0]), int(scale[1])] if scale else None
        self.color = tuple(color) if color else (100, 100, 255)
        self.size = [int(size[0]), int(size[1])] if size else (100, 100)
        self.alpha = max(0, min(255, int(alpha)))
        self.flip_x = bool(flip_x)
        self.flip_y = bool(flip_y)
        self.angle = int(angle)
        self.mode = mode
        self.image = self._get_image()

    @classmethod
    def clear_cache(cls):
        cls._image_cache.clear()
        cls._surface_cache.clear()
        cls._original_images.clear()

    def _get_original_image(self):
        """Получает оригинальное изображение без масштабирования"""
        if self.path and self.path != "placeholder.png":
            if self.path not in Sprite._original_images:
                try:
                    img = pygame.image.load(self.path).convert_alpha()
                    Sprite._original_images[self.path] = img
                except (FileNotFoundError, pygame.error):
                    return None
            return Sprite._original_images[self.path].copy()
        return None

    def _fit_image(self, img, target):
        mode = self.mode or "Stretch"
        if mode == "Stretch":
            return pygame.transform.smoothscale(img, target)
        iw, ih = img.get_size()
        tw, th = target
        if mode in ("Fit", "Fill"):
            ratio = min(tw / iw, th / ih) if mode == "Fit" else max(tw / iw, th / ih)
            scaled = pygame.transform.smoothscale(img, (max(1, int(iw * ratio)), max(1, int(ih * ratio))))
            canvas = pygame.Surface(target, pygame.SRCALPHA)
            canvas.blit(scaled, ((tw - scaled.get_width()) // 2, (th - scaled.get_height()) // 2))
            return canvas
        if mode == "Center":
            canvas = pygame.Surface(target, pygame.SRCALPHA)
            canvas.blit(img, ((tw - iw) // 2, (th - ih) // 2))
            return canvas
        if mode == "Tile":
            canvas = pygame.Surface(target, pygame.SRCALPHA)
            for x in range(0, tw, iw):
                for y in range(0, th, ih):
                    canvas.blit(img, (x, y))
            return canvas
        return pygame.transform.smoothscale(img, target)

    def _get_image(self):
        target = tuple(self.scale or self.size)
        
        # Проверяем кеш
        key = (self.path, target, self.color, self.alpha, self.flip_x, self.flip_y, self.angle, self.mode)
        if key in Sprite._image_cache:
            return Sprite._image_cache[key]
        
        # Получаем оригинальное изображение
        img = self._get_original_image()
        
        # Если нет изображения, создаём цветной прямоугольник
        if img is None:
            surf_key = (target, self.color)
            if surf_key not in Sprite._surface_cache:
                surf = pygame.Surface(target, pygame.SRCALPHA)
                surf.fill(self.color)
                Sprite._surface_cache[surf_key] = surf
            img = Sprite._surface_cache[surf_key].copy()
        else:
            # Масштабируем оригинальное изображение
            if img.get_size() != target:
                img = self._fit_image(img, target)
        
        # Применяем трансформации
        if self.flip_x or self.flip_y:
            img = pygame.transform.flip(img, self.flip_x, self.flip_y)
        if self.angle:
            img = pygame.transform.rotate(img, self.angle)
        if self.alpha != 255:
            img = img.copy()
            img.set_alpha(self.alpha)
        
        Sprite._image_cache[key] = img
        return img

    def set_scale(self, new_scale):
        self.scale = [int(new_scale[0]), int(new_scale[1])]
        # Очищаем кеш для этого объекта
        keys_to_remove = []
        for key in Sprite._image_cache:
            if key[0] == self.path and key[2] == self.color:  # Проверяем путь и цвет
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del Sprite._image_cache[key]
        self.image = self._get_image()
        return self.image

class Object:
    def __init__(self, sprite, pos, anchor="topleft"):
        self.sprite = sprite
        self.anchor = anchor
        self.pos = list(pos)
        self.rect = self.sprite.image.get_rect()
        self.clicked = False
        self.hovered = False
        self.set_position(pos, anchor)
        self.animator = None
        self.render_rect = None
        
        self.visible = True
        
        # Копируем все атрибуты чтобы все уникальные были, ибо щас пиздец с этим
        for attr_name, attr_value in list(self.__class__.__dict__.items()):
            if isinstance(attr_value, Stat):
                
                setattr(self, attr_name, copy.deepcopy(attr_value))

    def set_sprite(self, sprite):
        self.sprite = sprite
        old_anchor, old_pos = self.anchor, list(self.pos)
        self.rect = self.sprite.image.get_rect()
        self.set_position(old_pos, old_anchor)

    def set_scale(self, new_scale):
        """Изменяет масштаб спрайта и обновляет все связанные данные"""
        self.sprite.set_scale(new_scale)
        # Обновляем rect
        self.rect = self.sprite.image.get_rect()
        # Восстанавливаем позицию с текущим якорем
        setattr(self.rect, self.anchor, self.pos)

    def set_position(self, pos, anchor=None):
        self.pos = [int(pos[0]), int(pos[1])]
        if anchor is not None:
            self.anchor = anchor
        setattr(self.rect, self.anchor, self.pos)

    def click(self):
        return self.game.input.mouse_pressed(1) and self.rect.collidepoint(self.game.input.mouse_pos)
    
    def hover(self):
        return self.rect.collidepoint(self.game.input.mouse_pos)
    
    def update(self):
        self.clicked = self.click()
        self.hovered = self.hover()
    
    def draw(self):
        if not screen or not self.visible:
            return

        # 1. Сначала подготавливаем изображение (с анимацией или без)
        if hasattr(self, 'animator') and self.animator and self.animator.playing:
            state = self.animator.get_state()
            
            # Размеры
            target_w = max(1, int(self.rect.width * state.get("scale_x", 1.0)))
            target_h = max(1, int(self.rect.height * state.get("scale_y", 1.0)))
            
            img = self.sprite.image.copy()
            if img:
                if img.get_size() != (target_w, target_h):
                    img = pygame.transform.smoothscale(img, (target_w, target_h))
                if self.sprite.flip_x or self.sprite.flip_y:
                    img = pygame.transform.flip(img, self.sprite.flip_x, self.sprite.flip_y)
                
                # Вращение
                total_rot = self.sprite.angle + state.get("rotation", 0)
                if total_rot != 0:
                    img = pygame.transform.rotate(img, total_rot)
                    
                if self.sprite.alpha != 255:
                    img.set_alpha(self.sprite.alpha)
            else:
                img = pygame.Surface((target_w, target_h), pygame.SRCALPHA)
                img.fill(self.sprite.color)
            
            # Расчет позиции с учетом якоря и смещения (offset)
            ratio_x = self.rect.width / 80.0
            ratio_y = self.rect.height / 80.0
            
            anim_anchor = self.animator.current_anim.get("anchor", "center")
            base_pos = getattr(self.rect, anim_anchor)
            
            self.render_rect = img.get_rect()
            setattr(self.render_rect, anim_anchor, (
                base_pos[0] + int(state.get("offset_x", 0) * ratio_x),
                base_pos[1] + int(state.get("offset_y", 0) * ratio_y)
            ))
        else:
            # Если анимации нет — берем обычный спрайт и его rect
            img = self.sprite.image
            self.render_rect = self.rect

        # 2. Отрисовываем сам спрайт
        screen.blit(img, self.render_rect)

        # 3. ЕСЛИ ИДЕТ ВСПЫШКА — накладываем маску поверх отрисованного кадра!
        if getattr(self, "flash_timer", 0) > 0 and getattr(self, "flash_color", None):
            fade_ratio = self.flash_timer / self.flash_duration
            alpha = int(102 * fade_ratio) # Начальная прозрачность 0.6 (интенсивность цвета 0.4)
            
            r, g, b, _ = self.flash_color
            current_color = (r, g, b, alpha)

            # Берем маску прямо из подготовленного (уже сжатого/повернутого) img!
            mask = pygame.mask.from_surface(img)
            flash_surf = mask.to_surface(setcolor=current_color, unsetcolor=(0, 0, 0, 0))
            
            # Рисуем точно поверх подготовленного render_rect
            screen.blit(flash_surf, self.render_rect)

class Animator:
    def __init__(self, anim_manager):
        self.manager = anim_manager
        self.current_anim = None
        self.current_name = None
        self.last_name = None
        self.frame = 0
        self.frame_accumulator = 0.0
        self.loop = True
        self.playing = False
        self.reverse = False 
        self.speed_play = 1.0

    def play(self, anim_name, loop=True, reverse=False, force = True, speed = 1.0):
        if not force and self.playing and self.current_name == anim_name and self.reverse == reverse:
            return
        if anim_name in self.manager.animations:
            self.speed_play = speed
            self.current_anim = self.manager.animations[anim_name]
            self.current_name = anim_name
            self.loop = loop
            self.reverse = reverse
            self.playing = True
            
            self.frame = (len(self.current_anim["frames"]) - 1) if self.reverse else 0
            self.frame_accumulator = 0.0

    def update(self, speed_multiplier=1.0):
        if not self.playing or not self.current_anim:
            return
            
        self.frame_accumulator += speed_multiplier+self.speed_play
        
        if self.frame_accumulator >= 1.0:
            steps = int(self.frame_accumulator)
            self.frame_accumulator -= steps
            
            if self.reverse:
                self.frame -= steps
            else:
                self.frame += steps
            
            max_frame = len(self.current_anim["frames"]) - 1
            
            if self.reverse:
                if self.frame < 0:
                    if self.loop:
                        self.frame = max_frame
                    else:
                        self.frame = 0
                        self.playing = False
            else:
                if self.frame > max_frame:
                    if self.loop:
                        self.frame = 0
                    else:
                        self.frame = max_frame
                        self.playing = False

    def is_playing(self, anim_name, reverse=None):
        """
        Возвращает True, если сейчас проигрывается anim_name.
        Если передан reverse (True/False), то проверяет еще и направление.
        """
        if not self.playing or self.current_name != anim_name:
            return False
        if reverse is not None and self.reverse != reverse:
            return False
        return True

    def get_state(self):
        if self.current_anim and 0 <= self.frame < len(self.current_anim["frames"]):
            return self.current_anim["frames"][self.frame]
        return {"offset_x": 0, "offset_y": 0, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0}

class Text:
    _font_cache = {}
    _render_cache = {}

    def __init__(self, font, text, color, pos, anchor="topleft"):
        self.font = font
        self.text = text
        self.color = list(color)
        self.pos = list(pos)
        self.anchor = anchor
        self.render()

    @classmethod
    def get_font(cls, name="Arial", size=24):
        key = (name, int(size))
        if key not in cls._font_cache:
            cls._font_cache[key] = pygame.font.SysFont(name, int(size))
        return cls._font_cache[key]

    def render(self):
        key = (id(self.font), self.text, tuple(self.color))
        if key not in Text._render_cache:
            Text._render_cache[key] = self.font.render(self.text, True, self.color)
        self.surface = Text._render_cache[key]
        self.rect = self.surface.get_rect()
        setattr(self.rect, self.anchor, self.pos)

    def set_text(self, text=None, color=None, font=None, pos=None, anchor=None):
        if text is not None:
            self.text = text
        if color is not None:
            self.color = list(color)
        if font is not None:
            self.font = font
        if pos is not None:
            self.pos = list(pos)
        if anchor is not None:
            self.anchor = anchor
        self.render()

    def click(self):
        return self.game.input.mouse_pressed(1) and self.rect.collidepoint(self.game.input.mouse_pos)
    
    def hover(self):
        return self.rect.collidepoint(self.game.input.mouse_pos)
    
    def update(self):
        self.clicked = self.click()
        self.hovered = self.hover()

    def draw(self):
        if screen:
            screen.blit(self.surface, self.rect)

class InfoBar:
    def __init__(self):
        self.font = pygame.font.Font(res("Data", "font", "tf2secondary.ttf"), 26)
        self.fontMini = pygame.font.Font(res("Data", "font", "tf2secondary.ttf"), 19)
        
        self.offsetx_power = 6
        self.offsety_power = 10
        self.text = ""
        self.price = ""
        self.label = ""
        self.boxSize = (400, 100)
        
        self.style = 0 # 0: Defealt, 1: Branchs, 2: Shop
        # self.shop_panel = Sprite(None, scale=[800, HEIGHT], color=[69, 69, 69], alpha=50, flip_x=False, flip_y=False, angle=0, mode='Stretch')
    
    def clear(self):
        self.style = 0
        self.text = ""
    
    def draw(self, pos):
        if self.text == "": return 
        style = self.style
        if style == 1:
            self.offsetx_power = 20
            text_surface, text_rect = self.text_rotate(pos, self.label, (200, 200, 200))
            self.outlining(self.label, (0, 0, 0), 2, text_rect)
            
            xRect = text_rect.right-self.boxSize[0]+10 if pos[0] > WIDTH / 2 else text_rect.left-10
            boxRect = pygame.Rect(xRect, text_rect.top, self.boxSize[0], self.boxSize[1])
            
            pygame.draw.rect(screen, (45, 45, 45, 80), boxRect, border_radius=10)
            pygame.draw.rect(screen, (100, 100, 100, 80), boxRect, border_radius=10, width=2)
            screen.blit(text_surface, text_rect.topleft)
            pos = (pos[0], pos[1]+30)
            self.text_draw(pos, self.text)
            
            text_surface = self.fontMini.render(self.price, True, (180, 230, 190))
            text_rect = text_surface.get_rect()
            if pos[0] > WIDTH / 2:
                text_rect.topleft = (boxRect.topleft[0]-45, boxRect.topleft[1]+5)
                screen.blit(text_surface, text_rect.topright)
            else:
                text_rect.topright = (boxRect.topright[0]-5, boxRect.topright[1]+5)
                screen.blit(text_surface, text_rect.topleft)
        elif style == 2:
            # screen.blit(self.shop_panel.image, pygame.Rect(pos[0]-50, pos[1]-50, self.shop_panel.scale[0], self.shop_panel.scale[1]))
            self.offsetx_power = 6
            self.text_draw(pos, self.text, text_color=(230, 230, 230), outlining_color=(100, 100, 100), power_outlining=3)
        else:
            self.offsetx_power = 6
            self.text_draw(pos, self.text)
    
    def text_rotate(self, position, text, color):
        if text == "": return None, None
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if position[0] > WIDTH / 2:
            text_rect.right = position[0]-self.offsetx_power
            text_rect.y = position[1]-self.offsety_power
        else:
            text_rect.left = position[0]+10+self.offsetx_power
            text_rect.y = position[1]-self.offsety_power
        return text_surface, text_rect
    
    def text_draw(self, position, text, text_color=(170, 170, 170), outlining_color=(0, 0, 0), power_outlining=2):
        if text == "": return None, None
        text_surface, text_rect = self.text_rotate(position, text, text_color)
        if text_surface and text_rect:
            self.outlining(text, outlining_color, power_outlining, text_rect)
            screen.blit(text_surface, text_rect.topleft)
        return text_surface, text_rect
    
    def outlining(self, text, color, power, text_rect):
        screen.blit(self.font.render(text, True, color), (text_rect.x - power, text_rect.y))
        screen.blit(self.font.render(text, True, color), (text_rect.x + power, text_rect.y))
        screen.blit(self.font.render(text, True, color), (text_rect.x, text_rect.y - power))
        screen.blit(self.font.render(text, True, color), (text_rect.x, text_rect.y + power))


# Save Panel
class SavePanel(Object):
    def __init__(self, scene, id, pos):
        self.scene = scene
        self.game = scene.game
        self.data=self.scene.get_save(self.scene._get_save_directory(), id)
        if self.data:
            self.lp = PlayerOffside(self.game, self.data) # local player
        sprite = Sprite(self.game.pathManager.TEXTURES / self.cheak_image(), scale=[350, 525], color=[100, 100, 255], size=[350, 525], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.font_text_save = pygame.font.Font(self.game.pathManager.FONT / "tf2build.ttf", 50)
        self.font_text_time = pygame.font.Font(self.game.pathManager.FONT / "tf2secondary.ttf", 70)
        super().__init__(sprite, pos, "center")
        self.id = id
        
        self.animations = {
            'hover': 'hover shop',
            'unhover': 'not hover shop',
            'hovered': 'hovered shop',
            'idle': "idle shop"
        }
        self.animator = Animator(self.game.animationManager)
        self.status = 'leaving'
        self.animator.play(self.animations.get('idle'), loop=True, reverse=False, speed=0.1)
        
        self.background = pygame.image.load(self.game.pathManager.TEXTURES / "save_background.png").convert_alpha()
        self.background_rect = pygame.Rect(0, 0, 400, HEIGHT)
        self.background_rect.center = (self.rect.center[0], HEIGHT//2)
        self.background_alpha = 0
        
        self.text_time_y = -15
        self.text = self.scene.texts.make(self.font_text_save, f'Save {self.id}', [0, 0, 0], [self.rect.center[0], self.rect.center[1]-170+40+self.text_time_y], 'center') # [236, 236, 230]
        self.text_time  = self.scene.texts.make(self.font_text_time, self.scene.get_time_save(self.scene._get_save_directory(), self.id), [0, 0, 0], [self.rect.center[0]+64, self.rect.center[1]-173], 'midtop')
        scene.saves.append(self)
    
    def cheak_image(self):
        if self.data:
            if self.lp.record >= 50:
                return "save_win.png"
            if self.lp.time > 0:
                return "save_Start.png"
            else:
                return "save_How.png"
        return "save_NoData.png"
    
    def update(self):
        super().update()
        self.animator.update(speed_multiplier=1)
        
        anim_hover = self.animations.get('hover')
        anim_unhover = self.animations.get('unhover')
        anim_hovered = self.animations.get('hovered')
        anim_idle = self.animations.get('idle')
        
        if self.hovered:
            if self.clicked:
                self.game.soundManager.play("click")
                self.scene.selected_profile = self.id
                self.scene.selected()
            if self.status in ('idle', 'leaving'):
                self.game.soundManager.play("hover")
                self.status = 'hovering'
                if anim_hover:
                    self.animator.play(anim_hover, loop=False, reverse=False)
                else:
                    self.animator.playing = False 
            
            elif self.status == 'hovering' and not self.animator.playing:
                self.status = 'hovered'
                if anim_hovered:
                    self.animator.play(anim_hovered, loop=True)
        else:
            if self.status in ('hovering', 'hovered'):
                self.status = 'leaving'
                if anim_unhover:
                    is_reverse = (anim_unhover == anim_hover)
                    self.animator.play(anim_unhover, loop=False, reverse=is_reverse)
                else:
                    button.animator.playing = False
            
            elif self.status == 'leaving' and not self.animator.playing:
                self.status = 'idle'
                if anim_idle:
                    self.animator.play(anim_idle, loop=True)
        self.text.rect.y = self.render_rect.center[1]-75+self.text_time_y
        self.text_time.rect.y = self.render_rect.center[1]-230
    
    def draw(self):
        if self.hovered and self.background_alpha < 255:
            self.background_alpha=(self.background_alpha+5)**1.05
            if self.background_alpha > 255:
                self.background_alpha = 255
        if self.background_alpha > 0:
                if not self.hovered:
                    self.background_alpha-=15
                    if self.background_alpha < 0:
                        self.background_alpha =0
                self.background.set_alpha(self.background_alpha)
                screen.blit(self.background, self.background_rect)
        super().draw()

### ВНИМАНИЕ ЗОНА ИИ ВАЙБ КОДА, СПИЗЖЕНО ИЗ СТАРОЙ ЧАСТИ ###
from typing import Tuple, Optional
class CritText:
    def __init__(self, text: str, pos: Tuple[int, int],
                 font_size: int = 30,
                 color: Tuple[int, int, int] = (255, 215, 0),
                 duration: float = 1.8,
                 max_scale: float = 2.4,
                 launch_speed: float = -8.0,
                 deceleration: float = 0.35,
                 fall_accel: float = 0.08
                 ):
        self.text = text
        self.pos = list(pos)
        self.font_size = font_size
        self.color = color
        self.duration = duration
        self.max_scale = max_scale
        self.launch_speed = launch_speed
        self.deceleration = deceleration
        self.fall_accel = fall_accel

        self.start_time = pygame.time.get_ticks()
        self.alive = True

        # Состояние анимации
        self.velocity_y = self.launch_speed
        self.alpha = 255
        self.scale = 1.0
        self.peak_reached = False
        self.elapsed_at_peak = None  # будет установлено при достижении пика

    def update(self):
        if not self.alive:
            return

        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.start_time) / 1000  # сек
        t = elapsed / self.duration  # [0..1]

        if t > 1.0:
            self.alive = False
            return

        # 1. Физика движения
        if not self.peak_reached:
            self.velocity_y += self.deceleration
            if self.velocity_y >= 0:
                self.velocity_y = 0
                self.peak_reached = True
                self.elapsed_at_peak = elapsed  # запоминаем момент пика
        else:
            self.velocity_y += self.fall_accel

        self.pos[1] += self.velocity_y

        # 2. Масштаб
        if t < 0.15:
            self.scale = 1 + (self.max_scale - 1) * (t / 0.15)
        elif t < 0.4:
            self.scale = self.max_scale
        else:
            self.scale = self.max_scale * (1 - (t - 0.4) / 0.6)

        # 3. Прозрачность (начинается после пика)
        if self.peak_reached and self.elapsed_at_peak is not None:
            fade_start_t = self.elapsed_at_peak / self.duration
            fade_progress = (t - fade_start_t) / (1.0 - fade_start_t)
            self.alpha = int(255 * max(0, 1 - fade_progress))
        else:
            self.alpha = 255

    def draw(self, surface: pygame.Surface):
        if not self.alive:
            return

        font = pygame.font.SysFont(None, int(self.font_size * self.scale))
        text_surface = font.render(self.text, True, self.color)
        text_surface.set_alpha(self.alpha)

        text_rect = text_surface.get_rect(center=(self.pos[0], self.pos[1]))
        surface.blit(text_surface, text_rect)