global money
if reloadType == self.reload:
    count_attacs = 0
    if not self.follow_mouse:
        if self.mega == 2:
            money += self.damage+cat_works_boost
        elif self.mega == 4:
            for cat in list(cats):
                if count_attacs < self.dogs_count:
                    if pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(cat.rect.center)) <= self.aura_radius:
                        if cat.maxhe > cat.health:
                            cat.bump(-self.damage)
                        if cat.maxhe < cat.health:
                            cat.health = cat.maxhe
                else:
                    break