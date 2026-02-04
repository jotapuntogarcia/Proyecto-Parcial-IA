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
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = 2
        
    def move(self, jugador):
        # 1. Calculamos la distancia hacia el jugador
        dist_x = jugador.rect.centerx - self.rect.centerx
        dist_y = jugador.rect.centery - self.rect.centery
        
        # Teorema de Pitágoras
        distancia_total = math.sqrt(dist_x**2 + dist_y**2)
        
        # 2. Movimiento normalizado
        if distancia_total > 0:
            # Multiplicamos la dirección por la velocidad
            move_x = (dist_x / distancia_total) * self.velocidad
            move_y = (dist_y / distancia_total) * self.velocidad 
            
            self.rect.x += move_x
            self.rect.y += move_y
            
        # 3. Orientación del sprite
        if dist_x < 0:
            self.flip = True
        else:
            self.flip = False
            
    def update(self):
        # Velocidad de los pasos del guachimán
        cooldown_animacion = 100
        
        # Actualizar imagen actual
        self.image = self.animaciones[self.frame_index]
        
        # NOTA: Aquí agregué los () que faltaban en get_ticks
        if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            
        # Reiniciar animación al llegar al final
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0
           
    def dibujar(self, interfaz):
        # Dibujar al enemigo con el giro (flip) correspondiente
        img_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(img_flip, self.rect)