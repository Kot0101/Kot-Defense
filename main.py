import pygame
import sys
import math
import time
import threading
from pathlib import Path
from config import *
from debug import *
from evolution import *

# Loader + Console
widgetManager = WidgetManager()

console = DebugConsole()
widgetManager.add(console)

console.log("Debug Console Loaded !")

class Loader:
    def __init__(self, screen, width, height, min_duration=999):
        self.screen = screen
        self.width = width
        self.height = height
        
        self.loadImg = pygame.image.load(datapackM.get(res("Data", "textures", "loading.png")))
        self.loadImg = pygame.transform.smoothscale(self.loadImg, (300,300))
        screenRect = self.screen.get_rect()
        
        self.animated = False
        
        self.text = "Loading"

        self.font_large = pygame.font.Font(res("Data", "font", "tf2build.ttf"), 60)
        self.font_small = pygame.font.Font(res("Data", "font", "tf2build.ttf"), 40)

        self.is_loaded = False
        self.game = None

        self.start_time = time.time()
        self.min_duration = min_duration

        self.fade_time = 0.3

    def set(self, text):
        console.log("Loading stage - " + text)
        self.text = text
        self._update_frame()

    def loaded(self, game):
        console.log("")
        console.log(f"                          Kot Defense {version}", (96, 227, 73))
        console.log("                        Welcome to the terminal !", (96, 227, 73))
        console.log('Write "help" to learn the commands')
        self.game = game
        self.is_loaded = True
        self._update_frame()

    def wait_and_close(self):
        clock = pygame.time.Clock()

        while True:
            pygame.event.pump()

            if pygame.mouse.get_pressed()[0]:
                self._transition()
                return

            keys = pygame.key.get_pressed()
            if self.game is not None:
                self.game.musicManager.update()

            if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
                self._transition()
                return
            t = time.time() - self.start_time

            self._update_frame()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if self.is_loaded and t >= self.min_duration:
                    if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                        self._transition()
                        return

            if self.is_loaded and t >= self.min_duration:
                self._transition()
                return

            clock.tick(60)

    def _transition(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0,0,0))

        clock = pygame.time.Clock()

        start = time.time()

        while True:
            elapsed = time.time() - start
            k = min(elapsed / self.fade_time, 1)

            self.game.draw()

            overlay.set_alpha(int((1 - k) * 255))
            self.screen.blit(overlay, (0, 0))
            events = pygame.event.get()
            self.game.input.update(events)

            present()

            if k >= 1:
                self.animated = True
                break

            clock.tick(60)
    def _update_frame(self):
            t = time.time() - self.start_time

            self.screen.fill((0,0,0))

            scale = 1 + 0.1 * math.sin(t * 3)
            msgL = (
                "Done!"
                if self.is_loaded
                else "Loading"
                
            )
            text = self.font_large.render(msgL, True, (230, 230, 255))
            
            pygame.draw.rect(self.screen,(255, 255, 255),((self.width // 20, self.height // 1.2,1250,10)))


            self.screen.blit(text, (self.width // 20, self.height // 1.15))
            
            msg = (
                "Press any button to start :3"
                if self.is_loaded
                else self.text
            )

            color = (200, 200, 200) if self.is_loaded else (100, 100, 100)

            surf = self.font_small.render(msg, True, color)

            self.screen.blit(surf,(self.width // 20, self.height // 1.05))

            present()

load = Loader(screen, WIDTH, HEIGHT)

load.set("Loading modules")
from classes import *
from managers import *
from entity import *

pygame.display.set_caption("Kot Defense build " + version)
try:
    pygame.display.set_icon(pygame.image.load(datapackM.get(PathManager().TEXTURES / "icon.png")).convert_alpha())
except Exception:
    pass

clock = pygame.time.Clock()

# Scenes
load.set("Loading scenes (1/2)")
class LoginScene:
    def __init__(self, game_context=None):
        self.game = game_context
        self.objects = ObjectManager(self.game)
        self.texts = TextManager(self.game)
        self.selected_profile = 0
        
        sprite_background = Sprite(self.game.pathManager.TEXTURES / "save_fullbackground.png", (WIDTH,HEIGHT))
        self.backgroundObject = self.objects.new_object(sprite_background, [0, 0], 'topleft')
        self.saves = []
        dist = 270
        y = HEIGHT//2+100
        self.save2 = SavePanel(self, 0, (dist, y))
        self.save1 = SavePanel(self, 1, (WIDTH//2, y))
        self.save3 = SavePanel(self, 2, (WIDTH-dist, y))
        
        font_Text = pygame.font.Font(self.game.pathManager.FONT / 'tf2build.ttf', 110)
        self.Text = self.texts.make(font_Text, 'Select ur save slot', [255, 255, 255], [700, 180], 'midbottom')

        self.scroll_x = 0
        self.scroll_y = 0
        eventManager.event("login scene")
    
    def _get_save_directory(self) -> Path:
        """
        Определяет стандартный путь для сохранений в зависимости от ОС:
        Windows: C:\\Users\\User\\AppData\\Roaming\\FolderName
        Linux: /home/user/.config/FolderName
        Mac: /Users/user/Library/Application Support/FolderName
        """
        home = Path.home()
        
        if os.name == "nt":
            appdata = os.getenv("APPDATA")
            base_dir = Path(appdata) if appdata else home / "AppData" / "Roaming"
        elif os.uname().sysname == "Darwin":
            base_dir = home / "Library" / "Application Support"
        else:
            config_home = os.getenv("XDG_CONFIG_HOME")
            base_dir = Path(config_home) if config_home else home / ".config"
            
        final_path = base_dir / folder_name / "save_data.json"
        
        return final_path
    
    def get_time_save(self, save_path, profile):
        profile_data = self.get_save(save_path, profile)
        if not profile_data:
            return "No Save"
        
        total_seconds = profile_data.get("time", 0)
        if total_seconds < 0:
            total_seconds = 0
        
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        result = []
        if days > 0:
            result.append(f"{days:02d}")
        if hours > 0 or days > 0:
            result.append(f"{hours:02d}")
        result.append(f"{minutes:02d}")
        result.append(f"{seconds:02d}")
        
        return ":".join(result)
    
    def get_save(self, save_path, profile):
        save_path = Path(save_path)
        
        if not save_path.exists():
            return None
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            return None
        
        profile_key = str(profile)
        if profile_key not in data:
            return None
            
        profile_data = data[profile_key]
        
        return profile_data
    
    def started(self):
        eventManager.event("login scene started")

    def background(self):
        width_cells  = WIDTH // cell_size
        height_cells = HEIGHT // cell_size
        
        offset_x = (self.scroll_x % cell_size) - cell_size
        offset_y = (self.scroll_y % cell_size) - cell_size
        
        scroll_col = int(self.scroll_x // cell_size)
        scroll_row = int(self.scroll_y // cell_size)
        
        for row in range(height_cells + 2):
            for col in range(width_cells + 2):
                color = cell1 if (row + col + scroll_row + scroll_col) % 2 == 0 else cell2
                
                pygame.draw.rect(screen, color, (
                    col * cell_size + offset_x,
                    row * cell_size + offset_y,
                    cell_size, cell_size
                ))
    
    def selected(self):
        self.game.load_profile(self.selected_profile)
        
        self.game.sceneManager.init(MainMenu(self.game), "mainMenu")
        self.game.sceneManager.init(UpdateScene(self.game), "updateScene")
        self.game.sceneManager.init(GameScene(self.game), "mainGame")
        self.game.sceneManager.init(DeathScene(self.game),"death")
        self.game.sceneManager.init(OstUI(self.game),"ost")
        self.game.sceneManager.init(Tutorial(self.game),"tutorial")
        
        eventManager.event("login scene selected")
        if self.game.playerO.time > 0:
            self.game.sceneManager.go("mainMenu")
        else:
            self.game.sceneManager.go("tutorial")
    
    def update(self):
        self.texts.update()
        self.scroll_y -= 1
        self.objects.update()
        for save in self.saves:
            save.update()
        eventManager.event("login scene update")

    def draw(self):
        self.background()
        self.objects.draw()
        
        for save in self.saves:
            save.draw()
        
        self.texts.draw()
        eventManager.event("login scene draw")

class DeathScene:
    def __init__(self,game):
        self.game = game
        
        self.init_UI()
        self.BackButton.game = game
        self.RestartButton.game = game
        # self.RageQuitButton.game = game
        
        # self.survived You survived: xxx waves
        # self.money    Money spent: XXXX$
        # self.killed   Killed dogs: xxxx
        # self.died     Cats died: xxxx
        # self.score    the score
        eventManager.event("death scene")
    
    def started(self):
        self.game.playerO.ExitTime = time.time()
        self.game.playerO.entry_to_game()
        rpc.update(f"{self.game.player.money.value} 💵 {self.game.player.health.value} ❤", f"Death ({self.game.waveManager.wave} wave)")
        stat = self.game.statManager
        
        self.survived.set_text(f"You survived: {stat.wave} waves")
        self.money.set_text(f"Money spent: {stat.farm_money}$")
        self.killed.set_text("Killed dogs: " + str(stat.deaths["enemies"]))
        self.died.set_text("Cats died: " + str(stat.deaths["towers"]))
        self.score.set_text(str(stat.score))
        
        if not self.game.tutor:
            if self.game.waveManager.wave > self.game.playerO.record:
                self.game.playerO.record = self.game.waveManager.wave
        self.game.saveManager.save_game()
        if self.game.tutor:
            self.game.playerO.coins = 240
            self.game.gid.counter = 0
            self.game.gid.play("Ооооо братан\nМы 240 деняк заработали")
        eventManager.event("death scene started")
    
    def init_UI(self):
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_background = Sprite(path=None, scale=[1400, 800], color=[72, 72, 72], size=[1400, 800])
        self.background = Object(sprite_background, [1, 3], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_statistics = Sprite(path=None, scale=[375, 375], color=[97, 97, 97], size=[375, 375])
        self.statistics = Object(sprite_statistics, [301, 253], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_fill_frame = Sprite(path=None, scale=[350, 325], color=[72, 72, 72], size=[350, 325])
        self.fill_frame = Object(sprite_fill_frame, [326, 278], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_frame2 = Sprite(path=None, scale=[475, 125], color=[97, 97, 97], size=[475, 125])
        self.frame2 = Object(sprite_frame2, [676, 253], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_fill_frame2 = Sprite(path=None, scale=[450, 75], color=[72, 72, 72], size=[450, 75])
        self.fill_frame2 = Object(sprite_fill_frame2, [676, 278], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_background_copy_copy_1_copy = Sprite(path=None, scale=[25, 250], color=[97, 97, 97], size=[25, 250])
        self.background_copy_copy_1_copy = Object(sprite_background_copy_copy_1_copy, [676, 378], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_Text_1 = Text.get_font('Arial', 90)
        self.Text_1 = Text(font_Text_1, 'You death !', [251, 0, 0], [701, 128], 'center')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_label = Text.get_font('Arial', 60)
        self.label = Text(font_label, 'STATISTICS', [230, 182, 15], [501, 278], 'center')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_money = Text.get_font('Arial', 32)
        self.money = Text(font_money, 'Money spent: XXXX$', [233, 233, 233], [341, 383], 'midleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_survived = Text.get_font('Arial', 32)
        self.survived = Text(font_survived, 'You survived: xxx waves', [233, 233, 233], [341, 338], 'midleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_killed = Text.get_font('Arial', 32)
        self.killed = Text(font_killed, 'Killed dogs: xxxx', [233, 233, 233], [341, 428], 'midleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_died = Text.get_font('Arial', 32)
        self.died = Text(font_died, 'Cats died: xxxx', [233, 233, 233], [341, 473], 'midleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_scoreLabel = Text.get_font('Arial', 48)
        self.scoreLabel = Text(font_scoreLabel, 'SCORE:', [233, 233, 233], [496, 488], 'midtop')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_score = Text.get_font('Arial', 63)
        self.score = Text(font_score, 'XXXXX', [86, 255, 62], [496, 528], 'midtop')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_label_copy = Text.get_font('Arial', 62)
        self.label_copy = Text(font_label_copy, 'STATISTICS', [191, 151, 13], [501, 278], 'center')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_BackButton = Sprite(path=None, scale=[425, 100], color=[23, 255, 64], size=[425, 100])
        self.BackButton = Object(sprite_BackButton, [725, 400], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_Label_0_copy = Sprite(path=None, scale=[405, 80], color=[210, 255, 218], size=[405, 80])
        self.Label_0_copy = Object(sprite_Label_0_copy, [736, 410], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_Text_1_1 = Text.get_font('Arial', 48)
        self.Text_1_1 = Text(font_Text_1_1, 'Back to menu', [0, 0, 0], [936, 450], 'center')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_RestartButton = Sprite(path=None, scale=[250, 90], color=[23, 255, 64], size=[250, 90])
        self.RestartButton = Object(sprite_RestartButton, [726, 528], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_RestartButton_copy = Sprite(path=None, scale=[230, 70], color=[210, 255, 218], size=[230, 70])
        self.RestartButton_copy = Object(sprite_RestartButton_copy, [736, 538], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_RageQuitButton = Sprite(path=None, scale=[150, 90], color=[255, 32, 37], size=[150, 90])
        # self.RageQuitButton = Object(sprite_RageQuitButton, [1001, 528], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        sprite_RageQuitButton_copy = Sprite(path=None, scale=[130, 70], color=[255, 204, 205], size=[130, 70])
        self.RageQuitButton_copy = Object(sprite_RageQuitButton_copy, [1011, 538], 'topleft')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_Text_3 = Text.get_font('Arial', 60)
        self.Text_3 = Text(font_Text_3, 'Retry', [0, 0, 0], [851, 571], 'center')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_Text_5 = Text.get_font('Arial', 30)
        # self.Text_5 = Text(font_Text_5, 'RAGE', [0, 0, 0], [1074, 558], 'center')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_Text_5_copy = Text.get_font('Arial', 30)
        # self.Text_5_copy = Text(font_Text_5_copy, 'QUIT', [0, 0, 0], [1073, 587], 'center')
        # layout: pivot=[0.5, 0.5] alignment=center margin=[0, 0, 0, 0] padding=[0, 0, 0, 0]
        font_Text_0 = Text.get_font('Arial', 60)
        self.Text_0 = Text(font_Text_0, 'Not bad :D', [255, 255, 255], [882, 314], 'center')
    
    def update(self):
        self.BackButton.update()
        self.RestartButton.update()
        # self.RageQuitButton.update()
        if self.BackButton.clicked == True:
            self.game.sceneManager.go("mainMenu")
        elif self.RestartButton.clicked == True:
            if self.game.tutor:
                self.game.gid.play(f"Отказано")
            else:
                self.game.game_managers()
                self.game.load_entity()
                self.game.sceneManager.go("mainGame")
        # elif self.RageQuitButton.clicked == True:
            # self.game.running = False
        if self.game.gid.clicked:
            if self.game.gid.counter == 1:
                self.game.gid.play(f"Нажми выход в меню", "action1")
            else:
                self.game.gid.end()
        eventManager.event("death scene update")

    def draw(self): # бля нахуя оно существует
        self.background.draw()
        self.statistics.draw()
        self.fill_frame.draw()
        self.frame2.draw()
        self.fill_frame2.draw()
        self.background_copy_copy_1_copy.draw()
        self.Text_1.draw()
        self.label.draw()
        self.money.draw()
        self.survived.draw()
        self.killed.draw()
        self.died.draw()
        self.scoreLabel.draw()
        self.score.draw()
        self.label_copy.draw()
        self.BackButton.draw()
        self.Label_0_copy.draw()
        self.Text_1_1.draw()
        self.RestartButton.draw()
        self.RestartButton_copy.draw()
        # self.RageQuitButton.draw()
        self.RageQuitButton_copy.draw()
        self.Text_3.draw()
        # self.Text_5.draw()
        # self.Text_5_copy.draw()
        self.Text_0.draw()
        eventManager.event("death scene draw")

class OstUI:
    def __init__(self, game_context=None):
        self.game = game_context
        self.objects = ObjectManager(self.game)
        self.texts = TextManager(self.game)
        self.animators = []
        sprite_thumbnail = Sprite(self.game.pathManager.TEXTURES / 'thumbnail.png', scale=[1450*1.35, 850*1.35], color=[100, 100, 255], size=[1450, 850], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.thumbnail = self.objects.new_object(sprite_thumbnail, [700, 400], 'center')
        self.thumbnail.animator = Animator(self.game.animationManager)
        self.thumbnail.animator.play("evo locked", loop=True, speed=0.5)
        self.animators.append(self.thumbnail.animator)
        sprite_gradient = Sprite(self.game.pathManager.TEXTURES / 'gradient.png', scale=[1450, 850], color=[100, 100, 255], size=[1450, 850], alpha=96, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.gradient = self.objects.new_object(sprite_gradient, [700, 400], 'center')
        
        sprite_Label = Sprite(None, scale=[290, 4], color=[255, 255, 255], size=[290, 4], alpha=200, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Label = self.objects.new_object(sprite_Label, [1075, 775], 'topleft')
        
        font_Text = Text.get_font('Arial', 24)
        self.ost_name = self.texts.make(font_Text, '---', [255, 255, 255], [1119, 770], 'bottomleft')
        
        sprite_note = Sprite(self.game.pathManager.TEXTURES / 'note.png', scale=[32, 32], color=[100, 100, 255], size=[32, 32], alpha=255, flip_x=False, flip_y=False, angle=-360, mode='Stretch')
        self.note = self.objects.new_object(sprite_note, [1095, 757], 'center')
        self.note.animator = Animator(self.game.animationManager)
        self.note.animator.play("cat spiner", loop=True, speed=0.1)
        self.animators.append(self.note.animator)
        
        sprite_title = Sprite(self.game.pathManager.TEXTURES / 'title.png', scale=[575*1.2, 150*1.2], color=[100, 100, 255], size=[575, 150], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.title = self.objects.new_object(sprite_title, [1090, 90], 'center')
        self.title.animator = Animator(self.game.animationManager)
        self.title.animator.play("evo locked", loop=True, speed=0.3)
        self.animators.append(self.title.animator)
        
        sprite_ostImg = Sprite(self.game.pathManager.TEXTURES / 'OST.png', scale=[200, 120], color=[100, 100, 255], size=[200, 120], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.ostImg = self.objects.new_object(sprite_ostImg, [720, 90], 'center')
        self.ostImg.animator = Animator(self.game.animationManager)
        self.ostImg.animator.play("paused", loop=True, speed=0.6)
        self.animators.append(self.ostImg.animator)
        
        sprite_Image_004 = Sprite(self.game.pathManager.TEXTURES / 'save_fullbackground.png', scale=[1770, 1400], color=[100, 100, 255], size=[1770, 1400], alpha=255, flip_x=False, flip_y=False, angle=220, mode='Stretch')
        self.Image_004 = self.objects.new_object(sprite_Image_004, [-490, -500], 'topleft')
        
        sprite_Cat = Sprite(self.game.pathManager.TEXTURES / 'Cat_Attack.png', scale=[180, 180], color=[100, 100, 255], size=[180, 180], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Cat = self.objects.new_object(sprite_Cat, [30, 610], 'topleft')
        self.Cat.animator = Animator(self.game.animationManager)
        self.Cat.animator.play("idle", loop=True, speed=0.5)
        self.animators.append(self.Cat.animator)
        
        sprite_Dog = Sprite(self.game.pathManager.TEXTURES / 'Dog_Base.png', scale=[140, 150], color=[100, 100, 255], size=[140, 150], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        sprite_Dog.image = pygame.transform.flip(sprite_Dog.image, True, False)
        self.Dog = self.objects.new_object(sprite_Dog, [290, 620], 'topleft')
        self.Dog.animator = Animator(self.game.animationManager)
        self.Dog.animator.play("idle", loop=True, speed=1.4)
        self.animators.append(self.Dog.animator)
        
        self.ost = "Kot - Kot Defense Rap.mp3"
        # self.ost = "boom.mp3"

    def started(self):
        pass

    def update(self):
        self.objects.update()
        self.texts.update()
        if self.ost_name.text != self.ost:
            self.ost_name.set_text(self.ost)
            self.game.musicManager.init(self.game.pathManager.AUDIO / self.ost, self.ost)
            self.game.musicManager.state = self.ost
        for animator in self.animators:
            animator.update()

    def draw(self):
        self.objects.draw()
        self.texts.draw()

class PauseMenu: # НЕ СЦЕНА, ОТКРЫВАЕТСЯ ПО ВЕРХ СЦЕНЫ НА КОТОРОЙ ПАУЗА
    def __init__(self, scene):
        self.game = scene.game
        self.scene = scene
        
        self.objectManager = ObjectManager(self.game)
        self.textManager = TextManager(self.game)
        
        backgroundImg = Sprite(self.game.pathManager.TEXTURES / "pause_background.png", (877,951), alpha=100)
        self.background = self.objectManager.new_object(backgroundImg, (WIDTH//2-backgroundImg.scale[0]//2, -80))
        self.background.animator = Animator(self.game.animationManager)
        self.background.animator.play("paused", loop=True, speed=0.2)
        
        pausedImg = Sprite(self.game.pathManager.TEXTURES / "paused.png", (819,242))
        self.paused = self.objectManager.new_object(pausedImg, (WIDTH//2-pausedImg.scale[0]//2, 60))
        self.paused.animator = Animator(self.game.animationManager)
        self.paused.animator.play("paused", loop=True, speed=0.8)
        
        continueImg = Sprite(self.game.pathManager.TEXTURES / "continue.png", (473,147))
        self.continueBtn = self.objectManager.new_object(continueImg, (WIDTH//2-473//2, HEIGHT//2-70), button=True)
        
        exitImg = Sprite(self.game.pathManager.TEXTURES / "exit.png", (268,150))
        self.exitBtn = self.objectManager.new_object(exitImg, (WIDTH//2-268//2, HEIGHT//2+147), button=True)
        
        catImg = Sprite(self.game.pathManager.TEXTURES / "Cat_Attack.png", (216,216))
        self.cat = self.objectManager.new_object(catImg, (WIDTH//2-pausedImg.scale[0]//2-120, 120))
        self.cat.animator = Animator(self.game.animationManager)
        self.cat.animStep = 0
        self.cat.flip_anim = False
        
        catImg2 = Sprite(self.game.pathManager.TEXTURES / "Dog_Base.png", (150,150))
        self.cat2 = self.objectManager.new_object(catImg2, (WIDTH//2+pausedImg.scale[0]*0.4-5, 120))
        self.cat2.sprite.image = pygame.transform.flip(self.cat2.sprite.image, True, False)
        self.cat2.animator = Animator(self.game.animationManager)
        self.cat2.animator.play("cat spiner", loop=True, speed=0.4)
        
        # paused
        self.overlay_speed = 4
        self.overlay_p = pygame.Surface(screen.get_size(), pygame.SRCALPHA) # затемнение при старте волны
        self.overlay_p_speed = 20
        self.overlay_p_alpha = 0
        self.overlay_p2 = pygame.Surface(screen.get_size(), pygame.SRCALPHA) # Вспышка крутая пиздатенькая
        self.overlay_p2_speed = 20
        self.overlay_p2_alpha = 0 #аааааааааа гамно коддд
    
    def update(self):
        eventManager.event("game scene paused")
        self.objectManager.update()
        self.cat.animator.update()
        self.cat2.animator.update()
        self.paused.animator.update()
        self.background.animator.update()
        
        if self.continueBtn.clicked:
            self.scene.pause_toggle()
            
        if self.exitBtn.clicked:
            self.scene.pause_toggle()
            if self.game.waveManager.wave > self.game.playerO.record:
                self.game.playerO.record = self.game.waveManager.wave
            self.game.sceneManager.go("mainMenu")
        
        if self.overlay_p2_alpha > 0:
            self.overlay_p2_alpha -= self.overlay_speed
            self.overlay_p_alpha += self.overlay_speed
        
        if self.cat.animator.playing == False:
            if self.cat.animStep == 0:
                self.cat.animStep = 1
                self.cat.animator.play("jump part 1", loop=False, speed=0.1)
            elif self.cat.animStep == 1:
                self.cat.animStep = 0
                self.cat.flip_anim = not self.cat.flip_anim
                self.cat.animator.play("jump part 2", loop=False, speed=0.4)
    
    def draw(self):
        self.objectManager.draw()
        self.textManager.draw()
        screen.blit(self.overlay_p2.set_alpha(self.overlay_p2_alpha) or self.overlay_p2, (0, 0))
        if self.overlay_p2_alpha > 0:
            self.overlay_p2.fill((255, 255, 255, 150))
        
class GameScene:
    def __init__(self, game):
        self.game = game 
        self.settings = {
            "background": True,
            "error_fun": False,
        }
        
        self.hausManager = self.game.hausManager # Не доделано
        # self.hausManager.enable = True

        self.objectManager = ObjectManager(self.game)
        self.textManager = TextManager(self.game)
        blatImg = Sprite(self.game.pathManager.TEXTURES / "blat.png",(WIDTH//3.2,90))
        self.blat = self.objectManager.new_object(blatImg,(0,0))
        barImg = Sprite(self.game.pathManager.TEXTURES / "bar.png", (WIDTH,downbar))
        self.bar = self.objectManager.new_object(barImg, (0,HEIGHT-downbar))
        skipImg = Sprite(self.game.pathManager.TEXTURES / "skip.png", (800,800))
        skipImg.image = pygame.transform.smoothscale(skipImg.image,(100,100))
        self.skip = self.objectManager.new_object(skipImg, (WIDTH-140, HEIGHT-140), button = True)
        sprite_boarder = Sprite(self.game.pathManager.TEXTURES / 'boarder.png', scale=[30, HEIGHT], color=[255, 255, 255], size=[30, HEIGHT], alpha=100, mode='Stretch') #Сделать переход какой-то
        # self.boarder = self.objectManager.new_object(sprite_boarder, [10, HEIGHT//2], 'center')
        x2Img = Sprite(self.game.pathManager.TEXTURES / "x2.png", (248,124))
        self.x2Img = self.objectManager.new_object(x2Img, (WIDTH//2-248//2, HEIGHT//2+30))
        self.x2Img.animator = Animator(self.game.animationManager)
        self.x2Img.animator.play("x2", loop=True, speed=0.8)
        self.x2Img.visible = False
        
        coinsSprite = Sprite(self.game.pathManager.TEXTURES / "coins.png", (64,64))
        self.coinsImg = self.objectManager.new_object(coinsSprite, (WIDTH//2.5, 4))
        
        self.pauseScene = PauseMenu(self)
        self.pause = False      
        self.pause_visible = True # False чтобы сделать паузу без менюшки нахрен
        
        # wave started крч потом менеджер вспышек сделаю чтобы не ебаться с этим и лучше было
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA) # затемнение при старте волны
        self.overlay_speed = 4
        self.overlay_alpha = 0
        self.overlay_timer = 0
        
        self.fontWarning = pygame.font.Font(self.game.pathManager.FONT / "Yuyu-Regular.ttf",70)
        self.overlay_text = Text(self.fontWarning, "WAVE STARTED", (255, 0, 0, 100), (WIDTH//2, HEIGHT//2-55), anchor="center")
        
        self.cell1 = (101, 155, 94)
        self.cell2 = (93,143,86)# (94,136,89)
        
        self.font = pygame.font.Font(self.game.pathManager.FONT / "tf2secondary.ttf",26)
        self.font2 = pygame.font.Font(self.game.pathManager.FONT / "DejaVuSans.ttf",26)
        
        self.health = self.textManager.make(self.font, "Health: -", (64, 163, 34), (20, 13))
        self.money = self.textManager.make(self.font, "Money: -", (64, 163, 34), (20, 34))
        self.wave = self.textManager.make(self.font, "Press the red button to start", (64, 163, 34), (20, 28+26))
        
        self.money_o = self.textManager.make(self.font2, "-", (0, 0, 0), (WIDTH//2.5+65, 28))
          
        eventManager.event("game scene")
    
    def started(self):
        self.game.playerO.ExitTime = time.time()
        self.game.playerO.entry_to_game()
        self.hausManager.clear()
        if "waveSkip" in self.game.playerO.upgrades:
            self.game.waveManager.wave = 4
            self.game.player.money.base = 175
            
        if self.game.tutor == True and self.game.tutor_state == 0:
            self.game.player.money.base = 0
            self.game.waveManager.wave = 26
            
            # Build cats
            self.build_line("DefenseCat", 990, 90, 9, 60)
            self.build_line("DefenseCat", 990+60, 90, 9, 60)
            self.build_line("Cat", 990-60, 90, 9, 60)
            self.build_line("Cat", 990-120, 90, 9, 60)
            self.build_line("MagicCat", 990-120-60, 90+60, 4, 120)
            self.build_line("SupportCat", 990-120-60, 90, 5, 120)
            self.build_line("WorkerCat", 630, 270, 3, 60)
            self.build_line("WorkerCat", 630-60, 270, 3, 60)
            self.build_line("WorkerCat", 630-120, 270, 3, 60)
            self.build_line("Cat", 630-120*2, 90, 5, 120)
            self.build_line("DefenseCat", 630-120*2-60, 90, 5, 120)
            self.build_line("DefenseCat", 990+120+60, 90, 5, 120)
            self.build_line("DefenseCat", 990+120+60+120+60, 90, 5, 120)
            
            
            self.game.gid.counter = 0
            self.game.gid.play(f"Вот ты и на поле\nбратанчик")
        eventManager.event("game started")
    
    def build_line(self, cat, x, y, count, add):
        for i in range(count):
            self.game.towerManager.spawn(cat, (x, y), center=False)
            y += add
    
    def pause_toggle(self):
        self.pause = not self.pause
        self.pauseScene.overlay_p2_alpha = 200
        self.pauseScene.overlay_p_alpha = 100
        self.game.musicManager.state = "paused" if self.pause else "game"
        self.game.soundManager.play("paused")

    def update(self):
        # RPC
        waveText = f"Mega Wave: {str(self.game.waveManager.wave)}" if self.game.waveManager.wave % self.game.waveManager.mega_wave == 0 else f"Wave: {str(self.game.waveManager.wave)}"
        rpc.update(f"{self.game.player.money.value} 💵 {self.game.player.health.value} ❤", waveText)
        if self.game.input.key_pressed(pygame.K_SPACE):
            self.pause_toggle()
        if self.pause:
            if self.pause_visible:
                self.pauseScene.update()
        else:
            self.x2Img.animator.update()
            self.pauseScene.overlay_p2_alpha = 0
            eventManager.event("game scene update not paused")
            self.objectManager.update()
            self.game.waveManager.update()
            self.game.enemyManager.update()
            self.game.towerManager.update()
            self.game.storeManager.update()
            crit_manager.update()
            self.health.set_text(f"Health: {str(self.game.player.health.value)}")
            self.money.set_text(f"Money: {str(self.game.player.money.value)}")
            self.money_o.set_text(str(self.game.playerO.coins) + "$")
            
            if self.pauseScene.overlay_p_alpha > 0:
                self.pauseScene.overlay_p_alpha -= self.pauseScene.overlay_p_speed
            
            if self.overlay_timer > 0:
                self.overlay_timer -= 1
            elif self.overlay_alpha > 0:
                self.overlay_alpha -= self.overlay_speed
            else:
                self.overlay_animate = False
            
            if self.game.waveManager.wave > 0:
                self.wave.set_text(waveText)
            if self.skip.clicked == True and len(self.game.enemyManager.enemies) == 0 and self.overlay_alpha <= 0:
                self.overlay_timer = FPS*1.5
                self.overlay_alpha = 255
                self.game.waveManager.next_wave()
                self.game.soundManager.play("wave")
                # if self.game.waveManager.wave % self.game.waveManager.mega_wave == 0:
                self.pauseScene.overlay_p_alpha = 255
                if self.game.tutor == True: 
                    if self.game.tutor_state == 0:
                        self.game.gid.counter = 67
                    elif self.game.tutor_state == 1:
                        self.game.gid.counter = 2000
                        self.game.tutor_state = 2
            if self.game.player.cheak_death():
                if self.game.gid.counter >= 2000 or not self.game.tutor:
                    self.game.player.death()
                else:
                    self.game.player.health.base += 67
                    for dog in self.game.enemyManager.enemies:
                        dog.alive = False
                    for cat in self.game.towerManager.towers:
                        cat.alive = False
                    self.build_line("Cat", 990-120, 90, 9, 60)
                    self.build_line("MagicCat", 990-120-60, 90+60, 4, 120)
                    self.build_line("SupportCat", 990-120-60, 90, 5, 120)
                    self.build_line("WorkerCat", 630, 270, 3, 60)
                    self.build_line("WorkerCat", 630-60, 270, 3, 60)
                    self.build_line("WorkerCat", 630-120, 270, 3, 60)
                    self.build_line("Cat", 630-120*2, 90, 5, 120)
                    self.build_line("DefenseCat", 630-120*2-60, 90, 5, 120)
                    self.game.gid.play(f"ты не должен\nбыл умирать сейчас :/")
                    self.game.gid.counter -= 1
        if self.game.tutor == True:
            if self.game.gid.counter == 67 and len(self.game.enemyManager.enemies) == 0 and self.overlay_alpha <= 0:
                self.game.gid.play(f"ойййй как больно,\nнадо отстроить оборону")
            elif self.game.gid.counter == 2000 and len(self.game.enemyManager.enemies) == 0 and self.overlay_alpha <= 0:
                self.game.gid.play(f"Опа, следующая\nволна будет МЕГА")
            elif self.game.gid.counter == 70:
                if len(self.game.towerManager.towers) == self.oldCatsCount-6:
                    self.game.gid.play(f"Ладно, есть\nболее быстрый способ")
            elif len(self.game.towerManager.towers) == 0 and self.game.gid.counter == 72:
                self.game.gid.play(f"Красава, теперь\nпопробуй чот похожее сделать")
                self.game.gid.counter = 1485
            if self.game.gid.clicked:
                if self.game.gid.counter == 1:
                    self.game.gid.play(f"Я уже построил\nнеплохую оборону")
                elif self.game.gid.counter == 2:
                    self.game.gid.play(f"И сейчас будет\nочень сильная волна")
                elif self.game.gid.counter == 3:
                    self.game.gid.play(f"Нажми на рычаг\nсправа снизу", "action1")
                elif self.game.gid.counter == 68:
                    self.game.gid.play(f"Для начала давай\nудалим всех котов")
                elif self.game.gid.counter == 69:
                    self.game.gid.play(f"Чтобы их удалять\nнажимай ПКМ по котам")
                    self.oldCatsCount = len(self.game.towerManager.towers)
                elif self.game.gid.counter == 71:
                    self.game.gid.play(f"Зажми Ctrl+ПКМ чтобы\nудалять множество")
                elif self.game.gid.counter == 1485:
                    self.game.gid.play(f"На нижней панели\nбудут коты")
                elif self.game.gid.counter == 1486:
                    self.game.gid.play(f"Выбери кликом кота\nи место куда его")
                elif self.game.gid.counter == 1487:
                    self.game.gid.play(f"И не забывай про\nCtrl+ЛКМ ;-)", "action1")
                elif self.game.gid.counter == 1488:
                    self.game.gid.play(f"Как закончишь\nзапусти волну")
                    self.game.waveManager.wave = 13
                    self.game.player.money.base = 500
                    self.game.gid.counter += 1
                    self.game.tutor_state = 1
                    self.game.storeManager.cheak_unlocks()
                else:
                    self.game.gid.end()
        eventManager.event("game scene update")
    
    def background(self):
        
        width_cells  = WIDTH//cell_size
        height_cells = HEIGHT//cell_size
        
        offsets = (-cell_size//2, -cell_size//2)
        for row in range(height_cells+1):
            for col in range(width_cells+2):
                if self.hausManager.enable:
                    color = self.hausManager.get("cell1", (0, 255),"color") if (row+col) % 2 == 0 else self.hausManager.get("cell2", (0, 255),"color")
                else:
                    color = self.cell1 if (row+col) % 2 == 0 else self.cell2
                pygame.draw.rect(screen, color, (col*cell_size+offsets[0], row*cell_size+offsets[1], cell_size, cell_size))
    
    def draw(self):
        if self.settings["background"] == True:
            # screen.fill((101, 155, 94))
            self.background()
        
        #pygame.draw.rect(screen, (40, 63, 59), (0, HEIGHT-downbar, WIDTH, downbar))
        pygame.draw.rect(screen, (40, 63, 59), (0, upbar+7, WIDTH, 3))
        
        self.objectManager.draw()
        self.game.enemyManager.draw()
        self.game.towerManager.draw()
        self.game.storeManager.draw()
        self.textManager.draw()
        crit_manager.draw(screen)
        
        self.game.infoBar.draw(self.game.input.mouse_pos)
        
        # Затемнение типо старт волны
        screen.blit(self.overlay.set_alpha(self.overlay_alpha) or self.overlay, (0, 0))
        if self.overlay_alpha > 0:
            if self.settings["error_fun"] == True:
                self.settings["background"] = True
            self.overlay.fill((0, 0, 0, 150))
            self.overlay.blit(self.overlay_text.surface, self.overlay_text.rect)
            if self.game.waveManager.wave % self.game.waveManager.mega_wave == 0:
                self.x2Img.visible = True
                self.x2Img.sprite.alpha = self.overlay_alpha
                self.x2Img.draw() # Чтобы поверх хуйни этой была
        else:
            self.x2Img.visible = False
            if self.settings["error_fun"] == True:
                self.settings["background"] = False
        # Затемнение типо пауза аааааааааа гамно коддд x2
        screen.blit(self.pauseScene.overlay_p.set_alpha(self.pauseScene.overlay_p_alpha) or self.pauseScene.overlay_p, (0, 0))
        if self.pauseScene.overlay_p_alpha > 0:
            self.pauseScene.overlay_p.fill((0, 0, 0, 150))
        if self.pause and self.pause_visible:
            self.pauseScene.draw()
        eventManager.event("game scene draw")

class UpdateScene:
    def __init__(self, game_context=None):
        self.game = game_context
        self.objects = ObjectManager(self.game)
        self.texts = TextManager(self.game)
        
        self.lastClick = (0, 0)
        self.clicked = None
        
        init_branches(self.game.brManager)
        
        sprite_upPanel = Sprite(None, scale=[1400, 125], color=[69, 69, 69], size=[1375, 125], alpha=120, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.upPanel = self.objects.new_object(sprite_upPanel, [0, 0], 'topleft')
        
        sprite_Exit = Sprite(self.game.pathManager.TEXTURES / 'skip.png', scale=[90, 90], color=[100, 100, 255], size=[90, 90], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Exit = self.objects.new_object(sprite_Exit, [64, 64], 'center', button = True)
        
        font_Label = pygame.font.Font(self.game.pathManager.FONT / 'NotoSans-Bold.ttf', 80)
        self.label = self.texts.make(font_Label, 'Evolution', [255, 128, 128], [690, 60], 'center')
        
        font_xp = pygame.font.Font(self.game.pathManager.FONT / 'NotoSans-Bold.ttf', 63)
        self.xp = self.texts.make(font_xp, 'Coins', [255, 255, 255], [120, 60], 'midleft')
        
        # self.points = self.texts.make(font_xp, '(-)', [111, 255, 85], [self.xp.rect.x + self.xp.rect.w + 5, 40], 'midleft')
        
        # font_xp_copy = pygame.font.Font(self.game.pathManager.FONT / 'NotoSans-Bold.ttf', 40)
        # self.level = self.texts.make(font_xp_copy, 'Level -', [255, 255, 255], [120, 80], 'midleft')
        
        self.stars = []
        for _ in range(80):
            self.stars.append([
                random.randint(0, WIDTH), random.randint(0, HEIGHT),
                random.uniform(0.5, 2.5), random.randint(1, 3) 
            ])
        eventManager.event("update menu")

    def started(self):
        self.game.playerO.ExitTime = time.time()
        self.game.playerO.entry_to_game()
        self.safe = 30
        self.game.brManager.offset_x = WIDTH//-2+80
        self.game.brManager.offset_y = HEIGHT//-2+80
        for branch in self.game.brManager.branches:
            if branch.id in self.game.playerO.upgrades:
                branch.buyed = True
        if self.game.tutor:
            self.game.gid.counter = 0
            self.game.tutor_state = 6
            self.game.gid.play("Добро пожаловать в\nЕ В О Л Ю Ц И Ю")
        eventManager.event("update started")
    
    def background(self):
        screen.fill((10, 10, 18)) 
        for star in self.stars:
            star[1] += star[2]
            if star[1] > HEIGHT+3:
                star[0] = random.randint(0, WIDTH)
                star[1] = 0
                star[2] = random.uniform(0.5, 2.5)
            pygame.draw.circle(screen, (200, 220, 255), (int(star[0]), int(star[1])), star[3])

    def update(self):
        input = self.game.input
        brManager=self.game.brManager
        if self.clicked and not input.mouse_down(1):
            self.clicked = False
        pO = self.game.playerO
        
        self.xp.set_text(f'{pO.coins}$')
        # self.points.set_text(f'({pO.points})')
        # self.level.set_text(f'Level {pO.level}')
        # self.points.rect.x = self.xp.rect.x + self.xp.rect.w + 5
        
        self.objects.update()
        clickedBr=brManager.update()
        self.texts.update()
        self.clicked = True if clickedBr==True else self.clicked
        if self.Exit.clicked == True:
            self.safe = 30
            self.game.sceneManager.go("mainMenu")
        if self.Exit.hovered:
            self.game.cursorManager.set_state('hovered')
        
        if self.safe == 0:
            if not self.clicked and input.mouse_down(1):
                if input.mouse_pressed(1):
                    self.lastClick = (input.mouse_pos[0]+brManager.offset_x, input.mouse_pos[1]+brManager.offset_y)
                brManager.offset_x = self.lastClick[0] - input.mouse_pos[0]
                brManager.offset_y = self.lastClick[1] - input.mouse_pos[1]
        else:
            self.safe -= 1
        if self.game.gid.clicked:
            if self.game.gid.counter == 1:
                self.game.gid.play(f"Здесь ты можешь\nулучшать себя", "action1")
            elif self.game.gid.counter == 2:
                self.game.gid.play(f"В целом тебе стоит\nвкачать что-либо")
            elif self.game.gid.counter == 3:
                self.game.gid.play(f"Когда закончишь\nпросто выйди в меню")
            else:
                self.game.gid.end()
        eventManager.event("update menu update")
            
    def draw(self):
        self.background()
        self.game.brManager.draw()
        self.objects.draw()
        self.texts.draw()
        self.game.infoBar.draw(self.game.input.mouse_pos)
        eventManager.event("update draw")

class MainMenu:
    def __init__(self, game_context=None):
        self.game = game_context
        self.objects = ObjectManager(self.game)
        self.texts = TextManager(self.game)
        
        sprite_black = Sprite(self.game.pathManager.TEXTURES / 'black.png', scale=[WIDTH, HEIGHT], color=[255, 255, 255], size=[WIDTH, HEIGHT], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.perehod = self.objects.new_object(sprite_black, [0, 0], 'topleft')
        self.perehod.animator = Animator(self.game.animationManager)
        
        sprite_Title_background = Sprite(self.game.pathManager.TEXTURES / 'title_background.png', scale=[775, 175], color=[100, 100, 255], size=[775, 175], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Title_background = self.objects.new_object(sprite_Title_background, [425, 100], 'center')
        self.cats = []
        self.poshalko()
        #СГРУППИРОВАТЬ В ОДНУ ЦЕЛУЮ ХЕРНЮ ЧТОБЫ ДВИГАТЬ БЫЛО ЛЕГЧЕ😔😔
  
        # Image: pivot=[0.5, 0.5]
        sprite_Menu = Sprite(self.game.pathManager.TEXTURES / 'menu.png', scale=[210,430], color=[100, 100, 255], size=[210,430], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Menu = self.objects.new_object(sprite_Menu, [135, 400], 'center')
        # Image: pivot=[0.5, 0.5]
        sprite_Title = Sprite(self.game.pathManager.TEXTURES / 'title.png', scale=[1000, 200], color=[100, 100, 255], size=[1000, 200], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Title = self.objects.new_object(sprite_Title, [530, 100], 'center')
        self.Title.animator = Animator(self.game.animationManager)
        # Image: pivot=[0.5, 0.5]
        sprite_PlayButton = Sprite(self.game.pathManager.TEXTURES / 'play.png', scale=[235, 95], color=[100, 100, 255], size=[235, 95], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.PlayButton = self.objects.new_object(sprite_PlayButton, [220, 300], 'center', button = True)
        # Image: pivot=[0.5, 0.5]
        sprite_UpdateButton = Sprite(self.game.pathManager.TEXTURES / 'update.png', scale=[262,104], color=[100, 100, 255], size=[262,104], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.UpdateButton = self.objects.new_object(sprite_UpdateButton, [227,400], 'center', button = True)
        # Image: pivot=[0.5, 0.5]
        sprite_SettingsButton = Sprite(self.game.pathManager.TEXTURES / 'settings.png', scale=[280,113], color=[100, 100, 255], size=[280,113], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.SettingsButton = self.objects.new_object(sprite_SettingsButton, [237,490], 'center', button = True)
        # Image: pivot=[0.5, 0.5]
        self.scroll_x = 0
        self.scroll_y = 0
        eventManager.event("main menu")
    
    def poshalko(self):
        # В чём суть посхалки: крч за title спрятать всех котиков, а при нажатии на title крч проверь сам
        self.catsN = ["Cat_Attack.png", "Cat_Defender.png", "Cat_Magic.png", "Cat_Medic.png", "Cat_Worker.png", "Cat_Support.png", "Cat_cowboy.png"] # Посхалкооо
        x_start = self.Title_background.rect.x+80
        x_end = self.Title_background.sprite.scale[0]+self.Title_background.rect.x+40
        dist = x_end-x_start
        mover = 5 # на сколько двигать
        scale = (dist-len(self.catsN)*mover)//len(self.catsN)
        y = self.Title_background.rect.center[1]
        tempx = x_start
        for cat in self.catsN:
            sprite = Sprite(self.game.pathManager.TEXTURES / cat, (scale, scale))
            shket = self.objects.new_object(sprite, [tempx, y], 'center')
            shket.animator = Animator(self.game.animationManager)
            shket.animator.play("idle", speed=random.randint(10, 100)*0.01)
            self.cats.append(shket)
            tempx += mover+scale
    
    def started(self):
        self.game.playerO.ExitTime = time.time()
        self.game.playerO.entry_to_game()
        self.perehod.animator.play("cat spawned", speed=0.01, loop=False, reverse=True)
        if self.game.tutor == True and self.game.tutor_state == 0:
            self.game.gid.play(f"Добро пожаловать\nв игру!!1")
        if self.game.tutor == True and self.game.tutor_state == 2:
            self.game.gid.counter = 5
            self.game.gid.play(f"Время вкачать\nсвои силы :D", "action1")
        if self.game.tutor == True and self.game.tutor_state == 6:
            self.game.gid.counter = 10
            self.game.gid.play(f"Вцелом на этом всё!")
        eventManager.event("main menu started")
    
    def background(self):
        width_cells  = WIDTH // cell_size
        height_cells = HEIGHT // cell_size
        
        offset_x = (self.scroll_x % cell_size) - cell_size
        offset_y = (self.scroll_y % cell_size) - cell_size
        
        scroll_col = int(self.scroll_x // cell_size)
        scroll_row = int(self.scroll_y // cell_size)
        
        for row in range(height_cells +2):
            for col in range(width_cells+2):
                color = cell1 if (row + col + scroll_row + scroll_col) % 2 == 0 else cell2
                
                pygame.draw.rect(screen, color, (
                    col * cell_size + offset_x,
                    row * cell_size + offset_y,
                    cell_size, cell_size
                ))

    def update(self):
        self.objects.update()
        self.texts.update()
        self.Title.animator.update()
        
        self.perehod.animator.update()
        
        self.scroll_y += 0.5
        self.scroll_x += 0.5
        for cat in self.cats:
            cat.animator.update()
        if self.scroll_y >= cell_size * 1000:
            self.scroll_y -= cell_size * 1000
            self.scroll_x -= cell_size * 1000
        if self.PlayButton.clicked == True:
            if self.game.tutor and self.game.tutor_state > 0:
                self.game.gid.play(f"Не время для катки\nещё успеешь")
            else:
                self.game.game_managers()
                self.game.load_entity()
                self.game.sceneManager.go("mainGame")
        elif self.UpdateButton.clicked == True:
            if self.game.tutor and self.game.tutor_state == 0:
                self.game.gid.play(f"Нажми плей!!1", "action1")
            else:
                if self.game.tutor:
                    self.game.tutor_state = 5
                self.game.sceneManager.go("updateScene")
        elif self.SettingsButton.clicked:
            self.game.gid.play(f"В разработке", "action1")
            self.game.gid.counter = -666
        elif self.Title.clicked == True:
            self.Title.animator.play("title click", speed=0.3, loop=False)
            self.game.soundManager.play("meow")
        if not self.perehod.animator.playing:
            self.perehod.visible = False
        else:
            self.perehod.visible = True
        if self.game.tutor == True:
            if self.game.gid.clicked:
                if self.game.gid.counter == 1:
                    self.game.gid.play(f"Я научу играть чтобы\nты был как реально профи")
                elif self.game.gid.counter == 2:
                    self.game.gid.play(f"Для начала тапни плей\nдругие кнопки тебе не нужны")
                elif self.game.gid.counter == 6:
                    self.game.gid.play(f'Нажми на кнопку\n"улучшения"')
                elif self.game.gid.counter == 11:
                    self.game.gid.play(f'В игре много контента\nприятного изучения')
                elif self.game.gid.counter == 12:
                    self.game.gid.play(f'На этом туториал всё!\nпока-пока')
                elif self.game.gid.counter == 13:
                    self.game.gid.end()
                    self.game.tutor = False
                else:
                    self.game.gid.end()
        eventManager.event("main menu update")

    def draw(self):
        
        self.background()
        self.objects.draw()
        self.texts.draw()
        self.perehod.draw()
        eventManager.event("main menu draw")
        

class Gid:
    def __init__(self, game):
        self.game = game
        self.objects = ObjectManager(self.game)
        self.texts = TextManager(self.game)
        
        self.clicked = False
        self.counter = 0
        self.state = "idle"
        self.text = ""
        self.visible = False
        
        sprite_gid_light = Sprite(self.game.pathManager.TEXTURES / 'gid_light.png', scale=[WIDTH, HEIGHT], color=[255, 255, 255], size=[WIDTH, HEIGHT], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.gid_background = self.objects.new_object(sprite_gid_light, [0, 0], 'topleft')
        
        font_tutor = pygame.font.Font(self.game.pathManager.FONT / 'NotoSans-Bold.ttf', 76)
        self.text_obj = self.texts.make(font_tutor, "", [255, 255, 255], [71, 531], 'topleft')
        
        self.images = {
            "idle": "gid_idle.png",
            "action1": "gid_action1.png"
        }
        self.objects_my = self.generate_objects(self.images)
        self.current_object = None
        
        self.animations = {
            "say": "cat clicked"
        }
    
    def end(self):
        self.visible = False
    
    def play(self, text, image="idle", animate="say"):
        self.clicked = False
        self.text = text
        self.state = image
        for obj in self.objects_my.values():
            if obj.name == self.images[self.state]:
                self.current_object = obj
                obj.visible = True
            else:
                obj.visible = False
        
        self.text_obj.set_text(self.text)
        self.current_object.animator.play(self.animations[animate], loop=False, speed=0.8)
        self.visible = True
        
    def generate_objects(self, names):
        objects = {}
        for key, name in names.items():
            
            sprite = Sprite(self.game.pathManager.TEXTURES / name, scale=[428, 616], color=[255, 255, 255], size=[428, 616], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
            object = self.objects.new_object(sprite, [939, HEIGHT-616], 'topleft')
            object.animator = Animator(self.game.animationManager)
            object.visible = False
            object.name = name
            objects[key] = object
        return objects
    
    def update(self):
        if self.visible:
            self.current_object.animator.update()
            if self.game.input.mouse_pressed(1):
                self.clicked = True
                self.counter += 1
    
    def draw(self):
        if self.visible:
            self.objects.draw()
            self.texts.draw()
            
class Tutorial:
    def __init__(self, game_context):
        self.game = game_context
        self.objects = ObjectManager(self.game)
        self.texts = TextManager(self.game)
        
        self.comics_names = [
            "comics_jamal1.png", "comics_jamal2.png", "comics_jamal3.png", 
            "comics_jamal4.png", "comics_jamal5.png", "comics_jamal6.png"
        ] # пенегешке джамалов (порядок в списке = порядок в игре)
        
        sprite_black = Sprite(self.game.pathManager.TEXTURES / 'black.png', scale=[WIDTH, HEIGHT], color=[255, 255, 255], size=[WIDTH, HEIGHT], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        sprite_comics_panels = Sprite(self.game.pathManager.TEXTURES / 'comics_black.png', scale=[WIDTH, HEIGHT], color=[255, 255, 255], size=[WIDTH, HEIGHT], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        
        self.comics_panels = self.objects.new_object(sprite_comics_panels, [0, 0], 'topleft')
        self.comics_objects = self.generate_objects(self.comics_names)
        self.comics_current = 0
        
        self.perehod = self.objects.new_object(sprite_black, [0, 0], 'topleft')
        self.perehod.visible = False
        self.perehod.animator = Animator(self.game.animationManager)
        
        self.scroll_x = 0
        self.scroll_y = 0
    
    def generate_objects(self, names):
        objects = []
        for name in names:
            sprite = Sprite(self.game.pathManager.TEXTURES / name, scale=[WIDTH, HEIGHT], color=[255, 255, 255], size=[WIDTH, HEIGHT], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
            object = self.objects.new_object(sprite, [0, 0], 'topleft')
            object.visible = False
            object.name = name
            objects.append(object)
        return objects
    
    def started(self):
        self.game.tutor = True
        eventManager.event("tutorial started")
    
    def background(self):
        width_cells  = WIDTH // cell_size
        height_cells = HEIGHT // cell_size
        
        offset_x = (self.scroll_x % cell_size) - cell_size
        offset_y = (self.scroll_y % cell_size) - cell_size
        
        scroll_col = int(self.scroll_x // cell_size)
        scroll_row = int(self.scroll_y // cell_size)
        
        for row in range(height_cells + 2):
            for col in range(width_cells + 2):
                color = cell1 if (row + col + scroll_row + scroll_col) % 2 == 0 else cell2
                
                pygame.draw.rect(screen, color, (
                    col * cell_size + offset_x,
                    row * cell_size + offset_y,
                    cell_size, cell_size
                ))

    def update(self):
        self.scroll_y += 0.5
        self.scroll_x += 0.25
        
        self.objects.update()
        self.texts.update()
        self.perehod.animator.update()
        
        if self.game.input.mouse_pressed(1) and self.perehod.visible == False:
            if len(self.comics_objects) > self.comics_current+1:
                self.comics_current += 1
            else:
                self.perehod.visible = True
                self.perehod.animator.play("cat spawned", speed=0.01, loop=False)
        if not self.perehod.animator.playing and self.perehod.visible == True:
            self.game.sceneManager.go("mainMenu")

    def draw(self):
        self.background()
        self.objects.draw()
        self.texts.draw()
        
        for obj in self.comics_objects:
            if obj.name == self.comics_names[self.comics_current]:
                obj.visible = True
            else:
                obj.visible = False

# Game
class Game:
    def __init__(self):
        self.running = True
        self.tutor = False
        self.tutor_state = 0
        
        # Managers
        
        load.set("Init of managers")
        self.programManager = programManager
        self.widgetManager = widgetManager
        self.input = InputManager()
        self.pathManager = PathManager()
        self.sceneManager = SceneManager()
        self.soundManager = SoundManager(self)
        self.cursorManager = CursorManager(self)
        self.brManager = EvolutionManager(self)
        self.hausManager = HausManager(self) # Нахуй
        
        self.musicManager = MusicManager(self)
        
        self.infoBar = InfoBar()
        
        self.widgetManager.init_game(self)
        self.console = console
        
        self.sounds_init()
        self.animate_init()
        
        load.set("Scene starting...")
        self.sceneManager.init(LoginScene(self),"login")
        self.gid = Gid(self)
        
        load.loaded(self)
        eventManager.event("loaded")
        self.sceneManager.go("login")
        load.wait_and_close()
        self.loop()
    
    def load_profile(self, profile_id):
        self.saveManager = SaveManager(self, current_profile = profile_id)
        self.playerO = PlayerOffside(self, self.saveManager.load_game())
        eventManager.event("load profile")
        
    def game_managers(self):
        self.player = Player(self)
        self.statManager = Statistics()
        
        self.enemyManager = EnemyManager(self)
        self.towerManager = TowerManager(self)
        self.storeManager = StoreManager(self)
        self.waveManager = WaveManager(self)
        eventManager.event("load game managers")
    
    def load_entity(self):
        load_entity(self)
        eventManager.event("load entity")
    
    def animate_init(self):
        load.set("Loading animations")
        pm = self.pathManager
        self.animationManager = AnimationManager(self) # Спиздил идею у sounds_init
        
        eventManager.event("animate init")
        
        self.animationManager.init(pm.ANIMATIONS / "idle.json", "idle")
        self.animationManager.init(pm.ANIMATIONS / "cat_clicked.json", "cat clicked")
        self.animationManager.init(pm.ANIMATIONS / "cat_spawn.json", "cat spawned")
        self.animationManager.init(pm.ANIMATIONS / "cat_attack.json", "cat attack")
        self.animationManager.init(pm.ANIMATIONS / "walk.json", "walk")
        
        self.animationManager.init(pm.ANIMATIONS / "shop_hover.json", "hover shop")
        self.animationManager.init(pm.ANIMATIONS / "shop_hovered.json", "hovered shop")
        self.animationManager.init(pm.ANIMATIONS / "shop_unhover.json", "not hover shop")
        self.animationManager.init(pm.ANIMATIONS / "shop_idle.json", "idle shop")
        
        self.animationManager.init(pm.ANIMATIONS / "ui_hover.json", "hover")
        self.animationManager.init(pm.ANIMATIONS / "ui_hovered.json", "hovered")
        
        self.animationManager.init(pm.ANIMATIONS / "paused_anim.json", "paused")
        self.animationManager.init(pm.ANIMATIONS / "jump_mega_happy_animation_3000_part_1.json", "jump part 1")
        self.animationManager.init(pm.ANIMATIONS / "jump_mega_happy_animation_3000_part_2.json", "jump part 2")
        self.animationManager.init(pm.ANIMATIONS / "rotater_3000_penis_spiner_loop_while_true.json", "cat spiner")
        self.animationManager.init(pm.ANIMATIONS / "title.json", "title click")
        
        self.animationManager.init(pm.ANIMATIONS / "x2.json", "x2")
        
        self.animationManager.init(pm.ANIMATIONS / "evo_buttons.json", "evo idle")
        self.animationManager.init(pm.ANIMATIONS / "evo_locked.json", "evo locked")
        self.animationManager.init(pm.ANIMATIONS / "evo_hover.json", "evo hover")
        self.animationManager.init(pm.ANIMATIONS / "evo_unhover.json", "evo unhover")
        self.animationManager.init(pm.ANIMATIONS / "evo_hovered.json", "evo hovered")
    
    def sounds_init(self):
        load.set("Loading sounds")
        pm = self.pathManager # Чтобы не писать миллион писек
        # Музыка в MusicManager
        
        eventManager.event("sound init")
        
        self.soundManager.init(pm.AUDIO / "coin.mp3", "coin")                   # когда собако сдох
        self.soundManager.init(pm.AUDIO / "select.mp3", "select")               # взял в магазе
        self.soundManager.init(pm.AUDIO / "deselect.ogg", "deselect")           # убрал в магаз
        self.soundManager.init(pm.AUDIO / "buy.mp3", "buy", 0.2)                # поставил
        self.soundManager.init(pm.AUDIO / "wave.mp3", "wave", 0.45)             # начало волны
        
        self.soundManager.init(pm.AUDIO / "hover.wav", "hover", 0.2)            # при наводке на интерфейс
        self.soundManager.init(pm.AUDIO / "click.mp3", "click", 0.7)            # при нажатии на интерфейс
        self.soundManager.init(pm.AUDIO / "pause.mp3", "paused", 0.8)             # паузка
        
        self.soundManager.init(pm.AUDIO / "bump.mp3", "bump", 0.25)             # урон
        self.soundManager.init(pm.AUDIO / "bump_r.mp3", "bump revers", 0.5)     # урон?
        self.soundManager.init(pm.AUDIO / "heal.mp3", "heal", 0.4)              # Хиллится чорт какой-то
        self.soundManager.init(pm.AUDIO / "meow.mp3", "meow", 0.45)             # meow meow meow meow
        self.soundManager.init(pm.AUDIO / "boom.mp3", "explode", 0.4)           # начало волны

    def update(self):
        self.cursorManager.reset()
        self.musicManager.update()
        events = pygame.event.get()
        self.input.update(events)
        self.infoBar.clear()
        eventManager.event("game update")
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        self.gid.update()
        self.sceneManager.curent.update()
        self.widgetManager.update()
        self.cursorManager.apply()
    
    def draw(self):
        eventManager.event("game draw")
        self.sceneManager.curent.draw()
        self.widgetManager.draw()
        self.gid.draw()
    
    def loop(self):
        while self.running:
            self.update()
            self.draw()
            
            present()
            clock.tick(FPS)

# Датапак - это код из Data/DataPacks. На мобилке он опционален:
# если что-то пошло не так, игра должна запуститься, а не умереть.
try:
    if datapackM.enableDatapack is not None:
        exec(datapackM.get_code())
except Exception as _datapack_error:
    console.log("Datapack failed: " + str(_datapack_error), (255, 120, 120))

load.set("Init of RPC")
rpc = RPC()
load.set("Game starting...")
game = Game()
rpc.stop()