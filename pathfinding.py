import pygame
import constantes
import math

#para calcular los costos
class Nodo:
    def __init__(self, pos, padre=None):
        self.pos = pos #columna y fila
        self.padre = padre
        self.g = 0 #costo inicio
        self.h = 0 #europiel (heuristica)
        self.f = 0 #costo total
        
    def __eq__(self, otro):
        return self.pos == otro.pos    


class Grilla:
    def __init__(self):
        #matriz en 0, camino libre
        self.matriz = [[0 for _ in range(constantes.FILAS)] for _ in range(constantes.COLUMNAS)]
        
    def marcar_obstaculos(self, grupo_paredes):
        self.matriz = [[0 for _ in range(constantes.FILAS)] for _ in range(constantes.COLUMNAS)]
        
        for pared in grupo_paredes:
            col_inicio = pared.rect.x  // constantes.TILE_SIZE
            col_fin = (pared.rect.x + pared.rect.width - 1) // constantes.TILE_SIZE
            fila_inicio = pared.rect.y // constantes.TILE_SIZE
            fila_fin = (pared.rect.y + pared.rect.height - 1) // constantes.TILE_SIZE
            
        for col in range(col_inicio, col_fin + 1):
            for fila in range(fila_inicio, fila_fin + 1):
                if 0 <= col < constantes.COLUMNAS and 0  <= fila < constantes.FILAS:
                    self.matriz[col][fila] = 1
               
    def obtener_nodo(self, x, y):
        return x // constantes.TILE_SIZE, y // constantes.TILE_SIZE  
    
    def a_estrella(self, inicio_px, fin_px):
        #psamos los pixiales a coord de las grillas
        nodo_inicio = Nodo((inicio_px[0] // constantes.TILE_SIZE, inicio_px[1] // constantes.TILE_SIZE))
        
        lista_abierta = []
        lista_cerrada = []
        lista_abierta.append(nodo_inicio)
        
        while len(lista_abierta) > 0:
            nodo_actual = lista_abierta[0]
            indice_actual = 0
            for index, item in enumerate(lista_abierta):
                if item.f < nodo_actual.f:
                    nodo_actual = item
                    indice_actual = index
                                       
            lista_abierta.pop(indice_actual)
            lista_cerrada.append(nodo_actual)
            
            if nodo_actual == nodo_fin:
                camino = []
                actual = nodo_actual
                while actual is not None:
                    px_x = actual.pos[0] * constantes.TILE_SIZE + constantes.TILE_SIZE // 2
                    px_y = actual.pos[1] * constantes.TILE_SIZE + constantes.TILE_SIZE // 2
                    camino.append((px_x, px_y))
                    actual = actual.padre
                    
                return camino [::-1]
            
            hijos = []
            for nueva_posicion in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                pos_vecino = (nodo_actual.pos[0] + nueva_posicion[0], nodo_actual.pos[1] + nueva_posicion[1])
                
                #limites mapa
                
                if pos_vecino[0] >= constantes.COLUMNAS or pos_vecino[0] < 0 or \
                   pos_vecino[1] >= constantes.FILAS or pos_vecino[1] < 0:
                       continue
                   
                   #verificar si es una pared
                if self.matriz[pos_vecino[0]][pos_vecino[1]] !=0:
                    continue
                
                nuevo_nodo = Nodo(pos_vecino, nodo_actual)
                hijos.append(nuevo_nodo)
                
            for hijo in hijos:
                if hijo in lista_cerrada:
                    continue
                
                lista_abierta.append(hijo)
                
        return []               
                   
                                                   