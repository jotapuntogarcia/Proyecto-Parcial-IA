import pygame
import constantes
from personaje import Personaje
from weapons import Weapon
from enemigo import Enemigo

pygame.init() 

ventana= pygame.display.set_mode((constantes.ANCHO_VENTANA, 
                                  constantes.ALTO_VENTANA))


pygame.display.set_caption("El Muchacho Dembow")


def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen


#importa imagenes
#personaje
animaciones = []
for i in range(7):
    img = pygame.image.load(
        f"assets/images/characters/player/Player_{i}.png"
    ).convert_alpha()
    
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animaciones.append(img)
    
#arma
    
imagen_pistola = pygame.image.load(f"assets/images/weapons/gun.png")
imagen_pistola = escalar_img(imagen_pistola, constantes.SCALA_ARMA)


#balas

imagen_balas = pygame.image.load(f"assets/images/weapons/bullet.png").convert_alpha()
imagen_balas = escalar_img(imagen_balas, constantes.SCALA_ARMA)

#guachiman

animaciones_enemigo = []
for i in range(8):
    img = pygame.image.load(f"assets/images/characters/enemies/guachiman/guachi_{i}.png").convert_alpha()
    img = escalar_img(img, constantes.SCALA_ENEMIGO)
    animaciones_enemigo.append(img)

#crear arma clase weapon

pistola = Weapon(imagen_pistola, imagen_balas)

#crear grupo de sprites

grupo_balas = pygame.sprite.Group()


#crear jugador de la clase personake 
jugador = Personaje(50, 50, animaciones)



#variables movimientos jugador

mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

#controlar framerate
    
reloj = pygame.time.Clock()


guachiman = Enemigo(400, 300, animaciones_enemigo)


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
    
    
    #actualizar estado jugador
    jugador.update()
    
    guachiman.move(jugador)
    guachiman.update()
    
    #actualizar estado de arma
    
    bala = pistola.update(jugador)
    if bala:
        grupo_balas.add(bala)
        
    grupo_balas.update()
        
 
    
    #dibujar al jugador
    jugador.dibujar(ventana)
    
    #dibujar el arma
    
    pistola.dibujar(ventana)
    
    
    #dibujar balas
    
    for bala in grupo_balas:
        bala.dibujar(ventana)
    
    #dibujar guachi
    
    guachiman.dibujar(ventana)
    
    
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