import pygame
from classes import Sprite, Text
from managers import ObjectManager, TextManager

class GeneratedUI:
    def __init__(self, game_context=None):
        self.game = game_context
        self.objects = ObjectManager(self.game)
        self.texts = TextManager(self.game)
        # Image: pivot=[0.5, 0.5]
        sprite_save1 = Sprite('C:/Users/Константин Морозов/Desktop/Kot Defense Remake/Kot Defense Remake Dev/Data/textures/bar.png', scale=[350, 525], color=[100, 100, 255], size=[350, 525], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.save1 = self.objects.new_object(sprite_save1, [100, 225], 'topleft')
        # Image: pivot=[0.5, 0.5]
        sprite_save2 = Sprite('C:/Users/Константин Морозов/Desktop/Kot Defense Remake/Kot Defense Remake Dev/Data/textures/bar.png', scale=[350, 525], color=[100, 100, 255], size=[350, 525], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.save2 = self.objects.new_object(sprite_save2, [525, 225], 'topleft')
        # Image: pivot=[0.5, 0.5]
        sprite_save3 = Sprite('C:/Users/Константин Морозов/Desktop/Kot Defense Remake/Kot Defense Remake Dev/Data/textures/bar.png', scale=[350, 525], color=[100, 100, 255], size=[350, 525], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.save3 = self.objects.new_object(sprite_save3, [950, 225], 'topleft')
        # Text: pivot=[0.5, 0.5]
        font_text1 = Text.get_font('Arial', 83)
        self.text1 = self.texts.make(font_text1, 'Save 1', [236, 236, 230], [280, 315], 'center')
        # Text: pivot=[0.5, 0.5]
        font_text2 = Text.get_font('Arial', 83)
        self.text2 = self.texts.make(font_text2, 'Save 2', [236, 236, 230], [705, 315], 'center')
        # Text: pivot=[0.5, 0.5]
        font_text3 = Text.get_font('Arial', 83)
        self.text3 = self.texts.make(font_text3, 'Save 1', [236, 236, 230], [1130, 315], 'center')
        # Text: pivot=[0.5, 0.5]
        font_Text = Text.get_font('Arial', 171)
        self.Text = self.texts.make(font_Text, 'Select ur save slot', [15, 15, 9], [700, 225], 'midbottom')

    def started(self):
        pass

    def update(self):
        self.objects.update()
        self.texts.update()

    def draw(self):
        self.objects.draw()
        self.texts.draw()
