import pygame, random, time, threading, queue, json, math, os
from pathlib import Path
from config import *
from classes import *
from evolution import *

# Core
# pypresence нужен только на десктопе (Discord). На Android его нет, и импорт
# на верхнем уровне убивал бы весь запуск игры.
try:
    from pypresence import Presence
except Exception:
    Presence = None

class EventManager: #Самое важное
    def __init__(self):
        self.game = None
        self.events = []
    
    def event(self, name):
        self.events = [e for e in self.events if not e.canceled]
        for e_class in self.events:
            if name == e_class.event:
                e_class.trigger()
    
    def subscribe(self, name, func):
        event = Event(name, func)
        self.events.append(event)
        return event
    
    # def subscribe(self, func_sub, func): хой знает как это сделать
        
    
eventManager = EventManager()

class RPC:
    def __init__(self):
        self.connected = False
        self.running = True
        
        self.text = ""
        self.small_text = ""
        self.queue = queue.Queue()
        self.CLIENT_ID = 1210980897281802330
        
        self.last_data = None
        
        # На Android (и если pypresence не установлен) активность Discord
        # просто выключена - игра не должна от этого падать.
        if Presence is None or IS_ANDROID:
            self.running = False
            return
        
        self.start()
        self.update()
    
    def worker(self):
        while self.running:
            if not self.connected:
                try:
                    self.RPC = Presence(self.CLIENT_ID)
                    self.RPC.connect()
                    self.start_time = int(time.time())
                    
                    self.connected = True
                except Exception as e:
                    time.sleep(5)
                    continue
            try:
                data = self.queue.get(timeout=1)
                
                if data == self.last_data:
                    continue
                
                self.last_data = data
                text, small_text = data
                self.text = text
                self.small_text = small_text
                self.RPC.update(state=small_text, details=text, large_image="kotdefense", large_text="Kot Defense")
            except queue.Empty:
                pass
    
    def update(self, text=None, small_text=None):
        self.queue.put((
            text,
            small_text
        ))
    
    def start(self):
        self.threading = threading.Thread(target=self.worker, daemon=True)
        self.threading.start()
        
    def stop(self):
        self.running = False

class PathManager:
    def __init__(self):
        # Пути абсолютные: на Android текущая папка процесса - "/",
        # поэтому Path("Data") там не находит ничего.
        self.DATA = Path(BASE_DIR) / "Data"
        
        self.TEXTURES = self.DATA / "textures"
        self.AUDIO = self.DATA / "audio"
        self.FONT = self.DATA / "font"
        self.ANIMATIONS = self.DATA / "animations"

class InputManager:
    # Насколько долго держать палец, чтобы это считалось "зажатием" (удаление кота).
    LONG_PRESS_TIME = 0.55
    LONG_PRESS_DRAG = 24  # px: сдвиг больше этого отменяет зажатие

    def __init__(self):
        self.down, self.pressed, self.released = set(), set(), set()
        self.m_down, self.m_pressed, self.m_released = set(), set(), set()
        self.key_backspace = False
        self.key_enter = False
        self.text_queue = []
        
        self.scancodes = set()
        self.scancodes_pressed = set()
        
        self.mouse_pos = (0, 0)

        # Зажатие (long press) - единственный способ удалять котов на тач-экране:
        # правой кнопки мыши и Ctrl на телефоне нет.
        self._press_start = None
        self._press_pos = None
        self._long_press_fired = False
        self.long_press = False

        # Системная кнопка "Назад" на Android приходит как AC_BACK.
        self.BACK_KEY = getattr(pygame, "K_AC_BACK", getattr(pygame, "K_ESCAPE", 27))

    def scancode_pressed(self, scancode):
        return scancode in self.scancodes_pressed

    def update(self, events):
        self.pressed.clear(); self.released.clear()
        self.m_pressed.clear(); self.m_released.clear()
        self.text_queue.clear()
        self.scancodes_pressed.clear()
        self.key_backspace = False
        self.key_enter = False
        for e in events:
            if e.type == pygame.TEXTINPUT:
                self.text_queue.append(e.text)
            if e.type in (pygame.KEYDOWN, pygame.KEYUP):
                k = getattr(e, 'key', None)
                if k is None:
                    continue
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        self.key_backspace = True
                    elif e.key == pygame.K_RETURN:
                        self.key_enter = True
                    if k not in self.down:
                        self.pressed.add(k)
                    self.down.add(k)
                else:
                    self.down.discard(k)
                    self.released.add(k)
                sc = getattr(e, 'scancode', None)
                if sc is not None:
                    if e.type == pygame.KEYDOWN:
                        if sc not in self.scancodes:
                            self.scancodes_pressed.add(sc)
                        self.scancodes.add(sc)
                    else:
                        self.scancodes.discard(sc)
            elif e.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                b = getattr(e, 'button', None)
                if b is None:
                    continue
                # На телефоне палец даёт нажатие без предшествующего движения мыши,
                # поэтому позицию берём и из события кнопки тоже.
                self.mouse_pos = getattr(e, 'pos', self.mouse_pos)
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if b not in self.m_down:
                        self.m_pressed.add(b)
                    self.m_down.add(b)
                    if b == 1:
                        self._press_start = time.time()
                        self._press_pos = self.mouse_pos
                        self._long_press_fired = False
                else:
                    self.m_down.discard(b)
                    self.m_released.add(b)
                    if b == 1:
                        self._press_start = None
            elif e.type == pygame.MOUSEMOTION:
                self.mouse_pos = getattr(e, 'pos', self.mouse_pos)

        # Зажатие пальца на месте: считаем один раз за нажатие.
        self.long_press = False
        if (
            1 in self.m_down
            and self._press_start is not None
            and not self._long_press_fired
        ):
            held = time.time() - self._press_start
            dx = self.mouse_pos[0] - self._press_pos[0]
            dy = self.mouse_pos[1] - self._press_pos[1]
            if held >= self.LONG_PRESS_TIME and (dx * dx + dy * dy) <= self.LONG_PRESS_DRAG ** 2:
                self.long_press = True
                self._long_press_fired = True

    key_down = lambda s, k: k in s.down
    key_pressed = lambda s, k: k in s.pressed
    key_released = lambda s, k: k in s.released
    mouse_down = lambda s, b: b in s.m_down
    mouse_pressed = lambda s, b: b in s.m_pressed
    mouse_released = lambda s, b: b in s.m_released

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.curent = None
    
    def init(self, scene, name):
        self.scenes[name] = scene
    
    def get(self, name):
        return self.scenes[name]
    
    def go(self, name):
        self.curent = self.scenes[name]
        self.curent.started()

# Cursor
class CursorManager:
    def __init__(self, game):
        self.game = game
        # На Android курсоров ОС нет вообще, а на headless/серверных сборках
        # SDL не умеет их создавать - курсор просто не трогаем.
        self.available = not IS_ANDROID
        try:
            pygame.mouse.set_visible(True)
        except Exception:
            self.available = False
        
        self.cursors = {
            'idle': pygame.SYSTEM_CURSOR_ARROW,
            'hovered': pygame.SYSTEM_CURSOR_HAND,
            'text': pygame.SYSTEM_CURSOR_IBEAM
        }
        
        # Текущее реальное состояние курсора в ОС
        self.current_state = 'idle'
        # Желаемое состояние на текущий кадр (буфер)
        self.desired_state = 'idle'
        
        self._apply_cursor('idle')

    def _apply_cursor(self, state):
        if not self.available:
            return
        try:
            pygame.mouse.set_cursor(self.cursors[state])
        except Exception:
            self.available = False

    def set_state(self, state):
        """Виджеты теперь не меняют курсор сразу, а просто записывают своё желание"""
        if state in self.cursors:
            self.desired_state = state

    def reset(self):
        """В начале кадра просто сбрасываем буфер желаний, ОС не трогаем!"""
        self.desired_state = 'idle'

    def apply(self):
        """
        Вызывается ОДИН РАЗ в самом конце игрового update().
        Применяет курсор только если он реально изменился по сравнению с прошлым кадром.
        """
        if self.desired_state != self.current_state:
            self.current_state = self.desired_state
            self._apply_cursor(self.current_state)

# Dvizok
class SaveManager:
    def __init__(self, game, filename="save_data.json", current_profile=0):
        self.game = game
        self.profile = current_profile
        self.save_dir = self._get_save_directory()
        self.save_path = self.save_dir / filename
        
        self.version = version
        
        self.default_data = {
            "version": version,
            "level": 1,
            "xp": 0,
            "points": 0,
            "time": 0,
            "record": 0,
        }
    
    def _get_save_directory(self) -> Path:
        """
        Определяет стандартный путь для сохранений в зависимости от ОС:
        Windows: C:\\Users\\User\\AppData\\Roaming\\FolderName
        Linux: /home/user/.config/FolderName
        Mac: /Users/user/Library/Application Support/FolderName
        """
        home = Path.home()

        # Android: APPDATA/XDG нет, домашняя папка недоступна для записи.
        # Пишем во внутреннюю папку приложения.
        if IS_ANDROID:
            base_dir = Path(ensure_save_dir())
            final_path = base_dir
            final_path.mkdir(parents=True, exist_ok=True)
            return final_path
        
        if os.name == "nt":  # Windows
            # Пытаемся получить APPDATA, если нет — используем дефолтный путь в профиле
            appdata = os.getenv("APPDATA")
            base_dir = Path(appdata) if appdata else home / "AppData" / "Roaming"
        elif os.uname().sysname == "Darwin":  # macOS
            base_dir = home / "Library" / "Application Support"
        else:  # Linux и другие Unix-подобные системы
            # По стандарту XDG, если переменная XDG_CONFIG_HOME не задана, пишем в ~/.config
            config_home = os.getenv("XDG_CONFIG_HOME")
            base_dir = Path(config_home) if config_home else home / ".config"
            
        # Формируем финальный путь с названием твоей игры
        final_path = base_dir / folder_name
        
        # КРИТИЧЕСКИ ВАЖНО: Если папки игры еще нет в системной директории, создаем её!
        final_path.mkdir(parents=True, exist_ok=True)
        return final_path

    def _ensure_file_exists(self):
        if not self.save_path.exists():
            self._save_raw({})

    def _save_raw(self, data: dict):
        self.save_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except OSError as e:
            print(f"Ошибка записи файла:  {e}")
            raise
    
    def _load_raw(self) -> dict:
        try:
            with open(self.save_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            return {}

    def load_game(self):
        eventManager.event("game load")
        self._ensure_file_exists()
        all_data = self._load_raw()
        
        if str(self.profile) not in all_data:
            data = self.default_data.copy()
            all_data[str(self.profile)] = data
            self._save_raw(all_data)
            return data
        
        data = all_data[str(self.profile)].copy()
        for key, val in self.default_data.items():
            if key not in data:
                data[key] = val
            
        return data

    def save_game(self):
        eventManager.event("game save")
        self._ensure_file_exists()
        all_data = self._load_raw()
        data_to_save = self.game.playerO.to_dict()
        all_data[str(self.profile)] = data_to_save
        self._save_raw(all_data)
        print(f"Успешное сохранение в: {self.save_path} профиль ({self.profile})")
    
    def create_new_profile(self, profile_id: int):
        eventManager.event("game new profile")
        self._ensure_file_exists()
        all_data = self._load_raw()
        if str(profile_id) in all_data:
            raise(f"Профиль {profile_id} уже существует")
        all_data[str(profile_id)] = self.default_data.copy()
        self._save_raw(all_data)
    
    def delete_profile(self, profile_id: int):
        eventManager.event("delete profile")
        self._ensure_file_exists()
        all_data = self._load_raw()
        if str(profile_id) not in all_data:
            return False
        del all_data[str(profile_id)]
        self._save_raw(all_data)
        return True
    
    def list_profiles(self) -> list[int]:
        self._ensure_file_exists()
        all_data = self._load_raw()
        return list(all_data.keys())

class SoundManager:
    def __init__(self, game):
        self.game = game
        self.sounds = {}
        self.localVolume = {}
        
        self.volume = 1
    
    def init(self, path, name, volume=1):
        # На Android набор кодеков SDL_mixer может быть урезан (например, без mp3).
        # Звук - не повод ронять игру: пропускаем то, что не открылось.
        try:
            self.sounds[name] = pygame.mixer.Sound(datapackM.get(path))
        except Exception as error:
            print(f"[audio] skip {name}: {error}")
            return
        self.localVolume[name] = volume
        self.game.console.log(f"Loaded {path} sound, volume {volume}, name {name}")
    
    def change_volume(self, name, volume):
        self.sounds[name] = volume
    
    def play(self, name, volume=1, loops=0):
        sound = self.sounds.get(name)
        if sound is None:
            return
        # volume - локальный звука * volume - менеджера * volume - фукции. Крч чтобы регулировать почти везде можно было громкость
        sound.set_volume(self.localVolume[name]*self.volume*volume)
        sound.play(loops)
    
    def stop(self, name):
        sound = self.sounds.get(name)
        if sound is not None:
            sound.stop()

class MusicManager:
    def __init__(self, game):
        self.game = game
        pm = self.game.pathManager
        
        self.musics = {}
        self.vols = {} # music volume
        self.volume = 28 # В целом громкость
        
        self.speed = 5
        self.state = "game"
        
        self.init(datapackM.get(pm.AUDIO / "music_menu.mp3"), 'game', True)
        self.init(datapackM.get(pm.AUDIO / "music_menu_low.mp3"), 'paused', True)
    
    def init(self, path, name, sync=False):
        # Дальше бога нет
        m = pygame.mixer.Sound(path)
        if sync:
            m.play(loops=-1, fade_ms=1000)
            m.set_volume(0.0)
        self.musics[name] = m
        self.vols[name] = [0, 0, sync]
    
    def update(self):
        for name, music in self.musics.items():
            # Если название трека со состояние совпадает
            if name == self.state:
                if not self.vols[name][2] and self.vols[name][1] == 0:
                    music.play(loops=-1, fade_ms=1000)
                self.vols[name][1] = 100
            else:
                if not self.vols[name][2] and self.vols[name][1] == 100:
                    music.stop()
                self.vols[name][1] = 0
            
            # Регулировка громкости реал тайм диджей арбуz
            if self.vols[name][0] < self.vols[name][1]:
                self.vols[name][0] += self.speed
            elif self.vols[name][0] > self.vols[name][1]:
                self.vols[name][0] -= self.speed*2
        
            v = self.vols[name][0]*0.01 # 100% -> 0.01
            music.set_volume(self.volume*0.01*v)

class ObjectManager:
    def __init__(self, game):
        self.game = game
        self.objects = []
        self.buttons = []
    
    def new_object(self, sprite, pos, anchor="topleft", button=False):
        obj = Object(sprite, pos, anchor)
        obj.game = self.game
        if button:
            obj.button = True
            obj.animator = Animator(self.game.animationManager)
            obj.animations = {
                'hover': 'hover',
                'unhover': 'hover', # Если hover и unhover одинаковы, то unhover становится ревёрс версией hover
                'hovered': 'hovered',
                'idle': None
            }
            obj.status = 'idle'
            obj.speed = 2
            self.buttons.append(obj)
            
        self.objects.append(obj)
        return obj
    
    def update(self):
        self.animateForButtons()
        for obj in self.objects:
            obj.update()
    
    def animateForButtons(self):
        for button in self.buttons:
            button.animator.update(speed_multiplier=button.speed)
            
            anim_hover = button.animations.get('hover')
            anim_unhover = button.animations.get('unhover')
            anim_hovered = button.animations.get('hovered')
            anim_idle = button.animations.get('idle')

            if button.hovered:
                self.game.cursorManager.set_state('hovered')
                
                if button.status in ('idle', 'leaving'):
                    button.status = 'hovering'
                    if anim_hover:
                        button.animator.play(anim_hover, loop=False, reverse=False)
                    else:
                        button.animator.playing = False 
                
                elif button.status == 'hovering' and not button.animator.playing:
                    button.status = 'hovered'
                    if anim_hovered:
                        button.animator.play(anim_hovered, loop=True)
            else:
                if button.status in ('hovering', 'hovered'):
                    button.status = 'leaving'
                    
                    if anim_unhover:
                        is_reverse = (anim_unhover == anim_hover)
                        button.animator.play(anim_unhover, loop=False, reverse=is_reverse)
                    else:
                        button.animator.playing = False
                
                elif button.status == 'leaving' and not button.animator.playing:
                    button.status = 'idle'
                    if anim_idle:
                        button.animator.play(anim_idle, loop=True)

    def draw(self):
        for obj in self.objects:
            obj.draw()

class TextManager:
    def __init__(self, game):
        self.game = game
        self.texts = []
    
    def make(self, font, text, color, pos, anchor="topleft"):
        text = Text(font, text, color, pos, anchor)
        text.game = self.game
        self.texts.append(text)
        return text
    
    def update(self):
        for text in self.texts: text.update()

    def draw(self):
        for text in self.texts: text.draw()

class AnimationManager:
    def __init__(self, game):
        self.game = game
        self.animations = {}

    def init(self, path, name_animate="Chmo"):
        with open(path, "r") as f:
            data = json.load(f)
            
        easings = {
            "linear": lambda t: t,
            "easeInQuad": lambda t: t*t,
            "easeOutQuad": lambda t: t*(2-t),
            "easeInOutQuad": lambda t: 2*t*t if t<0.5 else -1+(4-2*t)*t,
            "easeInElastic": lambda t: 0 if t==0 else (1 if t==1 else -math.pow(2,10*t-10)*math.sin((t*10-10.75)*(2*math.pi)/3)),
            "easeOutElastic": lambda t: 0 if t==0 else (1 if t==1 else math.pow(2,-10*t)*math.sin((t*10-0.75)*(2*math.pi)/3)+1),
            "easeOutBounce": lambda t: 7.5625*t*t if t<1/2.75 else (7.5625*(t-1.5/2.75)**2+0.75 if t<2/2.75 else (7.5625*(t-2.25/2.75)**2+0.9375 if t<2.5/2.75 else 7.5625*(t-2.625/2.75)**2+0.984375))
        }

        for anim_name, anim_data in data.items():
            duration = anim_data["duration"]
            anchor = anim_data.get("anchor", "center")
            keyframes = {int(k): v for k, v in anim_data["keyframes"].items()}
            
            # --- ВАЖНЫЙ ФИКС ДЛЯ СТАРЫХ АНИМАЦИЙ ---
            # Дописываем недостающие параметры прямо в словарь ключей, 
            # чтобы интерполяция ниже никогда не крашилась.
            for kf in keyframes.values():
                kf.setdefault("rotation", 0)
                kf.setdefault("scale_x", 1.0)
                kf.setdefault("scale_y", 1.0)
            # ---------------------------------------

            sorted_kfs = sorted(list(keyframes.keys()))
            baked_frames = []
            
            for frame in range(duration + 1):
                if frame in keyframes:
                    baked_frames.append(keyframes[frame])
                    continue
                    
                left_kf, right_kf = 0, duration
                for kf in sorted_kfs:
                    if kf < frame: left_kf = kf
                    if kf > frame: right_kf = kf; break
                else:
                    right_kf = sorted_kfs[-1]
                    if frame >= right_kf:
                        baked_frames.append(keyframes[right_kf])
                        continue
                        
                lkf, rkf = keyframes[left_kf], keyframes[right_kf]
                t = (frame - left_kf) / (right_kf - left_kf)
                ease_fn = easings.get(lkf["ease"], lambda val: val)
                t_eased = ease_fn(t)
                
                baked_frames.append({
                    "offset_x": lkf["offset_x"] + (rkf["offset_x"] - lkf["offset_x"]) * t_eased,
                    "offset_y": lkf["offset_y"] + (rkf["offset_y"] - lkf["offset_y"]) * t_eased,
                    "scale_x": lkf["scale_x"] + (rkf["scale_x"] - lkf["scale_x"]) * t_eased,
                    "scale_y": lkf["scale_y"] + (rkf["scale_y"] - lkf["scale_y"]) * t_eased,
                    "rotation": lkf["rotation"] + (rkf["rotation"] - lkf["rotation"]) * t_eased
                })
                
            self.animations[name_animate] = { 
                "duration": duration,
                "anchor": anchor,
                "frames": baked_frames
            }
        print(f"Loaded and pre-baked animations from {path}")
        self.game.console.log(f"Loaded and pre-baked animations from {path}")

# Game
class EvolutionManager:
    def __init__(self, game):
        self.game = game
        self.branches = []
        self.branchesAndNames = {}
        self.lockedSprite = Sprite(game.pathManager.TEXTURES / "locked.png", (64, 64))
        self.width = 5
        self.offset_x = WIDTH//-2
        self.offset_y = HEIGHT//-2
    
    def loaded(self):
        for branch in self.branches:
            branch.animate_init(self.game)
    
    def addBranch(self, branch):
        branch.manager = self
        self.branchesAndNames[branch.id] = branch
        self.branches.append(branch)
    
    def draw(self):
        for br in self.branches:
            br.setOffset((self.offset_x, self.offset_y))
            if br.locked:
                br.sprite = self.lockedSprite
            else:
                br.sprite = br.base
            br.draw_lines()
        for br in self.branches:
            br.draw()
    
    def update(self):
        clicked = False
        for br in self.branches:
            br.update()
            if clicked == False:
                clicked = br.clicked
        return clicked

class Statistics:
    def __init__(self):
        self.deaths = {"towers": 0, "enemies": 0}
        self.farm_money = 0
        self.wave = 0
        
        self.score = 0

class HausManager:
    def __init__(self, game):
        self.game = game
        self.enable = False
        self.randomValues = {}
        self.oldValues = {}
    
    def clear(self):
        self.randomValues = {}
    
    def startHAUS(self):
        self.enable = True
        
    def endHAUS(self):
        self.enable = False
    
    def get(self, name, interval=(0, 100), type="number"):
        if name not in self.randomValues.keys():
            if type=="number":
                self.randomValues[name] = random.randint(interval[0], interval[1])
            elif type=="color":
                self.randomValues[name] = (random.randint(interval[0], interval[1]), random.randint(interval[0], interval[1]), random.randint(interval[0], interval[1]))
        return self.randomValues[name]

class WaveManager:
    def __init__(self, game):
        self.game = game
        self.enemyManager = self.game.enemyManager
        self.active = False
        self.clear = False
        self.wave = 0
        self.mega_wave = 5
        self.mega_wave_mutipiller = 2 if "start" in self.game.playerO.upgrades else 50
        self.budget = 5
        self.curentBudget = 0
        self.concentration = 100
    
    def wave_end(self):
        eventManager.event("wave end")
        self.clear = True
        self.game.storeManager.cheak_unlocks()
        print(f"Wave {self.wave} clear.")
        self.game.playerO.ExitTime = time.time()
        self.game.playerO.entry_to_game()
    
    def start_helper(self):
        if self.wave < 10 or ("start" in self.game.playerO.upgrades and self.wave < 5):
            self.game.player.farm_muiltipiler.base = 3
        else:
            self.game.player.farm_muiltipiler.base = 1
    
    def next_wave(self):
        eventManager.event("wave start")
        self.active = True
        self.clear = False
        self.wave += 1
        self.game.statManager.wave = self.wave
        self.start_helper()
        self.budget = round(self.wave*(self.wave*0.35+3)) * (self.mega_wave_mutipiller if self.game.waveManager.wave % self.game.waveManager.mega_wave == 0 else 1)
        self.curentBudget = self.budget
        print(f"Wave {self.wave} started. Budget [{str(self.budget)}]")
    
    def update(self):
        eventManager.event("wave update")
        if self.game.sceneManager.get("mainGame").overlay_alpha <= 15 and self.active == True and self.curentBudget > 0 and len(self.enemyManager.enemies) < self.concentration:
            enemy = self.enemyManager.spawn(self)
            self.curentBudget -= enemy.budget.value
        if self.clear == False and self.curentBudget <= 0 and len(self.enemyManager.enemies) == 0:
            self.wave_end()

class EnemyManager:
    def __init__(self, game):
        self.game = game
        self.enemies = []
        self.initEnemies = {}
    
    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
    
    def update(self):
        for enemy in self.enemies:
            if enemy.animator: enemy.animator.update(speed_multiplier=enemy.speed.value*1.5)
            enemy.update()
            
            if enemy.alive == False:
                enemy.death()
        self.enemies = [e for e in self.enemies if e.alive]
    
    def init(self, enemy, name):
        self.initEnemies[name] = enemy
    
    def spawn(self, wave):
        available = [e for e in self.initEnemies.values() if e.budget.value <= self.game.waveManager.curentBudget and e.check_lock(self.game)]
        weights = [getattr(e, 'weight', Stat(1)).value for e in available]
        enemyClass = random.choices(available, weights=weights, k=1)[0]
        return self.spawn_specific(enemyClass)

    def spawn_specific(self, enemyClass):
        enemy = enemyClass((random.randint(WIDTH, WIDTH+80*3), 0))
        enemy.rect.y = random.randint(upbar, HEIGHT-downbar-enemy.sprite.scale[1])
        enemy.game = self.game
        enemy.animate_init(self.game)
        self.enemies.append(enemy)
        self.enemies.sort(key=lambda cls: cls.priority.value)
        enemy.inited()
        return enemy

class StoreManager:
    def __init__(self, game):
        self.game = game
        self.spacing = 35
        self.shop_size = 90
        self.font = pygame.font.Font(self.game.pathManager.FONT / "Yuyu-Regular.ttf",24)
        
        self.startPos = (90, HEIGHT-downbar*0.5)
        self.ghostTower = None
        
        self.products = []
    
    def init(self, product):
        self.products.append(product)
        product.game = self.game
        product.animate_init(self.game)
        product.check_lock()
        product.inited()
    
    def cheak_unlocks(self):
        unlocked = 0
        for product in self.products:
            if product.check_lock():
                unlocked += 1
        
        if unlocked > 0:
            self.restore()
    
    def unlocker(self):
        return self.unlocked()
    
    def unlock_all(self):
        for product in self.products:
            self.check_lock = self.unlocker
        self.restore()
    
    def get_item(self, name):
        for item in self.products:
            if item.tower == name:
                return item
    
    def restore(self):
        x=self.startPos[0]
        y=self.startPos[1]
        self.products.sort(key=lambda cls: cls.cost.value)
        for product in self.products:
            if not product.visible:
                continue
            product.rect.center = (x, y)
            product.render(self.font)
            x+=self.shop_size+self.spacing
    
    def draw(self):
        for product in self.products:
            if product.visible:
                product.draw()
        if self.ghostTower:
            if self.ghostTower.error == True:
                self.ghostTower.sprite.image = self.ghostTower.sprite.error_image
            else:
                self.ghostTower.sprite.image = self.ghostTower.sprite.original_image
            self.ghostTower.draw()
            radius((self.ghostTower.rect.centerx, self.ghostTower.rect.centery), (255, 255, 255), self.ghostTower.range.value)
    
    def snap(self, pos):
        # Привязка к центрам клеток сетки (шаг GRID_SIZE от её начала),
        # а не к кратным координатам от угла экрана.
        x = round((pos[0] - GRID_X0) / GRID_SIZE) * GRID_SIZE + GRID_X0
        y = round((pos[1] - GRID_Y0) / GRID_SIZE) * GRID_SIZE + GRID_Y0
        
        return (x, y)
    
    def update(self):
        for product in self.products:
            if product.animator: product.animator.update()
            if product.visible:
                product.update()
        if self.ghostTower != None:
            self.ghostTower.rect.center = self.snap(self.game.input.mouse_pos)
            tower_collides = any(self.ghostTower.rect.colliderect(t.rect) for t in self.game.towerManager.towers if t != self.ghostTower)
            enemy_collides = any(self.ghostTower.rect.colliderect(e.rect) for e in self.game.enemyManager.enemies)
            XBoard = (self.ghostTower.rect.centerx < 0 or self.ghostTower.rect.centerx > WIDTH)
            if self.ghostTower.rect.y >= HEIGHT-downbar-self.ghostTower.rect.height+1 or self.ghostTower.rect.y <= upbar-1 or tower_collides or enemy_collides or XBoard:
                self.ghostTower.error = True
            else:
                self.ghostTower.error = False
                if self.game.input.mouse_down(1) and self.game.player.money.value >= self.ghostTower.parent.cost.value:
                    self.game.soundManager.play("buy")
                    self.game.player.money.base -= self.ghostTower.parent.cost.value
                    self.game.towerManager.spawn(self.ghostTower.parent.tower, self.ghostTower.rect.center, self.ghostTower.parent)
                    if self.game.player.money.value >= self.ghostTower.parent.cost.value and self.game.input.key_down(pygame.K_LCTRL):
                        return
                    self.ghostTower = None 

class TowerManager:
    def __init__(self, game):
        self.game = game
        self.towers = []
        self.initTowers = {}
    
    def draw(self):
        for tower in self.towers:
            tower.draw()
    
    def update(self):
        for tower in self.towers:
            if tower.animator: tower.animator.update()
            tower.update()
            
            if tower.alive == False:
                tower.death()
        self.towers = [t for t in self.towers if t.alive]
    
    def init(self, tower, name):
        self.initTowers[name] = tower
    
    def spawn(self, name, pos, parent=None, center=True):
        if parent is None:
            parent = self.game.storeManager.get_item(name)
        tower = self.initTowers[name](parent, pos)
        if center:
            tower.rect.center = pos
        else:
            tower.rect.x = pos[0]
            tower.rect.y = pos[1]
        tower.game = self.game
        tower.animate_init(self.game)
        self.towers.append(tower)
        self.towers.sort(key=lambda cls: cls.rect.y)
        tower.inited()
        return tower
    
    def prew(self, name, parent):
        tower = self.initTowers[name](parent, (0,0))
        tower.game = self.game
        tower.prew = True
        tower.sprite.original_image = tower.sprite.image.copy()
        tower.sprite.original_image.set_alpha(120)
        tower.sprite.error_image    = tower.sprite.original_image.copy()
        tower.sprite.error_image.fill((255, 0, 0, 120), special_flags=pygame.BLEND_RGBA_MULT)
        
        return tower



### ВНИМАНИЕ ЗОНА ИИ ВАЙБ КОДА, СПИЗЖЕНО ИЗ СТАРОЙ ЧАСТИ ###

class CritManager:
    def __init__(self):
        self.effects = []

    def add_text(self, text: str, pos: Tuple[int, int], **kwargs):
        """
        Добавить новый крит‑текст.
        :param text: текст для отображения
        :param pos: позиция (x, y)
        :param kwargs: любые параметры CritText (font_size, color, duration и т.д.)
        """
        effect = CritText(text, pos, **kwargs)
        self.effects.append(effect)

    def update(self):
        """Обновить все активные эффекты."""
        for effect in self.effects:
            effect.update()
        # Удалить мёртвые эффекты
        self.effects = [e for e in self.effects if e.alive]

    def draw(self, surface: pygame.Surface):
        """Отрисовать все активные эффекты на surface."""
        for effect in self.effects:
            effect.draw(surface)

crit_manager = CritManager()