import pygame
import math
import constantes
from proyectiles import Botella

class Enemigo():
    def __init__(self, x, y, animaciones_caminar, animaciones_ataque, img_botella):
        self.flip = False
        self.animaciones_caminar = animaciones_caminar
        self.animaciones_ataque = animaciones_ataque
        self.img_botella = img_botella
        
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones_caminar[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.vida = 100
        self.velocidad = 1.5
        
    
        self.estado = "caminar"
        self.distancia_ataque = 250 #si esta a menos de 250px ataca
        
        # COOLDOWN 
        self.ultimo_ataque = 0
        self.cooldown_ataque = 1000  #2 segundos entre botellazos
        self.ya_lanzada = False

    def move(self, jugador):
        # Calcular distancia
        dx = jugador.forma.centerx - self.rect.centerx
        dy = jugador.forma.centery - self.rect.centery
        distancia = math.sqrt(dx**2 + dy**2)
        
        # Mirar al jugador
        if dx < 0: self.flip = True
        else: self.flip = False
        
        # Si está lejos, CAMINA
        if distancia > self.distancia_ataque:
            self.estado = "caminar"
           
            if distancia != 0:
                self.rect.x += (dx / distancia) * self.velocidad
                self.rect.y += (dy / distancia) * self.velocidad
        
        elif pygame.time.get_ticks() - self.ultimo_ataque > self.cooldown_ataque:
            self.estado = "atacar"

    def update(self, jugador):
        botella_creada = None 
        cooldown_animacion = 100
        
        if self.estado == "caminar":
            lista_actual = self.animaciones_caminar
            self.ya_lanzada = False
        else:
            lista_actual = self.animaciones_ataque
            cooldown_animacion = 80 

        if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            
            if self.estado == "atacar" and self.frame_index == 3 and not self.ya_lanzada:
                botella_creada = Botella(self.rect.centerx, self.rect.centery,
                                         jugador.forma.centerx, jugador.forma.centery,
                                         self.img_botella)
                self.ya_lanzada = True
        
        if self.frame_index >= len(lista_actual):
            self.frame_index = 0
            #Despues que tira la botella camina otra vez
            if self.estado == "atacar":
                self.estado = "caminar"
                self.ultimo_ataque = pygame.time.get_ticks()

        self.image = lista_actual[self.frame_index]
        return botella_creada 

    def dibujar(self, interfaz):
        img_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(img_flip, self.rect)