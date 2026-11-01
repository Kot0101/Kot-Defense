import pygame, copy, math
from config import *
from classes import *
from pygame import gfxdraw

#Branches
class Branch(Object):
    def __init__(self, game, id, image="placeholder.png", pos=(WIDTH//2, HEIGHT//2)):
        self.game = game
        self.imageSize = 40
        self.base = Sprite(game.pathManager.TEXTURES / image, (64, 64))
        self.sprite = self.base
        super().__init__(self.sprite, pos)
        setattr(self, "originalRect", copy.deepcopy(self.rect))
        self.parents = []
        self.childs = []
        self.descript = ""
        self.price = 1
        self.boxSize = (400, 100)
        
        self.buyed = False
        self.locked = not self.parents_buyed()
        
        self.status = 'leaving'
        self.animateEnd = False
        self.animations = {
            'hover': 'evo hover',
            'unhover': 'evo unhover',
            'hovered': 'evo hovered',
            'locked': "evo locked",
            'idle': "evo idle"
        }
        self.colors = {
            "idle": (95, 95, 95),
            "hovered": (120, 120, 120),
            "buyed": (90, 200, 90),
            "locked": (45, 45, 45),
        }
        
        self.colors_width = {
            "idle": (70, 70, 70),
            "hovered": (200, 200, 200),
            "buyed": (90, 105, 90),
            "locked": (20, 20, 20),
        }
        
        self.colors_line = {
            "idle": (110, 110, 110),
            "hovered": (140, 140, 140),
            "buyed": (145, 210, 145),
            "locked": (45, 45, 45),
        }
        
        self.id = id
    
    def animateForButtons(self): # Спиздил из менеджера объектов
        self.animator.update(speed_multiplier=1)
        
        anim_hover = self.animations.get('hover')
        anim_unhover = self.animations.get('unhover')
        anim_hovered = self.animations.get('hovered')
        anim_idle = self.animations.get('idle')
        anim_locked = self.animations.get('locked')
        
        if self.locked:
            self.status = "locked"
        else:
            if self.status == 'locked':
                self.status = 'idle'
                if anim_idle:
                    self.animator.play(anim_idle, loop=True)
            if self.hovered:
                if self.status in ('idle', 'leaving'):
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
                    if self.buyed:
                        self.animateEnd = True
    
    def animate_init(self, game):
        self.animator = Animator(self.game.animationManager)
        self.locked = not self.parents_buyed()
        if self.locked:
            self.animator.play(self.animations.get('locked'), loop=True, reverse=False, speed=0.1)
        else:
            self.animator.play(self.animations.get('idle'), loop=True, reverse=False, speed=0.1)
        self.buyed = self.id in self.game.playerO.upgrades
    
    def setOffset(self, pos=(0, 0)):
        self.rect.x = self.originalRect.x - pos[0]
        self.rect.y = self.originalRect.y - pos[1]
    
    def draw_lines(self):
        for p in self.parents:
            parent = self.get_branch(p)
            state = parent.get_state()
            
            pygame.draw.line(screen, self.colors_line[state], parent.rect.center, self.rect.center)
    
    def draw(self):
        state = self.get_state()
        color = self.colors[state]
        colorW = self.colors_width[state]
        pygame.draw.rect(screen, color, (self.rect.x, self.rect.y, 64, 64), border_radius=10)
        pygame.draw.rect(screen, colorW, (self.rect.x, self.rect.y, 64, 64), border_radius=10, width=2 )
        super().draw()
    
    def buy(self):
        self.game.playerO.upgrades.append(self.id)
        self.game.playerO.coins -= self.price
        self.buyed = True
        self.game.saveManager.save_game()
    
    def update(self):
        super().update()
        self.locked = not self.parents_buyed()
        pb = self.parents_buyed()
        if self.hovered and not self.locked:
            self.game.infoBar.boxSize = self.boxSize
            self.game.infoBar.label = self.name
            self.game.infoBar.price = f"{self.price} coin"
            self.game.infoBar.text = self.descript
            self.game.infoBar.style = 1
            if pb:
                if not self.buyed:
                    self.game.cursorManager.set_state('hovered')
                if self.clicked and self.buyed == False and self.game.playerO.coins >= self.price:
                    self.buy()
        if not self.animateEnd:
            if self.buyed or not pb:
                self.hovered = False
            self.animateForButtons()
    
    def parents_buyed(self):
        value = True
        for b in self.parents:
            branch = self.get_branch(b)
            if not branch.buyed:
                value = False
                break
        return value
    
    def get_state(self):
        state = "idle"
        if self.locked:
            state = "locked"
        elif self.buyed:
            state = "buyed"
        elif self.hovered:
            state = "hovered"
        
        return state
    
    def get_branch(self, id):
        return self.game.brManager.branchesAndNames[id]
    
    def addParent(self, id):
        self.parents.append(id)
        self.get_branch(id).childs.append(self.id)

CELL = 140

# Преписка B_ нужна чтобы не засерать названия (B_ - Означает Branch_<name>)
class B_NormalWaves(Branch):
    def __init__(self, game):
        super().__init__(game, "start", "b_WaveEasy.png", (0, 0))
        self.name = "Адекватные волны" # Normal Waves
        self.descript = "Делает игру проходимой XD"
        self.price = 25
        self.boxSize = (320, 70)

class B_Crit(Branch):
    def __init__(self, game):
        super().__init__(game, "unlock_crits", "b_crit.png", (0, -CELL))
        self.name = "Криты !" # Crits !
        self.descript = "Добавляет криты"
        self.price = 150
        self.boxSize = (195, 70)
        
        self.addParent("start")


class B_Worker(Branch):
    def __init__(self, game):
        super().__init__(game, "worker", "cat_worker.png", (1*CELL, CELL))
        self.name = "Кот рабочий" # Cat worker
        self.descript = "Зарабатывает 7 баксов после волны"
        self.price = 150
        self.boxSize = (400, 70)
        
        self.addParent("start")

class B_WorkerMoneyUP(Branch):
    def __init__(self, game):
        super().__init__(game, "workerUP", "b_workUP.png", (1*CELL, CELL*1.7))
        self.name = "Работяга"
        self.descript = "Зарабатывает на 1 бакс больше"
        self.price = 150
        self.boxSize = (360, 70)
        
        self.addParent("worker")

class B_WorkerMoneyUP2(Branch):
    def __init__(self, game):
        super().__init__(game, "workerUP2", "b_workUP2.png", (1*CELL, CELL*2.4))
        self.name = "Китайцы"
        self.descript = "Зарабатывает на ещё один\nчортовый бакс больше"
        self.price = 150
        self.boxSize = (300, 100)
        
        self.addParent("workerUP")



class B_Magic(Branch):
    def __init__(self, game):
        super().__init__(game, "magic", "cat_magic.png", (1*CELL, 0))
        self.name = "Кот маг" # Cat magic
        self.descript = "Наносит урон по радиусу\nОткрывается с 10-й волны"
        self.price = 150
        self.boxSize = (300, 100)
        
        self.addParent("start")

class B_Cowboy(Branch):
    def __init__(self, game):
        super().__init__(game, "cowboy", "cat_cowboy.png", (1*CELL, -CELL))
        self.name = "Ковбой" # Cat cowboy
        self.descript = "Высокий шанс крита\nЕго снаряды рикошетят при критах\nОткрывается с 5-й волны"
        self.price = 150
        self.boxSize = (380, 130)
        
        self.addParent("unlock_crits")
        self.addParent("magic")

class B_Medic(Branch):
    def __init__(self, game):
        super().__init__(game, "medic", "cat_medic.png", (2*CELL, CELL))
        self.name = "Кот медик" # Cat medic
        self.descript = "Лечит союзников в небольшом радиусе\nОткрывается с 5-й волны"
        self.price = 150
        self.boxSize = (420, 100)
        
        self.addParent("worker")

class B_Support(Branch):
    def __init__(self, game):
        super().__init__(game, "support", "cat_support.png", (3*CELL, CELL))
        self.name = "Кот помощник" # Cat support
        self.descript = "Союзникам в радиусе -11% перезарядки,\n+5% к радиусу и +11% к шансу крита\nОткрывается с 10-й волны"
        self.price = 150
        self.boxSize = (430, 130)
        
        self.addParent("medic")

class B_SpeedRazvitie(Branch):
    def __init__(self, game):
        super().__init__(game, "moneyUP", "b_moneyUP.png", (-1*CELL, 0))
        self.name = "Быстрое развитие"
        self.descript = "Первые 10 волн умножает ВСЮ прибыль\nВ 3 РАЗА"
        self.price = 250
        self.boxSize = (430, 100)
        
        self.addParent("start")

class B_waveSkip(Branch):
    def __init__(self, game):
        super().__init__(game, "waveSkip", "b_waveSkip.png", (-1*CELL, -CELL))
        self.name = "Сразу к делу"
        self.descript = "175 баксов в начале игры\nИгра начинается сразу с 4-й волны"
        self.price = 250
        self.boxSize = (380, 100)
        
        self.addParent("moneyUP")

class B_stunDefender(Branch):
    def __init__(self, game):
        super().__init__(game, "stunDefender", "Cat_Defender.png", (3.5*CELL, CELL/2))
        self.name = "Ловкость"
        self.descript = "Полностью отражает первый удар за волну"
        self.price = 150
        self.boxSize = (460, 70)
        
        self.addParent("support")

class B_oneShot(Branch):
    def __init__(self, game):
        super().__init__(game, "oneShot", "Cat_Attack.png", (3.5*CELL, CELL*1.5))
        self.name = "Первый выстрел"
        self.descript = "Наносит x10 урона первым выстрелом за волну"
        self.price = 150
        self.boxSize = (500, 70)
        
        self.addParent("support")

def init_branches(brManager):
    brManager.addBranch(B_NormalWaves(brManager.game))
    
    brManager.addBranch(B_SpeedRazvitie(brManager.game))
    brManager.addBranch(B_waveSkip(brManager.game))
    
    brManager.addBranch(B_Crit(brManager.game))
    
    brManager.addBranch(B_Magic(brManager.game))
    brManager.addBranch(B_Cowboy(brManager.game))
    
    brManager.addBranch(B_Worker(brManager.game))
    brManager.addBranch(B_WorkerMoneyUP(brManager.game))
    brManager.addBranch(B_WorkerMoneyUP2(brManager.game))
    
    brManager.addBranch(B_Medic(brManager.game))
    brManager.addBranch(B_Support(brManager.game))
    
    brManager.addBranch(B_stunDefender(brManager.game))
    brManager.addBranch(B_oneShot(brManager.game))
    
    brManager.loaded()