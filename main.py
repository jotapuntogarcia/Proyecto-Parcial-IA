import pygame
import constantes
import random
from personaje import Personaje
from weapons import Weapon
from enemigo import Enemigo
from delivery import Delivery
from proyectiles import Botella
from obstaculo import Pared
from pathfinding import Grilla

pygame.init() 

pygame.mixer.pre_init(44100, -16, 1, 515)
pygame.mixer.init()
sonido_disparo = pygame.mixer.Sound("assets/audio/disparo.wav")

ventana= pygame.display.set_mode((constantes.ANCHO_VENTANA, 
                                  constantes.ALTO_VENTANA), pygame.SCALED | pygame.FULLSCREEN)


pygame.display.set_caption("El Muchacho Dembow")


def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (int(w*scale), int(h*scale)))
    return nueva_imagen

def generar_posicion_calle():
    entrada = random.randint(0, 2)
    
    y_calle = random.randint(180, constantes.ALTO_VENTANA - 80)
    
    if entrada == 0: #calle izquierda
        x = -50
        y = y_calle
    elif entrada == 1: #calle derecha
        x = constantes.ANCHO_VENTANA + 50
        y = y_calle
    else: #viene de arriba
        ancho_hueco = constantes.ANCHO_VENTANA - 600
        x = 300 + (ancho_hueco // 2) 
        y = -50 # Aparece arriba para bajar por el callejón
        
    return x, y    
        

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
for i in range(6):
    img = pygame.image.load(f"assets/images/characters/enemies/guachiman/run/run_{i}.png").convert_alpha()
    img = escalar_img(img, constantes.SCALA_ENEMIGO)
    animaciones_enemigo.append(img)
    
animaciones_ataque_guachi = []
for i in range (5):
    img = pygame.image.load(f"assets/images/characters/enemies/guachiman/attack/ataque_{i}.png").convert_alpha()
    img = escalar_img(img, constantes.SCALA_ENEMIGO)
    animaciones_ataque_guachi.append(img)

# Cargar botella ANTES de crear enemigos
img_botella = pygame.image.load("assets/images/weapons/botella.png").convert_alpha()
img_botella = escalar_img(img_botella, 0.8)    
    
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
grupo_botellas_enemigas = pygame.sprite.Group()
grupo_paredes = pygame.sprite.Group()

cerebro_ia = Grilla()

#muro

col_x = 9 * constantes.TILE_SIZE
fila_y = 7 * constantes.TILE_SIZE

muro_acera_izq = Pared(0, 130, 300, 40) 
muro_acera_der = Pared(constantes.ANCHO_VENTANA - 300, 130, 300, 40)

# Acera Inferior (El otro lado de la calle)
muro_abajo = Pared(0, constantes.ALTO_VENTANA - 40, constantes.ANCHO_VENTANA, 40)

# Agregamos todos al grupo
grupo_paredes.add(muro_acera_izq, muro_acera_der, muro_abajo)
cerebro_ia.marcar_obstaculos(grupo_paredes)


#crear jugador de la clase personaje 
jugador = Personaje(50, 50, animaciones)
jugador.rect = jugador.forma # CORRECCION: Referencia necesaria para spritecollideany



#variables movimientos jugador

mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

#controlar framerate
    
reloj = pygame.time.Clock()


#para que los enemigos aparezcan despues de iniciar
    
lista_enemigos = []
for i in range (3):
    x, y = generar_posicion_calle()
    nuevo_guachi = Enemigo (x, y, animaciones_enemigo, animaciones_ataque_guachi, img_botella)
    lista_enemigos.append(nuevo_guachi)

#esperar un tiempo antes de que empiecen a aparecer

tiempo_inicio_juego = pygame.time.get_ticks()
delay_inicial = 2000

def dibujar_grid(ventana):
    #lineas verticales
    for c in range(constantes.COLUMNAS + 1):
        pygame.draw.line(ventana, (255, 255, 255), (c * constantes.TILE_SIZE, 0), 
                         (c * constantes.TILE_SIZE, constantes.ALTO_VENTANA))
        #horizontales
    for f in range(constantes.FILAS + 1):
        pygame.draw.line(ventana, (255, 255, 255), (0, f * constantes.TILE_SIZE), 
                         (constantes.ANCHO_VENTANA, f * constantes.TILE_SIZE))    
        

#vida del personaje
def dibujar_vida(interfaz, x, y, vida):
    ratio = vida / 100
    pygame.draw.rect(interfaz, (50, 50, 50), (x - 2, y - 2, 204 , 24))
    pygame.draw.rect(interfaz, (255, 0, 0), (x, y, 200 * ratio, 20))

#oleadas

numero_oleada = 1
enemigos_por_oleada = 3

#fondo

img_fondo = pygame.image.load("assets/images/background/fondo.png").convert()
fondo_redimensionado = pygame.transform.scale(img_fondo, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))


run = True

while run == True:
    
    #MOVER A 60FPS
    reloj.tick(constantes.FPS)
    ventana.blit(fondo_redimensionado, (0, 0))
    
    cerebro_ia.marcar_obstaculos(grupo_paredes)
    
    #actualizar posicion del rect para colisiones
    jugador.rect.midbottom = jugador.forma.midbottom
    
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
    
    #colosionn jugador pared
    hit_pared = pygame.sprite.spritecollideany(jugador, grupo_paredes)
    if hit_pared:
        jugador.forma.x -= delta_x
        jugador.forma.y -= delta_y
        # Re-sincronizar imagen si chocamos
        jugador.rect.midbottom = jugador.forma.midbottom
    
    #actualizar estado de arma
    bala = pistola.update(jugador)
    if bala:
        grupo_balas.add(bala)
        
    grupo_balas.update() #esto mueve las balas
        
    tiempo_actual = pygame.time.get_ticks()    
        
    if tiempo_actual - ultimo_delivery > 5000: #5 segundos cada uno
        nuevo_delivery = Delivery(animaciones_delivery)
        lista_enemigos.append(nuevo_delivery)
        ultimo_delivery = tiempo_actual
        
    #oledas
    guachis_vivos = [e for e in lista_enemigos if isinstance(e, Enemigo)]
    
    if len(guachis_vivos) == 0: 
        numero_oleada += 1
        enemigos_por_oleada += 1 
        
        print(f"OLEADA {numero_oleada} INICIADA")
        
        for _ in range(enemigos_por_oleada):
            x , y = generar_posicion_calle()
            nuevo_guachi = Enemigo(x, y, animaciones_enemigo, animaciones_ataque_guachi, img_botella)
            lista_enemigos.append(nuevo_guachi)        

    #bluce de enemigos
    for enemigo in lista_enemigos[:]:
        
        if enemigo.rect.x < -100 or enemigo.rect.x > constantes.ANCHO_VENTANA + 100 or \
           enemigo.rect.y < -100 or enemigo.rect.y > constantes.ALTO_VENTANA + 100:
            if pygame.time.get_ticks() - tiempo_inicio_juego > 5000:
                lista_enemigos.remove(enemigo)
                continue
            
            
        # MOVER
        enemigo.move(jugador, cerebro_ia, grupo_paredes)    
            
        # UPDATE
        nueva_botella = None
        if isinstance(enemigo, Delivery):
             enemigo.update() 
        else:
             nueva_botella = enemigo.update(jugador)
        
        if nueva_botella:
            grupo_botellas_enemigas.add(nueva_botella)
            
        #colisiones Jugador vs Enemigo
        if jugador.forma.colliderect(enemigo.rect):
            if isinstance(enemigo, Delivery):
                jugador.vida -= 20
                if enemigo in lista_enemigos: lista_enemigos.remove(enemigo)
            else:
                jugador.vida -= 0.5

        #colisiones Enemigo vs Balas
        colision = pygame.sprite.spritecollide(enemigo, grupo_balas, True)
        if colision:
            enemigo.vida -= 50
            if enemigo.vida <= 0:
                if enemigo in lista_enemigos:
                    lista_enemigos.remove(enemigo)
                        
        if isinstance(enemigo, Delivery) and enemigo.completado:
            if enemigo in lista_enemigos:
                lista_enemigos.remove(enemigo)                

    #logica de vida jugador
    if jugador.vida <= 0:
        jugador.vida = 0
        jugador.vivo = False                
    
    grupo_botellas_enemigas.update()
    
    hit = pygame.sprite.spritecollideany(jugador, grupo_botellas_enemigas)
    if hit:
        jugador.vida -= 15
        hit.kill()
    
    
    # dibujar balas (Usamos .draw del grupo para evitar errores)
    grupo_balas.draw(ventana)
    
    #dibujar botellazos
    grupo_botellas_enemigas.draw(ventana)
    
    entidades = lista_enemigos + [jugador]
    entidades.sort(key=lambda obj: obj.rect.bottom)
    
    for entidad in entidades:
        entidad.dibujar(ventana)
        
    # dibujar el arma (siempre encima del jugador)
    pistola.dibujar(ventana)
    
    # dibujar interfaz
    dibujar_vida(ventana, 20, 20, jugador.vida)
    # dibujar_grid(ventana) 
    # grupo_paredes.draw(ventana)
    
    pygame.display.update() 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False  
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()    
            if event.key == pygame.K_a: mover_izquierda = True    
            if event.key == pygame.K_d: mover_derecha = True  
            if event.key == pygame.K_w: mover_arriba = True
            if event.key == pygame.K_s: mover_abajo = True    

                        
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_a: mover_izquierda = False  
            if event.key == pygame.K_d: mover_derecha = False 
            if event.key == pygame.K_w: mover_arriba = False
            if event.key == pygame.K_s: mover_abajo = False    
                                   
pygame.quit()