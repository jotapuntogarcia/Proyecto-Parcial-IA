import pygame
import constantes
import random
from personaje import Personaje
from weapons import Weapon
from enemigo import Enemigo
from delivery import Delivery

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
    
#delivery

animaciones_delivery = []
for i in range (5):
    img = pygame.image.load(f"assets/images/characters/enemies/delivery/dev_{i}.png").convert_alpha()
    img = escalar_img(img, constantes.SCALA_DELIVERY)
    animaciones_delivery.append(img)
    
ultimo_delivery = pygame.time.get_ticks()    
    
    

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
guachiman2 = Enemigo(600, 200, animaciones_enemigo)
lista_enemigos = [guachiman, guachiman2]

#para que los enemigos aparezcan despues de iniciar

def generar_posicion_enemigo():
    if random.randint(0, 1) == 0:
        x = random.choice ([-50, constantes.ANCHO_VENTANA + 50])
        y = random.randint(0, constantes.ALTO_VENTANA)
    else:
        x = random.randint(0, constantes.ANCHO_VENTANA)
        y = random.choice ([-50, constantes.ALTO_VENTANA])
    return x, y
    
lista_enemigos = []
for i in range (3):
    x, y = generar_posicion_enemigo()
    nuevo_guachi = Enemigo (x, y, animaciones_enemigo)
    lista_enemigos.append(nuevo_guachi)

#esperar un tiempo antes de que empiecen a aparecer

tiempo_inicio_juego = pygame.time.get_ticks()
delay_inicial = 2000


#esperar para que salga delivery
tiempo_actual = pygame.time.get_ticks()
if tiempo_actual - tiempo_inicio_juego > delay_inicial:
    if tiempo_actual - ultimo_delivery > 3000:
        nuevo_delivery = Delivery(animaciones_delivery)
        lista_enemigos.append(nuevo_delivery)
        ultimo_delivery = tiempo_actual

#vida del personaje
def dibujar_vida(interfaz, x, y, vida):
    ratio = vida / 100
    pygame.draw.rect(interfaz, (50, 50, 50), (x - 2, y - 2, 204 , 24))
    pygame.draw.rect(interfaz, (255, 0, 0), (x, y, 200 * ratio, 20))


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
        
        
    tiempo_actual = pygame.time.get_ticks()    
        
    if tiempo_actual - ultimo_delivery > 3000:
        nuevo_delivery = Delivery(animaciones_delivery)
        lista_enemigos.append(nuevo_delivery)
        ultimo_delivery = tiempo_actual
 
 #bluce de enemigos
    for enemigo in lista_enemigos[:]:
        enemigo.move(jugador)
        enemigo.update()
        enemigo.dibujar(ventana)
        if jugador.forma.colliderect(enemigo.rect):
            
            if isinstance(enemigo, Delivery):
                jugador.vida -= 20
                lista_enemigos.remove(enemigo)
                
            else:
                jugador.vida -= 0.5
                
    if jugador.vida <= 0:
        jugador.vida = 0
        jugador.vivo = False                
        
        colision = pygame.sprite.spritecollide(enemigo, grupo_balas, True)
        
        if colision:
            enemigo.vida -= 50
            if enemigo.vida <= 0:
                lista_enemigos.remove(enemigo)
        
 
 
    
    #dibujar al jugador
    jugador.dibujar(ventana)
    
    #dibujar el arma
    
    pistola.dibujar(ventana)
    
    
    #dibujar balas
    
    for bala in grupo_balas:
        bala.dibujar(ventana)
    
    
    
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
                                   
                    
    dibujar_vida(ventana, 20, 20, jugador.vida)        
            
    pygame.display.update()
    
    
    
pygame.QUIT()