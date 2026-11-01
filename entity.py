from pathlib import Path
from classes import *
from managers import *
from config import *
import pygame, random

def load_entity(game):
    class Product(Object):
        def __init__(self, sprite, cost):
            super().__init__(sprite, (0,0))
            self.cost = Stat(cost)
            self.color = (30, 30, 30)
            self.visible = False
            self.is_locked = None
            self.rendered = False
            self.moneySprite = Sprite(game.pathManager.TEXTURES / "moneybar.png", [80, 40])
            self.moneyObject = Object(self.moneySprite, [0, 0])
            
        def inited(self):
            pass
        
        def render(self, font): # Мега кастыль точка
            self.rendered = True
            size = self.sprite.size[0]
            self.text = font.render(f"{self.cost.value}", True, self.color)
            self.text_rect = self.text.get_rect()
            self.text_rect.x = self.rect.x+size//2
            self.text_rect.y = self.rect.y-28
            lSize = self.moneySprite.scale
            self.moneyObject.rect = pygame.Rect((self.text_rect.center[0]-34), self.text_rect.center[1]-20, lSize[0], lSize[1])
            self.text = font.render(f"{self.cost.value}$", True, self.color)
            self.text_rect = self.text.get_rect()
            self.text_rect.x = self.rect.x+size//2
            self.text_rect.y = self.rect.y-28
        
        def check_lock(self):
            if True: # Всегда тру, это чтобы по умолчанию всегда анлок у всех был, а так просто меняешь эту функцию на свою проверку и всё заепок работает
                return self.unlocked()
            return self.locked()
        
        def unlocked(self):
            if self.is_locked != False:
                self.visible = True
                self.is_locked = False
            return True
        
        def locked(self):
            if self.is_locked != True:
                # self.visible = False пошёл нахуй визибл
                self.is_locked = True
            return False
        
        def draw(self):
            if self.rendered == True:
                super().draw()
                
                self.moneyObject.draw()
                screen.blit(self.text, self.text_rect)
    
    class TowerProduct(Product):
        description = ""
        def __init__(self, icon, cost, name):
            self.productback = Sprite(game.pathManager.TEXTURES / "productback.png", (120, 120))
            super().__init__(self.productback, cost)
            self.icon = icon
            self.tower = name
            self.status = 0 # 0: idle, 1: hovered
        
        def animate_init(self, game):
            self.animator = Animator(self.game.animationManager)
            self.moneyObject.game = game
            self.moneyObject.animator = Animator(self.game.animationManager)
    
        def update(self):
            super().update()
            self.moneyObject.animator.update()
            if self.moneyObject.render_rect:
                self.text_rect.y = self.moneyObject.render_rect.y+6
            # Hover description
            if self.hovered == True:
                self.game.cursorManager.set_state('hovered')
                self.game.infoBar.text = self.description
                self.game.infoBar.style = 2
            # Animate
            if self.hovered == True and self.status == 0:
                self.status = 1
                self.animator.play("hover shop", loop=False)
                self.moneyObject.animator.play("hover shop", loop=False)
            elif self.hovered == False and self.status == 1:
                self.status = 0
                self.animator.play("not hover shop", loop=False)
                self.moneyObject.animator.play("not hover shop", loop=False)
            if self.clicked == True:
                remove = False
                if self.game.storeManager.ghostTower != None:
                    remove = True
                    self.game.storeManager.ghostTower = None
                    self.game.soundManager.play("deselect")
                if self.game.player.money.value >= self.cost.value and not remove:
                    self.game.soundManager.play("select")
                    self.game.storeManager.ghostTower = self.game.towerManager.prew(self.tower, self)
            if not self.animator.playing:
                if self.hovered:
                    self.animator.play("hovered shop", loop=True) # Зацикленный активный
                    self.moneyObject.animator.play("hovered shop", loop=True) 
                else:
                    self.animator.play("idle shop", loop=True)    # Зацикленный спокойный
                    self.moneyObject.animator.play("idle shop", loop=True)
        
        def draw(self):
            if not self.rendered:
                return
            
            state = self.animator.get_state()
            super().draw()
            original_icon = self.icon.image
            new_size = (
                int(original_icon.get_width() * state["scale_x"]),
                int(original_icon.get_height() * state["scale_y"])
            )
            scaled_icon = pygame.transform.smoothscale(original_icon, new_size)
            
            rotated_icon = pygame.transform.rotate(scaled_icon, state["rotation"])
            
            icon_rect = rotated_icon.get_rect()
            icon_rect.center = (
                self.rect.center[0] + state["offset_x"],
                self.rect.center[1] + state["offset_y"]
            )
            
            screen.blit(rotated_icon, icon_rect)
    
    class Tower(Object):
        max_hp = Stat(0)
        rate = Stat(0)
        range = Stat(0)
        strength = Stat(0)
        count = Stat(3)
        crit_chance = Stat(0)
        crit = Stat(2)
        def __init__(self, parent, sprite, pos):
            super().__init__(sprite, pos)
            self.parent = parent
            self.cost = Stat(parent.cost)
            self.prew = False
            
            self.flash_color = (255, 255, 255, 102)
            self.flash_timer = 0
            self.flash_duration = FPS/5
            self.cooldown = 0
            self.hp = Stat(self.max_hp.value)
            
            self.alive = True
            self.selling = False
        
        def inited(self):
            pass
        
        def flash(self, color):
            self.flash_color = color
            self.flash_timer = self.flash_duration
        
        def animate_init(self, game):
            self.animator = Animator(self.game.animationManager)
            self.animator.play("cat spawned", loop=False)
        
        def death(self):
            if self.selling == False:
                self.game.statManager.score -= 8
                self.game.statManager.deaths["towers"] += 1
        
        def take_damage(self, dmg, who=None):
            self.game.soundManager.play("bump")
            self.hp.base -= dmg
            if dmg > 0:
                self.flash((255, 0, 0, 102))
            elif dmg < 0:
                self.flash((0, 255, 0, 102))
            if self.hp.value <= 0:
                self.alive = False
        
        def crit_cheak(self):
            return self.crit.value if random.randint(1, 100) <= self.crit_chance.value and "unlock_crits" in self.game.playerO.upgrades else 1
        
        def crit_event(self, target):
            crit_manager.add_text(
                text=str(round(self.strength.value*self.crit.value,2)),
                pos=(target.rect.x, target.rect.y),
                font_size=32,
                color=(255, 50, 50),
                duration=2.0,
                max_scale=1.0, # размер
                launch_speed=-4.0, # взлёт
                deceleration=0.35, # торможение
                fall_accel=0.08 # падение
            )
        
        def attack(self, target):
            self.cooldown=0
            self.animator.play("cat attack", loop=False)
            bonus = self.crit_cheak()
            target.take_damage(self.strength.value*bonus, self)
            if bonus > 1:
                self.crit_event(target)
        
        def cheak(self):
            damaged = 0
            for e in self.game.enemyManager.enemies:
                if not e.immortality and e.alive and pygame.Vector2(self.rect.center).distance_to(e.rect.center) <= self.range.value+e.rect.width//2 and damaged < self.count.value:
                    damaged += 1
                    self.attack(e)
        
        def sell(self, per):
            self.selling = True
            self.alive = False
            self.game.player.money.base += round(self.parent.cost.value * per * 0.01)
        
        def update(self):
            input = self.game.input
            super().update()
            if self.flash_timer > 0:
                self.flash_timer -= 1
            if self.cooldown < self.rate.value:
                self.cooldown+=1
            else:
                self.cheak()
            if self.hovered == True:
                if self.clicked == True:
                    self.game.soundManager.play("meow")
                    self.animator.play("cat clicked", loop=False)
                health = round(max(0.0, self.hp.value), 1)
                max_hp = round(self.max_hp.value, 1)
                self.game.infoBar.text = f"{health:g}/{max_hp:g} HP"
                # Удаление кота: на ПК это ПКМ (или Ctrl+ПКМ), на телефоне -
                # долгое нажатие пальцем по коту.
                if self.game.input.long_press:
                    self.sell(50)
                elif not input.mouse_down(1) and (
                    (input.mouse_down(3) and input.key_down(pygame.K_LCTRL))
                    or input.mouse_pressed(3)
                ):
                    self.sell(50)
            if self.animator and not self.animator.playing and self.animator.current_anim != self.game.animationManager.animations.get("idle"):
                self.animator.play("idle", loop=True)
        
        def draw(self):
            super().draw()
            if self.hovered == True:
                self.game.cursorManager.set_state('hovered')
                radius((self.rect.centerx, self.rect.centery), (255, 255, 255), self.range.value)
    
    class Enemy(Object):
        weight = Stat(1)        # Редкость собаки (меньше - реже, 1 - деффолт)
        budget = Stat(0)        # На сколько дорогой для игры (чем больше тем меньше их спавнится будет) (к примеру если бюджет 5, то эта собака выйдет на поле бое вместо 5-ти обычных собак)
        cost = Stat(0)          # Сколько даст денег после смерти
        max_hp = Stat(0)        # Здоровье
        rate = Stat(0)          # Задержка между ударами (FPS = удар в секунду)
        speed = Stat(0)         # Скорость
        strength = Stat(0)      # Сила удара
        priority = Stat(0)      # Приоритет на получение по ебалу
        
        req_wave = Stat(0)      # С какой волны спавнится
        def __init__(self, sprite, pos, damage_player=True):
            super().__init__(sprite, pos)
            
            self.stoped = False
            self.target = None
            self.immortality = False
            
            self.flash_color = (255, 255, 255, 102)
            self.flash_timer = 0
            self.flash_duration = FPS/5
            self.cooldown = 0
            self.hp = Stat(self.max_hp.value)
            
            self.alive = True
        
        def inited(self):
            pass
        
        def flash(self, color):
            self.flash_color = color
            self.flash_timer = self.flash_duration
        
        def animate_init(self, game):
            self.animator = Animator(self.game.animationManager)
            self.animator.play("walk", loop=True)
        
        @classmethod
        def check_lock(cls, game):
            return game.waveManager.wave >= cls.req_wave.value
        
        def cheak_damage_player(self):
            if self.rect.x <= -self.sprite.scale[0]:
                self.hit_player()
            
        def move(self):
            self.rect.x -= self.speed.value
        
        def attack(self, tower):
            self.cooldown = 0
            tower.take_damage(self.strength.value, self)
        
        def death(self):
            self.game.statManager.score += max(self.budget.value, 0)
            self.game.statManager.farm_money += self.cost.value*self.game.player.farm_muiltipiler.value
            self.game.statManager.deaths["enemies"] += 1
            self.game.playerO.coins += round(max(1, self.cost.value/3))
            self.game.player.money.base += self.cost.value*self.game.player.farm_muiltipiler.value
        
        def take_damage(self, dmg, who=None):
            if self.immortality == False or dmg < 0:
                if dmg > 0:
                    self.flash((255, 0, 0, 102))
                elif dmg < 0:
                    self.flash((0, 255, 0, 102))
                self.game.soundManager.play("bump")
                self.hp.base -= dmg
                if self.hp.value <= 0:
                    self.alive = False
            else:
                self.flash((200, 200, 200, 102))
        
        def hit_player(self):
            self.game.player.health.base -= 1
            self.game.player.money.base += 30
            
            self.alive = False
        
        def cheak_towers(self):
            for t in self.game.towerManager.towers:
                if self.rect.colliderect(t.rect):
                    self.stoped = True
                    self.target = t
                    break
            else:
                self.stoped = False
                self.target = None
        
        def update(self):
            super().update()
            if self.flash_timer > 0:
                self.flash_timer -= 1
            if self.cooldown < self.rate.value:
                self.cooldown+=1
            self.cheak_towers()
            if self.target is None:
                self.move()
            elif self.cooldown==self.rate.value:
                self.attack(self.target)
            if self.hovered == True:
                if not self.immortality:
                    self.game.cursorManager.set_state('hovered')
                health = round(max(0.0, self.hp.value), 1)
                max_hp = round(self.max_hp.value, 1)
                self.game.infoBar.text = f"{health:g}/{max_hp:g} HP"
                if self.game.input.key_pressed(pygame.K_SPACE) or self.clicked == True:
                    self.take_damage(self.game.player.strength.value, self)
            self.cheak_damage_player()
        
        def draw(self):
            super().draw()

    class Dog(Enemy):
        budget = Stat(1)
        cost = Stat(2)
        max_hp = Stat(2)
        rate = Stat(FPS)
        speed = Stat(2)
        strength = Stat(1)
        def __init__(self, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Dog_Base.png", (60, 60))
            sprite.image = pygame.transform.flip(sprite.image, True, False)
            super().__init__(sprite, pos)
    
    # Spanwer Dog
    class SpawnedDog(Enemy):
        budget = Stat(0)
        cost = Stat(1)
        max_hp = Stat(0.5)
        rate = Stat(FPS*1.5)
        speed = Stat(2)
        strength = Stat(0.5)
        def __init__(self, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Dog_Base.png", (50, 50))
            sprite.image = pygame.transform.flip(sprite.image, True, False)
            super().__init__(sprite, pos)
    
    class SpawnerDog(Enemy):
        budget = Stat(30)
        cost = Stat(6)
        max_hp = Stat(15)
        rate = Stat(FPS)
        speed = Stat(1)
        strength = Stat(3)
        req_wave = Stat(10)
        priority = Stat(1)
        def __init__(self, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Dog_Base.png", (85, 85))
            sprite.image = pygame.transform.flip(sprite.image, True, False)
            super().__init__(sprite, pos)
            
            self.spawn_time = Stat(FPS*3)
            self.timer = 0
            self.moving_speed = 2
            self.moving_to = self.rect.height//2
            self.spawned = SpawnedDog
            self.UpDown = False # Чтобы чередовать верх вниз 
            
            self.moved_dog = {}
        
        def spawn(self, enemy):
            self.UpDown = not self.UpDown
            Doge = enemy((self.rect.x, self.rect.y+15))
            Doge.game = self.game
            self.game.enemyManager.enemies.append(Doge)
            Doge.UpDown = self.UpDown
            self.moved_dog[Doge] = 0
        
        def update(self):
            super().update()
            if self.spawn_time.value > self.timer:
                self.timer += 1
            
            if self.spawn_time.value == self.timer:
                self.timer = 0
                self.spawn(self.spawned)
            
            for doge, moved in self.moved_dog.items():
                if moved <= self.moving_to:
                    if doge.rect.y > upbar and doge.rect.y+doge.rect.height < HEIGHT-downbar:
                        doge.rect.y += self.moving_speed if doge.UpDown == True else self.moving_speed*-1
                    self.moved_dog[doge]+= 1
    
    # Guardian Dog
    class AliveDog(Enemy):
        budget = Stat(0)
        cost = Stat(4)
        max_hp = Stat(10)
        rate = Stat(FPS//2)
        speed = Stat(2)
        strength = Stat(0.4)
        priority = Stat(3)
        def __init__(self, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Dog_Shadow.png", (50, 50))
            sprite.image = pygame.transform.flip(sprite.image, True, False)
            super().__init__(sprite, pos)
            self.animateCircle = {
                "radius": 0,
                "timer": 0,
                "max": 36,
                "destroy": FPS # Меняется в GuardianDog.update где вызывается spawn
            }
        
        def draw(self):
            if self.immortality == True:
                pygame.gfxdraw.filled_circle(screen, self.rect.center[0], self.rect.center[1], 36, (255,255,255, 40))
                pygame.gfxdraw.circle(screen, self.rect.center[0], self.rect.center[1], self.animateCircle["radius"], (255,255,255, int(255 * (1-(self.animateCircle["timer"] / self.animateCircle["destroy"])))))
                if self.animateCircle["radius"] < self.animateCircle["max"]:
                    self.animateCircle["radius"] += 1
                elif self.animateCircle["timer"] < self.animateCircle["destroy"]:
                    self.animateCircle["timer"] += 1
                else:
                    self.animateCircle["timer"] = 0
                    self.animateCircle["radius"] = 0
            super().draw()
    
    class GuardianDog(Enemy):
        weight = Stat(0.4)
        budget = Stat(45)
        cost = Stat(9)
        max_hp = Stat(20)
        rate = Stat(FPS*3)
        speed = Stat(1)
        strength = Stat(15)
        req_wave = Stat(15)
        priority = Stat(2)
        def __init__(self, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Dog_Guardian.png", (90, 90))
            sprite.image = pygame.transform.flip(sprite.image, True, False)
            super().__init__(sprite, pos)
            self.spawned = AliveDog
            self.count = Stat(4)
            self.down = -90
            self.firstSpawn = False
            self.childers = []
        
        def death(self):
            for e in self.childers:
                e.immortality = False
                e.speed.base = 1
            super().death()
        
        def update(self):
            super().update()
            if self.firstSpawn == False:
                self.firstSpawn = True
                appendUp = abs(self.down)*2/self.count.value
                destroyAnimate = FPS
                for i in range(self.count.value):
                    self.down += appendUp
                    doge = self.spawn((self.rect.x+90+random.randint(-50, 50), min(max(self.rect.y+self.down+random.randint(-20, 20),upbar), HEIGHT-downbar-25)), self.spawned)
                    doge.animateCircle["destroy"] = destroyAnimate
                    doge.animateCircle["timer"] = destroyAnimate/(i+1)
        
        def draw(self):
            for e in self.childers:
                pygame.draw.line(screen, (150, 150, 150), self.rect.center, e.rect.center, width=random.randint(1, 4))
            super().draw()
        
        def spawn(self, pos, enemy):
            Doge = enemy(pos)
            Doge.game = self.game
            self.childers.append(Doge)
            Doge.immortality = True
            self.game.enemyManager.enemies.append(Doge)
            return Doge
    
    class BigDog(Enemy):
        budget = Stat(3)
        cost = Stat(2)
        max_hp = Stat(5)
        rate = Stat(FPS*2)
        speed = Stat(1)
        strength = Stat(4)
        def __init__(self, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Dog_Base.png", (80, 80))
            sprite.image = pygame.transform.flip(sprite.image, True, False)
            super().__init__(sprite, pos)
    
    class FastDog(Enemy):
        budget = Stat(3)
        cost = Stat(3)
        max_hp = Stat(1)
        rate = Stat(FPS/3)
        speed = Stat(4)
        strength = Stat(0.25)
        def __init__(self, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Dog_Base.png", (45, 45))
            sprite.image = pygame.transform.flip(sprite.image, True, False)
            super().__init__(sprite, pos)
    
    class ShadowDog(Enemy):
        budget = Stat(8)
        cost = Stat(5)
        max_hp = Stat(3)
        rate = Stat(FPS)
        speed = Stat(5)
        strength = Stat(0)
        req_wave = Stat(10)
        priority = Stat(1)
        def __init__(self, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Dog_Shadow.png", (80,80))
            sprite.image = pygame.transform.flip(sprite.image, True, False)
            super().__init__(sprite, pos)
            
            self.ghost_trail = []
            self.trail_length = 6 
            self.trail_interval = 3
            self._frame_count = 0
            
            self.super = True
        
        def update(self):
            super().update()
            self._frame_count += 1
            if self._frame_count >= self.trail_interval:
                self._frame_count = 0
                self.ghost_trail.append((self.rect.x, self.rect.y))
                if len(self.ghost_trail) > self.trail_length:
                    self.ghost_trail.pop(0)
            if self.super == True and self.stoped == True and self.target != None:
                self.target.take_damage(self.target.max_hp.value, self)
                self.trail_length = 0
                self.speed.base = 1
                self.strength.base = 2
                self.super = False
                return

        def draw(self):
            for i, ghost_pos in enumerate(self.ghost_trail):
                alpha = int(180 * (i + 1) / len(self.ghost_trail))
                
                ghost_surface = self.sprite.image.copy()
                ghost_surface.set_alpha(alpha)
                
                screen.blit(ghost_surface, ghost_pos)
            
            super().draw()
    
    class RightDog(Enemy):
        budget = Stat(2)
        cost = Stat(2)
        speed = Stat(2)
        max_hp = Stat(3)
        rate = Stat(FPS)
        strength = Stat(1)
        req_wave = Stat(10)
        def __init__(self, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Dog_Base.png", (60, 60))
            sprite.original_image   = sprite.image.copy()
            sprite.image = pygame.transform.flip(sprite.image, True, False)
            sprite.animate_image    = sprite.image.copy()
            sprite.animate_image.fill((255, 255, 255, 120), special_flags=pygame.BLEND_RGBA_MULT)
            super().__init__(sprite, pos)
            
            self.MoveToLeft = True
            self.Animate = False
            self.animate_speed = 8
            self.original_speed = self.speed.value
        
        def cheak_towers(self):
            if self.Animate == False:
                super().cheak_towers()

        def cheak_damage_player(self):
            if self.Animate:
                return

            if self.MoveToLeft:
                if self.rect.right < 0:
                    self.hit_player()
            else:
                if self.rect.left > WIDTH:
                    self.hit_player()

        def move(self):
            self.rect.x -= self.speed.value if self.MoveToLeft == True or self.Animate == True else self.speed.value*-1
            if self.rect.centerx <= -self.rect.width:
                self.speed.base = self.original_speed
                self.sprite.image = self.sprite.original_image
                self.Animate = False
                self.immortality = False
        
        def take_damage(self, dmg, who=None):
            if self.Animate == False:
                super().take_damage(dmg, who)
                if self.MoveToLeft == True:
                    self.stoped = False
                    self.target = None
                    self.speed.base = self.animate_speed
                    self.sprite.image = self.sprite.animate_image
                    self.MoveToLeft = False
                    self.Animate = True
                    self.immortality = True
    
    class BoomDog(Enemy):
        budget = Stat(50)
        cost = Stat(8)
        max_hp = Stat(15)
        rate = Stat(FPS*10)
        speed = Stat(5)
        strength = Stat(8)
        req_wave = Stat(20)
        weight = Stat(0.9)
        priority = Stat(3)
        def __init__(self, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Dog_BoomDog.png", (65,65))
            sprite.image = pygame.transform.flip(sprite.image, True, False)
            super().__init__(sprite, pos)
            self.explode_range = 150
        
        def explode(self, pos):
            for t in self.game.towerManager.towers:
                if pygame.Vector2(pos).distance_to(t.rect.center) <= self.explode_range+t.rect.width//2:
                    t.take_damage(self.strength.value, self)

        def death(self):
            self.explode(self.rect.center)
            self.game.soundManager.play("explode")
            super().death()
        
        def update(self):
            super().update()
            if self.stoped == True and self.target != None:
                self.explode(self.rect.center)
                self.alive = False

        def draw(self):
            radius(self.rect.center, (255, 30, 30), self.explode_range)
            
            super().draw()
    
    class GoldenDog(Enemy):
        weight = Stat(0.01)
        budget = Stat(-3)
        cost = Stat(100)
        max_hp = Stat(15)
        rate = Stat(FPS*2)
        speed = Stat(1)
        strength = Stat(20)
        def __init__(self, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Dog_Base.png", (60, 60))
            sprite.image = sprite.image.copy()
            sprite.image.fill((245, 237, 24, 255), special_flags=pygame.BLEND_RGBA_MULT)
            sprite.image = pygame.transform.flip(sprite.image, True, False)
            super().__init__(sprite, pos)
    
    #      = Attack Cat =
    class AttackCat(Tower):
        max_hp = Stat(3)
        rate = Stat(FPS*2)
        range = Stat(156)
        strength = Stat(1)
        crit_chance = Stat(3)
        count = Stat(2)
        def __init__(self, parent, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Attack.png", (cat_base_size, cat_base_size))
            super().__init__(parent, sprite, pos)
            self.oneShotBuff = Modifier("One Shot Buff", 10, "multiply")
            self.oneShots = 0
            self.oneShotsTemp = 0
            self.oldWave = self.parent.game.waveManager.wave
        
        def inited(self):
            if "oneShot" in self.game.playerO.upgrades:
                self.oneShots = 1
                self.oneShotsTemp = self.oneShots
        
        def attack(self, target):
            if self.oneShotsTemp > 0:
                self.oneShotsTemp -= 1
                self.strength.add(self.oneShotBuff)
            else:
                self.strength.remove(self.oneShotBuff)
                
            super().attack(target)
        
        def update(self):
            super().update()
            if self.game.waveManager.wave >= self.oldWave + 1:
                self.oldWave = self.game.waveManager.wave
                self.oneShotsTemp = self.oneShots
    
    class AttackCatProduct(TowerProduct):
        description = "Атакует раз в 2 секунды и наносит 1 урона" # Attacks once every 2 seconds and deals 1 damage
        def __init__(self):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Attack.png", (85, 85))
            super().__init__(sprite, cost=10, name="Cat")
        
        def check_lock(self):
            if self.game.gid.counter > 1488 or self.game.tutor == False:
                return self.unlocked()
            return self.locked()
    
    #      = DefenseCat Cat =
    class DefenseCat(Tower):
        max_hp = Stat(15)
        rate = Stat(0)
        range = Stat(0)
        strength = Stat(0)
        def __init__(self, parent, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Defender.png", (cat_base_size, cat_base_size))
            # sprite.image = pygame.transform.flip(sprite.image, True, False)
            self.stuns = 0
            self.stunsTemp = 0
            super().__init__(parent, sprite, pos)
            self.oldWave = self.parent.game.waveManager.wave
        
        def stun_regen(self):
            self.stunsTemp = self.stuns
        
        def death(self):
            self.event.cancel()
            super().death()
        
        def inited(self):
            self.event = eventManager.subscribe("wave end", self.stun_regen)
            if "stunDefender" in self.game.playerO.upgrades:
                self.stuns = 1
                self.stunsTemp = self.stuns
        
        def take_damage(self, dmg, who=None):
            if self.stunsTemp > 0 and dmg > 0:
                self.flash((255, 255, 255, 102))
                self.stunsTemp -= 1
                self.game.soundManager.play("bump revers")
                if who != None:
                    who.take_damage(dmg, self)
                return
            super().take_damage(dmg, who)
    
    class DefenseCatProduct(TowerProduct):
        description = "Не атакует, имеет большое здоровье" # Doesn't attack, has high health
        def __init__(self):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Defender.png", (85, 85))
            super().__init__(sprite, cost=5, name="DefenseCat")
        
        def check_lock(self):
            if self.game.gid.counter > 1488 or self.game.tutor == False:
                return self.unlocked()
            return self.locked()
    
    #      = Medic Cat =
    class MedicCat(Tower):
        max_hp = Stat(6)
        rate = Stat(FPS*3.5)
        range = Stat(80)
        strength = Stat(3)
        def __init__(self, parent, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Medic.png", (cat_base_size, cat_base_size))
            super().__init__(parent, sprite, pos)
            self.oldRate = self.rate.value
            self.fastRate = FPS//2
        
        def cheak(self):
            damaged = 0
            for t in self.game.towerManager.towers:
                if pygame.Vector2(self.rect.center).distance_to(t.rect.center) <= self.range.value+t.rect.width//2 and t.hp.value < t.max_hp.value:
                    damaged += 1
                    self.attack(t)
            if damaged > 0:
                self.game.soundManager.play("heal")
                self.animator.play("cat attack", loop=False)
        
        def attack(self, target):
            self.cooldown=0
            if target.hp.value+self.strength.value < target.max_hp.value:
                target.hp.base += self.strength.value
            else:
                target.hp.base = target.max_hp.value
            target.flash((0, 255, 0, 102))
        
        def update(self):
            super().update()
            if self.game.waveManager.clear == True:
                self.rate.base = self.fastRate
            else:
                self.rate.base = self.oldRate
    
    class MedicCatProduct(TowerProduct):
        description = "Лечит 3-х союзников на 3хп раз 3.5 сек во время волны \nи 0.5 сек в мирное время" # Heals their teammates for 3 HP every 3.5 sec.\nduring a wave and 0.5 sec. during intermission
        def __init__(self):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Medic.png", (89, 89))
            super().__init__(sprite, cost=100, name="MedicCat")
        
        def check_lock(self):
            if self.game.waveManager.wave > 4 and "medic" in self.game.playerO.upgrades:
                return self.unlocked()
            return self.locked()
    
    #      = Worker Cat =
    class WorkerCat(Tower):
        max_hp = Stat(2)
        rate = Stat(1)
        range = Stat(0)
        strength = Stat(7)
        def __init__(self, parent, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Worker.png", (cat_base_size, cat_base_size))
            super().__init__(parent, sprite, pos)
            self.randomazer = 0
        
        def death(self):
            self.event.cancel()
            super().death()
        
        def inited(self):
            self.event = eventManager.subscribe("wave end", self.farm)
            if "workerUP" in self.game.playerO.upgrades:
                self.strength.base += 1
            if "workerUP2" in self.game.playerO.upgrades:
                self.strength.base += 1
        
        def farm(self):
            self.randomazer = random.randint(0, 40)
        
        def pay(self):
            self.game.soundManager.play("bump", volume=0.9)
            self.animator.play("cat attack", loop=False)
            money=self.strength.value
            self.game.statManager.farm_money += money
            self.game.player.money.base += money
            crit_manager.add_text(
                text=f"+{money}$",
                pos=self.rect.center,
                font_size=32,
                color=(11, 210, 31),
                duration=2.0,
                max_scale=1.0, # размер
                launch_speed=-4.0, # взлёт
                deceleration=0.35, # торможение
                fall_accel=0.08 # падение
            )
        
        def update(self):
            super().update()
            if self.randomazer > 0:
                self.randomazer -= 1
                if self.randomazer == 0:
                    self.pay()
    
    class WorkerCatProduct(TowerProduct):
        description = "Зарабатывает 7 денег после волны" # Makes 7 currency at the start of every wave
        def __init__(self):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Worker.png", (95, 95))
            super().__init__(sprite, cost=50, name="WorkerCat")
        
        def inited(self):
            if "workerUP" in self.game.playerO.upgrades:
                self.description = "Зарабатывает 8 денег после волны"
            if "workerUP2" in self.game.playerO.upgrades:
                self.description = "Зарабатывает 9 денег после волны"
        
        def check_lock(self):
            if "worker" in self.game.playerO.upgrades:
                return self.unlocked()
            return self.locked()
    
    #      = Magic Cat =
    class MagicCat(Tower):
        max_hp = Stat(5)
        rate = Stat(FPS*3.5)
        range = Stat(350)
        strength = Stat(1)
        crit_chance = Stat(4)
        def __init__(self, parent, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Magic.png", (cat_base_size, cat_base_size))
            super().__init__(parent, sprite, pos)
            self.count = Stat(1)
            self.explode_range = Stat(75)
            self.explode_life = Stat(FPS*0.5)
            
            self.exp_pos = (0, 0)
            self.exp_rad_life = 0
        
        def explode(self, pos):
            self.exp_pos = pos
            self.exp_rad_life = self.explode_life.value
            for e in self.game.enemyManager.enemies:
                if pygame.Vector2(pos).distance_to(e.rect.center) <= self.explode_range.value+e.rect.width//2-5:
                    self.attack(e)
        
        def cheak(self):
            damaged = 0
            for e in self.game.enemyManager.enemies:
                if e.immortality == False and pygame.Vector2(self.rect.center).distance_to(e.rect.center) <= self.range.value+e.rect.width//2 and damaged < self.count.value:
                    damaged += 1
                    self.explode(e.rect.center)
        
        def draw(self):
            super().draw()
            if self.exp_rad_life > 0:
                self.exp_rad_life -= 1
                radius(self.exp_pos, (200, 40, 40), self.explode_range.value)
    
    class MagicCatProduct(TowerProduct):
        description = "Атакует сплеш атакой которая наносит 1 урон ВСЕМ собакам" # idk
        def __init__(self):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Magic.png", (85, 85))
            super().__init__(sprite, cost=50, name="MagicCat")
        
        def check_lock(self):
            if self.game.waveManager.wave > 9 and "magic" in self.game.playerO.upgrades:
                return self.unlocked()
            return self.locked()

    #      = Cowboy Cat =
    class CowboyCat(Tower):
        max_hp = Stat(2)
        count = Stat(1)
        rate = Stat(FPS*0.25)
        reload = Stat(FPS*4)
        shots = Stat(3) # Крч 3 выстрела делает а потом большую перезарядку
        range = Stat(240)
        strength = Stat(0.5)
        crit_chance = Stat(30)
        count = Stat(1)
        def __init__(self, parent, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Cowboy.png", (cat_base_size, cat_base_size))
            super().__init__(parent, sprite, pos)
            self.reloadTemp = 0
            self.shotsTemp = 0
            self.rangeTemp = self.range.value
            self.attackPos = self.rect.center
            self.attacked = []
            self.attackedPos = []
            self.animateLines = [] # [60, [..., ...]] # [time, [point, point, ...]]
        
        def stop_crits(self):
            self.animateLines.append([60, self.attackedPos]) 
            self.attacked = []
            self.attackedPos = []
            self.attackPos = self.rect.center
            self.rangeTemp = self.range.value
        
        def crit_event(self, target):
            super().crit_event(target)
            self.rangeTemp /= 1.5
            self.cheak(True)
        
        def draw(self):
            super().draw()
            for anim in self.animateLines:
                time = anim[0]
                positions = anim[1]
                if len(positions) > 1:
                    anim[0] -= 1
                    
                    pygame.draw.lines(screen, (225, 210, 30), False, positions, round(time/5)) # round(255*(time/60))
                else:
                    anim[0] = 0
            self.animateLines = [a for a in self.animateLines if a[0] > 0]
        
        def attack(self, target):
            self.cooldown=0
            self.animator.play("cat attack", loop=False)
            bonus = self.crit_cheak()
            target.take_damage(self.strength.value*bonus, self)
            if bonus > 1:
                if self.attackPos == self.rect.center:
                    self.attackedPos.append(self.attackPos)
                self.attackPos = target.rect.center
                self.attacked.append(target)
                self.attackedPos.append(target.rect.center)
                self.crit_event(target)
            else:
                self.stop_crits()
        
        def update(self):
            super().update()
            if self.shotsTemp > 0:
                self.reloadTemp += 1
            if self.reloadTemp >= self.reload.value:
                self.shotsTemp = 0
                self.reloadTemp = 0
            if self.game.waveManager.clear == True:
                self.shotsTemp = 0
                self.reloadTemp = 0
        
        def cheak(self, rikoshettt=False):
            damaged = 0
            if self.shotsTemp < self.shots.value and self.rangeTemp > 0:
                for e in self.game.enemyManager.enemies:
                    if e.immortality == False and pygame.Vector2(self.attackPos).distance_to(e.rect.center) <= self.range.value+e.rect.width//2 and damaged < self.count.value and e not in self.attacked:
                        damaged += 1
                        self.attack(e)
            if damaged == 0 and len(self.attacked) > 0:
                self.stop_crits()
            elif damaged > 0 and not rikoshettt:
                self.shotsTemp += 1
                self.reloadTemp = 0
    
    class CowboyCatProduct(TowerProduct):
        description = "Криты заставляют рикошетить пулю"
        def __init__(self):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Cowboy.png", (85, 85))
            super().__init__(sprite, cost=40, name="CowboyCat")
        
        def check_lock(self):
            if self.game.waveManager.wave > 4 and "cowboy" in self.game.playerO.upgrades:
                return self.unlocked()
            return self.locked()
    
    #      = Support Cat =
    class SupportCat(Tower):
        max_hp = Stat(6)
        rate = Stat(FPS*0.1)
        range = Stat(80)
        strength = Stat(3)
        def __init__(self, parent, pos):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Support.png", (cat_base_size, cat_base_size))
            super().__init__(parent, sprite, pos)
            self.rateBuff = Modifier("Support rate buff", -11, "precent")
            self.rangeBuff = Modifier("Support range buff", 8, "precent")
            self.critBuff = Modifier("Support crit buff", 11, "precent")
        
        def death(self):
            self.cheak(False)
            super().death()
        
        def cheak(self, life = True):
            for t in self.game.towerManager.towers:
                if pygame.Vector2(self.rect.center).distance_to(t.rect.center) <= self.range.value+t.rect.width//2 and t.parent.tower != "SupportCat":
                    if life == True:
                        self.attack(t)
                    else:
                        t.rate.remove(self.rateBuff)
                        t.crit_chance.remove(self.critBuff)
                        t.range.remove(self.rangeBuff)
                        if t.parent.tower == "CowboyCat":
                            t.reload.remove(self.rateBuff)
        
        def attack(self, target):
            target.rate.add(self.rateBuff)
            target.crit_chance.add(self.critBuff)
            target.range.add(self.rangeBuff)
            if target.parent.tower == "CowboyCat": # Я пока хз как проверить есть ли переменная reload
                target.reload.add(self.rateBuff)
    
    class SupportCatProduct(TowerProduct):
        description = "Уменьшает перезарядку на 11% союзникам во круг него,\nна 8% Увеличивает радиус и на 11% повышает шанса крита"
        def __init__(self):
            sprite = Sprite(game.pathManager.TEXTURES / "Cat_Support.png", (89, 89))
            super().__init__(sprite, cost=60, name="SupportCat")
        
        def check_lock(self):
            if self.game.waveManager.wave > 9 and "support" in self.game.playerO.upgrades:
                return self.unlocked()
            return self.locked()
    
    
    game.enemyManager.init(Dog, "Dog")
    game.enemyManager.init(GuardianDog, "GuardianDog")
    game.enemyManager.init(GoldenDog, "GoldenDog")
    game.enemyManager.init(BigDog, "BigDog")
    game.enemyManager.init(FastDog, "FastDog")
    game.enemyManager.init(ShadowDog, "ShadowDog")
    game.enemyManager.init(BoomDog, "BoomDog")
    game.enemyManager.init(RightDog, "RightDog")
    game.enemyManager.init(SpawnerDog, "SpawnerDog")
    
    
    game.towerManager.init(AttackCat, "Cat")
    game.storeManager.init(AttackCatProduct())
    
    game.towerManager.init(DefenseCat, "DefenseCat")
    game.storeManager.init(DefenseCatProduct())
    
    game.towerManager.init(MagicCat, "MagicCat")
    game.storeManager.init(MagicCatProduct())
    
    game.towerManager.init(SupportCat, "SupportCat")
    game.storeManager.init(SupportCatProduct())
    
    game.towerManager.init(WorkerCat, "WorkerCat")
    game.storeManager.init(WorkerCatProduct())
    
    game.towerManager.init(MedicCat, "MedicCat")
    game.storeManager.init(MedicCatProduct())
    
    game.towerManager.init(CowboyCat, "CowboyCat")
    game.storeManager.init(CowboyCatProduct())
    
    
    game.storeManager.restore()