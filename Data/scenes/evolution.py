import pygame
from classes import Sprite, Text
from managers import ObjectManager, TextManager

class GeneratedUI:
    def __init__(self, game_context=None):
        self.game = game_context
        self.objects = ObjectManager(self.game)
        self.texts = TextManager(self.game)
        # Label: pivot=[0.5, 0.5]
        sprite_Background = Sprite(None, scale=[1400, 800], color=[69, 69, 69], size=[1400, 800], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Background = self.objects.new_object(sprite_Background, [0, 0], 'topleft')
        # Image: pivot=[0.5, 0.5]
        sprite_Exit = Sprite('placeholder.png', scale=[75, 75], color=[100, 100, 255], size=[75, 75], alpha=255, flip_x=False, flip_y=False, angle=0, mode='Stretch')
        self.Exit = self.objects.new_object(sprite_Exit, [25, 25], 'topleft')
        # Text: pivot=[0.5, 0.5]
        font_Label = Text.get_font('Arial', 80)
        self.Label = self.texts.make(font_Label, 'Evolution', [255, 128, 128], [690, 50], 'center')
        # Text: pivot=[0.5, 0.5]
        font_xp = Text.get_font('Arial', 24)
        self.xp = self.texts.make(font_xp, 'XP 9999/9999', [255, 255, 255], [120, 40], 'midleft')
        # Text: pivot=[0.5, 0.5]
        font_level = Text.get_font('Arial', 24)
        self.level = self.texts.make(font_level, '(9999999)', [111, 255, 85], [250, 40], 'midleft')
        # Text: pivot=[0.5, 0.5]
        font_xp_copy = Text.get_font('Arial', 40)
        self.xp_copy = self.texts.make(font_xp_copy, 'Level 9999999', [255, 255, 255], [120, 80], 'midleft')

    def started(self):
        pass

    def update(self):
        self.objects.update()
        self.texts.update()

    def draw(self):
        self.objects.draw()
        self.texts.draw()
