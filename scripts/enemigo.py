#JUnior Garcia 19-SISN-2-011
import pygame
import math
from scripts import constantes
#from proyectiles import Botella
from scripts.proyectiles import Botella


class Nodo:
    def evaluar(self, contexto):
        raise NotImplementedError()

class Selector(Nodo):
    def __init__(self, hijos):
        self.hijos = hijos
    def evaluar(self, contexto):
        for hijo in self.hijos:
            estado = hijo.evaluar(contexto)
            if estado == "EXITO" or estado == "CORRIENDO":
                return estado
        return "FALLO"

class Secuencia(Nodo):
    def __init__(self, hijos):
        self.hijos = hijos
    def evaluar(self, contexto):
        for hijo in self.hijos:
            estado = hijo.evaluar(contexto)
            if estado == "FALLO": return "FALLO"
            if estado == "CORRIENDO": return "CORRIENDO"
        return "EXITO"

class CondicionPuedeAtacar(Nodo):
    def __init__(self, enemigo):
        self.enemigo = enemigo
    def evaluar(self, contexto):
        jugador = contexto["jugador"]
        grupo_paredes = contexto["grupo_paredes"]
        tiempo_actual = pygame.time.get_ticks()
        
        dx = jugador.forma.centerx - self.enemigo.rect.centerx
        dy = jugador.forma.centery - self.enemigo.rect.centery
        distancia_al_jugador = math.sqrt(dx**2 + dy**2)
        
        # enemigo ve al jugador
        tengo_vision = True
        for pared in grupo_paredes:
            if pared.rect.clipline(self.enemigo.rect.center, jugador.forma.center):
                tengo_vision = False
                break
            
        # ataca si esta cerca y puede ver   
        if distancia_al_jugador <= self.enemigo.distancia_ataque and tengo_vision:
            if tiempo_actual - self.enemigo.ultimo_ataque > self.enemigo.cooldown_ataque:
                return "EXITO"
        return "FALLO"

class AccionAtacar(Nodo):
    def __init__(self, enemigo):
        self.enemigo = enemigo
    def evaluar(self, contexto):
        self.enemigo.estado = "atacar"
        self.enemigo.ruta = [] # si ataca no camina
        return "EXITO"

class AccionPerseguir(Nodo):
    def __init__(self, enemigo):
        self.enemigo = enemigo
    def evaluar(self, contexto):
        jugador = contexto["jugador"]
        cerebro_ia = contexto["cerebro_ia"]
        grupo_paredes = contexto["grupo_paredes"]
        tiempo_actual = pygame.time.get_ticks()
        
        #pathfinding
        if tiempo_actual - self.enemigo.ultimo_recalculo > self.enemigo.espera_recalculo:
            self.enemigo.ruta = cerebro_ia.a_estrella(self.enemigo.rect.center, jugador.forma.center) #pide al a* el camino
            self.enemigo.ultimo_recalculo = tiempo_actual
            
        if self.enemigo.ruta and len(self.enemigo.ruta) > 1:
            #estamos en 0 vamos al 1
            obj_x, obj_y = self.enemigo.ruta[1]
            dx, dy = obj_x - self.enemigo.rect.centerx, obj_y - self.enemigo.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > 2:
                self.enemigo.estado = "caminar"
                # Mover y verificar colisión
                self.enemigo.rect.x += (dx / dist) * self.enemigo.velocidad
                for p in grupo_paredes:
                    if self.enemigo.rect.colliderect(p.rect): self.enemigo.rect.x -= (dx / dist) * self.enemigo.velocidad
                
                self.enemigo.rect.y += (dy / dist) * self.enemigo.velocidad
                for p in grupo_paredes:
                    if self.enemigo.rect.colliderect(p.rect): self.enemigo.rect.y -= (dy / dist) * self.enemigo.velocidad
            else:
                self.enemigo.ruta.pop(0)
        return "CORRIENDO"

class Enemigo():
    def __init__(self, x, y, animaciones_caminar, animaciones_ataque, img_botella):
        self.flip = False
        self.animaciones_caminar = animaciones_caminar
        self.animaciones_ataque = animaciones_ataque
        self.img_botella = img_botella
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones_caminar[0]
        self.rect = self.image.get_rect(center=(x, y))
        
        self.vida = 100
        self.velocidad = 1.5
        self.estado = "caminar"
        self.distancia_ataque = 300 #si esta a menos de 300px ataca
        
        # COOLDOWN 
        self.ultimo_ataque = 0
        self.cooldown_ataque = 1500 #milisegundos entre botellazos
        self.ya_lanzada = False
        self.ruta = []
        self.ultimo_recalculo = 0 
        self.espera_recalculo = 200 #cada 200milesimas

        #Configuración del Árbol (Cerebro)
        self.arbol = Selector([
            Secuencia([CondicionPuedeAtacar(self), AccionAtacar(self)]),
            AccionPerseguir(self)
        ])

    def move(self, jugador, cerebro_ia, grupo_paredes):
        if self.rect.centerx < 0:
            self.rect.x += self.velocidad
            return
        if self.rect.centerx > constantes.ANCHO_VENTANA:
            self.rect.x -= self.velocidad
            return
        if self.rect.centery < 0:
            self.rect.y += self.velocidad
            return

        #arbol de comportamiento en pantalla
        contexto = {
            "jugador": jugador, 
            "cerebro_ia": cerebro_ia, 
            "grupo_paredes": grupo_paredes
        }
        self.arbol.evaluar(contexto)
            
        #voltear sprite
        dx_final = jugador.forma.centerx - self.rect.centerx
        self.flip = True if dx_final < 0 else False           

    def update(self, jugador):
        botella_creada = None 
        cooldown_animacion = 100 if self.estado == "caminar" else 80
        lista_actual = self.animaciones_caminar if self.estado == "caminar" else self.animaciones_ataque
        
        if self.estado == "caminar": self.ya_lanzada = False

        if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.estado == "atacar" and self.frame_index == 3 and not self.ya_lanzada:
                botella_creada = Botella(self.rect.centerx, self.rect.centery, jugador.forma.centerx, jugador.forma.centery, self.img_botella)
                self.ya_lanzada = True
        
        if self.frame_index >= len(lista_actual):
            self.frame_index = 0
            #despues que tira la botella camina otra vez
            if self.estado == "atacar":
                self.estado = "caminar"
                self.ultimo_ataque = pygame.time.get_ticks()

        self.image = lista_actual[self.frame_index]
        return botella_creada 

    def dibujar(self, interfaz):
        img_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(img_flip, self.rect)