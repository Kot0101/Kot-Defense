if self.typee == 2:
    if self.who == []:
        pass
    elif self.damagecats == self.who.blacklist:
        self.health -= damage
    else:
        self.stope = True
if self.health <= 0:
    if self.mega == 6 and self.val3 == 0:
        self.health = 0.1
        self.val3 = 1
        self.stope = True
    elif self.mega == 6 and self.val3 == 1:
        self.health = 0.1
        self.stope = True
        