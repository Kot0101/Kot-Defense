import pygame
import os
import random
from pypresence import Presence
import pickle
import tkinter as tk
from tkinter import filedialog
import pygame.locals as pl
pygame.init()
try:
    pygame.mixer.init()
except:
    pass

global mods_count, port, event_game, stop_game, new_cat, all_cats, all_dogs, training_step, cmd_queue,first, wave
client_id = '1210980897281802330'
try:
    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(details=f"Загрузка", large_image="kotdefense", large_text="Kot Defense")
except:
    pass
first = False
wave = 0
mods_count = 0
port = random.randint(1, 65535)
scripts = []
event_game = None
stop_game = False
new_cat = None
all_cats = []
all_dogs = []
training_step = 0

width = 1400
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kot Defense 2.1")

text_color = (255, 255, 255)
text_outlining_color = (0, 0, 0)
text2_color = (30, 53, 49)
heart_color = (255, 0, 0)
money_color = (53, 189, 66)
background_color = (101, 155, 94)
event1_background_color = (91, 122, 24)
red_btn_color = (255, 0, 0)
green_btn_color = (0, 255, 0)
blue_btn_color = (0, 0, 255)
down_menu_cats = (40, 63, 59)
event1_down_menu_cats = (107, 66, 18)
info_text_outlining_color = (0, 0, 0)
info_text2_color = (170, 170, 170)
skip_button_color = (255, 0, 0)
skip_button_text_color = (0, 0, 0)
boss_background_color = (102, 125, 12)
hint_color_1 = (255, 255, 255)
hint_color_2 = (255, 255, 255)
hint_color_3 = (255, 255, 255)
hint_color_def = hint_color_1

cmd_queue = []

global translate, translate_dogs, translate_cats, translate_text, translate_baffs, Notifications
translate = "ru"
Notifications = []

translate_dogs = {
    "ru": {
        "FastDog": "Быстрые собаки",
        "BigDog": "Большые собаки",
        "KillerDog": "Ассасины собаки",
        "KiberDog": "Кибер-собаки",
        "BoomDog": "Бум-доги",
        "NecDog": "Некроманские псы",
        "MehoDog": "Мехо",
        "BomberDog": "Бомберы",
        "TrojanDog": "Троянский псы",
        "GhostDog": "Призраки собак",
        "Woolf": "Оборотни",
        "MedicDog": "Медицинские псы",
        "DogTitan": "Собаки титаны",
        "ManiakDog": "Маньяки",
        "Dog": "Собаки"
    },
    "en": {
        "fastdog": "Fast dogs", 
        "bigdog": "Big dogs", 
        "killerdog": "Assassin dogs", 
        "kiberdog": "Cyber dogs", 
        "boomdog": "Boom dogs", 
        "necdog": "Necromancer dogs", 
        "mehodog": "Meho", 
        "bomberdog": "Bombers", 
        "trojandog": "Trojan dogs", 
        "ghostdog": "Ghost dogs", 
        "woolf": "Werewolves", 
        "medicdog": "Medical dogs", 
        "dogtitan": "Titan dogs", 
        "maniakdog": "Maniacs", 
        "dog": "Dogs" 
    }
}

translate_cats = {
    "description": {
        "ru": {
            "official_kot_defense_info1": "4 жизни, атакует 2 собаки за раз, средняя перезарядка, 1 урон",
            "official_kot_defense_info2": "40 жизни, не атакует собак",
            "official_kot_defense_info3": "6 жизней, атакует 3 собаки за раз, долгая перезарядка, 10 урон",
            "official_kot_defense_info4": "20 жизнь, атакует 3 собаки за раз, быстрая перезарядка, 1.5 урон",
            "official_kot_defense_info5": "15 жизней, не атакует собак, но зарабатывает 10$ каждую волну",
            "official_kot_defense_info6": "80 жизней, не атакует собак, усиливает\nатаку курсором игрока",
            "official_kot_defense_info7": "60 жизней, не атакует собак, лечит котов в его радиусе",
            "official_kot_defense_info8": "60 жизней, атакует 1 собаки за раз, быстрая перезарядка, \nбьёт только взрывучих или в полёте собак, 150 урон",
            "official_kot_defense_info9": "30 жизней, атакует 1 собаки за раз, долгая перезарядка, 100 урон",
            "official_kot_defense_info10": "1000 жизней, собака получает 5%\nурона при нападение на кота",
            "official_kot_defense_info11": "80 жизней, не атакует собак, лечит котов в его радиусе",
            "official_kot_defense_info12": "1 жизнь, атакует 1 собаки за раз, быстрая перезарядка,\nпри получения урона, собака которая ударила кота получает урон 25% от своего хп",
            "official_kot_defense_info13": "20 жизней, атакует 6 собаки за раз,\nдолгая перезарядка, 3 урон",
            "official_kot_defense_info14": "1 жизня, каждую волну спавнит жабу",
            "official_kot_defense_info15": "1 жизня, каждую волну спавнит добрую собаку",
            "official_kot_defense_info16": "5 жизней, атакует всех в её зоне поражения,\nбыстрая перезарядка, 0.5 урон",
            "official_kot_defense_info17": "50 жизни, атакует 30 собак за раз, сверх быстрая перезарядка, 10 урон"
        },
        "en": {
            "official_kot_defense_info1": "4 lives, attacks 2 dogs at a time, medium cooldown, 1 damage", 
            "official_kot_defense_info2": "40 lives, does not attack dogs", 
            "official_kot_defense_info3": "6 lives, attacks 3 dogs at a time, long cooldown, 10 damage", 
            "official_kot_defense_info4": "20 lives, attacks 3 dogs at a time, fast cooldown, 1.5 damage", 
            "official_kot_defense_info5": "15 lives, does not attack dogs, but earns $10 per wave", 
            "official_kot_defense_info6": "80 lives, does not attack dogs, enhances the attack of the player's cursor", 
            "official_kot_defense_info7": "60 lives, does not attack dogs, heals cats in its radius", 
            "official_kot_defense_info8": "60 HP, attacks 1 dog at a time, quick reload, \nonly hits explosive or flying dogs, 150 damage", 
            "official_kot_defense_info9": "30 HP, attacks 1 dog at a time, long reload, 100 damage", 
            "official_kot_defense_info10": "1000 HP, dog takes 5%\ndamage when attacking a cat", 
            "official_kot_defense_info11": "80 HP, does not attack dogs, heals cats in its radius", 
            "official_kot_defense_info12": "1 HP, attacks 1 dog at a time, quick reload, \nwhen taking damage, the dog that hit the cat takes 25% of its HP damage", 
            "official_kot_defense_info13": "20 lives, attacks 6 dogs at a time, \nlong reload, 3 damage", 
            "official_kot_defense_info14": "1 life, spawns a toad every wave", 
            "official_kot_defense_info15": "1 life, spawns a good dog every wave", 
            "official_kot_defense_info16": "5 lives, attacks everyone in its area of ​​\ndamage, \nfast reload, 0.5 damage", 
            "official_kot_defense_info17": "50 lives, attacks 30 dogs at a time, super fast reload, 10 damage"
        }
    },
    "targets": {
        "ru": {
            "target_no": "",
            "target_any": ", цель: любая",
            "target_most": ", цель: больше всего хп",
            "target_least": ", цель: меньше всего хп",
            "target_fastest": ", цель: самый быстрый",
            "target_slowest": ", цель: самый медленный",
            "target_end": ", цель: ближе к концу",
            "target_beginning": ", цель: ближе к началу",
            "target_max": ", цель: убивать максимум за выстрел"
        },
        "en": {
            "target_no": "",
            "target_any": ", target: any",
            "target_most": ", target: most hp",
            "target_least": ", target: least hp",
            "target_fastest": ", target: fastest",
            "target_slowest": ", target: slowest",
            "target_end": ", target: closer to the end",
            "target_beginning": ", target: closer to the beginning",
            "target_max": ", target: kill max per shot"
        }
    }
}

translate_text = {
    "ru": {
        "wave_text_info": "На этой волне будут ",
        "health_id": "Жизней ",
        "load_pls_wait": "Пожалуйста подождите",
        "load": "Загрузка ",
        "load_main_data": "основных данных",
        "load_modif_data": "модифицированных данных",
        "load_data_packs": "дата паков",
        "load_class": "классов",
        "load_def": "функций",
        "load_baff_and_debaff": "бафов и дебафов",
        "load_game": "игры",
        "load_texts": "текста",
        "dog_info_boom": " жизней, взрываеться и наносит ",
        "dog_info_boom2": " урона всем котам в зоне поражения",
        "dog_info_life_damage": " жизней, лечит собак, наносит 1 урон",
        "dog_info_defolt_life_damage": " жизней, урон ",
        "dog_info_speed": ", скорость ",
        "cmd_cure": "Вылечит тех кого вы указали",
        "cmd_spawn": "Заспванит того кого вы указали",
        "cmd_random": "случайно заспавнит ентити",
        "cmd_money": "Установит указанное число денег",
        "cmd_wave": "Установит указанную волну",
        "cmd_budget": "Установит бюджет для игры",
        "cmd_kill": "Убьёт тех кого вы указали",
        "cmd_store": "Разблокирует магазин (иногда не работает)",
        "cmd_stop": "Остановит игру",
        "cmd_resum": "Возобновит игру",
        "cmd_baff_debaff": "Включит баффы и дебаффы",
        "cmd_save": "Сохранит игру",
        "cmd_load": "Загрузит игру",
        "cmd_reset_game": "СБРОСИТ ИГРУ",
        "cmd_language": "Изменит язык",
        "cmd_coordinates": "Выведет координаты курсора",
        "cmd_training": "Включит обучение",
        "cmd_event": "Изменит ивент",
        "save_mods_in_world": "В мире использовались моды:\n",
        "save_mods_not_in_world": "В мире не использовались моды\n",
        "save_world_created": "Мир был создан ",
        "save_in_world": "В мире ",
        "save_entyti": " существ ",
        "save_wave": " волна, ",
        "save_money": " денег",
        "save_health": " жизней, ",
        "lost_right": "Вы проиграли. Нажмите ПКМ, чтобы начать заново.",
        "info_play": "Играть проще не куда!",
        "info_info": "Не дай собакам дойти до правой стороны экрана\nСтавь котов чтобы они помогали отбивать нападения\nПри нажатие ПКМ по коту он продастся за половину его цены\nПри нажатие ЛКМ по собаке ей наносится урон\nЕсть вид собак 'в полёте' их может убить только ПВО\nВ паузе есть настройки",
        "RPC_record": "Рекорд: ",
        "RPC_Menu": "Меню",
        "menu_welcome": "Добро пожаловать в Kot Defense",
        "menu_record": "Ваш рекорд: ",
        "menu_event": 'Ивент "Магический лес"',
        "menu_you": "У вас ",
        "menu_mods": " модификаций",
        "buff_select": "Выберите бафф",
        "debuff_select": "Выберите дебаф",
        "win_text_event_1": "Поздравляю ! Вы прошли ивент, отправьте скришот этого экрана\nв тех поддержку чтобы получить бонус ваш код: ",
        "win_text_event_2": "\nНажмите ПКМ чтобы выйти",
        "win_text_game": "Поздравляю ! Вы официально прошли игру.\nДальше будет бесконечная игра\nНажмите ПКМ чтобы продолжить играть",
        "pause": "Пауза. Нажмите ПКМ, чтобы снять с паузы ",
        "skip": "Скип"
    },
    "en": {
        "wave_text_info": "This wave will have ",
        "health_id": "Lives ",
        "load_pls_wait": "Please wait",
        "load": "loading ",
        "load_main_data": "main data",
        "load_modif_data": "modified data",
        "load_data_packs": "data packs",
        "load_class": "classes",
        "load_def": "features",
        "load_baff_and_debaff": "buffs and debuffs",
        "load_game": "game",
        "load_texts": "texts",
        "dog_info_boom": " lives, explodes and deals ",
        "dog_info_boom2": " damage to all cats in the affected area",
        "dog_info_life_damage": " lives, heals dogs, deals 1 damage",
        "dog_info_defolt_life_damage": " lives, damage ",
        "dog_info_speed": ", speed ",
        "cmd_cure": "Will cure those you indicated",
        "cmd_spawn": "Will spawn one you indicated",
        "cmd_random": "Accidentally dormant entities",
        "cmd_money": "Set a certain number of moneys",
        "cmd_wave": "Set a certain number of wave",
        "cmd_budget": "Set a certain number of budget",
        "cmd_kill": "Will kill those you indicated",
        "cmd_store": "Unlocks store (sometimes does not work)",
        "cmd_stop": "Will stop game",
        "cmd_resum": "Will resume game",
        "cmd_baff_debaff": "Will enable buffs and debuffs",
        "cmd_save": "Will save game",
        "cmd_load": "Will load game",
        "cmd_reset_game": "RESET GAME",
        "cmd_language": "Change language",
        "cmd_coordinates": "Will display the coordinates of the cursor",
        "cmd_training": "Will include training",
        "cmd_event": "Will change the event",
        "save_mods_in_world": "Mods used in the world:\n",
        "save_mods_not_in_world": "Mods were not used in the world\n",
        "save_world_created": "the world was created on ",
        "save_in_world": "there are ",
        "save_entyti": " creatures in the world",
        "save_wave": " wave, ",
        "save_health": " health, ",
        "save_money": " money",
        "lost_right": "You lost. right click to start over.",
        "info_play": "It couldn't be easier to play",
        "info_info": "Don't let the dogs reach the right side of the screen\nput cats to help fight off attacks\nif you right-click on a cat, it will sell for half its price\nif you left-click on a dog, it will be damaged\nthere is a view of dogs 'in flight', only air defense can kill them\nthere are settings in the pause",
        "RPC_record": "Record: ",
        "RPC_Menu": "Menu",
        "menu_welcome": "Welcome to Kot Defense",
        "menu_record": "Your record: ",
        "menu_event": 'Event "Magic forest"',
        "menu_you": "You have ",
        "menu_mods": " modifications",
        "buff_select": "Select buff",
        "debuff_select": "Select debuff",
        "win_text_event_1": "Congratulations! you completed the event, send a screenshot of this screen\nto technical support to receive a bonus your code: ",
        "win_text_event_2": "\npress RMB  to exit",
        "win_text_game": "congratulations! you have officially completed the game.\nthe game will be endless\npress RMB to continue playing",
        "pause": "Paused. Press RMB to unpause game",
        "skip": "Skip"
    }
}

translate_baffs = {
    "ru": {
        "debaff_hard": "игра станет сложнее",
        "debaff_all_cats_damage": "некоторые коты получат 15% урона от своих жизней",
        "debaff_maxium_money": "отнимает 15% ваших денег",
        "debaff_frogs": "превращает 20% котов в лягушек",
        "baff_maxium_money": "добавить 10% ваших денег",
        "baff_main_heart": "+1 главных сердец",
        "baff_lives_all_cats": "добавит 10% жизней всем котам на поле боя",
        "baff_ez": "игра станет легче",
        "baff_works": "коты работники дают на 5$ больше",
        "baff_shield": "магический щит, защищает котов от вражеских собак"
    },
    "en": {
        "debaff_hard": "game will become more difficult",
        "debaff_all_cats_damage": "some cats will take 15% damage from their HP",
        "debaff_maxium_money": "takes away 15% of your money",
        "debaff_frogs": "turns 20% of cats into frogs",
        "baff_maxium_money": "add 10% of your money",
        "baff_main_heart": "+1 main health",
        "baff_lives_all_cats": "will add 10% HP to all cats on the battlefield",
        "baff_ez": "game will become easier",
        "baff_works": "cat workers give $5 more",
        "baff_shield": "magic shield, protects cats from enemy dogs"
    }
}

def loading_text(lo):
    global translate, translate_dogs, translate_cats, translate_text
    fonte = pygame.font.Font(None, 75)
    text = fonte.render(translate_text[translate]["load_pls_wait"], True, text2_color)
    text_rect = text.get_rect(center=(width/2, height/2))
    text2 = fonte.render(translate_text[translate]["load"]+f"{lo}...", True, text2_color)
    text_rect2 = text.get_rect(center=(width/2-50, height/2+70))
    screen.fill(background_color)
    screen.blit(text, text_rect)
    screen.blit(text2, text_rect2)
    pygame.display.flip()

loading_text(translate_text[translate]["load_main_data"])

#загрузка шрифтов
font = pygame.font.Font("Data/Fonts/segoe-ui-symbol.ttf", 35)
font2 = pygame.font.Font(None, 25)
fontSkip = pygame.font.Font(None, 40)

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
        if dangerous == False:
            scripts.append(self)
            del self

pause_image = pygame.image.load(r'Data\Img\pause.png')
icon = pygame.image.load(r'Data\Img\ico.png')
btn_image = pygame.image.load(r'Data\Img\btn.png')
btn2_image = pygame.image.load(r'Data\Img\btn2.png')
play_image = pygame.image.load(r'Data\Img\play.png')
back_image = pygame.image.load(r'Data\Img\back.png')
info_image = pygame.image.load(r'Data\Img\info.png')
discord_image = pygame.image.load(r'Data\Img\discord.png')
mult_image = pygame.image.load(r'Data\Img\mult.png')
host_image = pygame.image.load(r'Data\Img\host.png')
connect_image = pygame.image.load(r'Data\Img\connect.png')
cursor_img = pygame.image.load(r"Data\Img\cursor.png")
error_img = pygame.image.load(r"Data\Img\error.png")
mods_image = pygame.image.load(r"Data\Img\mods.png")
play2_image = pygame.image.load(r"Data\Img\EVENT PLAY.png")
loading_image = pygame.image.load(r"Data\Img\loading.png")
exit_image = pygame.image.load(r"Data\Img\exit.png")

cwa_image = pygame.image.load(r'Data\Img\cwa_image.png')
cwa_image = pygame.transform.scale(cwa_image, (60, 60))

try:
    dog_bump = pygame.mixer.Sound(r'Data/Sounds/bump.mp3')
    boom = pygame.mixer.Sound(r'Data/Sounds/boom.mp3')
    click = pygame.mixer.Sound(r'Data/Sounds/click.mp3')
    sirena = pygame.mixer.Sound(r'Data/Sounds/sirena.mp3')
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
loading_image = pygame.transform.scale(loading_image, (350, 110))
exit_image = pygame.transform.scale(exit_image, (350, 120))

pygame.display.set_icon(icon)

loading_text(translate_text[translate]["load_modif_data"])

#загрузка данных
folder_path = r'Data\\Mods\\'
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name == 'load.py':
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
                try:
                    exec(code)
                except Exception as e:
                    print(f"An error occurred: {e}")


loading_text(translate_text[translate]["load_data_packs"])
#Загрузка дата паков
music_path = r'Data/Sounds/music.mp3'
event1_music = r'Data/Sounds/event1_music.mp3'
music_path2 = r'Data/Sounds/music2.mp3'
music_path3 = r'Data/Sounds/music3.mp3'
music_path4 = r'Data/Sounds/music4.mp3'
music_path5 = r'Data/Sounds/music5.mp3'
folder_path = r'Data\DataPacks'

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
        elif file_name == 'loading.png':
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
        elif file_name == 'music3.mp3':
            try:
                music_path3 = file_path
            except:
                pass
        elif file_name == 'music4.mp3':
            try:
                music_path4 = file_path
            except:
                pass
        elif file_name == 'music5.mp3':
            try:
                music_path5 = file_path
            except:
                pass
        elif file_name == 'bump.mp3':
            try:
                dog_bump = pygame.mixer.Sound(file_name)
            except:
                pass
        elif file_name == 'boom.mp3':
            try:
                boom = pygame.mixer.Sound(file_name)
            except:
                pass
        elif file_name == 'click.mp3':
            try:
                click = pygame.mixer.Sound(file_name)
            except:
                pass
        elif file_name == 'sirena.mp3':
            try:
                sirena = pygame.mixer.Sound(file_name)
            except:
                pass
        elif file_name == 'cwa_image.png':
            cwa_image = pygame.image.load(file_path)
            cwa_image = pygame.transform.scale(cwa_image, (210, 90))
        elif file_name == 'theme.py':
            with open(file_path, 'r') as file:
                sperma = False
                for line in file:
                    line = line.strip()
                    try:
                        exec(line)
                    except Exception as e:
                        print(f"An error occurred: {e}")

global music_files
music_files = [music_path, music_path3, music_path4, music_path5]
try:
    music2 = music_path2
except:
    pass

loading_text(translate_text[translate]["load_class"])

#классы
def load_image(path, size_x, size_y):
    try:
        image = pygame.transform.scale(pygame.image.load(path), (size_x, size_y))
        return image
    except:
        try:
            return pygame.transform.scale(pygame.image.load(r"Data/Img/error.png"), (size_x, size_y))
        except:
            try:
                return pygame.transform.scale(pygame.image.load(r"Data/Img/error.png"), (60, 60))
            except:
                return None

class Checkbox:
    def __init__(self, x, y, text, checked=False, check_id=-1):
        self.x = x
        self.y = y
        self.checked = checked
        self.text = text
        self.font = pygame.font.SysFont(None, 30)
        self.id = check_id

    def draw(self, surface):
        checkbox = pygame.Rect(self.x, self.y, 20, 20)
        pygame.draw.rect(surface, (0, 0, 0), checkbox, 2)

        if self.checked:
            pygame.draw.line(surface, (0, 0, 0), (self.x+5, self.y+10), (self.x+10, self.y+15), 2)
            pygame.draw.line(surface, (0, 0, 0), (self.x+10, self.y+15), (self.x+15, self.y+5), 2)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surface, (self.x + 30, self.y))

    def toggle(self):
        global music_playing, music
        self.checked = not self.checked
        if self.id == 0:
            music_playing = self.checked
            play_music()
            save_game_settings()

class NotificationSystem:
    def __init__(self, text, color=(255, 255, 255), font_size=30, speed=1, fade_speed=2, time=2, x = screen.get_width()-20, y = screen.get_height() - 150, waiting = 0):
        global Notifications
        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(text, True, color)
        self.rect = self.text_surface.get_rect(bottomright=(x, y))
        self.speed = speed
        self.alpha = 255
        self.fade_speed = fade_speed
        self.frames = 60 * time
        self.waiting = waiting * 60
        Notifications.append(self)

    def update(self):
        global Notifications
        try:
            self.waiting -= 1
            if self.waiting <= 0:
                if self.frames < 0:
                    self.rect.bottom -= self.speed
                    self.alpha -= self.fade_speed
                self.frames -= 1
                if self.alpha <= 0:
                    Notifications.remove(self)
                    del self
                    return
                self.text_surface.set_alpha(self.alpha)
                screen.blit(self.text_surface, self.rect)
        except:
            pass

class effect:
    def __init__(self, id=0, color=(255, 255, 255), fade_start=255, fade_end=0, speed=1, time=2, x = screen.get_width()-20, y = screen.get_height() - 150, waiting = 0):
        global Notifications
        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(text, True, color)
        self.rect = self.text_surface.get_rect(bottomright=(x, y))
        self.speed = speed
        self.alpha = 255
        self.fade_speed = fade_speed
        self.frames = 60 * time
        self.waiting = waiting * 60
        Notifications.append(self)

    def update(self):
        global effects
        try:
            self.waiting -= 1
            if self.waiting <= 0:
                if self.frames < 0:
                    self.alpha -= self.fade_speed
                self.frames -= 1
                if self.alpha <= 0:
                    Notifications.remove(self)
                    del self
                    return
                bg_surface.fill((self.color, self.alpha))
        except:
            pass

class BuyCat:
    def __init__(self, moneys, info_self, aura_radius, cat_health, dogs_count, reload, damage_cat, mega, wawe, wawedel, path_my_image, size_x, size_y, ico_image_path):
        global buy_cats, scripts, buy_no_cats, wave, event_game, cats_moneys, translate, translate_cats
        for script in scripts:
            exec(str(start_script(script, 'create_buy_cat')))
        image = pygame.transform.scale(pygame.image.load(path_my_image), (size_x, size_y))
        if ico_image_path != None:
            ico = pygame.transform.scale(pygame.image.load(ico_image_path), (60, 60))
        else:
            ico = pygame.transform.scale(pygame.image.load(path_my_image), (60, 60))
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
        self.targetDeff = 0
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
        global buy_cats, scripts, buy_no_cats, wave, event_game
        
        try:
            if event_game == 1:
                self.delet_wave = 9999999999999999999999999999999999999999999999999999999999999999999999999999999999*99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                if self in buy_no_cats:
                    buy_no_cats.remove(self)
                if self not in buy_cats:
                    buy_cats.append(self)
                self.unblock = True
                new_cat_unblock()
            else:
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
        global cats_boost, cat_works_boost, xexe, scripts, translate_cats, translate
        for script in scripts:
            exec(str(start_script(script, 'info_buy_cat')))
        try:
            if self not in buy_no_cats:
                if self.rect.x > 1060:
                    return
                if xexe >0 and self.rect.x < 100:
                    return
                if self.rect.collidepoint(pos):
                    try:
                        info2 = translate_cats["description"][translate][str(self.info)]
                    except:
                        try:
                            info2 = self.info
                        except:
                            info2 = "ERROR INFO"
                    info(info2, (pos[0] + 15, pos[1] + 5))
        except:
            pass
    
    def buy(self, pos, mo):
        global cats, money, xexe, scripts, catown, catown2, buy_no_cats
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
                                new_cat = Cat(None, None, self.aura_radius, self.health, self.dogs_count, self.money, self.reload, self.damage, self.mega, self.path_my_image, self.size_x, self.size_y) 
                                for script in scripts:
                                    exec(str(start_script(script, 'buy_cat_create')))
                                catown = new_cat
                                new_cat.dds = mo
                                new_cat.blacklist.extend(self.blacklist)
                                new_cat.parent = self
                                new_cat.target = self.targetDeff
                                cats.append(new_cat)
                else:
                    if money >= self.money:
                        new_cat = Cat(None, None, self.aura_radius, self.health, self.dogs_count, self.money, self.reload, self.damage, self.mega, self.path_my_image, self.size_x, self.size_y) 
                        for script in scripts:
                            exec(str(start_script(script, 'buy_cat_create')))
                        catown = new_cat
                        new_cat.dds = 1
                        new_cat.blacklist.extend(self.blacklist)
                        new_cat.parent = self
                        new_cat.target = self.targetDeff
                        cats.append(new_cat)
        except:
            pass
    def random_buy(self, custom_X, custom_Y):
        global cats, money, xexe, scripts, catown, catown2, buy_no_cats
        
        for script in scripts:
            exec(str(start_script(script, 'buy_cat')))
        try:
            new_cat = Cat(None, None, self.aura_radius, self.health, self.dogs_count, self.money, self.reload, self.damage, self.mega, self.path_my_image, self.size_x, self.size_y) 
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
                cat_collides = any(new_cat.rect.colliderect(c.rect) for c in cats if c != new_cat)
                dog_collides = any(new_cat.rect.colliderect(d.rect) for d in dogs)
                if not cat_collides and not dog_collides:
                    break
            new_cat.parent = self
            cats.append(new_cat)
            new_cat.dds = 1
            new_cat.blacklist.extend(self.blacklist)
        except:
            pass


class Cat:
    def __init__(self, xee, yee, aura_radius, cat_health, dogs_count, cat_money, reload, damage_cat, mega, path_my_image, size_x, size_y):
        global scripts, all_cats, cats
        for script in scripts:
            exec(str(start_script(script, 'create_cat')))
        try:
            image = pygame.transform.scale(pygame.image.load(path_my_image), (size_x, size_y))
        except:
            try:
                image = pygame.transform.scale(pygame.image.load("Data/Img/error.png"), (size_x, size_y))
            except:
                try:
                    image = pygame.transform.scale(pygame.image.load("Data/Img/error.png"), (60, 60))
                except:
                    if self in cats:
                        cats.remove(self)
                    del self
        self.original_image = image.convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.aura_radius = aura_radius
        self.follow_mouse = True
        self.health = cat_health
        self.maxhealth = self.health
        self.dogs_count = dogs_count
        self.money = cat_money
        self.reload = reload * 60
        self.Maxreload = reload * 60
        self.speed = reload
        self.damage = damage_cat
        self.unable_to_place = False
        self.mega = mega
        self.maxhe = self.health
        self.stope = False
        self.blacklist = []
        self.dds = 0
        self.target = 0
        self.path_my_image = path_my_image
        self.size_x = size_x
        self.size_y = size_y
        self.parent = None
        self.targetList = {
            -1: "target_no",
            0: "target_any",
            1: "target_most",
            2: "target_least",
            3: "target_fastest",
            4: "target_slowest",
            5: "target_end",
            6: "target_beginning"
            # 7: "target_max"
        }
        if xee != None:
            self.rect.x = xee
            self.follow_mouse = False
        if yee != None:
            self.rect.y = yee
            self.follow_mouse = False
        if not self in cats and self.follow_mouse == False:
            cats.append(self)

    def update(self, pos):
        global scripts, shift_pressed
        self.stope = False
        for script in scripts:
            exec(str(start_script(script, 'update_cat')))
        if self.stope:
            return
        try:
            pause_rect = pause_image.get_rect(topleft=(width - 55, 10))
            rect22 = pygame.Rect(0, height - 155, 1400, 160)
            rect33 = pygame.Rect(0, 0, 1400, 150)
            if self.follow_mouse:
                if not shift_pressed:
                    self.rect.center = pos
                self.image.set_alpha(128)
                cat_collides = any(self.rect.colliderect(c.rect) for c in cats if c != self)
                dog_collides = any(self.rect.colliderect(d.rect) for d in dogs)
                if not rect22.collidepoint(pos) and not rect33.collidepoint(pos) and not pause_rect.collidepoint(pos) and not cat_collides and not dog_collides and self.rect.x < width and self.rect.x > 0 and self.rect.y > 0 and self.rect.y < height:
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
    
    def save(self):
        global all_cats, cats
        if self.follow_mouse == False:
            all_cats.append(f"new_cat=Cat({self.rect.x}, {self.rect.y}, {self.aura_radius}, {self.dogs_count}, {self.health}, {self.money}, {round(self.Maxreload/60)}, {self.damage}, {self.mega}, r'{self.path_my_image}', {self.size_x}, {self.size_y})\nnew_cat.maxhealth={self.maxhealth}\nnew_cat.reload = {self.reload}\nnew_cat.blacklist = {self.blacklist}\nnew_cat.target = {self.target}")
    
    def draw(self, screen, online):
        global scripts, catown2, catown, pos
        self.stope = False
        
        for script in scripts:
            exec(str(start_script(script, 'draw_cat')))
        try:
            if self.stope:
                return

            if len(cats) > 40:
                if pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(pos)) <= 500:
                    if self.aura_radius > 0:
                        if catown is not None:
                            self._draw_aura(screen)
            else:
                if self.aura_radius > 0:
                    if catown is not None or self.rect.collidepoint(pos):
                        self._draw_aura(screen)
            screen.blit(self.image, self.rect)
        except:
            pass

    def _draw_aura(self, screen):
        if self.aura_radius < 1400:
            circle_surface = pygame.Surface((self.aura_radius * 2, self.aura_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (255, 255, 255, 100), (self.aura_radius, self.aura_radius), self.aura_radius, 2)
            screen.blit(circle_surface, (self.rect.centerx - self.aura_radius, self.rect.centery - self.aura_radius))
    
    def info_ca(self, screen, pos):
        global scripts, translate_text, translate, translate_cats
        self.stope = False
        try:
            for script in scripts:
                exec(str(start_script(script, 'info_cat')))
            if self.rect.collidepoint(pos) and self.follow_mouse == False and self.stope == False:
                info(f'{round(self.health,1)} ' + translate_text[translate]["health_id"] + translate_cats['targets'][translate][self.targetList[self.target]], (pos[0] + 15, pos[1] + 5))
        except:
            pass
    
    def sorte(self, listis):
        sorted_list = listis
        if self.target == 1:
            sorted_list = sorted(listis, key=lambda entiti: entiti.maxhealth, reverse=True)
        elif self.target == 2:
            sorted_list = sorted(listis, key=lambda entiti: entiti.maxhealth)
        elif self.target == 3:
            sorted_list = sorted(listis, key=lambda entiti: entiti.speed, reverse=True)
        elif self.target == 4:
            sorted_list = sorted(listis, key=lambda entiti: entiti.speed)
        elif self.target == 5:
            sorted_list = sorted(listis, key=lambda entiti: entiti.rect.x, reverse=True)
        elif self.target == 6:
            sorted_list = sorted(listis, key=lambda entiti: entiti.rect.x)
        return sorted_list
    
    def remove_dogs_periodically(self, custom=None):
            global money, cat_works_boost, cats_boost, scripts, cats, dogs
            self.stope = False
            try:
                if not self.follow_mouse:
                    cutm = False
                    if custom is None:
                        self.reload -= 1
                    else:
                        cutm = self.Maxreload == custom
                    if self.reload == 0 or cutm:
                        self.reload = self.Maxreload
                        count_attacs = 0
                        cutm = True
                        if cutm:
                            if self.mega == 2:
                                money += self.damage + cat_works_boost
                            elif self.mega == 6:
                                dogs.append(Dog(self.rect.x, self.rect.y, 12, 0, 3, 1, 14, 1, 0, r'Data\Img\cwa_image.png', 60, 60))
                                dogs[-1].sigma = True
                            elif self.mega == 7:
                                dogs.append(Dog(self.rect.x, self.rect.y, 25, 0, 2, 3, 14, 1, 0, r'Data\Img\CatDog.jpg', 60, 60))
                                dogs[-1].sigma = True
                            elif self.mega == 4:
                                for cat in self.sorte(list(cats)):
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
                        if self.stope == False:
                            if self.mega == 1 or self.mega == 8:
                                if self.mega == 8:
                                    for dog in self.sorte(list(dogs)):
                                        if pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(dog.rect.center)) <= self.aura_radius and dog != self:
                                            dog.bump((self.damage) / 500)
                                for dog in self.sorte(list(dogs)):
                                    if self.blacklist == []:
                                        blackdog = False
                                    else:
                                        blackdog = True
                                        for blackitem in self.blacklist:
                                            if dog.typee == blackitem:
                                                blackdog = False
                                    if blackdog == False and dog.mega != 14:
                                        if count_attacs < self.dogs_count:
                                            if pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(dog.rect.center)) <= self.aura_radius + dog.size_x - 60:
                                                count_attacs += 1
                                                try:
                                                    dog_bump.play()
                                                except:
                                                    pass
                                                dog.bump(self.damage, True, self)
                                        else:
                                            break
            except:
                pass
    
    def sell(self, mn):
        global money, pause, scripts, cats
        self.stope = False
        try:
            for script in scripts:
                exec(str(start_script(script, 'sell_cat')))
            
            if self.stope == False:
                if self.follow_mouse == False:
                    money += round(self.money * mn)
                cats.remove(self)
                del self
        except:
            pass
    
    def handle_mouse_click(self, pos, mo):
        global cats, dogs, scripts, catown, catown2, all_cats, money, ctrl_pressed, shift_pressed
        self.stope = False
        try:
            for script in scripts:
                exec(str(start_script(script, 'handle_mouse_click_cat')))
            if mo == 1:
                if self == catown and self.stope == False:
                    self.old_rect = self.rect
                    self.rect.center = pos
                    pause_rect = pause_image.get_rect(topleft=(width-55, 10))
                    rect22 = pygame.Rect(0, height-155, 1400, 160)
                    rect33 = pygame.Rect(0, 0, 1400, 150)
                    cat_collides = any(self.rect.colliderect(c.rect) for c in cats if c != self)
                    dog_collides = any(self.rect.colliderect(d.rect) for d in dogs)
                    if rect22.collidepoint(self.rect.center) or rect33.collidepoint(self.rect.center) or pause_rect.collidepoint(self.rect.center) or cat_collides or dog_collides or self.rect.x > width or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > height:
                        if shift_pressed or ctrl_pressed:
                            self.unable_to_place = False
                        else:
                            self.rect.center = self.old_rect.center
                    if self.unable_to_place == True:
                        rect = pygame.Rect(0, height-100, 1400, 100)
                        self.follow_mouse = False
                        catown = None
                        money -= self.money
                        if ctrl_pressed or shift_pressed and money >= self.money:
                            self.parent.buy(pos, 2)
            else:
                if self == catown2 and self.stope == False:
                    rect22 = pygame.Rect(0, height-100, 1400, 100)
                    rect33 = pygame.Rect(0, 0, 1400, 100)
                    if self.unable_to_place == True:
                        rect = pygame.Rect(0, height-100, 1400, 100)
                        self.follow_mouse = False
                        money -= self.money
                        catown = None
                        if ctrl_pressed or shift_pressed and money >= self.money:
                            self.parent.buy(pos, 2)
        except:
            pass
    def targetChanged(self, pos):
        try:
            if self.rect.collidepoint(pos) and self.follow_mouse == False and self.target>-1:
                if len(list(self.targetList))-3 < self.target:
                    self.target = 0
                else:
                    self.target += 1
        except:
            pass
    def cwa(self):
        try:
            self.damage = 0
            self.health = 3
            self.aura_radius = 0
            self.image = pygame.transform.scale(pygame.image.load(r'Data\Img\cwa_image.png'), (self.size_x, self.size_y))
            self.money = 0
            self.original_image = self.image
            self.image_path = r'Data\Img\cwa_image.png'
        except:
            pass

class CreateDog:
    def __init__(self, money_dog, bugete, name, health_dog, speed, damage_dog, unikal, reload, typedog, path_my_image, size_x, size_y):
        global dogs_variants, dogs_moneys, dogs_class, scripts
        
        self.image = load_image(path_my_image, size_x, size_y)
        if self.image is None:
            del self
            return
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

        dogs_variants[name] = bugete
        dogs_moneys[name] = money_dog
        dogs_class[name] = self

        for script in scripts:
            exec(str(start_script(script, 'create_dog')))

    def create(self, custom_X=None, custom_Y=None):
        global dogs, scripts
        for script in scripts:
            exec(str(start_script(script, 'spawn_dog')))
        
        xx = random.randint(-900, -60) if custom_X is None else custom_X
        yy = random.randint(100 + self.size_y // 2, height - 255) if custom_Y is None else custom_Y

        try:
            new_dog = Dog(xx, yy, self.health, self.money, self.speed, self.damage, self.mega, self.reload, self.type, self.path_my_image, self.size_x, self.size_y)
            new_dog.sigma = True
            new_dog.damagecats = self.damagecats
            new_dog.parent = self
        except:
            pass

class Dog:
    def __init__(self, x, y, health_dog, money_dog, speed, damage_dog, unikal, reload, dogtype, path_my_image, size_x, size_y):
        global all_dogs, dogs
        for script in scripts:
            exec(str(start_script(script, 'spawn_dog')))
        self.image = load_image(path_my_image, size_x, size_y)
        if self.image is None:
            if self in dogs:
                dogs.remove(self)
            del self
            return
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.health = health_dog
        self.money = money_dog
        self.damage = damage_dog
        self.mega = unikal
        self.aura_radius = 200-30
        self.reload = reload * 60
        self.Maxreload = reload * 60
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
        self.sigma = False
        self.parent = None
        dogs.append(self)
    
    def save(self):
        global all_dogs
        all_dogs.append(f"new_dog=Dog({self.rect.x}, {self.rect.y}, {self.health}, {self.money}, {self.speed}, {self.damage}, {self.mega}, {round(self.Maxreload/60)}, {self.typee}, r'{self.path_my_image}', {self.size_x}, {self.size_y})\nnew_dog.reload = {self.reload}\nnew_dog.who = {self.who}\nnew_dog.maxhealth = {self.maxhealth}\nnew_dog.damagecats = {self.damagecats}\nnew_dog.aura_radius = {self.aura_radius}")

    def move(self):
        global dog_damag_boost, scripts, dogs
        self.stope = False
        moveE = True
        try:
            if self.mega != 14:
                for dog2 in list(dogs):
                    if dog2.mega == 14 and moveE and self.rect.colliderect(dog2.rect):
                        moveE = False
                for cat2 in list(cats):
                    if self.rect.colliderect(cat2.rect) and moveE:
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
                    self.stope = True
                for script in scripts:
                    exec(str(start_script(script, 'move_dog')))
                if moveE and not self.stope:
                    self.rect.x += self.speed
            else:
                for dog2 in list(dogs):
                    if self.rect.colliderect(dog2.rect) and dog2 != self and dog2.mega != 14:
                        moveE = False
                if moveE and not self.stope:
                    self.rect.x -= self.speed
                    self.bump(0.03, True, [])
        except:
            pass

    def delet(self):
        global dogs
        dogs.remove(self)
        del self

    def update(self):
        global scripts, dogs
        try:
            if self.sigma:
                for doge in dogs:
                    if doge == self:
                        dogs.remove(doge)
                dogs.append(self)
                self.sigma = False
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
                    info(str(round(self.health, 1)) + translate_text[translate]["dog_info_boom"] + str(self.damage + dog_damag_boost) + translate_text[translate]["dog_info_boom2"], (pos[0] + 15, pos[1] + 5))
                self.stope = True
            if self.mega == 12:
                circle_surface = pygame.Surface((self.aura_radius * 2, self.aura_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (255, 0, 0, 100), (self.aura_radius, self.aura_radius), self.aura_radius, 2)
                screen.blit(circle_surface, (self.rect.centerx - self.aura_radius, self.rect.centery - self.aura_radius))
                if self.rect.collidepoint(pos):
                    info(str(round(self.health, 1)) + translate_text[translate]["dog_info_life_damage"], (pos[0] + 15, pos[1] + 5))
                self.stope = True
            for script in scripts:
                exec(str(start_script(script, 'info_dog')))
            if not self.stope and self.rect.collidepoint(pos):
                info(str(round(self.health, 1)) + translate_text[translate]["dog_info_defolt_life_damage"] + str(self.damage + dog_damag_boost) + translate_text[translate]["dog_info_speed"] + str(self.speed), (pos[0] + 15, pos[1] + 5))
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
            if not self.stope:
                self.health -= damage
                if self.health <= 0:
                    if self.mega == 10:
                        for i in range(4):
                            new_dog = Dog(self.rect.x, self.rect.y, 7, 350, 5, 20, 2 if i < 2 else 7, 1, 1, r'Data\Img\Dog3.png', 60, 60)
                            dogs.append(new_dog)
                            new_dog.sigma = True
                        for i in range(2):
                            new_dog = Dog(self.rect.x, self.rect.y, 1, 1, 2, 1, 4 + i, 2, 0, r'Data\Img\Dog1.png', 60, 60)
                            dogs.append(new_dog)
                            new_dog.sigma = True
                        new_dog = Dog(self.rect.x, self.rect.y, 320, 5000, 1, 30, 6, 1, 0, r'Data\Img\Dog4.png', 60, 60)
                        dogs.append(new_dog)
                        new_dog.sigma = True
                    elif self.mega == 11:
                        new_dog = Dog(self.rect.x, self.rect.y, 40, 100, 1, 6, 1, 1, 0, r'Data\Img\Dog2.jpg', 60, 60)
                        dogs.append(new_dog)
                        new_dog.sigma = True
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
                    if not moveE:
                        if cat2.mega == 5:
                            try:
                                dog_bump.play()
                            except:
                                pass
                            self.bump(cat2.damage * (1/100) * self.maxhealth, True, [])
                            cat2.bump(self.damage + dog_damag_boost)
            for dog2 in list(dogs):
                if (self.mega == 14 and dog2.mega != 14 and self.rect.colliderect(dog2.rect)) or \
                   (dog2.mega == 14 and dog2 != self and self.rect.colliderect(dog2.rect)):
                    dog2.bump(self.damage + dog_damag_boost, True, [])
                else:
                    if self.mega == 12:
                        for dog3 in list(dogs):
                            if dog3.mega != 12 and dog3.mega != 14:
                                distance = ((self.rect.x - dog3.rect.x)*2 + (self.rect.y - dog3.rect.y)*2)*0.5
                                if distance <= 200:
                                    if dog3.maxhealth > dog3.health:
                                        if dog3.maxhealth > dog3.health + self.damage + dog_damag_boost:
                                            dog3.bump(-self.damage - dog_damag_boost, True, [])
                                        else:
                                            dog3.bump(-dog3.maxhealth + dog3.health, True, [])
            cutm = False
            stra = False
            if reloade == None:
                self.reload -= 1
            else:
                cutm = self.Maxreload == reloade
            if self.reload <= 0 or cutm:
                self.reload = self.Maxreload
                stra = True
                
                if self.mega == 6 and stra and self.val3 == 1:
                    for i in range(3):
                        new_dog = Dog(self.rect.x, self.rect.y, 7, 350, 5, 20, 2 + i * 5, 1, 1, r'Data\Img\Dog3.png', 60, 60)
                        dogs.append(new_dog)
                        new_dog.sigma = True
                    self.val3 = 2
                    self.stope = True
                if self.mega == 3 and stra:
                    new_dog = Dog(self.rect.x, self.rect.y, 1, 1, 2, 1, 4 + (self.val2), 2, 0, r'Data\Img\Dog1.png', 60, 60)
                    dogs.append(new_dog)
                    new_dog.sigma = True
                    self.val2 = not self.val2
                    for cat2 in list(cats):
                        if self.rect.colliderect(cat2.rect) and self.mega != 14:
                            if not moveE:
                                try:
                                    if stra:
                                        dog_bump.play()
                                except:
                                    pass
                                cat2.bump(self.damage + dog_damag_boost)
                                self.stope = True
                elif self.mega == 6 and stra:
                    for cat2 in list(cats):
                        if self.rect.colliderect(cat2.rect) and self.mega != 14:
                            if not moveE:
                                if self.val < 3:
                                    for i in range(2):
                                        new_dog = Dog(self.rect.x, self.rect.y, 7, 300, 5, 20, 7 + i, 1, 1, r'Data\Img\Dog3.png', 60, 60)
                                        dogs.append(new_dog)
                                        new_dog.sigma = True
                                try:
                                    dog_bump.play()
                                except:
                                    pass
                                cat2.bump(self.damage + dog_damag_boost)
                                self.stope = True
                if self.mega == 2 or self.mega == 7 or self.mega == 8:
                    boomp = False
                    for cat3 in list(cats):
                        if self.rect.colliderect(cat3.rect):
                            boomp = True
                            break
                    if boomp:
                        for cat2 in list(cats):
                            distance = ((self.rect.x - cat2.rect.x)*2 + (self.rect.y - cat2.rect.y)*2)*0.5
                            if distance <= self.aura_radius + self.size_x:
                                cat2.bump(self.damage + dog_damag_boost)
                        for dog2 in list(dogs):
                            if dog2.mega == 14:
                                distance = ((self.rect.x - dog2.rect.x)*2 + (self.rect.y - dog2.rect.y)*2)*0.5
                                if distance <= self.aura_radius:
                                    dog2.bump(self.damage + dog_damag_boost)
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
                        break 
        except:
            pass
        try:
            if self.stope == False and dog2.mega != 14 and stra:
                for cat2 in list(cats):
                    if self.rect.colliderect(cat2.rect) and self.mega != 14:
                        if not moveE:
                            try:
                                dog_bump.play()
                            except:
                                pass
                            cat2.bump(self.damage + dog_damag_boost)
                            break
        except:
            pass

class CMD_waiting:
    def __init__(self, cmd_line, waiting):
        self.cmd = cmd_line
        self.wait = waiting * 60
        cmd_queue.append(self)
    def update(self):
        self.wait -= 1
        if self.wait <= 0:
            text_input(self.cmd)
            cmd_queue.remove(self)
            del self


loading_text(translate_text[translate]["load_def"])

def cmd_ui(offset_x=0, offset_y=0, offset_size=0):
    fonte = pygame.font.Font(None, 30)
    screen.blit(fonte.render(input_text, True, text2_color), (10 + offset_x, 10 + offset_y))
    screen.blit(fonte.render(hint, True, hint_color_def), (10 + offset_x, 40 + offset_y))


def save_game_settings():
    global scripts, music_playing, best_score, first

    for script in scripts:
        exec(str(start_script(script, 'save')))

    try:
        best_score = max(best_score, wave)

        with open(r'Data/Save/settings.pickle', 'wb') as file:
            pickle.dump(
                f"global music_playing,best_score,first\nbest_score={best_score}\nmusic_playing={music_playing}\nfirst={first}",
                file,
            )
        load_game_settings()

    except Exception:
        pass


def load_game_settings():
    global scripts, music_playing, best_score, first
    for script in scripts:
        exec(str(start_script(script, 'load')))

    best_score = 0
    try:
        music_play_old = music_playing
        with open(r'Data/Save/settings.pickle', 'rb') as file:
            exec(str(pickle.load(file)))

        if music_play_old != music_playing:
            play_music()

    except FileNotFoundError:
        music_playing = False
    return best_score


def play_music(randome = True):
    global music_files, music_playing
    try:
        if randome == True:
            random_file = random.choice(music_files)
            pygame.mixer.music.load(random_file)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        if music_playing:
            pygame.mixer.music.unpause()
        else:   
            pygame.mixer.music.pause()
    except:
        pass

play_music()

def spawn_cats(custom_budget=None, xxx=None, yyy=None):
    global scripts, cats, cats_moneys
    
    for script in scripts:
        exec(str(start_script(script, 'spawn_cats')))
    
    available_cats = [cat_value for cat_value in cats_moneys if cat_value <= custom_budget]
    if not available_cats:
        return

    while custom_budget > 0:
        cat_value = random.choice(available_cats)
        cats_moneys[cat_value].random_buy(xxx, yyy)
        custom_budget -= cat_value
        available_cats = [cat_value for cat_value in cats_moneys if cat_value <= custom_budget]

def dop_dogs():
    global dogs_spawning, health, dogs, cats, cat, dop_budget, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing, dog_damag_boost, cat_works_boost, cats_boost, upping, buy_cats, xexe, mx, dogs_class, scripts, mods_count, catown2, pos, cursor_pos, bonus, new_music, event_game, maxMoney, input_text, hint, running, input_active, ctrl_pressed, shift_pressed
    global multipiller, unmultipiller, summa
    
    while dop_budget > 0 and len(dogs) <= 100:
        dog_name = random.choice(list(dogs_spawning))
        dog_cost = dogs_variants[dog_name]
        dog_mon = dogs_moneys[dog_name]
        dog_class = dogs_class[dog_name]

        if dog_cost <= dop_budget and len(dogs) < 80:
            dog_class.create()
            dop_budget -= dog_cost
        else:
            break

def spawn_dogs(custom_budget=None, xxx=None, yyy=None):
    global dogs_spawning, health, dogs, cats, cat, dop_budget, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing, dog_damag_boost, cat_works_boost, cats_boost, upping, buy_cats, xexe, mx, dogs_class, scripts, mods_count, catown2, pos, cursor_pos, bonus, new_music, event_game, maxMoney, input_text, hint, running, input_active, ctrl_pressed, shift_pressed
    global multipiller, unmultipiller, summa
    online = 0
    multipiller = 2.5
    unmultipiller = 10
    summa = 10

    for script in scripts:
        exec(str(start_script(script, 'spawn_dogs')))

    if custom_budget is not None:
        old_budget = budget
        budget = custom_budget

    new_wey = -1
    if custom_budget is None:
        budget += summa
        budget += round(budget / unmultipiller)

    remaining_budget = budget + dop_budget
    dop_budget = 0
    for_mega_wave -= 1
    if event_game == 1:
        for_mega_wave = 0

    save_game_settings()

    wave += 1
    if plustime < 50 and wave >= 4:
        plustime += 5

    if for_mega_wave == 0:
        remaining_budget = round(remaining_budget * multipiller)
    if for_mega_wave == -1:
        upping = False
        for_mega_wave = 4

    dogs_changed()

    while remaining_budget > 0 and len(dogs) <= 80:
        dog_name = random.choice(list(dogs_spawning))
        dog_cost = dogs_variants[dog_name]
        dog_mon = dogs_moneys[dog_name]
        dog_class = dogs_class[dog_name]

        if dog_cost <= remaining_budget and len(dogs) < 100:
            dog_class.create(xxx, yyy)
            remaining_budget -= dog_cost
            print(f"Готово: {((budget-remaining_budget+0.000000000000000000001) / budget) * 100:.2f}% ({(dop_budget+budget)-remaining_budget} из {dop_budget+budget}, {len(dogs)} собак)")
        else:
            break
    
    if remaining_budget >0:
        dop_budget += remaining_budget
        print(f"В следующей волне будет на {dop_budget} больше бюджета (дополнительный)")

    cat_unblock = False

    if custom_budget is not None:
        budget = old_budget
    else:
        new_wey -= 1


def show_lose_screen():
    global scripts, input_text, hint, running, input_active, ctrl_pressed, shift_pressed, wave
    for script in scripts:
        exec(str(start_script(script, 'lose_screen')))
    font = pygame.font.Font(None, 70)
    text = font.render(translate_text[translate]["lost_right"], True, text2_color)
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
                if wave == 50:
                    play_music()
                started = False
                menu()
                return
            for script in scripts:
                exec(str(start_script(script, 'lose_event')))
        for script in scripts:
            exec(str(start_script(script, 'lose_ui')))
        cmd_ui()

def info(text, position):
    global scripts
    for script in scripts:
        exec(str(start_script(script, 'info')))
    text_surface = font2.render(text, True, info_text2_color)
    text_rect = text_surface.get_rect()

    if position[0] > screen.get_width() / 2:
        text_rect.right = position[0]-25
        text_rect.y = position[1]-10
    else:
        text_rect.topleft = position

    # Добавляем обводку
    outlining(text, info_text_outlining_color, text_rect.x, text_rect.y, 2, font2)
    
    # Рендерим текст
    screen.blit(text_surface, text_rect.topleft)



def game_info():
    global music_playing, input_text, hint, running, input_active, ctrl_pressed, shift_pressed
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back_rect.collidepoint(pos):
                menu()
                return
        fonte = pygame.font.Font(None, 75)
        fonte2 = pygame.font.Font(None, 65)
        for script in scripts:
            exec(str(start_script(script, 'game_info_ui')))
        text = fonte.render(translate_text[translate]["info_play"], True, text2_color)
        text2 = fonte2.render(translate_text[translate]["info_info"], True, text2_color)
        text_rect = text.get_rect(center=(width/2, 70))
        text2_rect = text2.get_rect(center=(width/2+5, 70+200))
        screen.fill(background_color)
        screen.blit(back_image, back_rect)
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)
        cmd_ui()
        pygame.display.flip()
        clock.tick(60)

def menu():
    global music_playing, RPC,new_music, event_game, input_text, hint, running, input_active, ctrl_pressed, shift_pressed, best_score,first,Notifications, translate_text
    Notifications = []
    mods_count = 0
    music_playing = True
    best_wawe = load_game_settings()
    new_music= False
    event_game=None
    try:
        RPC.update(state=translate_text[translate]["RPC_record"]+str(best_wawe), details=translate_text[translate]["RPC_Menu"], large_image="kotdefense", large_text="Kot Defense", small_text=translate_text[translate]["RPC_record"]+str(best_wawe))
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
        loading_rect = play_image.get_rect(topleft=(width/2-200, height/2+130))
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for script in scripts:
                exec(str(start_script(script, 'main_menu_event')))
            CMD_codes(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and play_rect.collidepoint(pos):
                if first == False:
                    start(0)
                else:
                    event_game=-2
                    first = False
                    save_game_settings()
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
                start(0)
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and loading_rect.collidepoint(pos):
                event_game=-1
                start(0)
                return
        fonte = pygame.font.Font(None, 75)
        for script in scripts:
            exec(str(start_script(script, 'main_menu_ui')))
        text = fonte.render(translate_text[translate]["menu_welcome"], True, text2_color)
        fonte = pygame.font.Font(None, 45)
        fonte2 = pygame.font.Font(None, 35)
        text2 = fonte.render(translate_text[translate]["menu_record"]+ str(best_wawe), True, text2_color)
        text4 = fonte2.render(translate_text[translate]["menu_event"], True, text2_color)
        text3 = fonte.render(translate_text[translate]["menu_you"]+str(mods_count) + translate_text[translate]["menu_mods"], True, text2_color)
        text_rect = text.get_rect(center=(width/2, 70))
        text2_rect = (20, height - fonte.get_height() - 10)
        text3_rect = (20, height - fonte.get_height() - 43)
        text4_rect = (width-300, height-90)
        screen.fill(background_color)
        screen.blit(play_image, play_rect)
        screen.blit(loading_image, loading_rect)
        screen.blit(info_image, info_rect)
        screen.blit(discord_image, discord_rect)
        screen.blit(play2_image, play2_rect)
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)
        screen.blit(text4, text4_rect)
        cmd_ui()
        pygame.display.flip()
        clock.tick(60)

def outlining(text, color, text_rect_x, text_rect_y, outlining2, font):
    screen.blit(font.render(text, True, color), (text_rect_x - outlining2, text_rect_y))
    screen.blit(font.render(text, True, color), (text_rect_x + outlining2, text_rect_y))
    screen.blit(font.render(text, True, color), (text_rect_x, text_rect_y - outlining2))
    screen.blit(font.render(text, True, color), (text_rect_x, text_rect_y + outlining2))

def dogs_changed():
    global dogs_spawning, translate, translate_text, translate_dogs, budget, dog_damag_boost, money, health, cat_works_boost, cats_boost, cats, dogs, bad_list, good_list, maxMoney, input_text, hint, running, input_active, ctrl_pressed, shift_pressed
    global dogs_spawning, multipiller, unmultipiller, summa, dogs_while_spawn, dogs_spawn_count, dop_budget

    gebudged = budget + dop_budget
    dogs_spawning.clear()
    dogs_vibran = list(dogs_while_spawn)
    dogs_spawning.extend(dogs_while_spawn)

    dogs_spawn_count2 = dogs_spawn_count
    for dog3 in dogs_variants:
        if dogs_variants[dog3] < gebudged and dog3 not in dogs_vibran:
            dogs_spawn_count2 -= 1

    if dogs_spawn_count2 <= 0:
        dogs_spawn_count2 = dogs_spawn_count
    else:
        dogs_spawn_count2 = dogs_spawn_count - dogs_spawn_count2

    errors_count = 100 + len(dogs_variants)
    while dogs_spawn_count2 > 0 and errors_count > 0:
        dog3 = random.choice(list(dogs_variants))
        if dogs_variants[dog3] < gebudged and dog3 not in dogs_while_spawn and dog3 not in dogs_spawning:
            dogs_spawning.append(dog3)
            dogs_vibran.append(dog3)
            dogs_spawn_count2 -= 1
        errors_count -= 1

    if errors_count <= 0:
        print("ERROR: Не удалось добавить всех собак")

    if wave > 1:
        translated_dogs = [
            translate_dogs[translate].get(dog5, dog5) for dog5 in dogs_spawning
        ]
        NotificationSystem(translate_text[translate]["wave_text_info"] + ", ".join(translated_dogs),time=10,)

    return gebudged

def omg(wave2, online):
    global scripts, dogs_spawning, budget, dog_damag_boost, money, health, cat_works_boost, cats_boost, cats, dogs, bad_list, good_list, maxMoney, input_text, hint, running, input_active, ctrl_pressed, shift_pressed, translate_baffs
    for script in scripts:
        exec(str(start_script(script, 'bonus')))
    
    dog_damag_boost = 0
    ggbudget = round(budget / 5)

    # Выбираем 3 случайных разных элемента из good_list
    g1, g2, g3 = random.sample(list(good_list), 3)

    # Выбираем 3 случайных разных элемента из bad_list
    b1, b2, b3 = random.sample(list(bad_list), 3)

    g1t = translate_baffs[translate][g1]
    g2t = translate_baffs[translate][g2]
    g3t = translate_baffs[translate][g3]

    b1t = translate_baffs[translate][b1]
    b2t = translate_baffs[translate][b2]
    b3t = translate_baffs[translate][b3]

    starte = True
    loade = True
    clock = pygame.time.Clock()
    timer = 60 * 3

    for script in scripts:
        exec(str(start_script(script, 'bonus_loade')))

    while loade:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starte = False
                loade = False

            for script in scripts:
                exec(str(start_script(script, 'bonus_loade_event')))

        for script in scripts:
            exec(str(start_script(script, 'bonus_loade_ui')))

        loading_text(translate_text[translate]["load_baff_and_debaff"])
        pygame.display.flip()
        timer -= 1

        if timer <= 0:
            loade = False

        clock.tick(60)

    baffe = True

    while starte:
        for script in scripts:
            exec(str(start_script(script, 'bonus_ui')))

        rect1 = pygame.Rect(width // 2 - 300, height // 2 - 75, 150, 150)
        rect2 = pygame.Rect(width // 2, height // 2 - 75, 150, 150)
        rect3 = pygame.Rect(width // 2 + 300, height // 2 - 75, 150, 150)

        pos = pygame.mouse.get_pos()

        screen.fill(background_color)

        pygame.draw.rect(screen, red_btn_color, rect1)
        pygame.draw.rect(screen, green_btn_color, rect2)
        pygame.draw.rect(screen, blue_btn_color, rect3)

        font = pygame.font.Font(None, 100)
        text = font.render(
            translate_text[translate]["buff_select"]
            if baffe
            else translate_text[translate]["debuff_select"],
            True,
            text2_color,
        )
        text_rect = text.get_rect(center=(width // 2, 130))
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
                elif rect2.collidepoint(pos):
                    b = b2
                    g = g2
                elif rect3.collidepoint(pos):
                    b = b3
                    g = g3

                if rect1.collidepoint(pos) or rect2.collidepoint(pos) or rect3.collidepoint(pos):
                    if not baffe:
                        if b == "debaff_hard":
                            budget += ggbudget
                        elif b == "debaff_all_cats_damage":
                            cats_all2 = []
                            while cats_all2 != cats:
                                for cat9 in cats:
                                    if cat9 not in cats_all2:
                                        cat9.bump((15 / 100) * cat9.maxhealth)
                                        cats_all2.append(cat9)
                        elif b == "debaff_maxium_money":
                            money -= round((15 / 100) * money)
                        elif b == "debaff_frogs":
                            zzzcats = round(len(cats) * 0.2)
                            random_cats = random.sample(cats, zzzcats)
                            for cat2 in random_cats:
                                cat2.cwa()

                        game(online)
                        return
                    else:
                        if g == "baff_maxium_money":
                            money += round((10 / 100) * money)
                        elif g == "baff_main_heart":
                            health += 1
                        elif g == "baff_lives_all_cats":
                            cats_all2 = []
                            while cats_all2 != cats:
                                for cat9 in cats:
                                    if cat9 not in cats_all2:
                                        cat9.bump(((10 / 100) * cat9.maxhealth) * -1)
                                        cats_all2.append(cat9)
                        elif g == "baff_works":
                            cat_works_boost += 5
                        elif g == "baff_shield":
                            shild = Cat(random.randint(0, width - 60),random.randint(115, height - 255),0,2000,0,5000,0,0,0,r"Data\Img\cat_shield.png",60,60,)
                        baffe = False

        if baffe:
            if rect1.collidepoint(pos):
                info(g1t, (pos[0] + 15, pos[1] + 5))
            elif rect2.collidepoint(pos):
                info(g2t, (pos[0] + 15, pos[1] + 5))
            elif rect3.collidepoint(pos):
                info(g3t, (pos[0] + 15, pos[1] + 5))
        else:
            if rect1.collidepoint(pos):
                info(b1t, (pos[0] + 15, pos[1] + 5))
            elif rect2.collidepoint(pos):
                info(b2t, (pos[0] + 15, pos[1] + 5))
            elif rect3.collidepoint(pos):
                info(b3t, (pos[0] + 15, pos[1] + 5))

        pygame.display.flip()
        clock.tick(60)

def new_cat_unblock():
    global buy_cats, xexe, mx, input_text, hint, running, input_active, ctrl_pressed, shift_pressed
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
    global final_wave, end_boss, training_step, translate, translate_text, translate_dogs, start_budget, boss_steps, health, Number, TimeStart, event_game, dogs, cats, cat, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing, dog_damag_boost, cat_works_boost, cats_boost, upping, buy_cats, xexe, mx, dogs_class, __dangerous_keywords_pp2irooodjhjjjkjkn, scripts, bad_list, good_list, catown2, bonus, new_music, buy_no_cats, event_game, maxMoney, cat_unblock, cats_moneys, cats_dogs_spawns
    global dogs_spawning, Notifications, multipiller, unmultipiller, summa, dogs_while_spawn, dogs_spawn_count, dop_budget
    loading_text(translate_text[translate]["load_game"])
    for script in scripts:
        exec(str(start_script(script, 'start')))
    del_cat = False
    boss_steps = 0
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
    dogs_spawning = []
    dog_damag_boost = 0
    cat_works_boost = 0
    cats_boost = 100
    dogs_class = {}
    dogs_variants = {}
    dogs_moneys = {}
    cats_moneys = {}
    scripts = []
    bad_list = []
    good_list = []
    start_budget = 4
    budget = start_budget
    if event_game == 1:
        budget = 10
        money = 120
    upping = False
    pause = False
    end_boss = False
    
    frame_count = 0
    frame_count2 = 0
    frame_count3 = 0
    frame_count4 = 0
    plustime = 0
    new_wey = 60
    wave = 1
    bonus = False
    for_mega_wave = 4
    TimeStart = int(pygame.time.get_ticks()/1000)
    Number = 0
    online = 0
    multipiller = 2.5
    unmultipiller = 10
    summa = 10
    dop_budget = 0
    
    if event_game == -1:
        loading_game(None)
    
    new_dog = CreateDog(3, 1, 'Dog', 2, 2, 1, 1, 1, 0, r'Data\Img\Dog1.png', 60, 60)
    new_dog = CreateDog(7, 5, 'FastDog', 1, 4, 1, 1, 0.5, 0, r'Data\Img\Dog1.png', 50, 50)
    new_dog = CreateDog(7, 5, 'BigDog', 6, 1, 1, 1, 1, 0, r'Data\Img\Dog1.png', 70, 70)
    new_dog = CreateDog(20, 10, 'KillerDog', 4, 3, 4, 1, 2, 0, r'Data\Img\Dog1.png', 55, 55)
    new_dog = CreateDog(100, 65, 'KiberDog', 40, 1, 6, 1, 2, 0, r'Data\Img\Dog2.jpg', 65, 65)
    new_dog = CreateDog(300, 220, 'BoomDog', 50, 5, 20, 2, 0.01, 1, r'Data\Img\Dog3.png', 60, 60)
    new_dog = CreateDog(100, 50, 'NecDog', 15, 1, 2, 3, 3, 0, r'Data\Img\Dog1.png', 80, 80)
    new_dog = CreateDog(5000, 1500, 'MehoDog', 320, 1, 30, 6, 2, 0, r'Data\Img\Dog4.png', 60, 60)
    new_dog = CreateDog(1000, 1500, 'BomberDog', 400, 2, 100, 9, 2, 2, r'Data\Img\Dog5.png', 60, 60)
    new_dog.damagecats.append(1)
    new_dog.damagecats.append(2)
    new_dog = CreateDog(10000, 8400, 'TrojanDog', 1000, 1, 0, 10, 5, 0, r'Data\Img\Dog6.png', 120, 120) 
    new_dog = CreateDog(10, 100, 'GhostDog', 10, 2, 2, 9, 1.5, 0, r'Data\Img\Dog7.png', 70, 70)
    new_dog = CreateDog(30, 300, 'Woolf', 20, 2, 4, 11, 2.5, 0, r'Data\Img\Dog1.png', 70, 70)
    new_dog = CreateDog(600, 1000, 'MedicDog', 100, 1, 1, 12, 3, 0, r'Data\Img\Dog2.jpg', 70, 70)
    new_dog = CreateDog(11000, 10000, 'DogTitan', 5000, 1, 20, 1, 5, 0, r'Data\Img\Dog1.png', 150, 150)
    new_dog = CreateDog(21000, 20000, 'ManiakDog', 50, 9, 30, 1, 0.05, 0, r'Data\Img\Dog8.png', 40, 40)
    new_buy_cat = BuyCat(10, f'official_kot_defense_info1', 130, 4, 3, 1, 1, 1, 0, 10, r'Data\Img\Cat1.png', 60, 60, None)
    new_buy_cat.targetDeff = 0
    new_buy_cat = BuyCat(20, "official_kot_defense_info2", 0, 40, 0, 1, 0, 1, 0, 45, r'Data\Img\Cat2.png', 60, 60, None)
    new_buy_cat.targetDeff = -1
    new_buy_cat = BuyCat(200, f'official_kot_defense_info3', 400, 6, 3, 3, 10, 1, 20, -1, r'Data\Img\Cat3.png', 60, 60, None)
    new_buy_cat.targetDeff = 1
    new_buy_cat = BuyCat(80, f'official_kot_defense_info4', 150, 20, 3, 0.4, 1.5, 1, 10, -1, r'Data\Img\Cat4.png', 60, 60, None)
    new_buy_cat.targetDeff = 2
    new_buy_cat = BuyCat(70, f'official_kot_defense_info5', 0, 15, 0, -1, 10, 2, 5, -1, r'Data\Img\Cat5.png', 60, 60, None)
    new_buy_cat.targetDeff = -1
    new_buy_cat = BuyCat(5000, f'official_kot_defense_info6', 0, 80, 0, 1, 0.1, 3, 25, -1, r'Data\Img\Cat6.png', 60, 60, None)
    new_buy_cat.targetDeff = -1
    new_buy_cat = BuyCat(300, f'official_kot_defense_info7', 160, 60, 9999, 3.2, 0.3, 4, 25, -1, r'Data\Img\Cat7.png', 60, 60, None)
    new_buy_cat.targetDeff = -1
    new_buy_cat = BuyCat(600, f'official_kot_defense_info8', 300, 60, 1, 0.3, 150, 1, 15, -1, r'Data\Img\Cat8.png', 60, 60, None)
    new_buy_cat.targetDeff = 0
    new_buy_cat.blacklist.append(1)
    new_buy_cat.blacklist.append(2)
    new_buy_cat = BuyCat(500, f'official_kot_defense_info9', 500, 30, 1, 3, 100, 1, 40, -1, r'Data\Img\Cat9.png', 120, 60, r'Data\Img\Cat9_ico.jpg')
    new_buy_cat.targetDeff = 1
    new_buy_cat = BuyCat(10000, "official_kot_defense_info10", 0, 1000, 0, 60, 5, 5, 45, -1, r'Data\Img\Cat10.png', 60, 60, None)
    new_buy_cat.targetDeff = -1
    new_buy_cat = BuyCat(600, f'official_kot_defense_info11', 200, 80, 9999, 0.6, 0.1, 4, 35, -1, r'Data\Img\Cat11.png', 60, 60, None)
    new_buy_cat.targetDeff = -1
    new_buy_cat = BuyCat(50, f'official_kot_defense_info12', 0, 1, 1, 3, 25, 5, 5, -1, r'Data\Img\Cat12.png', 60, 60, None)
    new_buy_cat.targetDeff = -1
    new_buy_cat = BuyCat(1000, f'official_kot_defense_info13', 500, 20, 6, 3, 3, 1, 45, -1, r'Data\Img\Cat13.png', 60, 60, None)
    new_buy_cat.targetDeff = 2
    new_buy_cat = BuyCat(100, f'official_kot_defense_info14', 0, 1, 1, -1, 98, 6, 25, -1, r'Data\Img\Cat14.png', 60, 60, None)
    new_buy_cat.targetDeff = -1
    new_buy_cat = BuyCat(300, f'official_kot_defense_info15', 0, 1, 1, -1, 98, 7, 40, -1, r'Data\Img\Cat15.png', 60, 60, None)
    new_buy_cat.targetDeff = -1
    new_buy_cat = BuyCat(12000, f'official_kot_defense_info16', 600, 5, 99999999, 0.5, 0.5, 8, 30, -1, r'Data\Img\Cat16.png', 120, 120, None)
    new_buy_cat.targetDeff = -1
    new_buy_cat = BuyCat(15000, f'official_kot_defense_info17', 80, 50, 30, 0.1, 10, 1, 30, -1, r'Data\Img\Cat17.png', 40, 40, None)
    new_buy_cat.targetDeff = 0

    bad_list.extend(['debaff_all_cats_damage', 'debaff_maxium_money', 'debaff_frogs'])
    good_list.extend(['baff_maxium_money', 'baff_main_heart', 'baff_lives_all_cats', 'baff_works'])
    
    dogs_while_spawn = ["Dog"]
    dogs_spawn_count = 7
    dogs_changed()
    
    final_wave = [
        {
            "type": 0, 
            "step": 0,
            "time": 20,
            "code": {
                "dog": "TrojanDog", 
                "x": -100, 
                "y": 130, 
                "y_end": height-255, 
                "x_random": 0,
                "y_random": (random.randint(-100, 100) / 10), 
                "x_add": 0,
                "y_add": 120,
                "for_x_set": None,
                "for_y_set": None,
                "count": 1,
                "last_wave": False,
                "next_wave": False
            }
        },
        {
            "type": 0, 
            "step": 1,
            "time": 40,
            "code": {
                "dog": "BomberDog", 
                "x": -60, 
                "y": 130, 
                "y_end": height-255, 
                "x_random": 0,
                "y_random": 0, 
                "x_add": -30,
                "y_add": 60,
                "for_x_set": None,
                "for_y_set": None,
                "count": 1,
                "last_wave": False,
                "next_wave": False
            }
        },
        {
            "type": 0, 
            "step": 2,
            "time": 50,
            "code": {
                "dog": "TrojanDog", 
                "x": -100, 
                "y": 130, 
                "y_end": height-255, 
                "x_random": 0,
                "y_random": (random.randint(-100, 100) / 10), 
                "x_add": 0,
                "y_add": 130,
                "for_x_set": None,
                "for_y_set": None,
                "count": 1,
                "last_wave": False,
                "next_wave": False
            }
        },
        {
            "type": 0, 
            "step": 3,
            "time": 60,
            "code": {
                "dog": "KiberDog", 
                "x": -60, 
                "y": 140, 
                "y_end": height-255, 
                "x_random": (random.randint(-100, 100) / 10),
                "y_random": (random.randint(-100, 100) / 10), 
                "x_add": "((i+1) * -120)",
                "y_add": 60,
                "for_x_set": None,
                "for_y_set": None,
                "count": 2,
                "last_wave": False,
                "next_wave": False
            }
        },
        {
            "type": 0, 
            "step": 4,
            "time": 90,
            "code": {
                "dog": "BoomDog", 
                "x": -60, 
                "y": 130, 
                "y_end": height-255, 
                "x_random": (random.randint(-100, 100) / 10),
                "y_random": (random.randint(-100, 100) / 10), 
                "x_add": 0,
                "y_add": 60,
                "for_x_set": "((i+1) * -120)",
                "for_y_set": 130,
                "count": 4,
                "last_wave": False,
                "next_wave": True
            }
        },
        {
            "type": 0, 
            "step": 5,
            "time": 90,
            "code": {
                "dog": "BomberDog", 
                "x": -350, 
                "y": 130, 
                "y_end": height-255, 
                "x_random": 0,
                "y_random": 0, 
                "x_add": -30,
                "y_add": 60,
                "for_x_set": None,
                "for_y_set": None,
                "count": 1,
                "last_wave": False,
                "next_wave": True
            }
        },
        {
            "type": 0, 
            "step": 6,
            "time": 90,
            "code": {
                "dog": "BomberDog", 
                "x": -350, 
                "y": 595, 
                "y_end": 130, 
                "x_random": 0,
                "y_random": 0, 
                "x_add": -30,
                "y_add": -60,
                "for_x_set": None,
                "for_y_set": None,
                "count": 1,
                "last_wave": False,
                "next_wave": True
            }
        },
        {
            "type": 1, 
            "step": 7,
            "time": 110,
            "code": {
                "budget": 40000,
                "last_wave": False,
                "next_wave": False
            }
        },
        {
            "type": 1, 
            "step": 8,
            "time": 125,
            "code": {
                "budget": 40000,
                "last_wave": False,
                "next_wave": False
            }
        },
        {
            "type": 0, 
            "step": 9,
            "time": 140,
            "code": {
                "dog": "BoomDog", 
                "x": -60, 
                "y": 130, 
                "y_end": height-255, 
                "x_random": (random.randint(-100, 100) / 10),
                "y_random": (random.randint(-100, 100) / 10), 
                "x_add": 0,
                "y_add": 60,
                "for_x_set": "((i+1) * -70)",
                "for_y_set": 130,
                "count": 4,
                "last_wave": False,
                "next_wave": True
            }
        },
        {
            "type": 0, 
            "step": 10,
            "time": 150,
            "code": {
                "dog": "BomberDog", 
                "x": -350, 
                "y": 130, 
                "y_end": height-255, 
                "x_random": 0,
                "y_random": 0, 
                "x_add": -30,
                "y_add": 60,
                "for_x_set": None,
                "for_y_set": None,
                "count": 1,
                "last_wave": False,
                "next_wave": True
            }
        },
        {
            "type": 0, 
            "step": 11,
            "time": 150,
            "code": {
                "dog": "BomberDog", 
                "x": -350, 
                "y": 595, 
                "y_end": 130, 
                "x_random": 0,
                "y_random": 0, 
                "x_add": -30,
                "y_add": -60,
                "for_x_set": None,
                "for_y_set": None,
                "count": 1,
                "last_wave": False,
                "next_wave": True
            }
        },
        {
            "type": 1, 
            "step": 12,
            "time": 125,
            "code": {
                "budget": 50000,
                "last_wave": True,
                "next_wave": False
            }
        },
        {
            "type": 0, 
            "step": 13,
            "time": 50,
            "code": {
                "dog": "ManiakDog", 
                "x": -100, 
                "y": 130, 
                "y_end": height-275, 
                "x_random": 0,
                "y_random": (random.randint(-100, 100) / 10), 
                "x_add": 0,
                "y_add": 30,
                "for_x_set": None,
                "for_y_set": None,
                "count": 1,
                "last_wave": False,
                "next_wave": False
            }
        }
    ]
    
    #ОБУЧЕНИЕ
    if event_game == -2:
        if training_step == 0:
            budget = 1
            money = 0
            new_wey = 9999999999999
            NotificationSystem("Прочитай описания котов в нижнем меню (наведите курсор на кота)", (0, 100, 000), 30, 2, 2, 10)
            CMD_waiting("money 10", 12)
            NotificationSystem("Поставьте первого кота на поле", (0, 100, 000), 30, 2, 2, 10, waiting = 12)
            NotificationSystem("Нажмите СКИП", (0, 100, 000), 30, 2, 2, 5, waiting = 22)
    
    folder_path = r'Data\\Mods\\'
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name == 'main.py':
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    code = file.read()
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
    global music_playing, event_game, input_text, hint, running, input_active, ctrl_pressed, shift_pressed
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
        loading_text(translate_text[translate]["load_texts"])
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
            text = fonte.render(translate_text[translate]["win_text_event_1"]+str(mywincode)+translate_text[translate]["win_text_event_2"], True, text2_color)
        else:
            text = fonte.render(translate_text[translate]["win_text_game"], True, text2_color)
        play_music()
        text_rect = text.get_rect(center=(width/2, height/2))
        screen.fill(background_color)
        screen.blit(text, text_rect)
        cmd_ui()
        pygame.display.flip()
        clock.tick(60)

def game(online):
    global shift_pressed, dop_budget, translate, translate_text, translate_dogs, Notifications, training_step, final_wave, end_boss, boss_steps, health, TimeStart, Number, dogs, cats, cat, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing, dog_damag_boost, cat_works_boost, cats_boost, upping, buy_cats, xexe, mx, dogs_class, scripts, mods_count, catown2, pos, cursor_pos, bonus, new_music, event_game, maxMoney, input_text, hint, running, input_active, ctrl_pressed, shift_pressed, stop_game, pos
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
    exit_rect = play_image.get_rect(topleft=(width-350, height-120))
    for script in scripts:
        exec(str(start_script(script, 'game')))
    if new_music == True:
        try:
            if event_game == 1:
                pygame.mixer.music.load(event1_music)
                play_music(False)
            else:
                play_music()
            new_music = False
        except:
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            CMD_codes(event)
            for script in scripts:
                exec(str(start_script(script, 'game_event')))
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
            if pygame.mouse.get_pressed()[0] and event.type == pygame.MOUSEBUTTONDOWN and not pause:
                for cat2 in cats:
                    cat2.targetChanged(pos)
            if pygame.mouse.get_pressed()[0] and ctrl_pressed and catown is not None:
                try:
                    catown.handle_mouse_click(pos, 1)
                except:
                    pass
            elif pygame.mouse.get_pressed()[0] and shift_pressed and catown is not None:
                if custom_X2 == None:
                    custom_X2 = pos[0]
                    custom_Y2 = pos[1]
                    line_X = custom_X2-round(custom_X2 / catown.size_x) * catown.size_x
                    line_Y = custom_Y2-round(custom_Y2 / catown.size_y) * catown.size_y
                dx = abs(custom_X2 - pos[0])
                dy = abs(custom_Y2 - pos[1])
                try:
                    if dx > dy:
                        catown.handle_mouse_click((round(pos[0] / catown.size_x) * catown.size_x+line_X, custom_Y2), 1)
                    else:
                        catown.handle_mouse_click((custom_X2, round(pos[1] / catown.size_y) * catown.size_y+line_Y), 1)
                except:
                    pass
            elif pygame.mouse.get_pressed()[0] and catown is not None and event.type == pygame.MOUSEBUTTONDOWN and not pause:
                catown.handle_mouse_click(pos, 1)
            if pygame.mouse.get_pressed()[2] and ctrl_pressed:
                for cat in cats:
                    if cat.rect.collidepoint(pos):
                        if cat.follow_mouse == False:
                            cat.sell(0.5)
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] and not pause:
                for cat in cats:
                    if cat.rect.collidepoint(pos):
                        if cat.follow_mouse == False:
                            cat.sell(0.5)
            if not shift_pressed:
                custom_X2 = None
                custom_Y2 = None
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
                if skip_rect.collidepoint(pos) and len(dogs) == 0 and event_game != -2:
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
                if event_game == -2:
                    if skip_rect.collidepoint(pos) and training_step == 0 and len(cats) > 0 and len(dogs) == 0:
                        spawn_dogs(1, -80, height//2)
                        training_step += 1
                        CMD_waiting("money 20", 8)
                        NotificationSystem("Поставьте ещё 2 кота", (0, 100, 0), 30, 2, 2, 10, waiting = 8)
                        new_wey = 99999999
                    if skip_rect.collidepoint(pos) and training_step == 1 and len(dogs) == 0 and len(cats) > 2:
                        spawn_dogs(6)
                        training_step += 1
                        NotificationSystem("На собак можно нажимать тем самым нанося 0.1 урона", (100, 0, 0), 50, 2, 2, 10, waiting = 3)
                    if skip_rect.collidepoint(pos) and training_step == 3 and len(dogs) == 0 and len(cats) > 0 and wave == 4:
                        spawn_dogs(100)
                        new_wey = 99999999
                        CMD_waiting("mega_wave", 0)
                        training_step += 1
            if pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        pause = False
                    if event.button == 1:
                        for checkbox in checkboxes:
                            if checkbox.x <= event.pos[0] <= checkbox.x + 20 and checkbox.y <= event.pos[1] <= checkbox.y + 20:
                                checkbox.toggle()
                        if exit_rect.collidepoint(pos):
                            menu()
                            return
        
        if not pause:
            if dop_budget > 0 and len(dogs) < 80:
                dop_dogs()
            if maxMoney < money:
                maxMoney = money
            if event_game == 1:
                screen.fill(event1_background_color)
            else:
                if wave == 50:
                    screen.fill(boss_background_color)
                else:
                    screen.fill(background_color)
            if stop_game == False:
                for dog in list(dogs):
                    dog.move()
                    if dog.rect.x > width+dog.size_x/2:
                        if event_game != -2:
                            money += 100
                        health -= 1
                        dogs.remove(dog)
                        del dog
                    elif dog.mega == 14 and dog.rect.x < -60:
                        dogs.remove(dog)
                        del dog
            
            if event_game == 1:
                pygame.draw.rect(screen, event1_down_menu_cats, (0, height-130, 1400, 130))
            else:
                pygame.draw.rect(screen, down_menu_cats, (0, height-130, 1400, 130))
            if event_game == 1:
                pygame.draw.rect(screen, event1_down_menu_cats, (0, 115, 1400, 5))
            else:
                pygame.draw.rect(screen, down_menu_cats, (0, 115, 1400, 5))
            
            pygame.draw.rect(screen, skip_button_color, (width-120, height-118, 100, 100))
            cat_mon3 = fontSkip.render(translate_text[translate]["skip"], True, skip_button_text_color)
            screen.blit(cat_mon3, (width-101, height-84))
            
            for cat in cats:
                cat.remove_dogs_periodically(None)
            for dog in list(dogs):
                dog.attack(None)
            for cmd_linee in cmd_queue:
                cmd_linee.update()
            
            if event_game == -2:
                if training_step == 2 and len(dogs) == 0:
                    new_wey = 99999999
                    NotificationSystem("Котов можно продать на ПКМ", (0, 100, 0), 35, 2, 2, 7, waiting = 1)
                    NotificationSystem("Каждые 5 волн будут добавляться новые коты в ваше меню", (0, 100, 0), 30, 2, 2, 8, waiting = 8)
                    NotificationSystem("А так же каждые 5 волн будут <Мега волны> где всё количество собак умножается в два раза", (0, 100, 0), 30, 2, 2, 10, waiting = 17)
                    CMD_waiting("health 15", 27)
                    CMD_waiting("money 500", 27)
                    CMD_waiting("kill all", 27)
                    CMD_waiting("wave 4", 27)
                    NotificationSystem("Постройте надёжную защиту, так как мы попробуем отбить <мега волну>", (100, 0, 0), 30, 2, 2, 10, waiting = 27)
                    NotificationSystem("Если зажать CTRL можно сразу делать клон кота", (0, 100, 0), 35, 2, 2, 10, waiting = 37)
                    NotificationSystem("Ну и аналогично можно удалять котов зажав CTRL", (0, 100, 0), 30, 2, 2, 10, waiting = 47)
                    NotificationSystem("А если зажать SHIFT и потянуть в любую сторону можно построить идеальную стену из котов", (0, 100, 0), 30, 2, 2, 10, waiting = 57)
                    NotificationSystem("Как только будите готовы нажмите СКИП", (0, 100, 0), 30, 2, 2, 10, waiting = 67)
                    training_step += 1
                elif training_step == 4 and len(dogs) == 0:
                    NotificationSystem("Забыл тебе сказать что после <Мега волны> происходит выбор одного <баффа> и <Дебаффа>", (0, 100, 0), 35, 2, 2, 10, waiting = 1)
                    NotificationSystem("<Бафф> поможет вам играть дальше, а <Дебафф> затруднит", (0, 100, 0), 35, 2, 2, 9, waiting = 11)
                    NotificationSystem("И кстати, новые коты в нижнем меню, ознакомься с ними", (0, 100, 0), 35, 2, 2, 10, waiting = 20)
                    NotificationSystem("Чтобы пройти всю игру необходимо победить 50 волн", (100, 0, 0), 40, 2, 2, 10, waiting = 33)
                    NotificationSystem("Но это будет не скоро :)", (0, 100, 0), 30, 2, 2, 4, waiting = 43)
                    NotificationSystem("Если у вас будут собаки которые летают их нужно подбить котом ПВО он будет за 600$ на 15-й волне", (0, 100, 0), 30, 2, 2, 13, waiting = 47)
                    NotificationSystem("Ну и расскажу по мелочам, на эту игру можно ставить <моды> и <дата-паки>", (0, 100, 0), 30, 2, 2, 10, waiting = 60)
                    NotificationSystem("Всё проверенное есть на нашем <DISCORD> сервере (его можно найти в главном меню)", (0, 100, 0), 30, 2, 2, 10, waiting = 70)
                    NotificationSystem("Выключить музыку можно в паузе (сверху-справа) и там же выйти в меню", (0, 100, 0), 30, 2, 2, 10, waiting = 80)
                    NotificationSystem("Дальше будет информация необязательная для обычного игрока, чтобы закончить обучение перезайдите в бой", (0, 100, 0), 30, 2, 2, 10, waiting = 90)
                    NotificationSystem("В игре присутствует консоль, чтобы её вкл/выкл нажмите Shift+Ctrl+Space", (0, 100, 0), 30, 2, 2, 10, waiting = 100)
                    NotificationSystem("Дальше можно печатать команды, их можно узнать нажимая на стрелочки верх/низ (в поиске должно быть пусто)", (0, 100, 0), 30, 2, 2, 10, waiting = 110)
                    NotificationSystem("Спасибо за игру! Чтобы закончить обучение перезайдите в бой", (0, 100, 0), 30, 2, 2, 10, waiting = 120)
                    training_step += 1
            
            if online == 0:
                screen.blit(pause_image, (width-55, 10))
            
            if stop_game == False:
                frame_count += 1
            if wave == 50:
                boss_time += 1
            elif event_game == 1 and wave == 30 and stop_game == False:
                boss_time += 1
            
            if frame_count >= 60:
                if len(dogs) == 0:
                    new_wey -= 1
                try:
                    if for_mega_wave >0:
                        RPC.update(state=f"{money} 💵 {health} ❤", details=f"Волна {wave}", large_image="kotdefense", large_text="Kot Defense", small_text=f"{money} 💵 {health} ❤")
                    else:
                        RPC.update(state=f"{money} 💵 {health} ❤", details=f"Мега волна {wave}", large_image="kotdefense", large_text="Kot Defense", small_text=f"{money} 💵 {health} ❤")
                except:
                    pass
                frame_count = 0
            if len(dogs) == 0 and cat_unblock == False:
                cat_unblock = True
                for bc in list(buy_no_cats):
                    bc.spawn()
                for bc in list(buy_cats):
                    bc.spawn()
            if stop_game == False:
                if boss_time == 0 or wave > 50:
                    xexexe = True
                    if wave == 49 and len(dogs) == 0:
                        wave += 1
                    if len(dogs) == 0 and wave != 50:
                        if new_wey < 0 and online != 2:
                            new_wey = 60
                        elif new_wey == 0:
                            for cat in cats:
                                cat.remove_dogs_periodically(-60)
                            for dog in list(dogs):
                                dog.attack(-60)
                            spawn_dogs()
                            if event_game == 1:
                                zzzcats = round(len(cats) * 0.05)
                                random_cats = random.sample(cats, zzzcats)
                                for cat2 in random_cats:
                                    cat2.cwa()
                            try:
                                save_game(fr"Data\Save\{TimeStart}_{Number}_auto_save")
                            except:
                                pass
                            Number += 1
                else:
                    if xexexe == True and wave==50:
                        try:
                            pygame.mixer.music.load(music_path2)
                            play_music(False)
                        except:
                            pass
                        xexexe = False
                    
                    next_wave = False
                    attapts_spawn = 200
                    for wave_data in final_wave:
                        test = len(dogs) == 0 and wave_data["step"]>=boss_steps
                        if wave_data["time"]*60 == boss_time or test or next_wave:
                            boss_steps += 1
                            if wave_data["type"] == 0:
                                xb = wave_data["code"]["x"]
                                yb = wave_data["code"]["y"]
                                for i in range(wave_data["code"]["count"]):
                                    if wave_data["code"]["for_x_set"] != None:
                                        if isinstance(wave_data["code"]["for_x_set"], str):
                                            xb =eval(wave_data["code"]["for_x_set"])
                                        else:
                                            xb = wave_data["code"]["for_x_set"]
                                    if wave_data["code"]["for_y_set"] != None:
                                        if isinstance(wave_data["code"]["for_y_set"], str):
                                            yb = eval(wave_data["code"]["for_y_set"])
                                        else:
                                            yb = wave_data["code"]["for_y_set"]
                                    while yb < wave_data["code"]["y_end"] and attapts_spawn > 0:
                                        attapts_spawn -= 1
                                        dog_class = dogs_class[wave_data["code"]["dog"]]
                                        dog_class.create(xb, yb)
                                        if isinstance(wave_data["code"]["x_add"], str):
                                            xb +=eval(wave_data["code"]["x_add"])
                                        else:
                                            xb += wave_data["code"]["x_add"]
                                        if isinstance(wave_data["code"]["y_add"], str):
                                            yb +=eval(wave_data["code"]["y_add"])
                                        else:
                                            yb += wave_data["code"]["y_add"]
                            elif wave_data["type"] == 0:
                                spawn_dogs(wave_data["code"]["budget"])
                            next_wave = wave_data["code"]["next_wave"]
                            end_boss = wave_data["code"]["last_wave"]
                    
                    if end_boss and len(dogs) == 0:
                        wave += 1
                        if online == 0:
                            win(online)
                            return
            
            for cat in cats:
                cat.draw(screen, online)
                if online == 2:
                    cat.update(pos)
                else:
                    cat.update(pos)
            for dog2 in dogs:
                if dog2.rect.center[0] > (dog2.size_x/2)*-1:
                    dog2.update()
                
            for bc in buy_cats:
                bc.draw()
            if xexe >0:
                screen.blit(btn2_image, (20, height-90))
                screen.blit(btn_image, (1140, height-90))
            for bc in buy_cats:
                bc.info_cat(pos)
            
            for script in scripts:
                exec(str(start_script(script, 'game_game')))
                
            outlining2 = 3
            text = "❤️ "+str(health)
            
            health_text = font.render(text, True, text_color)
            screen.blit(health_text, (10, 2))
            heart_text2 = font.render("❤️", True, heart_color)
            screen.blit(heart_text2, (10, 2))
            
            text = "💵 "+str(money)
            money_text = font.render(text, True, text_color)
            screen.blit(money_text, (10, 34))
            
            money_text2 = font.render("💵", True, money_color)
            screen.blit(money_text2, (10, 34))
            cmd_ui(0, 120)
            
            for cat in cats:
                cat.info_ca(screen, pos)
            for dog in dogs:
                dog.info_do(pos)
            if for_mega_wave >0:
                text = "Wave: "+str(wave)
                wave_text = font.render(text, True, text_color)
                screen.blit(wave_text, (10, 66))
            else:
                text = "Mega wave: "+str(wave)
                wave_text = font.render(text, True, text_color)
                screen.blit(wave_text, (10, 66))
                if upping == False and len(dogs) == 0 and online == 0 and event_game != 1 and stop_game == False:
                    bonus = True
                    upping = True
                    for cat in cats:
                        cat.remove_dogs_periodically(-120)
                    for dog in list(dogs):
                        dog.attack(-120)
                    omg(wave, online)
                    return
            for noti in Notifications:
                noti.update()
            for script in scripts:
                exec(str(start_script(script, 'game_ui')))
        else:
            for script in scripts:
                exec(str(start_script(script, 'game_pause')))
            fonte = pygame.font.Font(None, 75)
            text = fonte.render(translate_text[translate]["pause"], True, text2_color) #350, 120
            text_rect = text.get_rect(center=(width/2, height/2))
            screen.fill(background_color)
            screen.blit(text, text_rect)
            screen.blit(exit_image, exit_rect)
            for checkbox in checkboxes:
                checkbox.draw(screen)
            pygame.display.flip()
            started = True
        pygame.display.flip()
        clock.tick(60)
        if health <=0:
            for script in scripts:
                exec(str(start_script(script, 'game_die')))
            show_lose_screen()
            return

global input_text, running, input_active, ctrl_pressed, shift_pressed, checkboxes, CMD_commands, hint, CMD_line
input_text= ''
running = True
input_active = False
ctrl_pressed = False
shift_pressed = False
hint = ""
CMD_line = 0

CMD_commands = [
    {
        "info": translate_text[translate]["cmd_cure"],
        "vals": {
            "health": None,
            "int": "Int value",
        }
    },
    {
        "info": translate_text[translate]["cmd_cure"],
        "vals": {
            "regen": None,
            "type": "cats/dogs/all",
        }
    },
    {
        "info": translate_text[translate]["cmd_spawn"],
        "vals": {
            "spawn": None,
            "dogs": "Dog names example: Dog,BoomDog",
            "x": "*Int value,String X",
            "y": "*Int value,String Y",
        }
    },
    {
        "info": translate_text[translate]["cmd_random"],
        "vals": {
            "random": None,
            "type": "*cats/dogs/all",
            "x": "*Int value,String X",
            "y": "*Int value,String Y",
            "budget": "*Int value,Budget on which to buy game",
        }
    },
    {
        "info": translate_text[translate]["cmd_money"],
        "vals": {
            "money": None,
            "int": "Int value",
        }
    },
    {
        "info": translate_text[translate]["cmd_wave"],
        "vals": {
            "wave": None,
            "int": "Int value",
        }
    },
    {
        "info": translate_text[translate]["cmd_budget"],
        "vals": {
            "wave": None,
            "int": "Int value",
        }
    },
    {
        "info": translate_text[translate]["cmd_kill"],
        "vals": {
            "kill": None,
            "type": "cats/dogs/all",
        }
    },
    {
        "info": translate_text[translate]["cmd_store"],
        "vals": {
            "shop": None,
        }
    },
    {
        "info": translate_text[translate]["cmd_stop"],
        "vals": {
            "stop": None,
        }
    },
    {
        "info": translate_text[translate]["cmd_resum"],
        "vals": {
            "play": None,
        }
    },
    {
        "info": translate_text[translate]["cmd_baff_debaff"],
        "vals": {
            "baffdebaff": None,
        }
    },
    {
        "info": translate_text[translate]["cmd_save"],
        "vals": {
            "save": None,
        }
    },
    {
        "info": translate_text[translate]["cmd_load"],
        "vals": {
            "load": None,
        }
    },
    {
        "info": translate_text[translate]["cmd_reset_game"],
        "vals": {
            "RESET_GAME": None,
        }
    },
    {
        "info": translate_text[translate]["cmd_language"],
        "vals": {
            "language": None,
            "lang": "language"
        }
    },
    {
        "info": translate_text[translate]["cmd_coordinates"],
        "vals": {
            "coordinates": None
        }
    },
    {
        "info": translate_text[translate]["cmd_training"],
        "vals": {
            "training": None,
            "step": "Training step"
        }
    },
    {
        "info": translate_text[translate]["cmd_event"],
        "vals": {
            "event": None,
            "num": "Event number"
        }
    }
]

def text_input(input_text2 = None):
    global hint, training_step, start_budget, first, CMD_line, translate, input_text, hint, all_dogs, best_score, all_cats, running, input_active, ctrl_pressed, shift_pressed, health, dogs, cats, cat, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing, dog_damag_boost, cat_works_boost, cats_boost, upping, buy_cats, xexe, mx, dogs_class, __dangerous_keywords_pp2irooodjhjjjkjkn, scripts, bad_list, good_list, catown2, bonus, new_music, buy_no_cats, event_game, maxMoney, cat_unblock, stop_game, cats_moneys, summa, unmultipiller, translate_baffs, translate_cats, translate_dogs, translate_text, pos
    if input_text2 == None:
        input_text= str(input_text)
    else:
        input_text = str(input_text2)
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
        elif input_text.split()[0] == "spawn":
            spawn_name = input_text.split()[1].split(",")
            try:
                xs = int(input_text.split()[2])
            except:
                xs = None
            try:
                ys = int(input_text.split()[3])
            except:
                ys = None
            attepts = 0
            good = 0
            good_wait = len(spawn_name)
            if any(item in dogs_class for item in spawn_name):
                while True:
                    for dog3 in dogs_class:
                        if len(spawn_name) <= 1 and spawn_name[0] == dog3:
                            dogs_class[dog3].create(xs, ys)
                            input_text= ''
                            return
                        else:
                            for na in spawn_name:
                                if na == dog3:
                                    spawn_name.remove(na)
                                    dogs_class[dog3].create(xs, ys)
                            good += 1
                    if attepts >= 500+good_wait:
                        print("ERROR")
                        input_text= ''
                        return
                    attepts += 1
                    if good_wait == good:
                        input_text= ''
                        return
            else:
                for dog2 in dogs_class:
                    if spawn_name.lower() == dog2.lower():
                        print(f"ERROR! Dog not found. Did you mean <{dog2}>?")
                        input_text= ''
                        return
                print("ERROR! Dog not found.")
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
            if WhoRan == 'dogs' or WhoRan == None or WhoRan == "All":
                spawn_dogs(custom_budget, xs, ys)
            if WhoRan == 'cats' or WhoRan == None or WhoRan == "All":
                spawn_cats(custom_budget, xs ,ys)
        elif input_text.split()[0] == "money":
            money = int(input_text.split()[1])
        elif input_text.split()[0] == "wave":
            old_wave = wave
            wave = int(input_text.split()[1])
            if wave - old_wave > 0:
                for i in range(wave - old_wave):
                    budget += summa
                    budget += round(budget/unmultipiller)
            else:
                budget = start_budget
                for i in range(wave):
                    budget += summa
                    budget += round(budget/unmultipiller)
        elif input_text.split()[0] == "budget":
            budget = int(input_text.split()[1])
        elif input_text.split()[0] == "mega_wave":
            for_mega_wave = 0
        elif input_text.split()[0] == "kill":
            WhiKill = input_text.split()[1]
            attepts = 0
            if WhiKill == "cats":
                while len(cats) != 0:
                    old_cats = len(cats)
                    for cat2 in cats:
                        cat2.health = 0
                        cat2.bump(cat2.maxhealth)
                        try: 
                            cats.remove(cat2)
                            del cat2
                        except:
                            pass
                    if old_cats == len(cats):
                        attepts += 1
                        if attepts >= 500:
                            print("ERROR")
                            break
            elif WhiKill == "dogs":
                while len(dogs) != 0:
                    old_dogs = len(dogs)
                    for dog2 in dogs:
                        dog2.health = 0
                        dog2.bump(dog2.maxhealth, [], False)
                        try: 
                            dogs.remove(dog2)
                            del dog2
                        except:
                            pass
                    if old_dogs == len(dogs):
                        attepts += 1
                        if attepts >= 500:
                            print("ERROR")
                            break
            elif WhiKill == "all":
                while len(dogs) != 0 or len(cats) != 0:
                    old_dogs = len(dogs)
                    old_cats = len(cats)
                    for dog2 in dogs:
                        dog2.health = 0
                        dog2.bump(dog2.maxhealth, [], False)
                        try: 
                            dogs.remove(dog2)
                            del dog2
                        except:
                            pass
                    for cat2 in cats:
                        cat2.health = 0
                        cat2.bump(cat2.maxhealth)
                        try: 
                            cats.remove(cat2)
                            del cat2
                        except:
                            pass
                    if old_dogs != 0:
                        old_dogs = old_dogs == len(dogs)
                    if old_cats != 0:
                        old_cats = old_cats == len(cats)
                    if old_cats or old_dogs:
                        attepts += 1
                        if attepts >= 500:
                            print("ERROR")
                            break
        elif input_text.split()[0] == "shop":
            for cd2 in buy_no_cats:
                cd2.unblock = True
            input_text= ''
            hint = ''
            game(0)
        elif input_text.split()[0] == "stop":
            stop_game = True
        elif input_text.split()[0] == "play":
            stop_game = False
        elif input_text.split()[0] == "baffdebaff":
            input_text= ''
            omg(wave, 0)
        elif input_text.split()[0] == "load":
            loading_game(None)
        elif input_text.split()[0] == "save":
            save_game(None)
        elif input_text.split()[0] == "RESET_GAME":
            best_score = 0
            music_playing = True
            first = True
            save_game_settings()
            try:
                if music_playing:
                    pygame.mixer.music.pause()
                else:   
                    pygame.mixer.music.unpause()
                save_game_settings()
            except:
                pass
            input_text= ''
            hint = ''
            menu()
        elif input_text.split()[0] == "language":
            lang = input_text.split()[1]
            if lang in translate_baffs and lang in translate_cats and lang in translate_dogs and lang in translate_text and lang in translate_dogs:
                translate = lang
            else:
                NotificationSystem("ERROR: Language is not found, translate_baffs: " + str(lang in translate_baffs) +" translate_cats: " + str(lang in translate_cats) +" translate_dogs: " + str(lang in translate_dogs) +" translate_text: " + str(lang in translate_text) +" translate_dogs: " + str(lang in translate_dogs), (255, 0, 0), 25, 3, 2, 10)
        elif input_text.split()[0] == "coordinates":
            print(pos)
        elif input_text.split()[0] == "training":
            try:
                training_step = int(input_text.split()[1])
            except:
                training_step = 0
            event_game = -2
            input_text= ''
            hint = ''
            start(0)
            return
        elif input_text.split()[0] == "event":
            try:
                event_game = int(input_text.split()[1])
            except:
                try:
                    event_game = input_text.split()[1]
                    input_text= ''
                    start(0)
                    return
                except:
                    pass
        else:
            for script in scripts:
                exec(str(start_script(script, 'cmd')))
    except:
        pass
    
    input_text= ''
    
def hint_def(name_list, hint_clear):
    global input_text, hint, running, input_active, ctrl_pressed, shift_pressed, CMD_commands, CMD_line
    if len(input_text.split()) > 0:
        hint = next((list(command["vals"].items())[0][0] for command in CMD_commands if input_text.split()[0] in list(command["vals"].items())[0][0]), None)
        if any(input_text.split()[0] in names2 for names2 in name_list):
            for command in CMD_commands:                        
                if input_text.split()[0] in list(command["vals"].items())[0][0]:
                    if len(list(command["vals"].items())) > len(input_text.split()):
                        hint += " "+list(command["vals"].items())[len(input_text.split())][1]
                    hint += " - "+command["info"]
                    return hint
    else:
        if hint_clear:
            hint = ""

def CMD_codes(event):
    global input_text, hint, running, input_active, ctrl_pressed, shift_pressed, CMD_commands, CMD_line
    for script in scripts:
        exec(str(start_script(script, 'cmd_event')))
    try:
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            name_list = [list(command["vals"].keys())[0] if command["vals"] else None for command in CMD_commands]
            if event.key == pl.K_LCTRL:
                ctrl_pressed = True
            if event.key == pl.K_LSHIFT:
                shift_pressed = True
            if ctrl_pressed and shift_pressed and event.key == pl.K_SPACE:
                input_active = not input_active
            elif input_active:
                hint_clear = True
                if event.key == pl.K_RETURN:
                    if input_text:
                        text_input()
                        hint_def(name_list, hint_clear)
                elif keys[pygame.K_LCTRL] and keys[pygame.K_BACKSPACE]:
                    if len(input_text.split()) > 1:
                        input_text= " ".join(input_text.split()[:-1])
                    else:
                        input_text= ""
                    hint_def(name_list, hint_clear)
                elif event.key == pl.K_BACKSPACE:
                    input_text= input_text[:-1]
                    hint_def(name_list, hint_clear)
                elif input_active and event.key == pl.K_TAB:
                    if len(input_text.split()) > 0:
                        if any(input_text.split()[0] in names2 for names2 in name_list):
                            if input_text.split()[0] != next((list(command["vals"].items())[0][0] for command in CMD_commands if input_text.split()[0] in list(command["vals"].items())[0][0]), None):
                                input_text = next((list(command["vals"].items())[0][0] for command in CMD_commands if input_text.split()[0] in list(command["vals"].items())[0][0]), None)
                                hint_def(name_list, hint_clear)
                elif input_active and event.key == pl.K_DOWN:
                    if any(hint == names2 for names2 in name_list) or hint == "":
                        CMD_line -= 1
                        if CMD_line < 0:
                            CMD_line = len(CMD_commands)-1
                        hint = name_list[CMD_line]
                        hint_clear = False
                elif input_active and event.key == pl.K_UP:
                    if any(hint == names2 for names2 in name_list) or hint == "":
                        CMD_line += 1
                        if CMD_line >= len(CMD_commands):
                            CMD_line = 0
                        hint = name_list[CMD_line]
                        hint_clear = False
                else:
                    input_text+= event.unicode
                    hint_def(name_list, hint_clear)

        if event.type == pygame.KEYUP:
            if event.key == pl.K_LCTRL:
                ctrl_pressed = False
            if event.key == pl.K_LSHIFT:
                shift_pressed = False
    except: 
        pass

def loading_game(folder_path):
    global input_text, hint, all_dogs, all_cats, running, input_active, ctrl_pressed, shift_pressed, health, dogs, cats, cat, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing, dog_damag_boost, cat_works_boost, cats_boost, upping, buy_cats, xexe, mx, dogs_class, __dangerous_keywords_pp2irooodjhjjjkjkn, scripts, bad_list, good_list, catown2, bonus, new_music, buy_no_cats, event_game, maxMoney, cat_unblock, stop_game, cats_moneys
    root = tk.Tk()
    root.withdraw()
    if folder_path == None:
        folder_path = filedialog.askdirectory(initialdir="Data\\Save")
    if folder_path:
        while len(cats) > 0:
            for cat33 in cats:
                cat33.sell(0)
        while len(dogs) > 0:
            for dog33 in dogs:
                dog33.delet()
        cat_path = os.path.join(folder_path, "all.pickle")
        game_path = os.path.join(folder_path, "game.pickle")
        if not os.path.exists(cat_path):
            with open(cat_path, "w") as file:
                file.write("")
        else:
            with open(cat_path, "rb") as file:
                exec(str(pickle.load(file)))
        if not os.path.exists(game_path):
            with open(game_path, "w") as file:
                file.write("")
        else:
            with open(game_path, "rb") as file:
                exec(str(pickle.load(file)))
    for buyCat in buy_no_cats:
        buyCat.spawn()
    for buyCat in buy_cats:
        buyCat.spawn()
    
    new_cat_unblock()
    

def save_game(folder_path):
    global input_text, hint, all_dogs, all_cats, running, input_active, ctrl_pressed, shift_pressed, health, dogs, cats, cat, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing, dog_damag_boost, cat_works_boost, cats_boost, upping, buy_cats, xexe, mx, dogs_class, __dangerous_keywords_pp2irooodjhjjjkjkn, scripts, bad_list, good_list, catown2, bonus, new_music, buy_no_cats, event_game, maxMoney, cat_unblock, stop_game, cats_moneys
    root = tk.Tk()
    root.withdraw()
    if folder_path == None:
        folder_path = filedialog.askdirectory(initialdir="Data\\Save")
    else:
        if folder_path:
            os.makedirs(folder_path, exist_ok=True)
    if folder_path:
        # информация о мире
        with open(os.path.join(folder_path, "Info.txt"), 'w') as file:
            path = 'Data\\Mods\\'
            folder_names = [
                f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))
                ]
            global text
            if len(folder_names)>0:
                text = translate_text[translate]["save_mods_in_world"]
                for ModName in folder_names:
                    text += str(ModName) + "\n"
            else:
                text = translate_text[translate]["save_mods_not_in_world"]
            text += translate_text[translate]["save_world_created"] + str(time.strftime('%d.%m.%Y %H:%M', time.localtime(time.time())))
            text += translate_text[translate]["save_in_world"] + str(len(dogs)+len(cats)) + translate_text[translate]["save_entyti"]
            text += str(wave) + translate_text[translate]["save_wave"] + str(health) + translate_text[translate]["save_health"] + str(money) + translate_text[translate]["save_money"]
            for script in scripts:
                exec(str(start_script(script, 'world save')))
            file.write(text)
        # сохраняем ентити
        cat_path = os.path.join(folder_path, "all.pickle")
        fileData = ""
        if len(cats) > 0:
            all_cats = []
            for cat3 in cats:
                cat3.save()
            for cat3 in all_cats:
                fileData+= cat3 + '\n'
        if len(dogs) > 0:
            all_dogs = []
            for dog3 in dogs:
                dog3.save()
            for dog3 in all_dogs:
                fileData+= dog3 + '\n'
        with open(cat_path, 'wb') as file:
            pickle.dump(fileData, file)
        # сохраняем значения игры
        game_path = os.path.join(folder_path, "game.pickle")
        fileData = ""
        global_vars = globals()
        
        for name, value in list(global_vars.items()):
            if not name.startswith("__"):
                try:
                    exec(f"{name}={value}\n")
                    fileData+=f"global {name}\n{name}={value}\n"
                except:
                    pass
        with open(game_path, 'wb') as file:
            pickle.dump(fileData, file)
load_game_settings()
checkbox1 = Checkbox(50, 50, "Music", music_playing, 0)
checkboxes = [checkbox1]
menu()
pygame.quit()
