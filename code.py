import pygame
import os
import random
import threading

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

width = 1400
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kot Defense")

black = (0, 0, 0)
green = (30, 150, 30)
gray = (100, 100, 100)
light_gray = (170, 170, 170)
white = (255, 255, 255)
red = (255, 0, 0)

#загрузка звуков, музыки
pygame.mixer.music.load('Data/Sounds/music.mp3')
dog_bump = pygame.mixer.Sound('Data/Sounds/bump.mp3')
boom = pygame.mixer.Sound('Data/Sounds/boom.mp3')

#загрузка шрифтов
font = pygame.font.Font("Data/Fonts/segoe-ui-symbol.ttf", 36)
font2 = pygame.font.Font(None, 25)

#загрузка изображений
dog_image = pygame.image.load('Data/Img/Dog1.png')
dog2_image = pygame.image.load('Data/Img/Dog2.jpg')
dog3_image = pygame.image.load('Data/Img/Dog3.png')
cat_image = pygame.image.load('Data/Img/Cat1.png')
cat2_image = pygame.image.load('Data/Img/Cat2.png')
cat3_image = pygame.image.load('Data/Img/Cat3.png')
cat4_image = pygame.image.load('Data/Img/Cat4.png')
cat5_image = pygame.image.load('Data/Img/Cat5.png')
pause_image = pygame.image.load('Data/Img/pause.png')

#обработка изображений
dog_image = pygame.transform.scale(dog_image, (60, 60))
dog2_image = pygame.transform.scale(dog2_image, (60, 60))
dog3_image = pygame.transform.scale(dog3_image, (60, 60))
cat_image = pygame.transform.scale(cat_image, (60, 60))
cat2_image = pygame.transform.scale(cat2_image, (60, 60))
cat3_image = pygame.transform.scale(cat3_image, (60, 60))
cat4_image = pygame.transform.scale(cat4_image, (60, 60))
cat5_image = pygame.transform.scale(cat5_image, (60, 60))
pause_image = pygame.transform.scale(pause_image, (40, 40))

#классы
class Dog:
    def __init__(self, x, y, image, health_dog, money_dog, speed, damage_dog, unikal):
        self.rect = image.get_rect(topleft=(x, y))
        self.image = image
        self.speed = speed
        self.health = health_dog
        self.money = money_dog
        self.damage = damage_dog
        self.mega = unikal
        self.aura_radius = 200-30

    def move(self, pos):
        moveE = True
        for cat in list(cats):
            if self.rect.colliderect(cat.rect):
                if cat.follow_mouse == False:
                    moveE = False
        if moveE:
            self.rect.x += self.speed
        screen.blit(self.image, self.rect)
        if self.mega == 2:
            circle_surface = pygame.Surface((self.aura_radius * 2, self.aura_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (255, 0, 0, 100), (self.aura_radius, self.aura_radius), self.aura_radius, 2)
            screen.blit(circle_surface, (self.rect.centerx - self.aura_radius, self.rect.centery - self.aura_radius))
            if self.rect.collidepoint(pos):
                info(f'{round(self.health,1)} жизней, взрываеться и наносит {self.damage} урона всем котам в зоне поражения', (pos[0] + 15, pos[1] + 5))
        else:
            if self.rect.collidepoint(pos):
                info(f'{round(self.health,1)} жизней, урон {self.damage}, скорость {self.speed}', (pos[0] + 15, pos[1] + 5))
        
        
    def bump(self, damage, die):
        global money
        self.health -= damage
        if self.health <= 0:
            if die:
                money += self.money
            dogs.remove(self)
    
    def attack(self):
        global dogs, cats
        if self.mega == 1:
            for cat2 in list(cats):
                if self.rect.colliderect(cat2.rect):
                    dog_bump.play()
                    cat2.bump(self.damage)
        elif self.mega:
            boomp = False
            for cat3 in list(cats):
                if self.rect.colliderect(cat3.rect):
                        boomp = True
            if boomp == True:
                for cat2 in list(cats):
                    distance = ((self.rect.x - cat2.rect.x)**2 + (self.rect.y - cat2.rect.y)**2)**0.5
                    if distance <= 200:
                        cat2.bump(self.damage)
                boom.play()
                dogs.remove(self)
                del self

class Cat:
    def __init__(self, image, aura_radius, cat_health, dogs_count, cat_money, reload, damage_cat, mega):
        self.original_image = image.convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.aura_radius = aura_radius
        self.follow_mouse = True
        self.health = cat_health
        self.dogs_count = dogs_count
        self.money = cat_money
        self.reload = reload
        self.damage = damage_cat
        self.unable_to_place = False
        self.mega = mega

    def update(self, pos):
        pause_rect = pause_image.get_rect(topleft=(width-55, 10))
        rect22 = pygame.Rect(0, height-160, 1400, 160)
        if self.follow_mouse:
            self.rect.center = pos
            self.image.set_alpha(128)
            cat_collides = any(cat.rect.colliderect(c.rect) for c in cats if c != self)
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
            if pygame.mouse.get_pressed()[2] and self.rect.collidepoint(pos):
                self.sell(0.5)
            if rect22.collidepoint(self.rect.center):
                self.sell(1)
    
    def bump(self, damage):
        global cats
        if self.follow_mouse == False:
            self.health -= damage
            if self.health <= 0:
                self.sell(0)
    
    def draw(self, screen, pos):
        global cat
        if self.aura_radius > 0: 
            if self.rect.collidepoint(pos) or catown != None:
                circle_surface = pygame.Surface((self.aura_radius * 2, self.aura_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (255, 255, 255, 100), (self.aura_radius, self.aura_radius), self.aura_radius, 2)
                screen.blit(circle_surface, (self.rect.centerx - self.aura_radius, self.rect.centery - self.aura_radius))
        screen.blit(self.image, self.rect)
        if self.rect.collidepoint(pos) and self.follow_mouse == False:
            info(f'{round(self.health,1)} жизней', (pos[0] + 15, pos[1] + 5))
    
    def remove_dogs_periodically(self, reloadType):
        global money
        if reloadType == self.reload:
            count_attacs = 0
            if not self.follow_mouse:
                if self.mega == 2:
                    money += 1
                for dog in list(dogs):
                    if count_attacs < self.dogs_count:
                        if pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(dog.rect.center)) <= self.aura_radius:
                            count_attacs += 1
                            if self.image != cat4_image:
                                dog_bump.play()
                            else:
                                boom.play()
                            dog.bump(self.damage, True)
    
    def sell(self, mn):
        global money, pause
        money += round(self.money * mn)
        cats.remove(self)
        del self
    
    def handle_mouse_click(self, pos):
        global catown, cats, dogs
        if self == catown:
            rect22 = pygame.Rect(0, height-100, 1400, 100)
            if pygame.mouse.get_pressed()[0] and self.unable_to_place == True:
                rect = pygame.Rect(0, height-100, 1400, 100)
                self.follow_mouse = False
                catown = None

global music_playing
music_playing = True
pygame.mixer.music.play(-1)
dog_bump.set_volume(0.1)
boom.set_volume(0.1)
pygame.mixer.music.set_volume(0.1)

def show_lose_screen():
    font = pygame.font.Font(None, 70)
    text = font.render("Вы проиграли. Нажмите ПКМ, чтобы начать заново.", True, black)
    text_rect = text.get_rect(center=(width/2, height/2))
    screen.fill(green)
    screen.blit(text, text_rect)
    pygame.display.flip()
    started = True
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and started:
                started = False
                start()
                return

def info(text, position):
    text_surface = font2.render(text, True, light_gray)
    text_rect = text_surface.get_rect()
    text_rect.topleft = position
    
    screen.blit(font2.render(text, True, (0, 0, 0)), (text_rect.x - 2, text_rect.y))
    screen.blit(font2.render(text, True, (0, 0, 0)), (text_rect.x + 2, text_rect.y))
    screen.blit(font2.render(text, True, (0, 0, 0)), (text_rect.x, text_rect.y - 2))
    screen.blit(font2.render(text, True, (0, 0, 0)), (text_rect.x, text_rect.y + 2))
    
    screen.blit(text_surface, text_rect.topleft)


#старт игры
def start():
    global health, dogs, cats, cat, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing
    del_cat = False
    health = 10
    money = 30
    dogs = []
    catown = None
    cats = []
    dogs_variants = {"Dog": 1, "FastDog": 5, "BigDog": 7, "KillerDog":10, "KiberDog":75, "BoomDog":200}
    dogs_moneys = {"Dog": 3, "FastDog": 7, "BigDog": 15, "KillerDog":20, "KiberDog":100, "BoomDog":300}

    budget = 2
    pause = False
    
    frame_count = 0
    frame_count2 = 0
    frame_count3 = 0
    frame_count4 = 0
    plustime = 0
    new_wey = 60*10
    wave = 1
    for_mega_wave = 4
    game()
    return

def game():
    global health, dogs, cats, cat, dogs_variants, del_cat, money, catown, dogs_moneys, budget, frame_count, frame_count2, frame_count3, frame_count4, plustime, new_wey, wave, for_mega_wave, pause, music_playing 
    running = True
    clock = pygame.time.Clock()
    while running:
        del_cat = False
        pause_rect = pause_image.get_rect(topleft=(width-55, 10))
        cat_rect = cat_image.get_rect(topleft=(20, height-77))
        cat_rect2 = cat2_image.get_rect(topleft=(100, height-77))
        cat_rect3 = cat3_image.get_rect(topleft=(260, height-77))
        cat_rect4 = cat4_image.get_rect(topleft=(180, height-77))
        cat_rect5 = cat5_image.get_rect(topleft=(340, height-77))
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if music_playing:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    music_playing = not music_playing
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and pause:
                pause = False
            if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                if pygame.mouse.get_pressed()[0]:
                    for dog in list(dogs):
                        if dog.rect.collidepoint(pos):
                            dog_bump.play()
                            dog.bump(0.1, True)
                if catown is not None:
                    catown.handle_mouse_click(pos)
                
                
                if cat_rect.collidepoint(pos) and del_cat == False:
                    if catown:
                        catown.sell(1)
                        catown = None
                    else:
                        if money >= 10:
                            money -= 10
                            new_cat = Cat(cat_image, 130, 4, 3, 10, 1, 1, 1) 
                            catown = new_cat
                            cats.append(new_cat)
                elif cat_rect2.collidepoint(pos) and del_cat == False:
                    if catown:
                        catown.sell(1)
                        catown = None
                    else:
                        if money >= 50:
                            money -= 50
                            new_cat = Cat(cat2_image, 0, 22, 0, 50, 1, 0, 1)
                            catown = new_cat
                            cats.append(new_cat)
                elif cat_rect3.collidepoint(pos) and del_cat == False:
                    if catown:
                        catown.sell(1)
                        catown = None
                    else:
                        if money >= 200:
                            money -= 200
                            new_cat = Cat(cat3_image, 400, 6, 10, 200, 2, 15, 1) 
                            catown = new_cat
                            cats.append(new_cat)
                elif cat_rect4.collidepoint(pos) and del_cat == False:
                    if catown:
                        catown.sell(1)
                        catown = None
                    else:
                        if money >= 100:
                            money -= 100
                            new_cat = Cat(cat4_image, 150, 10, 2, 100, 3, 1.5, 1) 
                            catown = new_cat
                            cats.append(new_cat)
                elif cat_rect5.collidepoint(pos) and del_cat == False:
                    if catown:
                        catown.sell(1)
                        catown = None
                    else:
                        if money >= 70:
                            money -= 70
                            new_cat = Cat(cat5_image, 0, 10, 0, 70, 2, 0, 2) 
                            catown = new_cat
                            cats.append(new_cat)
                if pause_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                    pause = True
        
        if not pause:
            screen.fill(green)
            
            for dog in list(dogs):
                dog.move(pos)
                if dog.rect.x > width+60:
                    health -= 1
                    dogs.remove(dog)
            
            pygame.draw.rect(screen, gray, (0, height-135, 1400, 135))
            health_text = font.render("❤️ "+str(health), True, (0, 0, 0))
            screen.blit(health_text, (10, 10))
            heart_text2 = font.render("❤️", True, red)
            screen.blit(heart_text2, (10, 10))
            screen.blit(cat_image, (20, height-77))
            
            money_text = font.render("💵 "+str(money), True, (0, 0, 0))
            screen.blit(money_text, (10, 45))
            money_text2 = font.render("💵", True, (10, 80, 10))
            screen.blit(money_text2, (10, 45))
            
            if for_mega_wave >0:
                wave_text = font.render("Wave: "+str(wave), True, (0, 0, 0))
                screen.blit(wave_text, (10, 80))
            else:
                wave_text = font.render("Mega wave: "+str(wave), True, (0, 0, 0))
                screen.blit(wave_text, (10, 80))
            
            screen.blit(pause_image, (width-55, 10))
            
            screen.blit(cat_image, (20, height-77))
            cat_mon1 = font.render("10$", True, black)
            screen.blit(cat_mon1, (23, height-130))
            
            screen.blit(cat2_image, (100, height-77))
            cat_mon2 = font.render("50$", True, black)
            screen.blit(cat_mon2, (103, height-130))
            
            screen.blit(cat4_image, (180, height-77))
            cat_mon4 = font.render("100$", True, black)
            screen.blit(cat_mon4, (180, height-130))
            
            screen.blit(cat3_image, (260, height-77))
            cat_mon3 = font.render("200$", True, black)
            screen.blit(cat_mon3, (260, height-130))
            
            screen.blit(cat5_image, (340, height-77))
            cat_mon3 = font.render("70$", True, black)
            screen.blit(cat_mon3, (343, height-130))
            
            frame_count += 1
            frame_count2 += 1
            frame_count3 += 1
            frame_count4 += 1
            
            if frame_count >= 60:
                for cat in cats:
                    cat.remove_dogs_periodically(1)
                for dog in list(dogs):
                    dog.attack()
                frame_count = 0
            if frame_count3 >= 60*3:
                for cat in cats:
                    cat.remove_dogs_periodically(2)
                for dog in list(dogs):
                    dog.attack()
                frame_count3 = 0
            if frame_count4 >= 30:
                for cat in cats:
                    cat.remove_dogs_periodically(3)
                for dog in list(dogs):
                    dog.attack()
                frame_count4 = 0
            
            if len(dogs) == 0:
                if new_wey < 0:
                    new_wey = 60 * (10+plustime)
                elif new_wey == 0:
                    new_wey = -1
                    budget += 5
                    budget += round(budget/5)
                    remaining_budget =0
                    remaining_budget = budget
                    for_mega_wave -= 1
                    wave += 1
                    if plustime < 50 and wave >= 4:
                        plustime += 5
                    if for_mega_wave == 0:
                        remaining_budget = remaining_budget * 2
                    if for_mega_wave == -1:
                        for_mega_wave = 4
                    while remaining_budget > 0:
                        dog_type = random.choice(list(dogs_variants.keys()))
                        dog_cost = dogs_variants[dog_type]
                        dog_mon = dogs_moneys[dog_type]
                        if dog_cost <= remaining_budget:
                            if dog_type == "Dog":
                                new_dog = Dog(random.randint(-900, -60), random.randint(70, height - 195), dog_image, 2, dog_mon, 2, 1, 1)
                            elif dog_type == "FastDog":
                                new_dog = Dog(random.randint(-900, -60), random.randint(70, height - 195), dog_image, 1, dog_mon, 4, 1, 1)
                            elif dog_type == "BigDog":
                                new_dog = Dog(random.randint(-900, -60), random.randint(70, height - 195), dog_image, 6, dog_mon, 1, 1, 1)
                            elif dog_type == "KillerDog":
                                new_dog = Dog(random.randint(-900, -60), random.randint(70, height - 195), dog_image, 4, dog_mon, 3, 4, 1)
                            elif dog_type == "KiberDog":
                                new_dog = Dog(random.randint(-900, -60), random.randint(70, height - 195), dog2_image, 30, dog_mon, 1, 6, 1)
                            elif dog_type == "BoomDog":
                                new_dog = Dog(random.randint(-900, -60), random.randint(70, height - 195), dog3_image, 10, dog_mon, 5, 20, 2)
                            
                            dogs.append(new_dog)
                            remaining_budget -= dog_cost
                else:
                    new_wey -= 1
            
            for cat in cats:
                cat.update(pygame.mouse.get_pos())
                cat.draw(screen, pos)
            
            if cat_rect.collidepoint(pos):
                info('4 жизни, атакует 2 собаки за раз, средняя перезарядка, 1 урон', (pos[0] + 15, pos[1] + 5))
            if cat_rect2.collidepoint(pos):
                info('22 жизни, не атакует собак', (pos[0] + 15, pos[1] + 5))
            if cat_rect3.collidepoint(pos):
                info('6 жизнь, атакует 10 собаки за раз, долгая перезарядка, 15 урон', (pos[0] + 15, pos[1] + 5))
            if cat_rect4.collidepoint(pos):
                info('10 жизнь, атакует 2 собаки за раз, быстрая перезарядка, 1.5 урон', (pos[0] + 15, pos[1] + 5))
            if cat_rect5.collidepoint(pos):
                info('10 жизней, не атакует собак, но зарабатывает 1$ в 5 секунд', (pos[0] + 15, pos[1] + 5))
        else:
            fonte = pygame.font.Font(None, 75)
            text = fonte.render("Пауза. Нажмите ПКМ, чтобы снять с паузы", True, black)
            text_rect = text.get_rect(center=(width/2, height/2))
            screen.fill(green)
            screen.blit(text, text_rect)
            pygame.display.flip()
            started = True
        pygame.display.flip()
        clock.tick(60)
        if health <=0:
            show_lose_screen()
            return
start()
pygame.quit()