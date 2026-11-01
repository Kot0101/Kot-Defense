import pygame
from classes import Sprite, Text
from managers import ObjectManager, TextManager

class GeneratedUI:
    def __init__(self, game_context=None):
        self.game = game_context
        self.objects = ObjectManager(self.game)
        self.texts = TextManager(self.game)
        # Image: pivot=[0.5, 0.5]
        sprite_Image = Sprite('C:/Users/Константин Морозов/Desktop/Kot Defense Remake/Kot Defense Remake Dev/Data/textures/thumbnail.png', scale=[1450, 850], color=[100, 100, 255], size=[1450, 850], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Image = self.objects.new_object(sprite_Image, [700, 400], 'center')
        # Image: pivot=[0.5, 0.5]
        sprite_Image_002 = Sprite('C:/Users/Константин Морозов/Desktop/Kot Defense Remake/Kot Defense Remake Dev/Data/textures/gradient.png', scale=[1450, 850], color=[100, 100, 255], size=[1450, 850], alpha=96, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Image_002 = self.objects.new_object(sprite_Image_002, [700, 400], 'center')
        # Label: pivot=[0.5, 0.5]
        sprite_Label = Sprite(None, scale=[290, 4], color=[255, 255, 255], size=[290, 4], alpha=200, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Label = self.objects.new_object(sprite_Label, [1075, 775], 'topleft')
        # Text: pivot=[0.5, 0.5]
        font_Text = Text.get_font('Arial', 24)
        self.Text = self.texts.make(font_Text, 'Kot - Kot Defense RAP', [255, 255, 255], [1119, 770], 'bottomleft')
        # Image: pivot=[0.5, 0.5]
        sprite_Image_001 = Sprite('C:/Users/Константин Морозов/Desktop/Kot Defense Remake/Kot Defense Remake Dev/Data/textures/note.png', scale=[32, 32], color=[100, 100, 255], size=[32, 32], alpha=255, flip_x=False, flip_y=False, angle=-360, mode='Stretch')
        self.Image_001 = self.objects.new_object(sprite_Image_001, [1095, 757], 'center')
        # Image: pivot=[0.5, 0.5]
        sprite_Image_003 = Sprite('C:/Users/Константин Морозов/Desktop/Kot Defense Remake/Kot Defense Remake Dev/Data/textures/title.png', scale=[575, 150], color=[100, 100, 255], size=[575, 150], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Image_003 = self.objects.new_object(sprite_Image_003, [1090, 90], 'center')
        # Image: pivot=[0.5, 0.5]
        sprite_Image_003_001 = Sprite('C:/Users/Константин Морозов/Desktop/Kot Defense Remake/Kot Defense Remake Dev/Data/textures/OST.png', scale=[200, 120], color=[100, 100, 255], size=[200, 120], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Image_003_001 = self.objects.new_object(sprite_Image_003_001, [720, 90], 'center')
        # Image: pivot=[0.5, 0.5]
        sprite_Image_004 = Sprite('C:/Users/Константин Морозов/Desktop/Kot Defense Remake/Kot Defense Remake Dev/Data/textures/save_fullbackground.png', scale=[1770, 1400], color=[100, 100, 255], size=[1770, 1400], alpha=255, flip_x=False, flip_y=False, angle=220, mode='Stretch')
        self.Image_004 = self.objects.new_object(sprite_Image_004, [-490, -500], 'topleft')
        # Image: pivot=[0.5, 0.5]
        sprite_Image_005 = Sprite('C:/Users/Константин Морозов/Desktop/Kot Defense Remake/Kot Defense Remake Dev/Data/textures/Cat_Attack.png', scale=[180, 180], color=[100, 100, 255], size=[180, 180], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Image_005 = self.objects.new_object(sprite_Image_005, [30, 610], 'topleft')
        # Image: pivot=[0.5, 0.5]
        sprite_Image_005_001 = Sprite('C:/Users/Константин Морозов/Desktop/Kot Defense Remake/Kot Defense Remake Dev/Data/textures/Dog_Base.png', scale=[140, 150], color=[100, 100, 255], size=[140, 150], alpha=255, flip_x=True, flip_y=False, angle=0, mode='Stretch')
        self.Image_005_001 = self.objects.new_object(sprite_Image_005_001, [290, 620], 'topleft')

    def started(self):
        pass

    def update(self):
        self.objects.update()
        self.texts.update()

    def draw(self):
        self.objects.draw()
        self.texts.draw()
