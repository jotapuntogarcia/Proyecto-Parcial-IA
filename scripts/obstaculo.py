#JUnior Garcia 19-SISN-2-011
import pygame

class Pared(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        
        self.image = pygame.Surface((ancho, alto))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        