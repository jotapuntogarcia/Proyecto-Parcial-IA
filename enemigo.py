import pygame
import math
import constantes

class Enemigo():
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        self.vida = 100
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = 1.8
        
    def move(self, jugador):
        dist_x = jugador.forma.centerx - self.rect.centerx
        dist_y = jugador.forma.centery - self.rect.centery
        

        distancia_total = math.sqrt(dist_x**2 + dist_y**2)
        

        if distancia_total > 0:
            move_x = (dist_x / distancia_total) * self.velocidad
            move_y = (dist_y / distancia_total) * self.velocidad 
            
            self.rect.x += move_x
            self.rect.y += move_y
            

        if dist_x < 0:
            self.flip = True
        else:
            self.flip = False
            
    def update(self):
        cooldown_animacion = 80
        
        self.image = self.animaciones[self.frame_index]
        
        if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            

        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0
           
    def dibujar(self, interfaz):
        img_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(img_flip, self.rect)