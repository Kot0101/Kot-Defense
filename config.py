import pygame, os, json

# Pocket Edition platform layer (works on Windows and Android alike)
from android_support import (
    IS_ANDROID, IS_DESKTOP, BASE_DIR, DATA_DIR, SAVE_DIR,
    res, ensure_workdir, ensure_save_dir,
    Display, install_cursor_guard, install_quit_on_back_button,
)

version = "150826-1"
WIDTH, HEIGHT = 1400, 800

folder_name = "KotDefense" # Название папки сохранения

downbar = 170
upbar = 80

cell1 = (148, 146, 124)
cell2 = (130, 128, 109)# (94,143,86)
cell_size = 104
GRID_SIZE = 104
cat_base_size = 96

# Начало сетки: клетки центрируются на точках привязки котов,
# а поле начинается ровно под верхней панелью.
GRID_X0 = cell_size // 2
GRID_Y0 = upbar + cell_size // 2

FPS = 60

CONSOLE_TOGGLE_SCANCODE = 53

# Все относительные пути ("Data/...") должны работать и на Android,
# где текущая папка процесса - это "/".
ensure_workdir()

if IS_ANDROID:
    try:
        pygame.mixer.pre_init(44100, -16, 2, 512)
    except Exception:
        pass

pygame.init()
try:
    pygame.mixer.init()
except Exception:
    pass

install_cursor_guard()
install_quit_on_back_button()

display = Display()
window, screen = display.init(
    WIDTH, HEIGHT,
    title="Kot Defense",
    icon_path=res("Data", "textures", "icon.png"),
)

def present():
    """Показать логический кадр 1400x800 на реальном окне (с полями по краям)."""
    display.present()

display.install_event_translation()

class DataPackManager:
    def __init__(self):
        self.game = None
        self.datapacks_folder = os.path.join(DATA_DIR, "DataPacks")
        self.temp_images = {}
        
        self.enableDatapack = None
    
    def init_game(self, game):
        self.game = game
    
    def _read_manifest(self, mod_path):
        manifest_path = os.path.join(mod_path, "manifest.json")
        if not os.path.exists(manifest_path):
            return None
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "name": data.get("name", os.path.basename(mod_path)),
                "version": data.get("version", "0.0"),
                "author": data.get("author", "Unknown"),
            }
    
    def set(self, name): # Необходима перезагрузка
        self.enableDatapack = name
    
    def get(self, path):
        file_name = str(path).replace("\\", "/").rstrip("/").split('/')[-1]
        name_list = ["textures", "audio"]
        for name in name_list:
            if self.enableDatapack is not None and file_name in self.get_folder(self.enableDatapack, name):
                return os.path.join( os.path.join(self.get_path(self.enableDatapack), name), file_name)
        return path
    
    def get_code(self):
        pack_path = self.get_path(self.enableDatapack)
        if self.enableDatapack is not None:
            code_path = os.path.join(pack_path, "main.py")
            with open(code_path, "r", encoding="utf-8") as f:
                return f.read()
        return "pass"
    
    def get_folder(self, pack, folder_name):
        files = []
        pack_path = self.get_path(pack)
        for folder in os.listdir(pack_path):
            if folder == folder_name:
                image_path = os.path.join(pack_path, folder)
                for file in os.listdir(image_path):
                    files.append(file)
        return files
    
    def data_list(self):
        datapacks = []
        if not os.path.exists(self.datapacks_folder):
            try:
                os.makedirs(self.datapacks_folder, exist_ok=True)
            except OSError:
                return datapacks
        for folder in os.listdir(self.datapacks_folder):
            pack_path = os.path.join(self.datapacks_folder, folder)
            if os.path.isdir(pack_path):
                info = self._read_manifest(pack_path)
                if info:
                    datapacks.append(folder)
        return datapacks
    
    def get_path(self, name):
        if not os.path.isdir(self.datapacks_folder):
            return None
        for root, dirs, files in os.walk(self.datapacks_folder):
            if name in dirs:
                return os.path.join(root, name)
        return None

datapackM = DataPackManager()
# datapackM.enableDatapack = "ShedevroPack"
