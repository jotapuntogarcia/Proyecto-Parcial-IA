import pygame
import constantes
import random

class Delivery():
    def __init__(self, animaciones):
        self.flip = False
        self.animaciones = animaciones 
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        self.rect = self.image.get_rect()
        
        
        direccion = random.choice(["izquierda", "derecha"])
        
        if direccion == "izquerda":
            self.rect.x = -50
            self.velocidad = random.randint(6, 9)
            self.flip = False
        else:
            self.rect.x = constantes.ANCHO_VENTANA + 50
            self.velocidad = random.randint(-9, -6)
            self.flip = True
            
        self.rect.y = random.randint(50, constantes.ALTO_VENTANA - 100)
        
        self.vida = 50
        
          
    def move(self, jugador= None):
        self.rect.x += self.velocidad
        
        
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
        
        
                                 