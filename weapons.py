import pygame
import math
import constantes  


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        # Rotamos la imagen de la bala según el ángulo de disparo
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.velocidad = 10
        self.delta_x = math.cos(math.radians(self.angulo)) * self.velocidad
        self.delta_y = -math.sin(math.radians(self.angulo)) * self.velocidad

    def update(self):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y


        if self.rect.right < 0 or self.rect.left > constantes.ANCHO_VENTANA or \
           self.rect.bottom < 0 or self.rect.top > constantes.ALTO_VENTANA:
            self.kill()

    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.rect)


class Weapon():
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.image_original = image
        self.angulo = 0
        self.imagen = self.image_original
        self.forma = self.imagen.get_rect()
        
        self.ultimo_disparo = 0 
        self.cooldown = 500  

    def update(self, personaje):
        bala_nueva = None 
        tiempo_actual = pygame.time.get_ticks()

        # Posicionamiento y Mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        centro_x = personaje.forma.centerx
        centro_y = personaje.forma.centery

        distancia_x = mouse_x - centro_x
        distancia_y = -(mouse_y - centro_y) 
        
        # Calcular ángulo de elevación
        angulo_base = math.degrees(math.atan2(distancia_y, abs(distancia_x)))
        limite = 40 
        self.angulo = max(-limite, min(limite, angulo_base))
        
        if pygame.mouse.get_pressed()[0]:
            if tiempo_actual - self.ultimo_disparo >= self.cooldown:
                angulo_bala = self.angulo
                if personaje.flip:
                    angulo_bala = 180 - self.angulo 
                
                bala_nueva = Bullet(self.imagen_bala, self.forma.centerx, self.forma.centery, angulo_bala)
                self.ultimo_disparo = tiempo_actual 


        offset_arma = personaje.forma.width / 2.5
        if personaje.flip:
            self.forma.center = (centro_x - offset_arma, centro_y)
            imagen_flip = pygame.transform.flip(self.image_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, -self.angulo)
        else:
            self.forma.center = (centro_x + offset_arma, centro_y)
            self.imagen = pygame.transform.rotate(self.image_original, self.angulo)

        self.forma = self.imagen.get_rect(center=self.forma.center)
        
        return bala_nueva

    def dibujar(self, interfaz):
        interfaz.blit(self.imagen, self.forma)