"""
Proyecto Snake 3D - comida.py

Este módulo gestiona la comida dentro del mundo cúbico.
Implementamos la clase Comida que se encarga de:
1. Representar la comida en el espacio 3D (x, y, z).
2. Generar nuevas posiciones aleatorias asegurando que aparezcan en la superficie.
3. Rotar sus coordenadas solidariamente con el mundo para mantener la coherencia
   con la serpiente durante las transiciones de cara.
"""

import random
from OpenGL.GL import *
from configuracion import GRID_SIZE, COLOR_COMIDA
from segmento import Segmento

class Comida:
    def __init__(self, snake_ref):
        """
        Inicializa la comida.
        :param snake_ref: Referencia a la serpiente para evitar generar comida sobre su cuerpo.
        """
        self.snake = snake_ref
        self.posicion = None
        self.generar_nueva_posicion()

    def generar_nueva_posicion(self):
        """
        Genera una posición aleatoria (x, y, z) que esté en la SUPERFICIE del cubo
        y que no colisione con la serpiente.
        """
        while True:
            # 1. Elegir una cara aleatoria (0=Front/Back, 1=Left/Right, 2=Top/Bottom)
            #    y fijar esa coordenada a 0 o GRID_SIZE-1.
            eje_fijo = random.randint(0, 2)
            lado = random.choice([0, GRID_SIZE - 1])

            coords = [0, 0, 0]
            coords[eje_fijo] = lado
            
            # 2. Las otras dos coordenadas son aleatorias dentro del rango.
            for i in range(3):
                if i != eje_fijo:
                    coords[i] = random.randint(0, GRID_SIZE - 1)
            
            x, y, z = coords

            # 3. Validar que no colisione con la serpiente
            colision = False
            for seg in self.snake.segmentos:
                if seg.x == x and seg.y == y and seg.z == z:
                    colision = True
                    break
            
            if not colision:
                # Usamos la clase Segmento para facilitar el dibujado, aunque sea comida
                self.posicion = Segmento(x, y, z, COLOR_COMIDA)
                break

    def rotar_coordenadas(self, eje, angulo_mundo):
        """
        Aplica la misma transformación de coordenadas que sufre la serpiente
        cuando el mundo rota, para que la comida se quede "quieta" visualmente
        respecto al tablero, aunque sus coordenadas lógicas cambien.
        """
        if not self.posicion:
            return

        N = GRID_SIZE - 1
        angulo_transformacion = -angulo_mundo # Inverso a la rotación visual

        x, y, z = self.posicion.x, self.posicion.y, self.posicion.z

        if eje == "y":
            if angulo_transformacion == 90.0:
                # Rotación +90º alrededor de Y (CCW)
                self.posicion.x = N - z
                self.posicion.z = x
            elif angulo_transformacion == -90.0:
                # Rotación -90º alrededor de Y (CW)
                self.posicion.x = z
                self.posicion.z = N - x

        elif eje == "x":
            if angulo_transformacion == 90.0:
                # Rotación +90º alrededor de X
                self.posicion.y = z
                self.posicion.z = N - y
            elif angulo_transformacion == -90.0:
                # Rotación -90º alrededor de X
                self.posicion.y = N - z
                self.posicion.z = y

    def dibujar(self, tablero):
        if self.posicion:
            # Reutilizamos el método de dibujo de Segmento
            self.posicion.dibujar(tablero)
