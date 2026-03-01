#JUnior Garcia 19-SISN-2-011
import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self, jugador):
        if self.rect.colliderect(jugador.forma):
            jugador.vida += 20 #+20 de vida
            
            #100 maximo
            if jugador.vida > 100:
                jugador.vida = 100
            
            #desaparecer el item
            self.kill()
            
            