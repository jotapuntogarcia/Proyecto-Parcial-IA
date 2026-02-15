import pygame
import math
import constantes  

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.velocidad = 10
        self.delta_x = math.cos(math.radians(self.angulo)) * self.velocidad
        self.delta_y = -math.sin(math.radians(self.angulo)) * self.velocidad

    def update(self):
        # Mover la bala
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        # Si sale de la pantalla, desaparece
        if self.rect.right < 0 or self.rect.left > constantes.ANCHO_VENTANA or \
           self.rect.bottom < 0 or self.rect.top > constantes.ALTO_VENTANA:
            self.kill()

    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.rect)

class Weapon():
    def __init__(self, image, imagen_bala):
        self.image_original = image
        self.imagen_bala = imagen_bala
        self.angulo = 0
        
        self.image = self.image_original
        self.rect = self.image.get_rect()
        
        self.ultimo_disparo = 0 
        self.cooldown = 500  

    def update(self, personaje):
        bala_nueva = None 
        tiempo_actual = pygame.time.get_ticks()
        
        # Ajuste de posicion del arma
        offset_y = 15 #bajar para que pistola este cerca de la mano
        distancia_mano = 20 #distancia arma del centro a mano
        
        if personaje.flip:
            offset_x = -distancia_mano #Izquierda
        else:
            offset_x = distancia_mano  #Derecha
        
        self.rect.centerx = personaje.rect.centerx + offset_x
        self.rect.centery = personaje.rect.centery + offset_y
        
        # Rotación mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        distancia_x = mouse_x - self.rect.centerx
        distancia_y = -(mouse_y - self.rect.centery)

        angulo_base = math.degrees(math.atan2(distancia_y, abs(distancia_x)))
        limite = 40 
        self.angulo = max(-limite, min(limite, angulo_base))
        
        if personaje.flip:
            imagen_flip = pygame.transform.flip(self.image_original, True, False)
            self.image = pygame.transform.rotate(imagen_flip, -self.angulo)
        else:
            self.image = pygame.transform.rotate(self.image_original, self.angulo)

        self.rect = self.image.get_rect(center=self.rect.center)
        
        # logica disparo
        if pygame.mouse.get_pressed()[0]:
            if tiempo_actual - self.ultimo_disparo >= self.cooldown:
                angulo_bala = self.angulo
                if personaje.flip:
                    angulo_bala = 180 - self.angulo 
                
                # bala sale del centro del arma
                bala_nueva = Bullet(self.imagen_bala, self.rect.centerx, self.rect.centery, angulo_bala)
                self.ultimo_disparo = tiempo_actual 

        return bala_nueva

    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.rect)