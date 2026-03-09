#JUnior Garcia 19-SISN-2-011
import pygame
from scripts import constantes
import random
import math

class Delivery():
    def __init__(self, x, y, animaciones):
        self.animaciones = animaciones 
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        self.rect = self.image.get_rect()
        
        if x > 200 and x < 1000:
            x = random.choice([-50, constantes.ANCHO_VENTANA + 50])
            y = 430 
            
        self.rect.center = (x, y)
        self.completado = False
        self.vida = 50
        self.velocidad = random.randint(7, 10)

        if self.rect.centerx < 200:
            self.objetivo_x = constantes.ANCHO_VENTANA + 200
            self.flip = False
        else:
            self.objetivo_x = -200
            self.flip = True
            
        self.objetivo_y = self.rect.centery

    def move(self, jugador, cerebro_ia, grupo_paredes):
        vel = self.velocidad
        if not self.flip: 
            self.rect.x += vel
        else:
            self.rect.x -= vel
            
        if self.rect.x > constantes.ANCHO_VENTANA + 150 or self.rect.x < -150:
            self.completado = True
                        
    def update(self):
        cooldown_animacion = 50
        self.image = self.animaciones[self.frame_index]
        
        if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0
            
    def dibujar(self, interfaz):
        img_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(img_flip, self.rect)