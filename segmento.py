"""
Proyecto Snake 3D - segmento.py

En este módulo definimos la unidad básica de la serpiente: el segmento.

Cada `Segmento`:

- Representa un bloque cúbico de la serpiente en el mundo de vóxeles.
- Se describe mediante coordenadas discretas (x, y, z) dentro del cubo
  planetario.
- Es responsable de dibujarse a sí mismo en la escena, apoyándose en el
  `Tablero` para convertir posiciones lógicas de rejilla en coordenadas del
  mundo 3D.

En esta fase del proyecto los segmentos se mantienen estáticos, pero el modelo
de datos ya está preparado para soportar movimiento, crecimiento y cambios de
orientación en futuras iteraciones.
"""

from OpenGL.GL import glBegin, glEnd, glColor4f, glVertex3f, GL_QUADS
from configuracion import TAMANO_CELDA
from transformaciones import transformar
from tablero import Tablero

class Segmento:
    def __init__(self, x: int, y: int, z: int, color: tuple):
        self.x = x
        self.y = y
        self.z = z
        self.color = color

    def dibujar(self, tablero: Tablero):
        # Obtenemos la posición real en el mundo a partir de las coordenadas
        # discretas del segmento y del sistema de referencia definido por el
        # tablero cúbico.
        px, py, pz = tablero.obtener_posicion_mundo(self.x, self.y, self.z)

        transformar(
            t_x=px, t_y=py, t_z=pz,
            s_x=TAMANO_CELDA, s_y=TAMANO_CELDA, s_z=TAMANO_CELDA,
            objeto_dibujado=self._dibujar_cubo_solido
        )

    def _dibujar_cubo_solido(self):
        """
        Dibuja un cubo sólido centrado en el origen local, utilizando el color
        asociado al segmento.

        El escalado y la traslación reales se aplican externamente mediante la
        función `transformar`, de forma que esta primitiva se mantiene genérica
        y reutilizable.
        """
        hs = 0.5 # Ocupa toda la celda
        glColor4f(*self.color)
        
        glBegin(GL_QUADS)
        # Cara Frontal
        glVertex3f(-hs, -hs,  hs); glVertex3f( hs, -hs,  hs)
        glVertex3f( hs,  hs,  hs); glVertex3f(-hs,  hs,  hs)
        # Cara Trasera
        glVertex3f(-hs, -hs, -hs); glVertex3f(-hs,  hs, -hs)
        glVertex3f( hs,  hs, -hs); glVertex3f( hs, -hs, -hs)
        # Cara Izquierda
        glVertex3f(-hs, -hs, -hs); glVertex3f(-hs, -hs,  hs)
        glVertex3f(-hs,  hs,  hs); glVertex3f(-hs,  hs, -hs)
        # Cara Derecha
        glVertex3f( hs, -hs, -hs); glVertex3f( hs,  hs, -hs)
        glVertex3f( hs,  hs,  hs); glVertex3f( hs, -hs,  hs)
        # Cara Arriba
        glVertex3f(-hs,  hs, -hs); glVertex3f(-hs,  hs,  hs)
        glVertex3f( hs,  hs,  hs); glVertex3f( hs,  hs, -hs)
        # Cara Abajo
        glVertex3f(-hs, -hs, -hs); glVertex3f( hs, -hs, -hs)
        glVertex3f( hs, -hs,  hs); glVertex3f(-hs, -hs,  hs)
        glEnd()