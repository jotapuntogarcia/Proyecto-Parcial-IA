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
        self.cooldown_ataque = 2000  #segundos entre botellazos
        self.ya_lanzada = False
        
        self.ruta = []
        self.ultimo_recalculo = 0 
        self.espera_recalculo = 500 #cada medio segundo

    def move(self, jugador, cerebro_ia, grupo_paredes):
        
        tiempo_actual = pygame.time.get_ticks()
        
        if self.rect.centerx < 0:
            self.rect.x += self.velocidad
            return
        if self.rect.centerx > constantes.ANCHO_VENTANA:
            self.rect.x -= self.velocidad
            return
        if self.rect.centery < 0:
            self.rect.y += self.velocidad
            return
        
        # Calcular distancia
        dx_final = jugador.forma.centerx - self.rect.centerx
        dy_final = jugador.forma.centery - self.rect.centery
        distancia_al_jugador = math.sqrt(dx_final**2 + dy_final**2)
        
        #enemigo ve al jugador
        tengo_vision = True
        
        for pared in grupo_paredes:
            if pared.rect.clipline(self.rect.center, jugador.forma.center):
                tengo_vision = False
                break
            
         #ataca si esta cerca y puede ver   
        if distancia_al_jugador <= self.distancia_ataque and tengo_vision:
            if tiempo_actual - self.ultimo_ataque > self.cooldown_ataque:
                self.estado = "atacar"
                self.ruta = [] #si ataca no camina
            return        
        
        #pathfinding
        if tiempo_actual - self.ultimo_recalculo > self.espera_recalculo:
            self.ruta = cerebro_ia.a_estrella(self.rect.center, jugador.forma.center) #pide al a* el camino de guachi a jugador
            self.ultimo_recalculo = tiempo_actual
            
        if self.ruta and len(self.ruta) > 1:
            #estamos en 0 vamos al 1
            objetivo_x, objetivo_y = self.ruta[1]
            
            dx = objetivo_x - self.rect.centerx
            dy = objetivo_y - self.rect.centery
            
            distancia_nodo = math.sqrt(dx**2 + dy**2)
            
            if distancia_nodo > 2:
                self.estado = "caminar"
                
                # Mover en X y verificar colisión
                self.rect.x += (dx / distancia_nodo) * self.velocidad
                for pared in grupo_paredes:
                    if self.rect.colliderect(pared.rect):
                        self.rect.x -= (dx / distancia_nodo) * self.velocidad
                
                # Mover en Y y verificar colisión
                self.rect.y += (dy / distancia_nodo) * self.velocidad
                for pared in grupo_paredes:
                    if self.rect.colliderect(pared.rect):
                        self.rect.y -= (dy / distancia_nodo) * self.velocidad
            else:
                self.ruta.pop(0)
            
        #mirar hacia el jugador        
        self.flip = True if dx_final < 0 else False            
                

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