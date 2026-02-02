import pygame
import math
import constantes  

class Weapon():
    def __init__(self, image):
        self.image_original = image
        self.angulo = 0
        self.imagen = self.image_original
        self.forma = self.imagen.get_rect()

    def update(self, personaje):
        #Obtener coordenadas
        mouse_x, mouse_y = pygame.mouse.get_pos()
        centro_x = personaje.forma.centerx
        centro_y = personaje.forma.centery

        # Calcular distancias
        # Usamos distancia_x para calcular la elevación del mouse
        # sin importar si está a la izquierda o derecha del personaje.
        distancia_x = mouse_x - centro_x
        distancia_y = -(mouse_y - centro_y) # Invertimos Y porque en pygame Y crece hacia abajo
    
        angulo = math.degrees(math.atan2(distancia_y, abs(distancia_x)))

        #cuánto puede subir o bajar el arma, en grados
        limite = 40 
        self.angulo = max(-limite, min(limite, angulo))

        #Offset para que el arma salga del costado del cuerpo
        offset_arma = personaje.forma.width / 2.5
        
        if personaje.flip:
            #MIRANDO A LA IZQUIERDA
            
            # Movemos el arma a la izquierda del centro
            self.forma.center = (centro_x - offset_arma, centro_y)
            
            # Volteamos la imagen del arma
            imagen_flip = pygame.transform.flip(self.image_original, True, False)
            
            self.imagen = pygame.transform.rotate(imagen_flip, -self.angulo)
            
        else:
            #PERSONAJE MIRANDO A LA DERECHA
            
            self.forma.center = (centro_x + offset_arma, centro_y)
            
            imagen_normal = self.image_original
            
            self.imagen = pygame.transform.rotate(imagen_normal, self.angulo)

        self.forma = self.imagen.get_rect(center=self.forma.center)

    def dibujar(self, interfaz):
        interfaz.blit(self.imagen, self.forma)
        # pygame.draw.rect(interfaz, constantes.COLOR_ARMA, self.forma, 1)