import pygame
import constantes
from personaje import Personaje

pygame.init() 

ventana= pygame.display.set_mode((constantes.ANCHO_VENTANA, 
                                  constantes.ALTO_VENTANA))


pygame.display.set_caption("El Muchacho Dembow")


def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen

animaciones = []
for i in range(7):
    img = pygame.image.load(
        f"assets/images/characters/player/Player_{i}.png"
    ).convert_alpha()
    
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animaciones.append(img)


 
jugador = Personaje(50, 50, animaciones)



#variables movimientos jugador

mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

#controlar framerate
    
reloj = pygame.time.Clock()


run=True

while run == True:
    
    
    
    #MOVER A 60FPS
    
    reloj.tick(constantes.FPS)
    
    
    ventana.fill(constantes.COLOR_BG)
    
    #calcular movimeinto jugador
    
    delta_x = 0
    delta_y = 0
    
    if mover_derecha == True:
        delta_x = constantes.VELOCIDAD        
    if mover_izquierda == True:
        delta_x = -constantes.VELOCIDAD
    if mover_arriba == True:
        delta_y = -constantes.VELOCIDAD
    if mover_abajo == True:
        delta_y = constantes.VELOCIDAD            
    
    
    #mover jugador
    
    jugador.movimiento(delta_x, delta_y)
    
    jugador.update()
    
    
    
    jugador.dibujar(ventana)
    
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
                
            run=False  
    
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                mover_derecha = True  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                mover_arriba = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                mover_abajo = True    
                        
        
        #soltando la tecla
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_a:
                mover_izquierda = False  
            if event.key == pygame.K_d:
                mover_derecha = False 
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False    
                                   
                    
            
            
    pygame.display.update()
    
    
    
pygame.QUIT()