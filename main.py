import pygame
import constantes
import random
import os
from personaje import Personaje
from weapons import Weapon
from enemigo import Enemigo
from delivery import Delivery
from proyectiles import Botella
from obstaculo import Pared
from pathfinding import Grilla
from items import Item

pygame.init() 

pygame.mixer.pre_init(44100, -16, 1, 515)
pygame.mixer.init()
sonido_disparo = pygame.mixer.Sound("assets/audio/disparo.wav")
sonido_disparo.set_volume(1.0)

pygame.mixer_music.set_volume(0.4)

volumen_musica_fondo = 0.15
pygame.mixer.music.set_volume(volumen_musica_fondo)

track_menu = "assets/audio/menu.mp3"
track_gameplay = "assets/audio/gameplay.mp3"

def reproducir_musica(pista):
    if not os.path.exists(pista):
        return
    try:
        print(f"No se encontró el archivo: {pista}")
        pygame.mixer.music.load(pista)
        pygame.mixer.music.play(-1) #loop infinito
        pygame.mixer.music.set_volume(volumen_musica_fondo)
    except Exception as e:
        print(f"Error al reproducir {pista}: {e}")

ventana= pygame.display.set_mode((constantes.ANCHO_VENTANA, 
                                  constantes.ALTO_VENTANA), pygame.SCALED | pygame.FULLSCREEN)
#menu

img_fondo_menu = pygame.image.load("assets/images/background/fondo_menu.png").convert()
img_fondo_menu = pygame.transform.scale(img_fondo_menu, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

font_titulo = pygame.font.SysFont("Comic Sans", 80)
font_boton = pygame.font.SysFont("Arial", 40, bold=True)

estado_juego = "MENU" 

pygame.display.set_caption("El Muchacho Dembow")


def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (int(w*scale), int(h*scale)))
    return nueva_imagen

def generar_posicion_calle():
    entrada = random.randint(0, 2)    
    y_calle = random.randint(220, constantes.ALTO_VENTANA - 100)
    
    if entrada == 0: #calle izquierda
        x = -50
        y = y_calle
    elif entrada == 1: #calle derecha
        x = constantes.ANCHO_VENTANA + 50
        y = y_calle
    else: #viene de arriba
        min_x = 350
        max_x = constantes.ANCHO_VENTANA - 350
        x = random.randint(min_x, max_x)
        y = -50 # Aparece arriba para bajar por el callejón
        
    return x, y    

def reiniciar_juego():
    #variables globales
    global puntuacion, numero_oleada, lista_enemigos, grupo_balas, grupo_items, jugador
    global mover_arriba, mover_abajo, mover_izquierda, mover_derecha
    
    #reiniciar jugador
    jugador.vida = 100
    jugador.vivo = True
    jugador.forma.center = (constantes.ANCHO_VENTANA // 2, constantes.ALTO_VENTANA // 2)
    
    #FORZAR DETENCIÓN PARA QUE EL CUANDO PERDAMOS NO SE QUEDE EL JUGADOR LOCO
    mover_arriba = False
    mover_abajo = False
    mover_izquierda = False
    mover_derecha = False
    
    #Reiniciar stats
    puntuacion = 0
    numero_oleada = 1
    
    lista_enemigos.clear()
    grupo_balas.empty()
    grupo_botellas_enemigas.empty()
    grupo_items.empty()
    
    #crear enemigos iniciales
    for i in range (3):
        x, y = generar_posicion_calle()
        nuevo_guachi = Enemigo (x, y, animaciones_enemigo, animaciones_ataque_guachi, img_botella)
        lista_enemigos.append(nuevo_guachi)

def dibujar_menu(ventana):
    ventana.blit(img_fondo_menu, (0, 0))
    
    #oscurecer el fondo para hacer texto visible
    overlay = pygame.Surface((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    overlay.set_alpha(100) #transparente    
    overlay.fill((0, 0, 0))
    ventana.blit(overlay, (0, 0))
    
    #titulo
    titulo_sombra = font_titulo.render("El Muchacho Dembow", True, (0, 0, 0))
    titulo = font_titulo.render("El Muchacho Dembow", True, (255, 215, 0)) #color dorado
    
    rect_titulo = titulo.get_rect(center=(constantes.ANCHO_VENTANA//2, 150))
    ventana.blit(titulo_sombra, (rect_titulo.x + 5, rect_titulo.y + 5))
    ventana.blit(titulo, rect_titulo)
    
    #mensaje inicio
    
    msg = font_boton.render("[ESPACIO] o [X] para salir a la calle", True, (255, 255, 255))
    rect_msg = msg.get_rect(center=(constantes.ANCHO_VENTANA//2,450))
    
    #efecto parpardeo prueba
    if pygame.time.get_ticks() % 1000 > 500:
        ventana.blit(msg, rect_msg)

def dibujar_game_over(ventana, puntuacion):
    ventana.fill((20, 0, 0)) # Fondo rojo oscuro
    
    txt_muerte = font_titulo.render("Te dieron pa'bajo", True, (255, 0, 0))
    rect_muerte = txt_muerte.get_rect(center=(constantes.ANCHO_VENTANA//2, 200))
    ventana.blit(txt_muerte, rect_muerte)
    
    txt_score = font_boton.render(f"Te llevaste a: {puntuacion}", True, (255, 255, 255))
    rect_score = txt_score.get_rect(center=(constantes.ANCHO_VENTANA//2, 300))
    ventana.blit(txt_score, rect_score)
    
    txt_restart = font_boton.render("Presiona [R] o [X] para volver a intentar", True, (255, 255, 0))
    rect_restart = txt_restart.get_rect(center=(constantes.ANCHO_VENTANA//2, 450))
    ventana.blit(txt_restart, rect_restart)


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

#salami

img_salami = pygame.image.load("assets/images/icons/salami.png").convert_alpha()
img_salami = escalar_img(img_salami, 0.6)

grupo_items = pygame.sprite.Group()

#contador de bajas

fuente_score = pygame.font.SysFont("Comic Sans", 30, bold=True)  #COMIC SANS!
puntuacion= 0

def dibujar_interfaz(ventana, jugador, puntuacion, oleada):
    
    #vida
    dibujar_vida(ventana, 20, 20, jugador.vida)
    
    #kills
    texto_kills = fuente_score.render(f"Guachi Down: {puntuacion}", True, (255, 255, 0))
    ventana.blit(texto_kills, (20, 50))
    
    #oleada
    texto_oleada = fuente_score.render(f"Oleada: {oleada}", True, (0, 255, 255))    
    ventana.blit(texto_oleada, (constantes.ANCHO_VENTANA - 180, 20))
    
reproducir_musica(track_menu)

pygame.joystick.init()
mando = None

if pygame.joystick.get_count() > 0:
    mando = pygame.joystick.Joystick(0)
    mando.init()
    print(f"Mando conectado: {mando.get_name()}")
else:
    print("No hay mando, use el teclado")    

run = True
while run:
    #MOVER A 60FPS
    reloj.tick(constantes.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if estado_juego == "JUGANDO":
                    estado_juego = "MENU"
                    reproducir_musica(track_menu)
                else:
                    run = False
            
            if estado_juego == "MENU":
                if event.key == pygame.K_SPACE:
                    estado_juego = "JUGANDO"
                    reiniciar_juego()
                    reproducir_musica(track_gameplay)
            
            elif estado_juego == "GAME_OVER":
                if event.key == pygame.K_r:
                    reiniciar_juego()
                    estado_juego = "JUGANDO"
                    reproducir_musica(track_gameplay)

            #controles de movimiento
        if event.type == pygame.KEYDOWN:    
            if estado_juego == "JUGANDO":
                if event.key == pygame.K_f: pygame.display.toggle_fullscreen()    
                if event.key == pygame.K_a: mover_izquierda = True    
                if event.key == pygame.K_d: mover_derecha = True  
                if event.key == pygame.K_w: mover_arriba = True
                if event.key == pygame.K_s: mover_abajo = True

        if event.type == pygame.KEYUP: 
            if estado_juego == "JUGANDO":
                if event.key == pygame.K_a: mover_izquierda = False  
                if event.key == pygame.K_d: mover_derecha = False 
                if event.key == pygame.K_w: mover_arriba = False
                if event.key == pygame.K_s: mover_abajo = False 

        if event.type == pygame.JOYBUTTONDOWN:
            if estado_juego == "MENU" or estado_juego == "GAME_OVER":
                if event.button == 0: #0 es la X
                    estado_juego = "JUGANDO"
                    reiniciar_juego()
                    reproducir_musica(track_gameplay)
            elif estado_juego == "JUGANDO":
                if event.button in [9, 10]:
                    estado_juego = "MENU"
                    reproducir_musica(track_menu)

    #mando conrol dualshock
    disparo_mando = False
    aim_y = 0
    
    if mando:
        eje_x = mando.get_axis(0)
        eje_y = mando.get_axis(1)
        
        zona_muerta = 0.1
        
        if eje_x < -zona_muerta: mover_izquierda = True
        elif eje_x > zona_muerta: mover_derecha = True
        else:
            if not (pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]):
                mover_izquierda = False
                mover_derecha = False
                
        if eje_y < -zona_muerta: mover_arriba = True
        elif eje_y > zona_muerta: mover_abajo = True
        else:
            if not (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s]):
                mover_arriba = False
                mover_abajo = False

        aim_y = mando.get_axis(4)
        
        #R2 es 5
        if mando.get_axis(5) > 0.1:
            disparo_mando = True
        #R1
        if mando.get_button(5):
            disparo_mando = True
                     

    #estados

    if estado_juego == "MENU":
        dibujar_menu(ventana)

    elif estado_juego == "GAME_OVER":
        dibujar_game_over(ventana, puntuacion)

    elif estado_juego == "JUGANDO":
        
        #dibujar fondo y paredes
        ventana.blit(fondo_redimensionado, (0, 0))
        cerebro_ia.marcar_obstaculos(grupo_paredes)
        
        jugador.rect.midbottom = jugador.forma.midbottom
        
        #calcular movimeinto jugador
        delta_x = 0
        delta_y = 0
        
        if mover_derecha == True: delta_x = constantes.VELOCIDAD        
        if mover_izquierda == True: delta_x = -constantes.VELOCIDAD
        if mover_arriba == True: delta_y = -constantes.VELOCIDAD
        if mover_abajo == True: delta_y = constantes.VELOCIDAD            
        
        #mover jugador
        jugador.movimiento(delta_x, delta_y)
        jugador.update()
        
        #colosionn jugador pared
        hit_pared = pygame.sprite.spritecollideany(jugador, grupo_paredes)
        if hit_pared:
            jugador.forma.x -= delta_x
            jugador.forma.y -= delta_y
            jugador.rect.midbottom = jugador.forma.midbottom
        
        #actualizar estado de arma
        bala = pistola.update(jugador, disparo_mando, aim_y)
        if bala:
            grupo_balas.add(bala)
            
        grupo_balas.update() #esto mueve las balas
            
        #generar enemigos
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
            
            for _ in range(enemigos_por_oleada):
                x , y = generar_posicion_calle()
                nuevo_guachi = Enemigo(x, y, animaciones_enemigo, animaciones_ataque_guachi, img_botella)
                lista_enemigos.append(nuevo_guachi)        

        #bucle enemigos
        for enemigo in lista_enemigos[:]:
            
            #si los enemigos se quedan fuera de la pantalla se borran
            if enemigo.rect.x < -100 or enemigo.rect.x > constantes.ANCHO_VENTANA + 100 or \
               enemigo.rect.y < -100 or enemigo.rect.y > constantes.ALTO_VENTANA + 100:
                if pygame.time.get_ticks() - tiempo_inicio_juego > 5000:
                    lista_enemigos.remove(enemigo)
                    continue
                
            enemigo.move(jugador, cerebro_ia, grupo_paredes)    
                
            #ataque
            nueva_botella = None
            if isinstance(enemigo, Delivery):
                 enemigo.update() 
            else:
                 nueva_botella = enemigo.update(jugador)
            
            if nueva_botella:
                grupo_botellas_enemigas.add(nueva_botella)
                
            #jugador vs enemigo
            if jugador.forma.colliderect(enemigo.rect):
                if isinstance(enemigo, Delivery):
                    jugador.vida -= 20
                    if enemigo in lista_enemigos: lista_enemigos.remove(enemigo)
                else:
                    jugador.vida -= 0.5

            #bala vs enemigo
            colision = pygame.sprite.spritecollide(enemigo, grupo_balas, True) #True borra la bala
            if colision:
                enemigo.vida -= 50
                if enemigo.vida <= 0:
                    #enemigo muerto
                    puntuacion += 1
                    
                    #probabilidad del salami
                    if random.random() < 0.4:
                        nuevo_item = Item(enemigo.rect.centerx, enemigo.rect.centery, img_salami)
                        grupo_items.add(nuevo_item)
                        
                    if enemigo in lista_enemigos:
                        lista_enemigos.remove(enemigo)
                            
            #limpiar delivery 
            if isinstance(enemigo, Delivery) and enemigo.completado:
                if enemigo in lista_enemigos:
                    lista_enemigos.remove(enemigo)                

        #vida y muerte muchacho
        if jugador.vida <= 0:
            jugador.vida = 0
            jugador.vivo = False
            estado_juego = "GAME_OVER"
            pygame.mixer.music.fadeout(500)
        
        grupo_botellas_enemigas.update()
        
        hit = pygame.sprite.spritecollideany(jugador, grupo_botellas_enemigas)
        if hit:
            jugador.vida -= 15
            hit.kill()
                
        grupo_balas.draw(ventana)
        
        grupo_botellas_enemigas.draw(ventana)
        
        grupo_items.update(jugador) 
        grupo_items.draw(ventana) 
        
        entidades = lista_enemigos + [jugador]
        entidades.sort(key=lambda obj: obj.rect.bottom)
        
        for entidad in entidades:
            entidad.dibujar(ventana)
            
        pistola.dibujar(ventana)
        
        dibujar_interfaz(ventana, jugador, puntuacion, numero_oleada)
    
    pygame.display.update()
                                   
pygame.quit()