import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import shutil
import pygame
import pygame.locals as pl
"""module for setup GUI"""
import json5
# from PySide6.QtWidgets import *
from PyQt5.QtCore import *

def construct_stylesheet(data):
        stylesheet = ""
        for item in data:
            selector = item["selector"]
            properties = item.get("properties", {})
            states = item.get("states", {})
            sub_controls = item.get("sub-controls", {})

            properties_str = ";\n".join([f"{k}: {v}" for k, v in properties.items()]) + ";"
            stylesheet += f"{selector} {{\n{properties_str}\n}}\n"

            for state, state_properties in states.items():
                state_properties_str = ";\n".join([f"{k}: {v}" for k, v in state_properties.items()]) + ";"
                stylesheet += f"{selector}:{state} {{\n{state_properties_str}\n}}\n"

            for sub_control, sub_control_properties in sub_controls.items():
                sub_control_properties_str = ";\n".join([f"{k}: {v}" for k, v in sub_control_properties.items()]) + ";"
                stylesheet += f"{selector}::{sub_control} {{\n{sub_control_properties_str}\n}}\n"

        return stylesheet

# def setStyle(self, stylesheet="stylesheet.json",modern=True):
#     '''
#     if modern is on=>use modern style, if modern is off=>use basic style,
#     args: file-path to stylesheet.json, boolean for modern 
#     '''
#     with open(stylesheet, 'r') as f:
#         data = json5.load(f)["stylesheet"]
#         stylesheet = construct_stylesheet(data)
#         self.setStyleSheet(stylesheet)
#     # if modern:



import os
global previewbool
previewbool = False

def setNewStyle(self, stylesheet="stylesheet.json",modern=True):
    '''
    if modern is on=>use modern style, if modern is off=>use basic style,
    args: file-path to stylesheet.json, boolean for modern 
    '''
    # _open(self)
def setStyle(self,name=None):
    """
    The function `setStyle` attempts to load a style sheet from a JSON file in the `json_module`
    directory and opens it.
    """
    if not name:
        stylesheet_path = os.path.join(os.path.dirname(__file__), "stylesheet.json")

        if not os.path.exists(stylesheet_path):
            stylesheet_path = "stylesheet.json"
        _open(self, stylesheet_path)

    else:
        _open(self, name)
def _open(self, stylesheet):
    """
    The function `_open` reads a JSON5 file containing stylesheet data, constructs a stylesheet from the
    data, and applies it to the widget.
    
    :param stylesheet: The `stylesheet` parameter in the `_open` method is a file path to a JSON5 file
    containing style information for a GUI application. The method reads the file, extracts the
    stylesheet data, constructs a stylesheet from the data, and applies it to the GUI component using
    `self.setStyleSheet(stylesheet)
    """
    
    with open(stylesheet, 'r') as f:
        data = json5.load(f)["stylesheet"]
        stylesheet = construct_stylesheet(data)
        self.setStyleSheet(stylesheet)

    # # Load custom fonts
    # QFontDatabase.addApplicationFont("json_module/fonts/CustomFont.ttf")
    

os.system("cls")

def error_box(Title, Text, Icon):
    error_message = QMessageBox()
    error_message.setWindowTitle(Title)
    error_message.setText(Text)
    error_message.setIcon(Icon)
    error_message.exec_()

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kot Defense Maker 1.0")
        self.setWindowIcon(QIcon("icon.ico"))
        self.entrys = {}
        self.previewbool = False

        self.tab_widget = QTabWidget()
        self.tabs = {"Cats": ("Cat", "BuyCat"), "Dogs": ("Dog", "CreateDog")}
        
        for tab_name, (prefix, buy_function) in self.tabs.items():
            tab = QWidget()
            self.create_elements(tab, prefix, buy_function)
            self.tab_widget.addTab(tab, tab_name)

        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.save_settings)
        
        self.button_preview = QPushButton("Preview")
        self.button_preview.clicked.connect(self.preview)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.button_save)
        main_layout.addWidget(self.button_preview)
        
        self.fields = {}
        self.entrys = {}
        self.setLayout(main_layout)
        self.show()

    
    def create_elements(self, tab, prefix, buy_function):
        layout = QVBoxLayout()
        self.add_entry_row(layout, "Mod Name", "mod")
        
        if prefix == "Cat":
            self.fields = {
                "Price":"moneys", "Information":"self_info", "Radius of damage":"aura_radius", "Health":"health", 
                "Maximum dog attacks":"dogs_count", "Reload":"reload", "Damage":"damage_cat", "Uniqueness":"mega",
                "Will appear on wave":"wawe", "Disappears on wave: (-1 never)":"wawedel",
                "Size x":"size_x", "Size y":"size_y"
            }
        elif prefix == "Dog":
            self.fields = {
                "For murder they will give":"moneys", "Price":"bugete", "Name":"name", "Health":"health", 
                "Speed":"speed", "Damage":"damage_dog", "Uniqueness":"unikal", "Reload":"reload",
                "Type":"typedog", "Size x":"size_x", "Size y":"size_y"
            }
        
        for field, name in self.fields.items():
            self.add_entry_row(layout, field, name)

        self.add_file_select_row(layout, f"Path to {prefix} picture", "path_my_image")
        if prefix == "Cat":
            self.add_file_select_row(layout, "Store icon path", "ico_image_path")
        tab.setLayout(layout)

    def add_entry_row(self, layout, label_text, entry_name):
        entry_layout = QHBoxLayout()
        label = QLabel(label_text)
        entry = QLineEdit()
        entry.textChanged.connect(lambda: self.entry_update(entry.text(), entry_name))
        entry_layout.addWidget(label)
        entry_layout.addWidget(entry)
        layout.addLayout(entry_layout)
        # setattr(self, f"entry_{entry_name}", entry)
        self.entrys[str(entry_name)] = ""

    def add_file_select_row(self, layout, label_text, entry_name):
        file_layout = QHBoxLayout()
        label = QLabel(label_text)
        entry = QLineEdit()
        entry.textChanged.connect(lambda: self.entry_update(entry.text(), entry_name))
        # setattr(self, f"entry_{entry_name}", entry)
        button_select = QPushButton("Select file")
        button_select.clicked.connect(lambda: self.select_file(entry))
        file_layout.addWidget(label)
        file_layout.addWidget(entry)
        file_layout.addWidget(button_select)
        layout.addLayout(file_layout)
        self.entrys[str(entry_name)] = ""

    def entry_update(self, entry, entry_name):
        self.entrys[entry_name] = entry

    def select_file(self, entry):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "Images (*.jpg *.jpeg *.png *.gif *.bmp);;All files (*)"
        )
        if filepath:
            entry.setText(filepath)

    def save_settings(self):
        # try:
        current_widget = self.tab_widget.currentWidget()
        tab_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
        self.prefix = tab_name
        mod_name = os.path.join("Mods", self.entrys["mod"])
        settings = [self.entrys[entry] for _, entry in self.fields.items()]
        
        self.create_mod_folders(mod_name)
        if "ico_image_path" not in self.entrys:
            self.entrys["ico_image_path"] = None
        self.copy_images(self.entrys["path_my_image"], self.entrys["ico_image_path"], mod_name)
        self.write_to_main_py(mod_name, *settings[1:])

        print(f"Mod {mod_name} was saved in 'Mods' folder")
        # except:
            # pass

    def create_mod_folders(self, mod_name):
        folders = ["Data", "Data/Img", "Data/Songs", "Data/Saves", "Data/Fonts", "Data/Scripts"]
        for folder in folders:
            os.makedirs(os.path.join(os.getcwd(), mod_name, folder), exist_ok=True)

    def copy_images(self, path_my_image, ico_image_path, mod_name):
        try:
            img_path = os.path.join(os.getcwd(), mod_name, "Data", "Img")
            for image_path in [path_my_image, ico_image_path]:
                if image_path :
                    try:
                        shutil.copy2(image_path, os.path.join(img_path, os.path.basename(image_path)))
                    except:
                        pass
                    if path_my_image == image_path:
                        self.entrys["path_my_image"] = os.path.join("Data", mod_name, "Data", "Img", os.path.basename(image_path))
                    else:
                        self.entrys["ico_image_path"] = fr'r"{os.path.join("Data", mod_name, "Data", "Img", os.path.basename(image_path))}"'
        except:
            pass


    def write_to_main_py(self, mod_name, *args):
        main_path = os.path.join(os.getcwd(), mod_name, "main.py")
        save_text = ""
        if self.prefix == "Cats":
            save_text = f"BuyCat({self.entrys['moneys']}, '{self.entrys['self_info']}', {self.entrys['aura_radius']}, {self.entrys['health']}, {self.entrys['dogs_count']}, {self.entrys['reload']}, {self.entrys['damage_cat']}, {self.entrys['mega']}, {self.entrys['wawe']}, {self.entrys['wawedel']}, r'{self.entrys['path_my_image']}', {self.entrys['size_x']}, {self.entrys['size_y']}, {self.entrys['ico_image_path']})"
        elif self.prefix == "Dogs":
            save_text = f"CreateDog({self.entrys['moneys']}, {self.entrys['bugete']}, '{self.entrys['name']}', {self.entrys['health']}, {self.entrys['speed']}, {self.entrys['damage_dog']}, {entrys['unikal']}, {self.entrys['reload']}, {self.entrys['typedog']}, r'{self.entrys['path_my_image']}', {self.entrys['size_x']}, {self.entrys['size_y']})"
        block = False
        if os.path.isfile(main_path):
            with open(main_path, "r", encoding="utf-8") as file:
                for line in file:
                  if line.strip() == save_text:
                    block = True
        if block == False:
            with open(main_path, "a", encoding="utf-8") as f:
                f.write(save_text+'\n')
        else:
            error_box("Ошибка", "У вас уже есть точно такое же существо", QMessageBox.Critical)
    def preview(self):
        preview(self.entrys, self.tab_widget.tabText(self.tab_widget.currentIndex()))

def outlining(text, color, text_rect_x, text_rect_y, outlining2, font, screen):
    screen.blit(font.render(text, True, color), (text_rect_x - outlining2, text_rect_y))
    screen.blit(font.render(text, True, color), (text_rect_x + outlining2, text_rect_y))
    screen.blit(font.render(text, True, color), (text_rect_x, text_rect_y - outlining2))
    screen.blit(font.render(text, True, color), (text_rect_x, text_rect_y + outlining2))

def info(text, position, screen):
    font2 = pygame.font.Font(None, 25)
    text_surface = font2.render(text, True, (170, 170, 170))
    text_rect = text_surface.get_rect()

    if position[0] > screen.get_width() / 2:
        text_rect.right = position[0]-25
        text_rect.y = position[1]-10
    else:
        text_rect.topleft = position

    outlining(text, (0, 0, 0), text_rect.x, text_rect.y, 2, font2, screen)
    
    screen.blit(text_surface, text_rect.topleft)

def preview(entrys, prefix):
    global previewbool
    try:
        previewbool = not previewbool
        
        width = 1400
        height = 800
        pygame.init()
        os.system("cls")
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Kot Defense Maker")
        pygame.display.set_icon(pygame.image.load(r'icon.ico'))
        
        image = pygame.transform.scale(pygame.image.load(entrys['path_my_image']), (int(entrys['size_x']), int(entrys['size_y'])))
        
        rect = image.get_rect()
        rect.x = width / 2 - int(entrys['size_x']) / 2
        rect.y = height / 2 - int(entrys['size_y']) / 2
        
        clock = pygame.time.Clock()
        
        while previewbool:
            stope = False
            position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    previewbool = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    previewbool = False
                    pygame.quit()
                    return
            screen.fill((101, 155, 94))
            if prefix == "Cats":
                if int(entrys['aura_radius']) > 0: 
                    circle_surface = pygame.Surface((int(entrys['aura_radius']) * 2, int(entrys['aura_radius']) * 2), pygame.SRCALPHA)
                    pygame.draw.circle(circle_surface, (255, 255, 255, 100), (int(entrys['aura_radius']), int(entrys['aura_radius'])), int(entrys['aura_radius']), 2)
                    screen.blit(circle_surface, (rect.centerx - int(entrys['aura_radius']), rect.centery - int(entrys['aura_radius'])))
                screen.blit(image, rect)
                if rect.collidepoint(position):
                    info(f"{int(entrys['health'])} жизней", (position[0] + 15, position[1] + 5), screen)
            elif prefix == "Dogs":
                rect.x += int(entrys['speed'])
                if rect.x > width + int(entrys['size_x']) / 2:
                    rect.x = -int(entrys['size_x'])/ 2
                screen.blit(image, rect)
                if entrys['unikal'] == 2 or entrys['unikal'] == 7 or entrys['unikal'] == 8:
                    circle_surface = pygame.Surface((int(entrys['aura_radius']) * 2, int(entrys['aura_radius']) * 2), pygame.SRCALPHA)
                    pygame.draw.circle(circle_surface, (255, 0, 0, 100), (int(entrys['aura_radius']), int(entrys['aura_radius'])), int(entrys['aura_radius']), 2)
                    screen.blit(circle_surface, (rect.centerx - int(entrys['aura_radius']), rect.centery - int(entrys['aura_radius'])))
                    if rect.collidepoint(position):
                        info(f"{int(entrys['health'])} жизней, взрываеться и наносит {int(entrys['damage_dog'])} урона всем котам в зоне поражения", (position[0] + 15, position[1] + 5), screen)
                    stope = True
                elif entrys['unikal'] == 12:
                    circle_surface = pygame.Surface((int(entrys['aura_radius']) * 2, int(entrys['aura_radius']) * 2), pygame.SRCALPHA)
                    pygame.draw.circle(circle_surface, (255, 0, 0, 100), (int(entrys['aura_radius']), int(entrys['aura_radius'])), int(entrys['aura_radius']), 2)
                    screen.blit(circle_surface, (rect.centerx - int(entrys['aura_radius']), rect.centery - int(entrys['aura_radius'])))
                    if rect.collidepoint(position):
                        info(f"{int(entrys['health'])} жизней, лечит собак, наносит 1 урон", (position[0] + 15, position[1] + 5), screen)
                    stope = True
                elif stope == False and rect.collidepoint(position):
                    info(f"{int(entrys['health'])} жизней, урон {int(entrys['damage_dog'])}, скорость {int(entrys['speed'])}", (position[0] + 15, position[1] + 5), screen)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
    except:
        pass
    

app = QApplication(sys.argv)
app.setStyle("Fusion")
settings_window = SettingsWindow()
setStyle(settings_window)
sys.exit(app.exec())

os.system("pause")
