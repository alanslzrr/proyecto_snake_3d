"""
Proyecto Snake 3D - snake.py

En este módulo agrupamos la serpiente como entidad lógica del juego dentro del
“Cubo Planetario”.

En la fase actual:

- Representamos la serpiente como una lista ordenada de segmentos cúbicos.
- La inicializamos de forma estática sobre la cara frontal del mundo (Z
  máxima), utilizando coordenadas discretas (x, y, z) coherentes con el
  `Tablero`.
- Diferenciamos visualmente la cabeza del cuerpo mediante una paleta de
  colores definida en `configuracion.py`.

En fases posteriores extenderemos esta clase para incorporar movimiento
“crawler” sobre la superficie del cubo, transición entre caras, detección de
colisiones y crecimiento dinámico al recoger comida.
"""

from configuracion import (
    GRID_SIZE, COLOR_SERPIENTE_CABEZA, COLOR_SERPIENTE_CUERPO
)
from segmento import Segmento
from tablero import Tablero

class Snake:
    def __init__(self, tablero: Tablero):
        self.tablero = tablero
        self.segmentos = []
        self._crear_inicial()

    def _crear_inicial(self):
        """
        Crea la configuración inicial de la serpiente sobre la cara frontal del
        cubo (Z positivo).

        Colocamos la cabeza en el centro de la cara y situamos dos segmentos
        adicionales del cuerpo inmediatamente por debajo en el eje Y, de manera
        que la cadena sea claramente visible sobre la superficie del mundo
        cúbico.
        """
        z_face = GRID_SIZE - 1 
        mid = GRID_SIZE // 2
        
        # Cabeza
        self.segmentos.append(Segmento(mid, mid, z_face, COLOR_SERPIENTE_CABEZA))
        
        # Cuerpo (2 segmentos hacia abajo)
        self.segmentos.append(Segmento(mid, mid - 1, z_face, COLOR_SERPIENTE_CUERPO))
        self.segmentos.append(Segmento(mid, mid - 2, z_face, COLOR_SERPIENTE_CUERPO))

    def dibujar(self):
        for seg in self.segmentos:
            seg.dibujar(self.tablero)