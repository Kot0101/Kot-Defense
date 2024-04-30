moveE = True
for cat in list(cats):
    if self.rect.colliderect(cat.rect):
        if cat.follow_mouse == False:
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
        screen.blit(self.image, self.rect)
        self.stope = True
elif self.mega == 9:
    self.rect.x += self.speed
    self.stope == True