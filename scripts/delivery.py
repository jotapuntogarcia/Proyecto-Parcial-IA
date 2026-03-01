#JUnior Garcia 19-SISN-2-011
import pygame
from scripts import constantes
import random
import math

class Delivery():
    def __init__(self, animaciones):
        self.flip = False
        self.animaciones = animaciones 
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        self.rect = self.image.get_rect()
        self.completado = False
        

        direccion = random.choice(["izquierda", "derecha"])
        
        if direccion == "izquierda":
            self.rect.x = -50
            self.objetivo_x = constantes.ANCHO_VENTANA + 100
            self.velocidad = random.randint(6, 9)
            self.flip = False
        else:
            self.rect.x = constantes.ANCHO_VENTANA + 50
            self.objetivo_x = -100
            self.velocidad = random.randint(6, 9)
            self.flip = True 
            
        self.rect.y = random.randint(50, constantes.ALTO_VENTANA - 100)
        self.vida = 50
        
    def move(self, jugador, cerebro_ia, grupo_paredes):
        destino = (self.objetivo_x, self.rect.centery)
        
        ruta = cerebro_ia.a_estrella(self.rect.center, destino)
        vel = abs(self.velocidad)
        
        if ruta and len(ruta) > 1:
            proximo_punto = ruta[1]
            
            dx = proximo_punto[0] - self.rect.centerx
            dy = proximo_punto[1] - self.rect.centery
            distancia = math.sqrt(dx**2 + dy**2)
            
            if distancia > vel:
                self.rect.centerx += int((dx / distancia) * vel)
                self.rect.centery += int((dy / distancia) * vel)
            else:
                self.rect.centerx = proximo_punto[0]
                self.rect.centery = proximo_punto[1]
                
        else:
            if self.objetivo_x > constantes.ANCHO_VENTANA:
                self.rect.x += vel
            elif self.objetivo_x < 0:
                self.rect.x -= vel            
                
            if self.rect.x > constantes.ANCHO_VENTANA + 50 or self.rect.x < -50:
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