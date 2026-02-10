import pygame
import constantes

class Grilla:
    def __init__(self):
        #matriz en 0, camino libre
        self.matriz = [[0 for _ in range(constantes.FILAS)] for _ in range(constantes.COLUMNAS)]
        
    def marcar_obstaculos(self, grupo_paredes):
        self.matriz = [[0 for _ in range(constantes.FILAS)] for _ in range(constantes.COLUMNAS)]
        
        for pared in grupo_paredes:
            col_inicio = pared.rect.x  // constantes.TILE_SIZE
            col_fin = (pared.rect.x + pared.rect.width) // constantes.TILE_SIZE
            fila_inicio = pared.rect.y // constantes.TILE_SIZE
            fila_fin = (pared.rect.y + pared.rect.height) // constantes.TILE_SIZE
            
        for col in range(col_inicio, col_fin + 1):
            for fila in range(fila_inicio, fila_fin + 1):
                if 0 <= col < constantes.COLUMNAS and 0  <= fila < constantes.FILAS:
                    self.matriz[col][fila] = 1
               
    def obtener_nodo(self, x, y):
        return x // constantes.TILE_SIZE, y // constantes.TILE_SIZE                     