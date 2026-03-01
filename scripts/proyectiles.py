#JUnior Garcia 19-SISN-2-011
import pygame
import math
from scripts import constantes

class Botella(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = image
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.velocidad = 7
        self.angulo_rotacion = 0
        
        x_dist = target_x - x
        y_dist = target_y - y
        self.angle = math.atan2(y_dist, x_dist)
        
        self.dx = math.cos(self.angle) * self.velocidad
        self.dy = math.sin(self.angle) * self.velocidad
        
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        #mover la botella visualmente
        self.angulo_rotacion -= 15
        self.image = pygame.transform.rotate(self.image_original, self.angulo_rotacion)    
        
        self.rect = self.image.get_rect(center=self.rect.center)
        
        #cuando salga de la pantalla desaparece
        if (self.rect.right < 0 or self.rect.left > constantes.ANCHO_VENTANA or
            self.rect.bottom < 0 or self.rect.top > constantes.ALTO_VENTANA):
            self.kill()
            
            