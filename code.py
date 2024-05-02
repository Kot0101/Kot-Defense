import pygame
import os
import random
from pypresence import Presence
import pickle
# import socket
# import json
import time
import webbrowser
import pygame.locals as pl

# Инициализация Pygame
pygame.init()
try:
    pygame.mixer.init()
except:
    pass

client_id = '1210980897281802330'

try:
    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(details=f"Загрузка", large_image="kotdefense", large_text="Kot Defense")
except:
    pass

global dangerous_keywords_pp2irooodjhjjjkjkn, mods_count_11d23s2saaa, port, event_game, stop_game, new_cat
dangerous_keywords_pp2irooodjhjjjkjkn= ['os.system', 'os.popen']
mods_count_11d23s2saaa = 0
port = random.randint(1, 65535)
scripts = []
event_game = None
stop_game = False
new_cat = None

width = 1400
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kot Defense 1.81")

text_color = (0, 0, 0)
heart_color = (255, 0, 0)
money_color = (10, 80, 10)
background_color = (30, 150, 30)
event1_background_color = (91, 122, 24)
red_btn_color = (255, 0, 0)
green_btn_color = (0, 255, 0)
blue_btn_color = (0, 0, 255)
down_menu_cats = (100, 100, 100)
event1_down_menu_cats = (107, 66, 18)
info_text_outlining_color = (0, 0, 0)
info_text_color = (170, 170, 170)
skip_button_color = (255, 0, 0)
boss_background_color = (102, 125, 12)

def loading_text(lo):
    fonte = pygame.font.Font(None, 75)
    text = fonte.render("Пожалуйста подождите", True, text_color)
    text_rect = text.get_rect(center=(width/2, height/2))
    text2 = fonte.render(f"Загрузка {lo}...", True, text_color)
    text_rect2 = text.get_rect(center=(width/2-50, height/2+70))
    screen.fill(background_color)
    screen.blit(text, text_rect)
    screen.blit(text2, text_rect2)
    pygame.display.flip()

loading_text('основных данных')

#загрузка шрифтов
font = pygame.font.Font("Data/Fonts/segoe-ui-symbol.ttf", 35)
font2 = pygame.font.Font(None, 25)

def start_script(script, type2):
    if type2 == script.type:
        return script.code

class Script:
    def __init__(self, file_path, type2):
        global scripts
        self.type = type2
        with open(file_path, 'r', encoding='utf-8') as file:
            self.code = file.read()
            dangerous = False
            for keyword in dangerous_keywords_pp2irooodjhjjjkjkn:
                if keyword in self.code:
                    dangerous = True
                    break
        if dangerous == False:
            scripts.append(self)
            del self

pause_image = pygame.image.load('Data/Img/pause.png')
icon = pygame.image.load('Data/Img/ico.png')
btn_image = pygame.image.load('Data/Img/btn.png')
btn2_image = pygame.image.load('Data/Img/btn2.png')
play_image = pygame.image.load('Data/Img/play.png')
back_image = pygame.image.load('Data/Img/back.png')
info_image = pygame.image.load('Data/Img/info.png')
discord_image = pygame.image.load('Data/Img/discord.png')
mult_image = pygame.image.load('Data/Img/mult.png')
host_image = pygame.image.load('Data/Img/host.png')
connect_image = pygame.image.load('Data/Img/connect.png')
cursor_img = pygame.image.load("Data/Img/cursor.png")
error_img = pygame.image.load("Data/Img/error.png")
mods_image = pygame.image.load("Data/Img/mods.png")
play2_image = pygame.image.load("Data/Img/EVENT PLAY.png")

cat_image = pygame.image.load('Data/Img/Cat1.png')
cat2_image = pygame.image.load('Data/Img/Cat2.png')
cat3_image = pygame.image.load('Data/Img/Cat3.png')
cat4_image = pygame.image.load('Data/Img/Cat4.png')
cat5_image = pygame.image.load('Data/Img/Cat5.png')
cat6_image = pygame.image.load('Data/Img/Cat6.png')
cat7_image = pygame.image.load('Data/Img/Cat7.png')
cat8_image = pygame.image.load('Data/Img/Cat8.png')
cat9_image = pygame.image.load('Data/Img/Cat9.png')
cat9_ico_image = pygame.image.load('Data/Img/Cat9_ico.jpg')
cat10_image = pygame.image.load('Data/Img/Cat10.png')
cat11_image = pygame.image.load('Data/Img/Cat11.png')
cat12_image = pygame.image.load('Data/Img/Cat12.png')
cat13_image = pygame.image.load('Data/Img/Cat13.png')
cat14_image = pygame.image.load('Data/Img/Cat14.png')
CatDog_image = pygame.image.load('Data/Img/CatDog.jpg')
shild_image = pygame.image.load('Data/Img/cat_shield.png')
cwa_image = pygame.image.load('Data/Img/cwa_image.png')
cat15_image = pygame.image.load('Data/Img/Cat15.png')

dog_image = pygame.image.load('Data/Img/Dog1.png')
dog2_image = pygame.image.load('Data/Img/Dog2.jpg')
dog3_image = pygame.image.load('Data/Img/Dog3.png')
dog4_image = pygame.image.load('Data/Img/Dog4.png')
dog5_image = pygame.image.load('Data/Img/Dog5.png')
dog6_image = pygame.image.load('Data/Img/Dog6.png')
dog7_image = pygame.image.load('Data/Img/Dog7.png')

cat_image = pygame.transform.scale(cat_image, (60, 60))
cat2_image = pygame.transform.scale(cat2_image, (60, 60))
cat3_image = pygame.transform.scale(cat3_image, (60, 60))
cat4_image = pygame.transform.scale(cat4_image, (60, 60))
cat5_image = pygame.transform.scale(cat5_image, (60, 60))
cat6_image = pygame.transform.scale(cat6_image, (60, 60))
cat7_image = pygame.transform.scale(cat7_image, (60, 60))
cat8_image = pygame.transform.scale(cat8_image, (60, 60))
cat9_image = pygame.transform.scale(cat9_image, (120, 60))
cat9_ico_image = pygame.transform.scale(cat9_ico_image, (60, 60))
cat10_image = pygame.transform.scale(cat10_image, (60, 60))
cat11_image = pygame.transform.scale(cat11_image, (60, 60))
cat12_image = pygame.transform.scale(cat12_image, (60, 60))
cat13_image = pygame.transform.scale(cat13_image, (60, 60))
cat14_image = pygame.transform.scale(cat14_image, (60, 60))
CatDog_image = pygame.transform.scale(CatDog_image, (60, 60))
shild_image = pygame.transform.scale(shild_image, (60, 60))
cwa_image = pygame.transform.scale(cwa_image, (60, 60))
cat15_image = pygame.transform.scale(cat15_image, (60, 60))

dog_image = pygame.transform.scale(dog_image, (60, 60))
dog2_image = pygame.transform.scale(dog2_image, (60, 60))
dog3_image = pygame.transform.scale(dog3_image, (60, 60))
dog4_image = pygame.transform.scale(dog4_image, (60, 60))
dog5_image = pygame.transform.scale(dog5_image, (60, 60))
dog6_image = pygame.transform.scale(dog6_image, (70, 70))
dog7_image = pygame.transform.scale(dog7_image, (60, 60))

try:
    dog_bump = pygame.mixer.Sound('Data/Sounds/bump.mp3')
    boom = pygame.mixer.Sound('Data/Sounds/boom.mp3')
    click = pygame.mixer.Sound('Data/Sounds/click.mp3')
    sirena = pygame.mixer.Sound('Data/Sounds/sirena.mp3')
except:
    pass

global music_playing
music_playing = True
try:
    dog_bump.set_volume(0.1)
    boom.set_volume(0.1)
except:
    pass

btn_image = pygame.transform.scale(btn_image, (60, 60))
btn2_image = pygame.transform.scale(btn2_image, (60, 60))
pause_image = pygame.transform.scale(pause_image, (40, 40))
play_image = pygame.transform.scale(play_image, (220, 220))
back_image = pygame.transform.scale(back_image, (120, 120))
info_image = pygame.transform.scale(info_image, (120, 120))
discord_image = pygame.transform.scale(discord_image, (100, 100))
mult_image = pygame.transform.scale(mult_image, (240, 60))
host_image = pygame.transform.scale(host_image, (160, 80))
connect_image = pygame.transform.scale(connect_image, (200, 65))
mods_image = pygame.transform.scale(mods_image, (120, 45))
play2_image = pygame.transform.scale(play2_image, (210, 90))

pygame.display.set_icon(icon)

loading_text('модифицированных данных')

#загрузка данных
folder_path = 'Data\\Mods\\'
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name == 'load.py':
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
                dangerous = False
                for keyword in dangerous_keywords_pp2irooodjhjjjkjkn:
                    if keyword in code:
                        dangerous = True
                        break
                if dangerous == True:
                    pass
                else:
                    try:
                        exec(code)
                    except Exception as e:
                        print(f"An error occurred: {e}")


loading_text('дата паков')
#Загрузка дата паков
music_path = 'Data/Sounds/music.mp3'
event1_music = 'Data/Sounds/event1_music.mp3'
music_path2 = 'Data/Sounds/music2.mp3'
folder_path = 'Data\DataPacks'

for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        if file_name == 'back.png':
            back_image = pygame.image.load(file_path)
            back_image = pygame.transform.scale(back_image, (120, 120))
        elif file_name == 'btn.png':
            btn_image = pygame.image.load(file_path)
            btn_image = pygame.transform.scale(btn_image, (60, 60))
        elif file_name == 'btn2.png':
            btn2_image = pygame.image.load(file_path)
            btn2_image = pygame.transform.scale(btn2_image, (60, 60))
        elif file_name == 'pause.png':
            pause_image = pygame.image.load(file_path)
            pause_image = pygame.transform.scale(pause_image, (40, 40))
        elif file_name == 'play.png':
            play_image = pygame.image.load(file_path)
            play_image = pygame.transform.scale(play_image, (220, 220))
        elif file_name == 'play2.png':
            play2_image = pygame.image.load(file_path)
            play2_image = pygame.transform.scale(play2_image, (210, 90))
        elif file_name == 'music.mp3':
            try:
                music_path = file_path
            except:
                pass
        elif file_name == 'event1_music.mp3':
            try:
                event1_music = file_path
            except:
                pass
        elif file_name == 'music2.mp3':
            try:
                music_path2 = file_path
            except:
                pass
        elif file_name == 'theme.py':
            with open(file_path, 'r') as file:
                sperma = False
                for line in file:
                    line = line.strip()
                    if any(var_name in line for var_name in ['text_color', 'heart_color', 'money_color', 'background_color', 'event1_background_color', 'red_btn_color',
                                                              'green_btn_color', 'blue_btn_color', 'down_menu_cats', 'event1_down_menu_cats', 'info_text_outlining_color',
                                                              'info_text_color', 'skip_button_color', ]) and any(var_name in line for var_name in [name for name in dir() if not name.startswith('__')]):
                        sperma = True
                if sperma == False:
                    try:
                        exec(line)
                    except Exception as e:
                        print(f"An error occurred: {e}")

try:
    music2 = music_path2
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
except:
    pass

loading_text('классов')

#классы
class BuyCat:
    def __init__(self, ico, moneys, info_self, image, aura_radius, cat_health, dogs_count, reload, damage_cat, mega, wawe, wawedel, path_my_image, size_x, size_y):
        global buy_cats, scripts, buy_no_cats, wave, event_game, cats_moneys
        for script in scripts:
            exec(str(start_script(script, 'create_buy_cat')))
        self.ico = ico
        self.rect = ico.get_rect(topleft=(20, height-77))
        self.xtext = self.rect.x+3
        self.ytext = height-130
        self.money = moneys
        cats_moneys[moneys] = self
        self.info = info_self
        self.image = image
        self.aura_radius = aura_radius
        self.health = cat_health
        self.dogs_count = dogs_count
        self.reload = reload
        self.damage = damage_cat
        self.mega = mega
        self.blacklist = []
        self.wave = wawe
        self.delet_wave = wawedel
        self.path_my_image = path_my_image
        self.size_x = size_x
        self.size_y = size_y
        self.unblock = False
        if self.delet_wave == -1 or event_game == 1:
            self.delet_wave = 9999999999999999999999999999999999999999999999999999999999999999999999999999999999*99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        if self.delet_wave <= wave:
            buy_no_cats.append(self)
        else:
            if self.wave <= wave or event_game == 1:
                buy_cats.append(self)
            else:
                buy_no_cats.append(self)

    
    def draw(self):
        global xexe, scripts, buy_no_cats
        for script in scripts:
            exec(str(start_script(script, 'draw_buy_cat')))
        try:
            self.xtext = self.rect.x+3
            self.ytext = height-130
            if self.rect.x > 1060:
                return
            if xexe >0 and self.rect.x < 100:
                return
            
            if self not in buy_no_cats:
                screen.blit(self.ico, (self.rect.x, self.rect.y))
            money_str = str(self.money)  
            x, y = self.xtext, self.ytext
            num_newlines = len(money_str) // 3 
            if len(money_str) % 3 == 0:
                num_newlines -= 1 
            y -= 10 * num_newlines
            last_chunk_height = 0

            if self not in buy_no_cats:
                for i in range(0, len(money_str), 3):
                    chunk = money_str[i:i+3]
                    text_surface = font.render(chunk, True, text_color)
                    text_width, text_height = font.size(chunk)
                    screen.blit(text_surface, (x, y))
                    y += text_height - 20  
                    last_chunk_height = text_height
                
                text_surface = font.render("$", True, text_color)
                screen.blit(text_surface, (x + text_width, y - last_chunk_height + 20))
        except:
            pass
    
    def move(self, xe):
        global scripts
        for script in scripts:
            exec(str(start_script(script, 'move_buy_cat')))
        try:
            self.rect.x += xe
        except:
            pass
    
    def spawn(self):
        global buy_cats, scripts, buy_no_cats, wave
        
        try:
            if self in buy_cats and self.delet_wave <= wave:
                buy_cats.remove(self)
                buy_no_cats.append(self)
                new_cat_unblock()
            elif self in buy_no_cats and self.wave <= wave and self.delet_wave > wave or self.unblock == True:
                buy_no_cats.remove(self)
                buy_cats.append(self)
                new_cat_unblock()
        except:
            pass
    
    def info_cat(self, pos):
        global cats_boost, cat_works_boost, xexe, scripts
        for script in scripts:
            exec(str(start_script(script, 'info_buy_cat')))
        try:
            if self not in buy_no_cats:
                if self.rect.x > 1060:
                    return
                if xexe >0 and self.rect.x < 100:
                    return
                if self.rect.collidepoint(pos):
                    info(self.info, (pos[0] + 15, pos[1] + 5))
        except:
            pass
    
    def buy(self, pos, mo):
        global cats, money, xexe, scripts, catown, catown2, buy_no_cats, new_cat
        for script in scripts:
            exec(str(start_script(script, 'buy_cat')))
        try:
            if self not in buy_no_cats:
                if self.rect.x > 1060:
                    return
                if xexe >0 and self.rect.x < 100:
                    return
                if mo == 1:
                    if self.rect.collidepoint(pos):
                        if catown:
                            catown.sell(1)
                            catown = None
                        else:
                            if money >= self.money:
                                money -= self.money
                                new_cat = Cat(self.image, self.aura_radius, self.health, self.dogs_count, self.money, self.reload, self.damage, self.mega, self.path_my_image, self.size_x, self.size_y) 
                                for script in scripts:
                                    exec(str(start_script(script, 'buy_cat_create')))
                                catown = new_cat
                                cats.append(new_cat)
                                new_cat.dds = mo
                                new_cat.blacklist.extend(self.blacklist)
                else:
                    if self.rect.collidepoint(pos):
                        if catown2:
                            catown2.sell(1)
                            catown2 = None
                        else:
                            if money >= self.money:
                                money -= self.money
                                new_cat = Cat(self.image, self.aura_radius, self.health, self.dogs_count, self.money, self.reload, self.damage, self.mega, self.path_my_image, self.size_x, self.size_y) 
                                catown2 = new_cat
                                new_cat.dds = mo
                                new_cat.blacklist.extend(self.blacklist)
                                cats.append(new_cat)
        except:
            pass
    def random_buy(self, custom_X, custom_Y):
        global cats, money, xexe, scripts, catown, catown2, buy_no_cats
        for script in scripts:
            exec(str(start_script(script, 'buy_cat')))
        try:
            new_cat = Cat(self.image, self.aura_radius, self.health, self.dogs_count, self.money, self.reload, self.damage, self.mega, self.path_my_image, self.size_x, self.size_y) 
            new_cat.follow_mouse = False
            popitki = 0
            while True:
                if custom_X == None:
                    xx = random.randint(60, width-60)
                else:
                    xx = custom_X
                if custom_Y == None:
                    yy = random.randint(60, height-195)
                else:
                    yy = custom_Y
                popitki += 1
                if popitki == 10000:
                    break
                new_cat.rect.center = (xx, yy)
                cat_collides = any(new_cat.rect.colliderect(c.rect) for c in cats if c != self)
                dog_collides = any(new_cat.rect.colliderect(d.rect) for d in dogs)
                if not cat_collides and not dog_collides:
                    break
            cats.append(new_cat)
            new_cat.dds = 1
            new_cat.blacklist.extend(self.blacklist)
        except:
            pass


class Cat:
    def __init__(self, image, aura_radius, cat_health, dogs_count, cat_money, reload, damage_cat, mega, path_my_image, size_x, size_y):
        global scripts
        for script in scripts:
            exec(str(start_script(script, 'create_cat')))
        self.original_image = image.convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.aura_radius = aura_radius
        self.follow_mouse = True
        self.health = cat_health
        self.maxhealth = self.health
        self.dogs_count = dogs_count
        self.money = cat_money
        self.reload = reload
        self.damage = damage_cat
        self.unable_to_place = False
        self.mega = mega
        self.maxhe = self.health
        self.stope = False
        self.blacklist = []
        self.dds = 0
        self.path_my_image = path_my_image
        self.size_x = size_x
        self.size_y = size_y
        

    def update(self, pos):
        global scripts
        self.stope = False
        for script in scripts:
            exec(str(start_script(script, 'update_cat')))
        try:
            if self.stope == False:
                pause_rect = pause_image.get_rect(topleft=(width-55, 10))
                rect22 = pygame.Rect(0, height-160, 1400, 160)
                if self.follow_mouse:
                    self.rect.center = pos
                    self.image.set_alpha(128)
                    cat_collides = any(self.rect.colliderect(c.rect) for c in cats if c != self)
                    dog_collides = any(self.rect.colliderect(d.rect) for d in dogs)
                    if not rect22.collidepoint(self.rect.center) and not pause_rect.collidepoint(self.rect.center) and not cat_collides and not dog_collides:
                        self.unable_to_place = True
                        self.image = self.original_image.copy()
                        self.image.set_alpha(128)
                    else:
                        self.unable_to_place = False
                        self.image.fill((255, 50, 50), special_flags=pygame.BLEND_RGBA_MULT) 

                else:
                    self.image = self.original_image.copy()
                    if rect22.collidepoint(self.rect.center):
                        self.sell(1)
        except:
            pass
    
    def bump(self, damage):
        global cats, scripts
        self.stope = False
        try:
            for script in scripts:
                exec(str(start_script(script, 'bump_cat')))
            if self.follow_mouse == False and self.stope == False:
                self.health -= damage
                if self.health <= 0:
                    self.sell(0)
        except:
            pass
    
    def draw(self, screen, online):
        global cat, scripts, catown2, catown, cursor_pos, pos
        self.stope = False
        for script in scripts:
            exec(str(start_script(script, 'draw_cat')))
        try:
            if self.aura_radius > 0 and self.stope == False: 
                if online != 0:
                    if catown2 != None or catown != None or self.rect.collidepoint(pos) or self.rect.collidepoint(cursor_pos):
                        circle_surface = pygame.Surface((self.aura_radius * 2, self.aura_radius * 2), pygame.SRCALPHA)
                        pygame.draw.circle(circle_surface, (255, 255, 255, 100), (self.aura_radius, self.aura_radius), self.aura_radius, 2)
                        screen.blit(circle_surface, (self.rect.centerx - self.aura_radius, self.rect.centery - self.aura_radius))
                else:
                    if catown != None or self.rect.collidepoint(pos):
                        circle_surface = pygame.Surface((self.aura_radius * 2, self.aura_radius * 2), pygame.SRCALPHA)
                        pygame.draw.circle(circle_surface, (255, 255, 255, 100), (self.aura_radius, self.aura_radius), self.aura_radius, 2)
                        screen.blit(circle_surface, (self.rect.centerx - self.aura_radius, self.rect.centery - self.aura_radius))

            screen.blit(self.image, self.rect)
        except:
            pass
    
    def info_ca(self, screen, pos):
        global scripts
        self.stope = False
        for script in scripts:
            exec(str(start_script(script, 'info_cat')))
        try:
            if self.rect.collidepoint(pos) and self.follow_mouse == False and self.stope == False:
                info(f'{round(self.health,1)} жизней', (pos[0] + 15, pos[1] + 5))
        except:
            pass
    
    def remove_dogs_periodically(self, reloadType):
        global money, cat_works_boost, cats_boost, scripts
        self.stope = False
        try:
            if reloadType == self.reload:
                count_attacs = 0
                if not self.follow_mouse:
                    if self.mega == 2:
                        money += self.damage+cat_works_boost
                    elif self.mega == 6:
                        new_dog = Dog(self.rect.x, self.rect.y, cwa_image, 12, 0, 3, 1, 14, 1, 0, 'Data/Img/cwa_image.png', 60, 60)
                        dogs.append(new_dog)
                    elif self.mega == 7:
                        new_dog = Dog(self.rect.x, self.rect.y, CatDog_image, 25, 0, 2, 3, 14, 1, 0, 'Data/Img/CatDog.jpg', 60, 60)
                        dogs.append(new_dog)
                    elif self.mega == 4:
                        for cat in list(cats):
                            if count_attacs < self.dogs_count:
                                if pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(cat.rect.center)) <= self.aura_radius:
                                    if cat.maxhe > cat.health:
                                        cat.bump(-self.damage)
                                    if cat.maxhe < cat.health:
                                        cat.health = cat.maxhe
                            else:
                                break
                for script in scripts:
                    exec(str(start_script(script, 'remove_dogs_periodically')))
                count_attacs = 0
                if not self.follow_mouse and self.stope == False:
                    if self.mega == 1:
                        for dog in list(dogs):
                            if self.blacklist == []:
                                blackdog = False
                            else:
                                blackdog = True
                                for blackitem in self.blacklist:
                                    if dog.typee == blackitem:
                                        blackdog = False
                            if blackdog == False and dog.mega != 14:
                                if count_attacs < self.dogs_count:
                                    if pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(dog.rect.center)) <= self.aura_radius:
                                        count_attacs += 1
                                        if self.image != cat4_image:
                                            try:
                                                dog_bump.play()
                                            except:
                                                pass
                                        else:
                                            try:
                                                boom.play()
                                            except:
                                                pass
                                        dog.bump(self.damage+cats_boost, True, self)
                                else:
                                    break
        except:
            pass
    
    def sell(self, mn):
        global money, pause, scripts
        self.stope = False
        try:
            for script in scripts:
                exec(str(start_script(script, 'sell_cat')))
            
            if self.stope == False:
                money += round(self.money * mn)
                cats.remove(self)
                del self
        except:
            pass
    
    def handle_mouse_click(self, pos, mo):
        global cats, dogs, scripts, catown, catown2
        self.stope = False
        try:
            for script in scripts:
                exec(str(start_script(script, 'handle_mouse_click_cat')))
            if mo == 1:
                if self == catown and self.stope == False:
                    rect22 = pygame.Rect(0, height-100, 1400, 100)
                    if self.unable_to_place == True:
                        rect = pygame.Rect(0, height-100, 1400, 100)
                        self.follow_mouse = False
                        catown = None
            else:
                if self == catown2 and self.stope == False:
                    rect22 = pygame.Rect(0, height-100, 1400, 100)
                    if self.unable_to_place == True:
                        rect = pygame.Rect(0, height-100, 1400, 100)
                        self.follow_mouse = False
                        catown2 = None
        except:
            pass
    def cwa(self):
        try:
            self.damage = 0
            self.health = 3
            self.aura_radius = 0
            self.image = cwa_image
            self.money = 0
            self.original_image = cwa_image
            self.image_path = 'Data\Img\cwa_image.png'
        except:
            pass

class CreateDog:
    def __init__(self, money_dog, bugete, name, image, health_dog, speed, damage_dog, unikal, reload, typedog, path_my_image, size_x, size_y):
        global dogs_variants, dogs_moneys, dogs_class, scripts
        for script in scripts:
            exec(str(start_script(script, 'create_dog')))
        dogs_variants[name] = bugete
        dogs_moneys[name] = money_dog
        dogs_class[name] = self
        self.image = image
        self.speed = speed
        self.health = health_dog
        self.money = money_dog
        self.damage = damage_dog
        self.mega = unikal
        self.reload = reload
        self.type = typedog
        self.damagecats = []
        self.path_my_image = path_my_image
        self.size_x = size_x
        self.size_y = size_y
    
    def create(self, custom_X, custom_Y):
        global dogs, scripts
        for script in scripts:
            exec(str(start_script(script, 'spawn_dog')))
        try:
            if custom_X == None:
                xx = random.randint(-900, -60)
            else:
                xx = custom_X
            if custom_Y == None:
                yy = random.randint(115, height - 255)
            else:
                yy = custom_Y
            new_dog = Dog(xx, yy, self.image, self.health, self.money, self.speed, self.damage, self.mega, self.reload, self.type, self.path_my_image, self.size_x, self.size_y)
            dogs.append(new_dog)
            new_dog.damagecats = self.damagecats
        except:
            pass

class Dog:
    def __init__(self, x, y, image, health_dog, money_dog, speed, damage_dog, unikal, reload, dogtype, path_my_image, size_x, size_y):
        for script in scripts:
            exec(str(start_script(script, 'spawn_dog')))
        self.rect = image.get_rect(topleft=(x, y))
        self.image = image
        self.speed = speed
        self.health = health_dog
        self.money = money_dog
        self.damage = damage_dog
        self.mega = unikal
        self.aura_radius = 200-30
        self.reload = reload
        self.val = 0
        self.val2 = True
        self.val3 = 0
        self.typee = dogtype
        self.stope = False
        self.damagecats = []
        self.who = []
        self.maxhealth = self.health
        self.path_my_image = path_my_image
        self.size_x = size_x
        self.size_y = size_y

    def move(self):
        global dog_damag_boost, scripts
        self.stope = False
        moveE = True
        try:
            if self.mega != 14:
                for dog2 in list(dogs):
                    if dog2.mega == 14 and moveE == True and self.rect.colliderect(dog2.rect):
                        moveE = False
                for cat2 in list(cats):
                    if self.rect.colliderect(cat2.rect) and moveE == True:
                        if cat2.follow_mouse == False:
                            moveE = False
                if self.mega == 6:
                    if self.val3 == 2 or self.val3 == 1:
                        self.stope = True
                elif self.mega == 4 and self.val <= 60 or self.mega == 7 and self.val <= 60:
                    self.val += 2
                    self.rect.y += 2
                elif self.mega == 5 and self.val <= 60 or self.mega == 8 and self.val <= 60:
                    self.val += 2
                    self.rect.y -= 2
                elif self.mega == 5 or self.mega == 4 or self.mega == 7 or self.mega == 8:
                    if moveE and self.val > 60 or self.mega == 7 and self.val <= 60:
                        self.rect.x += self.speed
                        self.stope = True
                elif self.mega == 9:
                    self.rect.x += self.speed
                    self.stope == True
                for script in scripts:
                    exec(str(start_script(script, 'move_dog')))
                if moveE and self.stope == False:
                    self.rect.x += self.speed
            else:
                for dog2 in list(dogs):
                    if self.rect.colliderect(dog2.rect) and dog2 != self and dog2.mega != 14:
                        moveE = False
                if moveE and self.stope == False:
                    self.rect.x -= self.speed
                    self.bump(0.03, True, [])
        except:
            pass
            
    def update(self):
        global scripts
        try:
            screen.blit(self.image, self.rect)
        except:
            pass
        
    def info_do(self, pos):
        global scripts
        self.stope = False
        try:
            if self.mega == 2 or self.mega == 7 or self.mega == 8:
                circle_surface = pygame.Surface((self.aura_radius * 2, self.aura_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (255, 0, 0, 100), (self.aura_radius, self.aura_radius), self.aura_radius, 2)
                screen.blit(circle_surface, (self.rect.centerx - self.aura_radius, self.rect.centery - self.aura_radius))
                if self.rect.collidepoint(pos):
                    info(f'{round(self.health,1)} жизней, взрываеться и наносит {self.damage+dog_damag_boost} урона всем котам в зоне поражения', (pos[0] + 15, pos[1] + 5))
                self.stope = True
            if self.mega == 12:
                circle_surface = pygame.Surface((self.aura_radius * 2, self.aura_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (255, 0, 0, 100), (self.aura_radius, self.aura_radius), self.aura_radius, 2)
                screen.blit(circle_surface, (self.rect.centerx - self.aura_radius, self.rect.centery - self.aura_radius))
                if self.rect.collidepoint(pos):
                    info(f'{round(self.health,1)} жизней, лечит собак, наносит 1 урон', (pos[0] + 15, pos[1] + 5))
                self.stope = True
            for script in scripts:
                exec(str(start_script(script, 'info_dog')))
            if self.stope == False and self.rect.collidepoint(pos):
                info(f'{round(self.health,1)} жизней, урон {self.damage+dog_damag_boost}, скорость {self.speed}', (pos[0] + 15, pos[1] + 5))
        except:
            pass
        
    def bump(self, damage, die, kto):
        try:
            self.who = kto
            global money, dogs, scripts
            self.stope = False
            if self.typee == 2:
                if self.who == []:
                    pass
                elif self.damagecats == self.who.blacklist:
                    self.health -= damage
                else:
                    self.stope = True
            if self.health <= 0:
                if self.mega == 6 and self.val3 == 0:
                    self.health = 0.1
                    self.val3 = 1
                    self.stope = True
                elif self.mega == 6 and self.val3 == 1:
                    self.health = 0.1
                    self.stope = True
                    
            for script in scripts:
                exec(str(start_script(script, 'bump_dog')))
            if self.stope == False:
                self.health -= damage
                if self.health <= 0:
                    if self.mega == 10:
                        new_dog = Dog(self.rect.x, self.rect.y, dog3_image, 7, 350, 5, 20, 2, 1, 1, 'Data/Img/Dog3.png', 60, 60)
                        dogs.append(new_dog)
                        new_dog = Dog(self.rect.x, self.rect.y, dog3_image, 7, 350, 5, 20, 7, 1, 1, 'Data/Img/Dog3.png', 60, 60)
                        dogs.append(new_dog)
                        new_dog = Dog(self.rect.x, self.rect.y, dog3_image, 7, 350, 5, 20, 8, 1, 1, 'Data/Img/Dog3.png', 60, 60)
                        dogs.append(new_dog)
                        new_dog = Dog(self.rect.x, self.rect.y, dog3_image, 7, 350, 5, 20, 8, 1, 1, 'Data/Img/Dog3.png', 60, 60)
                        dogs.append(new_dog)
                        new_dog = Dog(self.rect.x, self.rect.y, dog_image, 1, 1, 2, 1, 4, 2, 0, 'Data/Img/Dog.png', 60, 60)
                        dogs.append(new_dog)
                        new_dog = Dog(self.rect.x, self.rect.y, dog_image, 1, 1, 2, 1, 5, 2, 0, 'Data/Img/Dog.png', 60, 60)
                        dogs.append(new_dog)
                        new_dog = Dog(self.rect.x, self.rect.y, dog4_image, 320, 5000, 1, 30, 6, 1, 0, 'Data/Img/Dog4.png', 60, 60)
                        dogs.append(new_dog)
                    elif self.mega == 11:
                        new_dog = Dog(self.rect.x, self.rect.y, dog2_image, 40, 100, 1, 6, 1, 1, 0, 'Data/Img/Dog2.png', 60, 60)
                        dogs.append(new_dog)
                    if die:
                        money += self.money
                    dogs.remove(self)
                    del self
        except:
            pass
    
    def attack(self, reloade):
        global dogs, cats, dog_damag_boost, scripts
        self.stope = False
        moveE = True
        try:
            for cat2 in list(cats):
                if self.rect.colliderect(cat2.rect):
                    if cat2.follow_mouse == False:
                        moveE = False
                if self.rect.colliderect(cat2.rect):
                    if moveE == False:
                        if cat2.mega == 5:
                            self.bump(self.maxhealth/(100-cat2.damage), True, [])
            for dog2 in list(dogs):
                if self.mega == 14 and dog2.mega != 14 and self.rect.colliderect(dog2.rect):
                    dog2.bump(self.damage+dog_damag_boost, True, [])
                if dog2.mega == 14 and dog2 != self and self.rect.colliderect(dog2.rect):
                    dog2.bump(self.damage+dog_damag_boost, True, [])
                else:
                    if self.mega == 12:
                        for dog3 in list(dogs):
                            if dog3.mega != 12 and dog.mega != 14:
                                distance = ((self.rect.x - dog3.rect.x)**2 + (self.rect.y - dog3.rect.y)**2)**0.5
                                if distance <= 200:
                                    if dog3.maxhealth > dog3.health:
                                        if dog3.maxhealth > dog3.health + self.damage+dog_damag_boost:
                                            dog3.bump(-self.damage-dog_damag_boost, True, [])
                                        else:
                                            dog3.bump(-dog3.maxhealth+dog3.health, True, [])
            if self.mega == 6 and reloade == 3 and self.val3 == 1:
                new_dog = Dog(self.rect.x, self.rect.y, dog3_image, 7, 350, 5, 20, 2, 1, 1, 'Data/Img/Dog3.png', 60, 60)
                dogs.append(new_dog)
                new_dog = Dog(self.rect.x, self.rect.y, dog3_image, 7, 350, 5, 20, 7, 1, 1, 'Data/Img/Dog3.png', 60, 60)
                dogs.append(new_dog)
                new_dog = Dog(self.rect.x, self.rect.y, dog3_image, 7, 350, 5, 20, 8, 1, 1, 'Data/Img/Dog3.png', 60, 60)
                dogs.append(new_dog)
                self.val3 = 2
                self.stope = True
            if self.mega == 3 and reloade == self.reload:
                if self.val2 == True:
                    self.val2 = False
                    new_dog = Dog(self.rect.x, self.rect.y, dog_image, 1, 1, 2, 1, 4, 2, 0, 'Data/Img/Dog1.png', 60, 60)
                else:
                    self.val2 = True
                    new_dog = Dog(self.rect.x, self.rect.y, dog_image, 1, 1, 2, 1, 5, 2, 0, 'Data/Img/Dog1.png', 60, 60)
                dogs.append(new_dog)
                for cat2 in list(cats):
                    if self.rect.colliderect(cat2.rect) and self.mega != 14:
                        if moveE == False:
                            try:
                                dog_bump.play()
                            except:
                                pass
                            cat2.bump(self.damage+dog_damag_boost)
                            self.stope = True
            elif self.mega == 6 and reloade == self.reload:
                for cat2 in list(cats):
                    if self.rect.colliderect(cat2.rect) and self.mega != 14:
                        if moveE == False:
                            if self.val < 3:
                                #self.val += 1
                                new_dog = Dog(self.rect.x, self.rect.y, dog3_image, 7, 300, 5, 20, 7, 1, 1, 'Data/Img/Dog3.png', 60, 60)
                                dogs.append(new_dog)
                                new_dog = Dog(self.rect.x, self.rect.y, dog3_image, 7, 300, 5, 20, 8, 1, 1, 'Data/Img/Dog3.png', 60, 60)
                                dogs.append(new_dog)
                            try:
                                dog_bump.play()
                            except:
                                pass
                            cat2.bump(self.damage+dog_damag_boost)
                            self.stope = True
            elif self.mega == 2 or self.mega == 7 or self.mega == 8:
                boomp = False
                for cat3 in list(cats):
                    if self.rect.colliderect(cat3.rect):
                            if moveE == False:
                                boomp = True
                if boomp == True:
                    for cat2 in list(cats):
                        distance = ((self.rect.x - cat2.rect.x)**2 + (self.rect.y - cat2.rect.y)**2)**0.5
                        if distance <= 200:
                            cat2.bump(self.damage+dog_damag_boost)
                    for dog2 in list(cats):
                        if dog2.mega == 14:
                            distance = ((self.rect.x - cat2.rect.x)**2 + (self.rect.y - cat2.rect.y)**2)**0.5
                            if distance <= 200:
                                dog2.bump(self.damage+dog_damag_boost)
                    try:
                        boom.play()
                    except:
                        pass
                    dogs.remove(self)
                    del self
        except:
            pass
        for script in scripts:
            exec(str(start_script(script, 'attack_dog')))
        moveE = True
        try:
            for cat in list(cats):
                if self.rect.colliderect(cat.rect):
                    if cat.follow_mouse == False:
                        moveE = False
        except:
            pass
        try:
            if self.stope == False and dog2.mega != 14:
                for cat2 in list(cats):
                    if self.rect.colliderect(cat2.rect) and self.mega != 14:
                        if moveE == False:
                            try:
                                dog_bump.play()
                            except:
                                pass
                            cat2.bump(self.damage+dog_damag_boost)
        except:
            pass

loading_text('функций')

def save_best_score(score):
    global scripts
    for script in scripts:
        exec(str(start_script(script, 'save')))
    try:
        with open('Data/Save/best_score.pickle', 'wb') as file:
            pickle.dump(score, file)
        load_best_score()
    except:
        pass

def load_best_score():
    global scripts
    for script in scripts:
        exec(str(start_script(script, 'load')))
    try:
        with open('Data/Save/best_score.pickle', 'rb') as file:
            best_score = pickle.load(file)
    except FileNotFoundError:
        best_score = 0
    return best_score

def spawn_cats(custom_budget = None, xxx = None, yyy = None):
    global scripts, cats, cats_moneys
    for script in scripts:
        exec(str(start_script(script, 'spawn_cats')))
    try:
        while True:
            cat_value = random.choice(list(cats_moneys.keys()))
            cat_values = list(cats_moneys.keys())
            cat_value = random.choice(cat_values)
            spermatozoid2 = False
            fork = False
            all_buy_cats = buy_cats + buy_no_cats
            for cat_value2 in cats_moneys:
                fork = True
                if cat_value2 <= custom_budget:
                    spermatozoid2 = True
                    break
            if spermatozoid2 == False and fork == True or custom_budget <= 0:
                break
            if custom_budget >= cat_value:
                cats_moneys[cat_value].random_buy(xxx, yyy)
                custom_budget -= cat_value
    except:
        pass

def spawn_dogs(custom_budget = None, xxx = None, yyy = None):
    global health, dogs, cats, cat, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing, dog_damag_boost, cat_works_boost, cats_boost, upping, buy_cats, xexe, mx, dogs_class, scripts, mods_count_11d23s2saaa, catown2, pos, cursor_pos, bonus, new_music, event_game, maxMoney, input_text, running, input_active, ctrl_pressed, shift_pressed
    online = 0
    for script in scripts:
        exec(str(start_script(script, 'spawn_dogs')))
    if custom_budget != None:
        old_budget = budget
        budget = custom_budget
    if online != 2:
        new_wey = -1
        if custom_budget == None:
            budget += 5
            budget += round(budget/5)
        remaining_budget =0
        remaining_budget = budget
        for_mega_wave -= 1
        if event_game == 1:
            for_mega_wave = 0
        save_best_score(wave)
        wave += 1
        if plustime < 50 and wave >= 4:
            plustime += 5
        if for_mega_wave == 0:
            remaining_budget = remaining_budget * 2
        if for_mega_wave == -1:
            upping = False
            for_mega_wave = 4
        while remaining_budget > 0:
            dog_type = random.choice(list(dogs_variants.keys()))
            dog_cost = dogs_variants[dog_type]
            dog_mon = dogs_moneys[dog_type]
            dog_class = dogs_class[dog_type]
            if dog_cost <= remaining_budget:
                dog_class.create(xxx, yyy)
                remaining_budget -= dog_cost
        dogs_list_data = []
        for dog in dogs:
            data_dog = {'image_path': dog.path_my_image, 'size_x': dog.size_x, 'size_y': dog.size_y, 'type': dog.typee, 'dog_health': dog.health, 'moneys': dog.money, 'speed': dog.speed, 'reload': dog.reload, 'damage_dog': dog.damage, 'xd': dog.rect.x, 'mega': dog.mega, 'yd': dog.rect.y}
            dogs_list_data.append(data_dog)
        # data_back2[6] = str(dogs_list_data)
        cat_unblock = False
    if custom_budget != None:
        budget = old_budget
    else:
        new_wey -= 1

def show_lose_screen():
    global scripts, input_text, running, input_active, ctrl_pressed, shift_pressed
    for script in scripts:
        exec(str(start_script(script, 'lose_screen')))
    font = pygame.font.Font(None, 70)
    text = font.render("Вы проиграли. Нажмите ПКМ, чтобы начать заново.", True, text_color)
    text_rect = text.get_rect(center=(width/2, height/2))
    screen.fill(background_color)
    screen.blit(text, text_rect)
    pygame.display.flip()
    started = True
    
    while True:
        for event in pygame.event.get():
            CMD_codes(event)
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and started:
                started = False
                menu()
                return
            for script in scripts:
                exec(str(start_script(script, 'lose_event')))
        for script in scripts:
            exec(str(start_script(script, 'lose_ui')))
        text_surface = font.render(input_text, True, text_color)
        screen.blit(text_surface, (10, 10))

def info(text, position):
    global scripts
    for script in scripts:
        exec(str(start_script(script, 'info')))
    text_surface = font2.render(text, True, info_text_color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = position
    
    screen.blit(font2.render(text, True, info_text_outlining_color), (text_rect.x - 2, text_rect.y))
    screen.blit(font2.render(text, True, info_text_outlining_color), (text_rect.x + 2, text_rect.y))
    screen.blit(font2.render(text, True, info_text_outlining_color), (text_rect.x, text_rect.y - 2))
    screen.blit(font2.render(text, True, info_text_outlining_color), (text_rect.x, text_rect.y + 2))
    
    screen.blit(text_surface, text_rect.topleft)

# def loading_online():
    # global client, input_text, running, input_active, ctrl_pressed, shift_pressed
    # running = True
    # port2 = ""
    # fonte = pygame.font.Font(None, 75)
    # clock = pygame.time.Clock()
    # while running:
        # for event in pygame.event.get():
            # if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_RETURN:
                    # running = False
                # elif event.key == pygame.K_BACKSPACE:
                    # port2 = port2[:-1]
                # else:
                    # port2 += event.unicode
    
        # text = fonte.render("Ведите порт сервера: " + port2, True, text_color)
        # text_rect = text.get_rect(center=(width/2, height/2))
        # screen.fill(background_color)
        # screen.blit(text, text_rect)
        # pygame.display.flip()
        # clock.tick(60)
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # i = 0
    # connect = False
    # while True:
        # i += 1
        # try:
            # client.connect((socket.gethostname(), int(port2)))
            # connect = True
            # break
        # except:
            # pass
        # if i == 10:
            # menu_mult()
            # return
    # start(2)

# def menu_mult():
    # global music_playing, port, server_socket, user, adres, input_text, running, input_active, ctrl_pressed, shift_pressed
    # mods_count_11d23s2saaa = 0
    # music_playing = True
    # clock = pygame.time.Clock()
    # running = True
    # while running:
        # host_rect = host_image.get_rect(topleft=(width/2-160, height/2-80))
        # connect_rect = connect_image.get_rect(topleft=(width/2-180, height/2+80-65))
        # back_rect = back_image.get_rect(topleft=(width-145, 20))
        # pos = pygame.mouse.get_pos()
        # for event in pygame.event.get():
            # if event.type == pygame.QUIT:
                # running = False
            # CMD_codes(event)
            # if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_SPACE:
                    # if music_playing:
                        # try:
                            # pygame.mixer.music.pause()
                        # except:
                            # pass
                    # else:
                        # try:
                            # pygame.mixer.music.unpause()
                        # except:
                            # pass
                    # music_playing = not music_playing
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back_rect.collidepoint(pos):
                # menu()
                # return
            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and connect_rect.collidepoint(pos):
                # loading_online()
                # return
            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and host_rect.collidepoint(pos):
                # fonte = pygame.font.Font(None, 75)
                # text = fonte.render("Ожидаем подключение игрока...", True, text_color)
                # text_rect = text.get_rect(center=(width/2, height/2))
                # pygame.display.flip()
                # screen.fill(background_color)
                # screen.blit(text, text_rect)
                # screen.blit(text3, text3_rect)
                # pygame.display.flip()
                # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # server_socket.bind((socket.gethostname(), port))
                # server_socket.listen()
                # user, adres = server_socket.accept()
                # start(1)
                # return
        # fonte = pygame.font.Font(None, 75)
        # text = fonte.render("Выберите действие", True, text_color)
        # text_rect = text.get_rect(center=(width/2, 70))
        # screen.fill(background_color)
        # screen.blit(back_image, back_rect)
        # screen.blit(connect_image, connect_rect)
        # screen.blit(host_image, host_rect)
        # fonte = pygame.font.Font(None, 45)
        # text3 = fonte.render(f"Ваш порт: {port}", True, text_color)
        # text3_rect = (20, height - fonte.get_height() - 10)
        # screen.blit(text, text_rect)
        # screen.blit(text3, text3_rect)
        # text_surface = font.render(input_text, True, text_color)
        # screen.blit(text_surface, (10, 10))
        # pygame.display.flip()
        # clock.tick(60)

def game_info():
    global music_playing, input_text, running, input_active, ctrl_pressed, shift_pressed
    running = True
    clock = pygame.time.Clock()
    for script in scripts:
        exec(str(start_script(script, 'game_info')))
    while running:
        back_rect = back_image.get_rect(topleft=(width-140, 20))
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for script in scripts:
                exec(str(start_script(script, 'game_info_event')))
            CMD_codes(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if music_playing:
                        try:
                            pygame.mixer.music.pause()
                        except:
                            pass
                    else:
                        try:
                            pygame.mixer.music.unpause()
                        except:
                            pass
                    music_playing = not music_playing
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back_rect.collidepoint(pos):
                menu()
                return
        fonte = pygame.font.Font(None, 75)
        fonte2 = pygame.font.Font(None, 65)
        for script in scripts:
            exec(str(start_script(script, 'game_info_ui')))
        text = fonte.render("Играть проще не куда!", True, text_color)
        text2 = fonte2.render("Не дай собакам дойти до правой стороны экрана\nСтавь котов чтобы они помогали отбивать нападения\nПри нажатие ПКМ по коту он продастся за половину его цены\nПри нажатие ЛКМ по собаке ей наносится урон\nЕсть вид собак 'в полёте' их может убить только ПВО\nПри нажатие space выключаеться музыка", True, text_color)
        text_rect = text.get_rect(center=(width/2, 70))
        text2_rect = text2.get_rect(center=(width/2+5, 70+200))
        screen.fill(background_color)
        screen.blit(back_image, back_rect)
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)
        text_surface = font.render(input_text, True, text_color)
        screen.blit(text_surface, (10, 10))
        pygame.display.flip()
        clock.tick(60)

def menu():
    global music_playing, RPC,new_music, event_game, input_text, running, input_active, ctrl_pressed, shift_pressed
    mods_count_11d23s2saaa = 0
    music_playing = True
    best_wawe = load_best_score()
    new_music= False
    event_game=None
    try:
        RPC.update(state=f"Рекорд: {best_wawe}", details=f"Меню", large_image="kotdefense", large_text="Kot Defense", small_text=f"Рекорд: {best_wawe}")
    except:
        pass
    clock = pygame.time.Clock()
    running = True
    for script in scripts:
        exec(str(start_script(script, 'main_menu')))
    while running:
        play_rect = play_image.get_rect(topleft=(width/2-140, height/2-100))
        info_rect = info_image.get_rect(topleft=(width-140, 20))
        mult_rect = play_image.get_rect(topleft=(width-265, height-80))
        play2_rect = play2_image.get_rect(topleft=(width-270, height-90))
        mods_rect = play_image.get_rect(topleft=(20, 10))
        discord_rect = info_image.get_rect(topleft=(width-250, 30))
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for script in scripts:
                exec(str(start_script(script, 'main_menu_event')))
            CMD_codes(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if music_playing:
                        try:
                            pygame.mixer.music.pause()
                        except:
                            pass
                    else:
                        try:
                            pygame.mixer.music.unpause()
                        except:
                            pass
                    music_playing = not music_playing
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and play_rect.collidepoint(pos):
                new_music = True
                start(0)
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and info_rect.collidepoint(pos):
                game_info()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and discord_rect.collidepoint(pos):
                webbrowser.open("https://discord.gg/8bQQShRwH7")
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and play2_rect.collidepoint(pos):
                event_game=1
                new_music = True
                start(0)
                return
            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mult_rect.collidepoint(pos):
                # menu_mult()
                # return
        fonte = pygame.font.Font(None, 75)
        for script in scripts:
            exec(str(start_script(script, 'main_menu_ui')))
        text = fonte.render("Добро пожаловать в Kot Defense", True, text_color)
        fonte = pygame.font.Font(None, 45)
        fonte2 = pygame.font.Font(None, 35)
        text2 = fonte.render(f"Ваш рекорд: {best_wawe}", True, text_color)
        text4 = fonte2.render(f'Ивент "Магический лес"', True, text_color)
        text3 = fonte.render(f"У вас {mods_count_11d23s2saaa} модификаций", True, text_color)
        text_rect = text.get_rect(center=(width/2, 70))
        text2_rect = (20, height - fonte.get_height() - 10)
        text3_rect = (20, height - fonte.get_height() - 43)
        text4_rect = (width-300, height-90)
        screen.fill(background_color)
        screen.blit(play_image, play_rect)
        screen.blit(info_image, info_rect)
        screen.blit(discord_image, discord_rect)
        #screen.blit(mult_image, mult_rect)
        #screen.blit(mods_image, mods_rect)
        screen.blit(play2_image, play2_rect)
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)
        screen.blit(text4, text4_rect)
        text_surface = font.render(input_text, True, text_color)
        screen.blit(text_surface, (10, 10))
        pygame.display.flip()
        clock.tick(60)

def omg(wave2, screen, online):
    global scripts
    for script in scripts:
        exec(str(start_script(script, 'bonus')))
    global budget, dog_damag_boost, money, health, cat_works_boost, cats_boost, cats, dogs, bad_list, good_list, maxMoney, input_text, running, input_active, ctrl_pressed, shift_pressed
    dog_damag_boost = 0
    ggbudget = round(budget/5)

    errors = True
    while errors:
        g3 = random.choice(list(good_list))
        g1 = random.choice(list(good_list))
        g2 = random.choice(list(good_list))
        if g1 == g2 or g1 == g3:
            pass
        elif g3 == g1 or g3 == g2:
            pass
        else:
            errors = False
    errors = True
    while errors:
        b2 = random.choice(list(bad_list))
        b1 = random.choice(list(bad_list))
        b3 = random.choice(list(bad_list))
        if b1 == b2 or b1 == b3:
            pass
        elif b3 == b1 or b3 == b2:
            pass
        else:
            errors = False
    
    starte = True
    loade = True
    clock = pygame.time.Clock()
    timer = 60*3
    for script in scripts:
        exec(str(start_script(script, 'bonus_loade')))
    while loade:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starte = False
                loade= False
            for script in scripts:
                exec(str(start_script(script, 'bonus_loade_event')))
        for script in scripts:
            exec(str(start_script(script, 'bonus_loade_ui')))
        loading_text('бафов и дебафов')
        pygame.display.flip()
        timer -= 1
        if timer <=0:
            loade = False
        clock.tick(60)
    baffe = True
    while starte:
        for script in scripts:
            exec(str(start_script(script, 'bonus_ui')))
        rect1 = pygame.Rect((width/2-150/2)-200, height/2-150/2, 150, 150)
        rect2 = pygame.Rect(width/2-150/2, height/2-150/2, 150, 150)
        rect3 = pygame.Rect((width/2-150/2)+200, height/2-150/2, 150, 150)
        pos = pygame.mouse.get_pos()
        screen.fill(background_color)
        pygame.draw.rect(screen, green_btn_color, (width/2-150/2, height/2-150/2, 150, 150))
        pygame.draw.rect(screen, red_btn_color, ((width/2-150/2)-200, height/2-150/2, 150, 150))
        pygame.draw.rect(screen, blue_btn_color, ((width/2-150/2)+200, height/2-150/2, 150, 150))
        
        font = pygame.font.Font(None, 100)
        if baffe == True:
            text = font.render("Выберите баф", True, text_color)
        else:
            text = font.render("Выберите дебаф", True, text_color)
        text_rect = text.get_rect(center=(width/2, 130))
        screen.blit(text, text_rect)
        for event in pygame.event.get():
            CMD_codes(event)
            if event.type == pygame.QUIT:
                starte = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for script in scripts:
                    exec(str(start_script(script, 'bonus_event')))
                if rect1.collidepoint(pos):
                    b = b1
                    g = g1
                if rect2.collidepoint(pos):
                    b = b2
                    g = g2
                if rect3.collidepoint(pos):
                    b = b3
                    g = g3
                if rect1.collidepoint(pos) or rect2.collidepoint(pos) or rect3.collidepoint(pos):
                    if baffe == False:
                        if b == 'собаки наносят больше урона':
                            dog_damag_boost += 1
                        elif b == 'игра станет сложнее':
                            budget += ggbudget
                        elif b == 'некоторым котам на поле боя нанесут 10 урона':
                            for cat in cats:
                                cat.bump(10)
                        elif b == f'-Максимальное число денег которое у вас было':
                            money -= maxMoney
                        elif b == f'превращает 10% котов в лягушек':
                            zzzcats = int(len(cats) * 0.2)
                            random_cats = random.sample(cats, zzzcats)
                            for cat2 in random_cats:
                                cat2.cwa()
                        game(online)
                        return
                    else:
                        if g == f'+Максимальное число денег которое у вас было':
                            money += maxMoney
                        elif g == '+1 главных сердец':
                            health += 1
                        elif g == '+30 жизней некоторым котам на поле боя':
                            for cat in cats:
                                cat.bump(-30)
                        elif g == 'Игра станет легче':
                            if budget - ggbudget >1:
                                budget -= ggbudget
                            else:
                                budget = 1
                        elif g == 'Коты работники дают на 5$ больше':
                            cat_works_boost += 1
                        elif g == 'Коты наносят больше урона':
                            cats_boost += 1
                        elif g == 'Магический щит, защищает котов от вражеских заклинаний':
                            shild = Cat(shild_image, 0, 2000, 0, 5000, 0, 0, 0, "Data\Img\cat_shield.png", 60, 60)
                            shild.rect.x = random.randint(0, width-60)
                            shild.rect.y = random.randint(115, height - 255)
                            shild.follow_mouse = False
                            cats.append(shild)
                        baffe = False
        if baffe == True:
            if rect1.collidepoint(pos):
                info(g1, (pos[0] + 15, pos[1] + 5))
            if rect2.collidepoint(pos):
                info(g2, (pos[0] + 15, pos[1] + 5))
            if rect3.collidepoint(pos):
                info(g3, (pos[0] + 15, pos[1] + 5))
        else:
            if rect1.collidepoint(pos):
                info(b1, (pos[0] + 15, pos[1] + 5))
            if rect2.collidepoint(pos):
                info(b2, (pos[0] + 15, pos[1] + 5))
            if rect3.collidepoint(pos):
                info(b3, (pos[0] + 15, pos[1] + 5))
        text_surface = font.render(input_text, True, text_color)
        screen.blit(text_surface, (10, 10))
        pygame.display.flip()

def new_cat_unblock():
    global buy_cats, xexe, mx, input_text, running, input_active, ctrl_pressed, shift_pressed
    for script in scripts:
        exec(str(start_script(script, 'new_cat_unblock')))
    buy_cats = sorted(buy_cats, key=lambda x: x.money)
    xexe = 100
    if len(buy_cats) <= 14:
        xexe = 20
    for bc in buy_cats:
        if xexe >= 1140:
            mx = 1140
            bc.rect.x = xexe
        else:
            bc.rect.x = xexe
        xexe += 80
    if len(buy_cats) <= 14:
        xexe = -3000

#старт игры
def start(online):
    loading_text('игры')
    global health, dogs, cats, cat, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing, dog_damag_boost, cat_works_boost, cats_boost, upping, buy_cats, xexe, mx, dogs_class, dangerous_keywords_pp2irooodjhjjjkjkn, scripts, bad_list, good_list, catown2, bonus, new_music, buy_no_cats, event_game, maxMoney, cat_unblock, cats_moneys
    for script in scripts:
        exec(str(start_script(script, 'start')))
    del_cat = False
    money = 30
    maxMoney = 0
    health = 10
    mx = 0
    catown = None
    catown2 = None
    dogs = []
    cats = []
    buy_cats=[]
    buy_no_cats = []
    dog_damag_boost = 0
    cat_works_boost = 0
    cats_boost = 0
    dogs_class = {}
    dogs_variants = {}
    dogs_moneys = {}
    cats_moneys = {}
    scripts = []
    bad_list = []
    good_list = []
    budget = 4
    if event_game == 1:
        budget = 10
        money = 120
    upping = False
    pause = False
    
    frame_count = 0
    frame_count2 = 0
    frame_count3 = 0
    frame_count4 = 0
    plustime = 0
    new_wey = 60*10
    wave = 1
    bonus = False
    for_mega_wave = 4
    
    new_dog = CreateDog(3, 1, 'Dog', dog_image, 2, 2, 1, 1, 1, 0, 'Data/Img/Dog1.png', 60, 60)
    new_dog = CreateDog(7, 5, 'FastDog', dog_image, 1, 4, 1, 1, 1, 0, 'Data/Img/Dog1.png', 60, 60)
    new_dog = CreateDog(7, 5, 'BigDog', dog_image, 6, 1, 1, 1, 1, 0, 'Data/Img/Dog1.png', 60, 60)
    new_dog = CreateDog(20, 10, 'KillerDog', dog_image, 4, 3, 4, 1, 1, 0, 'Data/Img/Dog1.png', 60, 60)
    new_dog = CreateDog(100, 65, 'KiberDog', dog2_image, 40, 1, 6, 1, 1, 0, 'Data/Img/Dog2.png', 60, 60)
    new_dog = CreateDog(300, 220, 'BoomDog', dog3_image, 50, 5, 20, 2, 1, 1, 'Data/Img/Dog3.png', 60, 60)
    new_dog = CreateDog(100, 50, 'NecDog', dog_image, 15, 1, 2, 3, 2, 0, 'Data/Img/Dog1.png', 60, 60)
    new_dog = CreateDog(5000, 1500, 'MehoDog', dog4_image, 320, 1, 30, 6, 1, 0, 'Data/Img/Dog4.png', 60, 60)
    new_dog = CreateDog(1000, 1500, 'BomberDog', dog5_image, 400, 2, 100, 9, 1, 2, 'Data/Img/Dog5.png', 60, 60)
    new_dog.damagecats.append(1)
    new_dog.damagecats.append(2)
    new_dog = CreateDog(10000, 8400, 'TrojanDog', dog6_image, 1000, 1, 0, 10, 1, 0, 'Data/Img/Dog6.png', 60, 60) 
    new_dog = CreateDog(10, 100, 'GostDog', dog7_image, 10, 2, 2, 9, 1, 0, 'Data/Img/Dog7.png', 60, 60)
    new_dog = CreateDog(30, 300, 'Woolf', dog_image, 20, 2, 4, 11, 1, 0, 'Data/Img/Dog1.png', 60, 60)
    new_dog = CreateDog(600, 1000, 'MedicDog', dog2_image, 100, 1, 1, 12, 1, 0, 'Data/Img/Dog2.png', 60, 60)
    new_buy_cat = BuyCat(cat_image, 10, f'4 жизни, атакует 2 собаки за раз, средняя перезарядка, {1+cats_boost} урон', cat_image, 130, 4, 3, 1, 1, 1, 0, 10, 'Data/Img/Cat1.png', 60, 60)
    new_buy_cat = BuyCat(cat2_image, 20, "40 жизни, не атакует собак", cat2_image, 0, 40, 0, 1, 0, 1, 0, 45, 'Data/Img/Cat2.png', 60, 60)
    new_buy_cat = BuyCat(cat3_image, 200, f'6 жизней, атакует 3 собаки за раз, долгая перезарядка, {10+cats_boost} урон', cat3_image, 400, 6, 3, 2, 10, 1, 20, -1, 'Data/Img/Cat3.png', 60, 60)
    new_buy_cat = BuyCat(cat4_image, 80, f'20 жизнь, атакует 3 собаки за раз, быстрая перезарядка, {1.5+cats_boost} урон', cat4_image, 150, 20, 3, 3, 1.5, 1, 10, -1, 'Data/Img/Cat4.png', 60, 60)
    new_buy_cat = BuyCat(cat5_image, 70, f'15 жизней, не атакует собак, но зар  абатывает {10+cat_works_boost}$ каждую волну', cat5_image, 0, 15, 0, 4, 10, 2, 5, -1, 'Data/Img/Cat5.png', 60, 60)
    new_buy_cat = BuyCat(cat6_image, 10000, f'80 жизней, не атакует собак, усиливает\nатаку курсором игрока', cat6_image, 0, 80, 0, 1, 0.1, 3, 30, -1, 'Data/Img/Cat6.png', 60, 60)
    new_buy_cat = BuyCat(cat7_image, 300, f'60 жизней, не атакует собак, лечит котов в его радиусе', cat7_image, 160, 60, 9999, 2, 0.3, 4, 25, -1, 'Data/Img/Cat7.png', 60, 60)
    new_buy_cat = BuyCat(cat8_image, 600, f'60 жизней, атакует 1 собаки за раз, быстрая перезарядка, \nбьёт только взрывучих или в полёте собак, {150+cats_boost} урон', cat8_image, 300, 60, 1, 3, 150, 1, 15, -1, 'Data/Img/Cat8.png', 120, 60)
    new_buy_cat.blacklist.append(1)
    new_buy_cat.blacklist.append(2)
    new_buy_cat = BuyCat(cat9_ico_image, 500, f'30 жизней, атакует 1 собаки за раз, долгая перезарядка, {100+cats_boost} урон', cat9_image, 500, 30, 1, 2, 100, 1, 40, -1, 'Data/Img/Cat9.png', 60, 60)
    new_buy_cat = BuyCat(cat10_image, 60000, "1000 жизней, собака получает 5%\nурона при нападение на кота", cat10_image, 0, 1000, 0, 1, 5, 5, 45, -1, 'Data/Img/Cat10.png', 60, 60)
    new_buy_cat = BuyCat(cat11_image, 600, f'80 жизней, не атакует собак, лечит котов в его радиусе', cat11_image, 200, 80, 9999, 1, 0.3, 4, 35, -1, 'Data/Img/Cat11.png', 60, 60)
    new_buy_cat = BuyCat(cat12_image, 50, f'1 жизнь, атакует 1 собаки за раз, быстрая перезарядка,\nпри получения урона собака получает урон 50% от своего хп', cat12_image, 0, 1, 1, 3, 98, 5, 5, -1, 'Data/Img/Cat12.png', 60, 60)
    new_buy_cat = BuyCat(cat13_image, 1000, f'20 жизней, атакует 6 собаки за раз,\nдолгая перезарядка, {3+cats_boost} урон', cat13_image, 500, 20, 6, 2, 3, 1, 45, -1, 'Data/Img/Cat13.png', 60, 60)
    new_buy_cat = BuyCat(cat14_image, 100, f'1 жизня, каждую волну спавнит жабу', cat14_image, 0, 1, 1, 4, 98, 6, 25, -1, 'Data/Img/Cat14.png', 60, 60)
    new_buy_cat = BuyCat(cat15_image, 300, f'1 жизня, каждую волну спавнит добрую собаку', cat15_image, 0, 1, 1, 4, 98, 7, 40, -1, 'Data/Img/Cat15.png', 60, 60)

    bad_list.extend(['собаки наносят больше урона', 'игра станет сложнее', 'некоторым котам на поле боя нанесут 10 урона', f'-Максимальное число денег которое у вас было', 'превращает 20% котов в лягушек'])
    good_list.extend([f'+Максимальное число денег которое у вас было', '+1 главных сердец', '+30 жизней некоторым котам на поле боя', 'Игра станет легче', 'Коты работники дают на 5$ больше', 'Коты наносят больше урона', 'Магический щит, защищает котов от вражеских заклинаний'])
    folder_path = 'Data\\Mods\\'
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name == 'main.py':
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    code = file.read()
                    dangerous = False
                    for keyword in dangerous_keywords_pp2irooodjhjjjkjkn:
                        if keyword in code:
                            dangerous = True
                            break
                    if dangerous == True:
                        pass
                    else:
                        try:
                            exec(code)
                        except Exception as e:
                            print(f"An error occurred: {e}")
            pygame.time.delay(50)
        pygame.time.delay(50)
    
    new_cat_unblock()
    
    
    game(online)
    return

def win(online):
    global music_playing, event_game, input_text, running, input_active, ctrl_pressed, shift_pressed
    running = True
    loade = True
    clock = pygame.time.Clock()
    timer = 60*2
    mywincode = int(time.time())
    for script in scripts:
        exec(str(start_script(script, 'win')))
    while loade:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                loade= False
        loading_text('текста')
        pygame.display.flip()
        timer -= 1
        if timer <=0:
            loade = False
        clock.tick(60)
    
    while running:
        back_rect = back_image.get_rect(topleft=(width-140, 20))
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for script in scripts:
                exec(str(start_script(script, 'win_event')))
            CMD_codes(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if music_playing:
                        try:
                            pygame.mixer.music.pause()
                        except:
                            pass
                    else:
                        try:
                            pygame.mixer.music.unpause()
                        except:
                            pass
                    music_playing = not music_playing
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if event_game == 1:
                    menu()
                else:
                    game(online)
                return
        fonte = pygame.font.Font(None, 60)
        for script in scripts:
            exec(str(start_script(script, 'win_event')))
        if event_game == 1:
            text = fonte.render(f"Поздравляю ! Вы прошли ивент, отправьте скришот этого экрана\nв тех поддержку чтобы получить бонус ваш код: {mywincode}\nНажмите ПКМ чтобы выйти", True, text_color)
        else:
            text = fonte.render("Поздравляю ! Вы официально прошли игру.\nДальше будет бесконечная игра\nНажмите ПКМ чтобы продолжить играть", True, text_color)
        text_rect = text.get_rect(center=(width/2, height/2))
        screen.fill(background_color)
        screen.blit(text, text_rect)
        text_surface = font.render(input_text, True, text_color)
        screen.blit(text_surface, (10, 10))
        pygame.display.flip()
        clock.tick(60)

def game(online):
    global health, dogs, cats, cat, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing, dog_damag_boost, cat_works_boost, cats_boost, upping, buy_cats, xexe, mx, dogs_class, scripts, mods_count_11d23s2saaa, catown2, pos, cursor_pos, bonus, new_music, event_game, maxMoney, input_text, running, input_active, ctrl_pressed, shift_pressed, stop_game, pos
    running = True
    bonus = False
    clock = pygame.time.Clock()
    cursor_pos = (0,0)
    down = False
    up = False
    left_or_right = False
    data_back = [(0, 0), False, False, False]
    data_back2 = [(0, 0), 30, 10, 1, 4, [], []]
    boss_time = 0
    cat_unblock = False
    for script in scripts:
        exec(str(start_script(script, 'game')))
    if new_music == True:
        try:
            if event_game == 1:
                pygame.mixer.music.load(event1_music)
            else:
                pygame.mixer.music.load(music_path)
            if music_playing:
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
            else:
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.pause()
            new_music = False
        except:
            pass
    if online == 1:
        try:
            data_back2[0] = pos_new
            data_back2[1] = money
            data_back2[2] = health
            data_back2[3] = wave
            data_back2[4] = for_mega_wave
            data_back2[5] = []
            user.send(data_back2.encode('utf-8'))
            
            screen.blit(cursor_img, cursor_pos)
            
        except Exception as e:
            pass
            
    elif online == 2:
        try:
            data_back = json.dumps(data_back)
            client.send(data_back.encode('utf-8'))
            
            screen.blit(cursor_img, cursor_pos)
            
        except Exception as e:
            pass
    while running:
        data_back = [(0, 0), False, False, False]
        data_back2 = [(0, 0), 30, 10, 1, 4, [], []]
        del_cat = False
        pause_rect = pause_image.get_rect(topleft=(width-55, 10))
        skip_rect = pygame.Rect(width-120, height-118, 100, 100)
        btn_rect = pygame.Rect(20, height-90, 60, 60)
        btn2_rect = pygame.Rect(1140, height-90, 60, 60)
        pos = pygame.mouse.get_pos()
        # data2 = [0,0,0,0,0,"[{'image_path': 'Data/Img/Cat1.png', 'size_x': 60, 'size_y': 60, 'aura_radius': 130, 'cat_health': 4, 'dogs_count': 3, 'cat_money': 10, 'reload': 1, 'damage_cat': 1, 'xc': 232, 'unable_to_place': True, 'follow_mouse': False, 'mega': 1, 'yc': 411}]"]
        # if online == 1:
            # try:
                # data = user.recv(20971520).decode('utf-8')
                # data = json.loads(data)
                
                # cursor_pos = tuple(data[0])
                # down = data[1]
                # up = data[2]
                # left_or_right = data[3]
                
            # except Exception as e:
                # pass
                
        # elif online == 2 and not bonus:
            # try:
                # data2 = client.recv(20971520).decode('utf-8')
                # data2 = json.loads(data2)
                # cursor_pos = tuple(eval(data2[0]))
                # money = int(data2[1])
                # health = int(data2[2])
                # wave = int(data2[3])
                # for_mega_wave = int(data2[4])
                
                # for cat in cats:
                    # cat.sell(0)
                # cats = []
                # data2[5] = eval(data2[5])
                # data2[6] = eval(data2[6])
                # if data2[6] != []:
                    # for dog in dogs:
                        # dog.bump(dog.health, False, [])
                    # for dog_data in data2[6]:
                        # image_path = dog_data['image_path']
                        # dog_image = pygame.image.load(image_path)
                        # dog_image = pygame.transform.scale(dog_image, (dog_data['size_x'], dog_data['size_y']))
                        # dog = Dog(dog_data['xd'], dog_data['yd'], dog_image, dog_data['dog_health'], dog_data['moneys'], dog_data['speed'], dog_data['damage_dog'], dog_data['mega'], dog_data['reload'], dog_data['type'], image_path, dog_data['size_x'], dog_data['size_y'])
                        # dogs.append(dog)
                
                # for cat_data in data2[5]:
                    # image_path = cat_data['image_path']
                    # try:
                        # cat_image = pygame.image.load(image_path)
                        # cat_image = pygame.transform.scale(cat_image, (cat_data['size_x'], cat_data['size_y']))
                        # cat = Cat(cat_image, cat_data['aura_radius'], cat_data['cat_health'], cat_data['dogs_count'], cat_data['cat_money'], cat_data['reload'], cat_data['damage_cat'], cat_data['mega'], image_path, cat_data['size_x'], cat_data['size_y'])
                        # cat.unable_to_place = cat_data['unable_to_place']
                        # cat.follow_mouse = cat_data['follow_mouse']
                        # cat.rect.x = cat_data['xc']
                        # cat.rect.y = cat_data['yc']
                        # cats.append(cat)
                    # except pygame.error:
                        # cat_image = pygame.image.load('error_img.png')
                        # cat_image = pygame.transform.scale(cat_image, (cat_data['size_x'], cat_data['size_y']))
                        # cat = Cat(cat_image, cat_data['aura_radius'], cat_data['cat_health'], cat_data['dogs_count'], cat_data['cat_money'], cat_data['reload'], cat_data['damage_cat'], cat_data['mega'], image_path, cat_data['size_x'], cat_data['size_y'])
                        # cat.unable_to_place = cat_data['unable_to_place']
                        # cat.follow_mouse = cat_data['follow_mouse']
                        # cat.rect.x = cat_data['xc']
                        # cat.rect.y = cat_data['yc']
                        # cats.append(cat)
                
            # except Exception as e:
                # pass
        # if online != 0:
            # pos_new = json.dumps(pos) 
        # if online == 2:
            # data_back[0] = pos
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            CMD_codes(event)
            for script in scripts:
                exec(str(start_script(script, 'game_event')))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if music_playing:
                        try:
                            pygame.mixer.music.pause()
                        except:
                            pass
                    else:
                        try:
                            pygame.mixer.music.unpause()
                        except:
                            pass
                    music_playing = not music_playing
            if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                if btn2_rect.collidepoint(pos) and xexe > 0 and mx<xexe:
                    try:
                        click.play()
                    except:
                        pass
                    mx += 80
                    for bc in buy_cats:
                        bc.move(-80)
                elif btn_rect.collidepoint(pos) and xexe > 0 and mx> 1140:
                    try:
                        click.play()
                    except:
                        pass
                    mx -= 80
                    for bc in buy_cats:
                        bc.move(80)
            # if online == 2:
                # if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                    # data_back[1] = True
                    # if event.button == 1:
                        # data_back[3] = False
                    # elif event.button == 3:
                        # data_back[3] = True
                # elif event.type == pygame.MOUSEBUTTONUP and not pause:
                    # data_back[2] = True
                    # if event.button == 1:
                        # data_back[3] = False
                    # elif event.button == 3:
                        # data_back[3] = True
            # else:
            if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                if pygame.mouse.get_pressed()[0] and event.button == 1:
                    for dog in list(dogs):
                        if dog.rect.collidepoint(pos):
                            try:
                                dog_bump.play()
                            except:
                                pass
                            damage_combo = 0.1
                            for cat in cats:
                                if cat.mega == 3:
                                    damage_combo += cat.damage
                            dog.bump(damage_combo, True, [])
                for cat in cats:
                    if pygame.mouse.get_pressed()[2] and cat.rect.collidepoint(pos):
                        if cat.follow_mouse == False:
                            cat.sell(0.5)
                if pygame.mouse.get_pressed()[0] and catown is not None:
                    catown.handle_mouse_click(pos, 1)
                if skip_rect.collidepoint(pos) and len(dogs) == 0:
                    if wave != 50:
                        if event_game == 1:
                            if wave != 30:
                                new_wey = 0
                        else:
                            new_wey = 0
                if del_cat == False:
                    for bc in buy_cats:
                        bc.buy(pos, 1)
                if pause_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and online == 0:
                    pause = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and pause:
                pause = False
        
        if not pause:
            if maxMoney < money:
                maxMoney = money
            if event_game == 1:
                screen.fill(event1_background_color)
            else:
                if wave == 50:
                    screen.fill(boss_background_color)
                else:
                    screen.fill(background_color)
            
            # if online == 1:
                # if down == True:
                    # if left_or_right == False:
                        # for dog in list(dogs):
                            # if dog.rect.collidepoint(cursor_pos):
                                # try:
                                    # dog_bump.play()
                                # except:
                                    # pass
                                # damage_combo = 0.1
                                # for cat in cats:
                                    # if cat.mega == 3:
                                        # damage_combo += cat.damage
                                # dog.bump(damage_combo, True, [])
                    # for cat in cats:
                        # if left_or_right == True and cat.rect.collidepoint(cursor_pos):
                            # cat.sell(0.5)
                    # if left_or_right == False and catown2 is not None:
                        # catown2.handle_mouse_click(pos, 2)
                    # if skip_rect.collidepoint(cursor_pos) and len(dogs) == 0:
                        # new_wey = 0
                    # if del_cat == False:
                        # for bc in buy_cats:
                            # bc.buy(cursor_pos, 2)
            if stop_game == False:
                for dog in list(dogs):
                    dog.move()
                    if dog.rect.x > width+60:
                        money += 100
                        health -= 1
                        dogs.remove(dog)
                        del dog
                    elif dog.mega == 14 and dog.rect.x < -60:
                        dogs.remove(dog)
                        del dog
            
            if event_game == 1:
                pygame.draw.rect(screen, event1_down_menu_cats, (0, height-135, 1400, 135))
            else:
                pygame.draw.rect(screen, down_menu_cats, (0, height-135, 1400, 135))
            pygame.draw.rect(screen, skip_button_color, (width-120, height-118, 100, 100))
            cat_mon3 = font.render("Skip", True, text_color)
            screen.blit(cat_mon3, (width-101, height-96))
            
            if online == 0:
                screen.blit(pause_image, (width-55, 10))
            
            if stop_game == False:
                frame_count += 1
                frame_count2 += 1
                frame_count3 += 1
                frame_count4 += 1
            if wave == 50:
                boss_time += 1
            elif event_game == 1 and wave == 30 and stop_game == False:
                boss_time += 1
            
            if frame_count >= 60:
                try:
                    if for_mega_wave >0:
                        RPC.update(state=f"{money} 💵 {health} ❤", details=f"Волна {wave}", large_image="kotdefense", large_text="Kot Defense", small_text=f"{money} 💵 {health} ❤")
                    else:
                        RPC.update(state=f"{money} 💵 {health} ❤", details=f"Мега волна {wave}", large_image="kotdefense", large_text="Kot Defense", small_text=f"{money} 💵 {health} ❤")
                except:
                    pass
                for cat in cats:
                    cat.remove_dogs_periodically(1)
                for dog in list(dogs):
                    dog.attack(1)
                frame_count = 0
            if frame_count3 >= 60*3:
                for cat in cats:
                    cat.remove_dogs_periodically(2)
                for dog in list(dogs):
                    dog.attack(2)
                frame_count3 = 0
            if frame_count4 >= 30:
                for cat in cats:
                    cat.remove_dogs_periodically(3)
                for dog in list(dogs):
                    dog.attack(3)
                frame_count4 = 0
            if len(dogs) == 0 and cat_unblock == False:
                cat_unblock = True
                for bc in list(buy_no_cats):
                    bc.spawn()
                for bc in list(buy_cats):
                    bc.spawn()
            if stop_game == False:
                if boss_time == 0:
                    if wave == 49 and len(dogs) == 0:
                        wave += 1
                    if len(dogs) == 0 and wave != 50:
                        if new_wey < 0 and online != 2:
                            new_wey = 60 * (10+plustime)
                        elif new_wey == 0:
                            for cat in cats:
                                cat.remove_dogs_periodically(4)
                            for dog in list(dogs):
                                dog.attack(4)
                            spawn_dogs()
                else:
                    if new_music == False:
                        try:
                            if event_game == 1:
                                pygame.mixer.music.load(event1_music)
                            else:
                                pygame.mixer.music.load(music_path)
                            if music_playing:
                                pygame.mixer.music.play(-1)
                                pygame.mixer.music.set_volume(0.1)
                            else:
                                pygame.mixer.music.play(-1)
                                pygame.mixer.music.set_volume(0.1)
                                pygame.mixer.music.pause()
                            new_music = False
                        except:
                            pass
                    if boss_time == 20*60:
                        xb = -60
                        yb = 0
                        while yb < height-255:
                            yb +=120
                            dog_class = dogs_class['TrojanDog']
                            dog_class.create(xb, yb+random.randint(-100, 100) / 10)
                        # dogs_list_data = []
                        # for dog in dogs:
                            # data_dog = {'image_path': dog.path_my_image, 'size_x': dog.size_x, 'size_y': dog.size_y, 'type': dog.typee, 'dog_health': dog.health, 'moneys': dog.money, 'speed': dog.speed, 'reload': dog.reload, 'damage_dog': dog.damage, 'xd': dog.rect.x, 'mega': dog.mega, 'yd': dog.rect.y}
                            # dogs_list_data.append(data_dog)
                        # data_back2[6] = str(dogs_list_data)
                    elif boss_time == 40*60:
                        xb = -60
                        yb = 55
                        while yb < height-255:
                            xb -= 30
                            yb +=60
                            dog_class = dogs_class['BomberDog']
                            dog_class.create(xb, yb)
                        # dogs_list_data = []
                        # for dog in dogs:
                            # data_dog = {'image_path': dog.path_my_image, 'size_x': dog.size_x, 'size_y': dog.size_y, 'type': dog.typee, 'dog_health': dog.health, 'moneys': dog.money, 'speed': dog.speed, 'reload': dog.reload, 'damage_dog': dog.damage, 'xd': dog.rect.x, 'mega': dog.mega, 'yd': dog.rect.y}
                            # dogs_list_data.append(data_dog)
                        # data_back2[6] = str(dogs_list_data)
                    elif boss_time == 50*60:
                        xb = -60
                        yb = 0
                        while yb < height-255:
                            yb +=120
                            dog_class = dogs_class['TrojanDog']
                            dog_class.create(xb, yb+random.randint(-100, 100) / 10)
                        # dogs_list_data = []
                        # for dog in dogs:
                            # data_dog = {'image_path': dog.path_my_image, 'size_x': dog.size_x, 'size_y': dog.size_y, 'type': dog.typee, 'dog_health': dog.health, 'moneys': dog.money, 'speed': dog.speed, 'reload': dog.reload, 'damage_dog': dog.damage, 'xd': dog.rect.x, 'mega': dog.mega, 'yd': dog.rect.y}
                            # dogs_list_data.append(data_dog)
                        # data_back2[6] = str(dogs_list_data)
                    elif boss_time == 60*60:
                        xb = -60
                        yb = 55
                        for i in range(2):
                            xb = (i+1) * -120
                            yb = 55
                            while yb < height-255:
                                yb +=60
                                dog_class = dogs_class['KiberDog']
                                dog_class.create(xb+random.randint(-100, 100) / 10, yb+random.randint(-100, 100) / 10)
                        # dogs_list_data = []
                        # for dog in dogs:
                            # data_dog = {'image_path': dog.path_my_image, 'size_x': dog.size_x, 'size_y': dog.size_y, 'type': dog.typee, 'dog_health': dog.health, 'moneys': dog.money, 'speed': dog.speed, 'reload': dog.reload, 'damage_dog': dog.damage, 'xd': dog.rect.x, 'mega': dog.mega, 'yd': dog.rect.y}
                            # dogs_list_data.append(data_dog)
                        # data_back2[6] = str(dogs_list_data)
                    elif boss_time == 90*60:
                        xb = -60
                        yb = 55
                        for i in range(4):
                            xb = (i+1) * -70
                            yb = 55
                            while yb < height-255:
                                yb +=60
                                dog_class = dogs_class['BoomDog']
                                dog_class.create(xb+random.randint(-100, 100) / 10, yb+random.randint(-100, 100) / 10)
                        xb = -350
                        yb = 55
                        yb2 = 595
                        while yb < height-255:
                            xb -= 30
                            yb +=60
                            yb2 -=60
                            dog_class = dogs_class['BomberDog']
                            dog_class.create(xb, yb)
                            dog_class = dogs_class['BomberDog']
                            dog_class.create(xb, yb2)
                            # dogs_list_data = []
                            # for dog in dogs:
                                # data_dog = {'image_path': dog.path_my_image, 'size_x': dog.size_x, 'size_y': dog.size_y, 'type': dog.typee, 'dog_health': dog.health, 'moneys': dog.money, 'speed': dog.speed, 'reload': dog.reload, 'damage_dog': dog.damage, 'xd': dog.rect.x, 'mega': dog.mega, 'yd': dog.rect.y}
                                # dogs_list_data.append(data_dog)
                            # data_back2[6] = str(dogs_list_data)
                    elif boss_time == 110 *60:
                        spawn_dogs(30000)
                    elif boss_time == 140*60:
                        xb = -60
                        yb = 55
                        for i in range(4):
                            xb = (i+1) * -70
                            yb = 55
                            while yb < height-255:
                                yb +=60
                                dog_class = dogs_class['BoomDog']
                                dog_class.create(xb+random.randint(-100, 100) / 10, yb+random.randint(-100, 100) / 10)
                        xb = -350
                        yb = 55
                        yb2 = 595
                        while yb < height-255:
                            xb -= 30
                            yb +=60
                            yb2 -=60
                            dog_class = dogs_class['BomberDog']
                            dog_class.create(xb, yb)
                            dog_class = dogs_class['BomberDog']
                            dog_class.create(xb, yb2)
                    elif boss_time >= 150*60 and len(dogs) == 0:
                        wave += 1
                        if online == 0:
                            win(online)
                            return
            
            for cat in cats:
                cat.draw(screen, online)
                if online == 2:
                    cat.update(pos)
                # elif cat.dds == 1:
                    # cat.update(pos)
                else:
                    cat.update(pos)
            for dog2 in dogs:
                dog2.update()
                
            for bc in buy_cats:
                bc.draw()
            if xexe >0:
                screen.blit(btn2_image, (20, height-90))
                screen.blit(btn_image, (1140, height-90))
            for bc in buy_cats:
                bc.info_cat(pos)
            # if online == 1:
                # for bc in buy_cats:
                    # bc.info_cat(cursor_pos)
            
            for script in scripts:
                exec(str(start_script(script, 'game_game')))
                
            health_text = font.render("❤️ "+str(health), True, text_color)
            screen.blit(health_text, (10, 10))
            heart_text2 = font.render("❤️", True, heart_color)
            screen.blit(heart_text2, (10, 10))
            
            money_text = font.render("💵 "+str(money), True, text_color)
            screen.blit(money_text, (10, 45))
            money_text2 = font.render("💵", True, money_color)
            screen.blit(money_text2, (10, 45))
            text_surface = font.render(input_text, True, text_color)
            screen.blit(text_surface, (10, 10))
            
            for cat in cats:
                cat.info_ca(screen, pos)
            for dog in dogs:
                dog.info_do(pos)
            # if online != 0:
                # for cat in cats:
                    # cat.info_ca(screen, cursor_pos)
                # for dog in dogs:
                    # dog.info_do(cursor_pos)
            if for_mega_wave >0:
                wave_text = font.render("Wave: "+str(wave), True, text_color)
                screen.blit(wave_text, (10, 80))
            else:
                wave_text = font.render("Mega wave: "+str(wave), True, text_color)
                screen.blit(wave_text, (10, 80))
                if upping == False and len(dogs) == 0 and online == 0 and event_game != 1 and stop_game == False:
                    bonus = True
                    upping = True
                    for cat in cats:
                        cat.remove_dogs_periodically(5)
                    for dog in list(dogs):
                        dog.attack(5)
                    omg(wave, screen, online)
                    return
            for script in scripts:
                exec(str(start_script(script, 'game_ui')))
            
            # if online == 1:
                # try:
                    # data_back2[0] = pos_new
                    # data_back2[1] = money
                    # data_back2[2] = health
                    # data_back2[3] = wave
                    # data_back2[4] = for_mega_wave
                    # cats_list_data = []
                    # for cat in cats:
                        # data_cat = {'image_path': cat.path_my_image, 'size_x': cat.size_x, 'size_y': cat.size_y, 'aura_radius': cat.aura_radius, 'cat_health': cat.health, 'dogs_count': cat.dogs_count, 'cat_money': cat.money, 'reload': cat.reload, 'damage_cat': cat.damage, 'xc': cat.rect.x, 'unable_to_place': cat.unable_to_place, 'follow_mouse': cat.follow_mouse, 'mega': cat.mega, 'yc': cat.rect.y}
                        # cats_list_data.append(data_cat)
                    # data_back2[5] = str(cats_list_data)
                    
                    # data_back2 = json.dumps(data_back2)
                    
                    # user.send(data_back2.encode('utf-8'))
                    
                    # screen.blit(cursor_img, cursor_pos)
                    
                # except Exception as e:
                    # pass
                    
            # elif online == 2:
                # try:
                    # data_back = json.dumps(data_back)
                    # client.send(data_back.encode('utf-8'))
                    
                    # screen.blit(cursor_img, cursor_pos)
                    
                # except Exception as e:
                    # pass
            
        # elif bonus:
            # for script in scripts:
                # exec(str(start_script(script, 'game_pause')))
            # fonte = pygame.font.Font(None, 75)
            # text = fonte.render("Ваш напарник выберает бонус, подождите...", True, text_color)
            # text_rect = text.get_rect(center=(width/2, height/2))
            # screen.fill(background_color)
            # screen.blit(text, text_rect)
            # pygame.display.flip()
        else:
            for script in scripts:
                exec(str(start_script(script, 'game_pause')))
            fonte = pygame.font.Font(None, 75)
            text = fonte.render("Пауза. Нажмите ПКМ, чтобы снять с паузы", True, text_color)
            text_rect = text.get_rect(center=(width/2, height/2))
            screen.fill(background_color)
            screen.blit(text, text_rect)
            pygame.display.flip()
            started = True
        pygame.display.flip()
        clock.tick(60)
        if health <=0:
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
            except:
                pass
            for script in scripts:
                exec(str(start_script(script, 'game_die')))
            show_lose_screen()
            return

global input_text, running, input_active, ctrl_pressed, shift_pressed
input_text = ''
running = True
input_active = False
ctrl_pressed = False
shift_pressed = False

def text_input():
    global input_text, running, input_active, ctrl_pressed, shift_pressed, health, dogs, cats, cat, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing, dog_damag_boost, cat_works_boost, cats_boost, upping, buy_cats, xexe, mx, dogs_class, dangerous_keywords_pp2irooodjhjjjkjkn, scripts, bad_list, good_list, catown2, bonus, new_music, buy_no_cats, event_game, maxMoney, cat_unblock, stop_game, cats_moneys
    input_text = str(input_text)
    try:
        if input_text.split()[0] == "health":
            health = int(input_text.split()[1])
        elif input_text.split()[0] == "regen":
            WhoRegen = input_text.split()[1]
            if WhoRegen == "cats":
                for cat2 in cats:
                    cat2.health = cat2.maxhealth
            elif WhoRegen == "dogs":
                for dog2 in dogs:
                    dog2.health = dog2.maxhealth
            elif WhoRegen == "all":
                for dog2 in dogs:
                    dog2.health = dog2.maxhealth
                for cat2 in cats:
                    cat2.health = cat2.maxhealth
        # elif input_text.split()[0] == "spawn":
            # spawn_name = input_text.split()[1]
            # xs = input_text.split()[2]
            # ys = input_text.split()[3]
            # for dog2 in dogs_class:
                # if spawn_name == dog2:
                    # dog2.CreateDog(xs, ys)
        elif input_text.split()[0] == "random":
            try:
                WhoRan = input_text.split()[1]
            except:
                WhoRan = None
            try:
                xs = int(input_text.split()[3])
            except:
                xs = None
            try:
                ys = int(input_text.split()[4])
            except:
                ys = None
            try:
                custom_budget = int(input_text.split()[2])
            except:
                custom_budget = random.randint(1, 400000)
            if custom_budget < 0:
                custom_budget = random.randint(1, 400000)
            if WhoRan == 'dogs' or WhoRan == None:
                spawn_dogs(custom_budget, xs, ys)
            if WhoRan == 'cats' or WhoRan == None:
                spawn_cats(custom_budget, xs ,ys)
        elif input_text.split()[0] == "money":
            money = int(input_text.split()[1])
        elif input_text.split()[0] == "wave":
            wave = int(input_text.split()[1])
            budget = 0
            for wave in range(1, wave + 1):
                budget += 5
                budget += round(budget / 5)
        elif input_text.split()[0] == "budget":
            budget = int(input_text.split()[1])
        # elif input_text.split()[0] == "budget_to_wave":
            # budget = int(input_text.split()[1])
            # wave = 0
            # for budget in range(1, budget + 1):
                # wave += 5
                # wave += round(wave / 5)
                # if wave >= budget:
                    # break
        elif input_text.split()[0] == "mega_wave":
            for_mega_wave = 0
        elif input_text.split()[0] == "kill":
            WhiKill = input_text.split()[1]
            if WhiKill == "cats":
                while len(cats) != 0:
                    for cat2 in cats:
                        cat2.bump(cat2.maxhealth)
            elif WhiKill == "dogs":
                while len(dogs) != 0:
                    for dog2 in dogs:
                        dog2.bump(dog2.maxhealth, [], False)
            elif WhiKill == "all":
                while len(dogs) != 0 or len(cats) != 0:
                    for dog2 in dogs:
                        dog2.bump(dog2.maxhealth, [], False)
                    for cat2 in cats:
                        cat2.bump(cat2.maxhealth)
        elif input_text.split()[0] == "shop":
            for cd2 in buy_no_cats:
                cd2.unblock = True
            input_text = ''
            game(0)
        elif input_text.split()[0] == "stop":
            stop_game = True
        elif input_text.split()[0] == "play":
            stop_game = False
        # elif input_text.split()[0] == "save":
            # save_game()
        # elif input_text.split()[0] == "load":
            # load_game()
        else:
            for script in scripts:
                exec(str(start_script(script, 'cmd')))
    except:
        pass
    
    input_text = ''

def CMD_codes(event):
    global input_text, running, input_active, ctrl_pressed, shift_pressed
    for script in scripts:
        exec(str(start_script(script, 'cmd_event')))
    if event.type == pygame.KEYDOWN:
        if event.key == pl.K_LCTRL:
            ctrl_pressed = True
        if event.key == pl.K_LSHIFT:
            shift_pressed = True
        if ctrl_pressed and shift_pressed and event.key == pl.K_SPACE:
            input_active = not input_active
        elif input_active:
            if event.key == pl.K_RETURN:
                if input_text:
                    try:
                        text_input()
                    except:
                        pass
            elif event.key == pl.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    if event.type == pygame.KEYUP:
        if event.key == pl.K_LCTRL:
            ctrl_pressed = False
        if event.key == pl.K_LSHIFT:
            shift_pressed = False

menu()
pygame.quit()
