moveE = True
for cat in list(cats):
    if self.rect.colliderect(cat.rect):
        if cat.follow_mouse == False:
            moveE = False
for cat2 in list(cats):
    if self.rect.colliderect(cat2.rect):
        if moveE == False:
            if cat2.mega == 5:
                self.bump(self.maxhealth/(100-cat2.damage), True, [])
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
        if self.rect.colliderect(cat2.rect):
            if moveE == False:
                try:
                    dog_bump.play()
                except:
                    pass
                cat2.bump(self.damage+dog_damag_boost)
                self.stope = True
elif self.mega == 6 and reloade == self.reload:
    for cat2 in list(cats):
        if self.rect.colliderect(cat2.rect):
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
        try:
            boom.play()
        except:
            pass
        dogs.remove(self)
        del self