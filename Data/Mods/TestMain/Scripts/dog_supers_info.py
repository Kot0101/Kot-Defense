if self.mega == 2 or self.mega == 7 or self.mega == 8:
    circle_surface = pygame.Surface((self.aura_radius * 2, self.aura_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, (255, 0, 0, 100), (self.aura_radius, self.aura_radius), self.aura_radius, 2)
    screen.blit(circle_surface, (self.rect.centerx - self.aura_radius, self.rect.centery - self.aura_radius))
    if self.rect.collidepoint(pos):
        info(f'{round(self.health,1)} жизней, взрываеться и наносит {self.damage+dog_damag_boost} урона всем котам в зоне поражения', (pos[0] + 15, pos[1] + 5))
    self.stope = True