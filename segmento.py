"""
Proyecto Snake 3D - segmento.py

En este módulo definimos un segmento individual de la serpiente.

De momento nos basta con:

- Guardar la posición lógica del segmento en coordenadas de celda (x, z).
- Poder dibujarlo como un cubo sencillo sobre el tablero.

Más adelante, cuando implementemos el movimiento real de la serpiente, iremos
afinando cómo se actualizan estas posiciones y qué información extra necesita
cada segmento.
"""

from __future__ import annotations

from OpenGL.GL import (
    glBegin,
    glEnd,
    glColor3f,
    glVertex3f,
    GL_QUADS,
)

from configuracion import TAMANO_CELDA
from transformaciones import transformar
from tablero import Tablero


class Segmento:
    """
    Representa un segmento básico de la serpiente.

    Trabajamos siempre en coordenadas de celda, para que la lógica de juego
    sea simple. El propio segmento se encarga de convertir su celda a mundo
    3D cuando llega el momento de dibujarse.
    """

    def __init__(
        self,
        celda_x: int,
        celda_z: int,
        color: tuple[float, float, float],
    ) -> None:
        self.celda_x = celda_x
        self.celda_z = celda_z
        self.color = color

    # ------------------------------------------------------------------
    # Dibujado
    # ------------------------------------------------------------------

    def dibujar(self, tablero: Tablero) -> None:
        """
        Dibujamos el segmento como un cubo apoyado sobre el tablero.

        Usamos `obtener_posicion_mundo` para situarnos en el centro de la
        celda y elevamos el cubo media unidad de celda para que quede justo
        encima de la superficie del tablero.
        """
        x, y, z = tablero.obtener_posicion_mundo(self.celda_x, self.celda_z)
        y += TAMANO_CELDA / 2.0

        def _dibujar_cubo_unitario() -> None:
            """Cubo centrado en el origen, de arista 1, usando quads."""
            glColor3f(*self.color)

            # Coordenadas de un cubo de arista 1 centrado en el origen
            # (de -0.5 a 0.5 en cada eje).
            hs = 0.5  # half size

            glBegin(GL_QUADS)

            # Cara frontal (z positiva)
            glVertex3f(-hs, -hs, hs)
            glVertex3f(hs, -hs, hs)
            glVertex3f(hs, hs, hs)
            glVertex3f(-hs, hs, hs)

            # Cara trasera (z negativa)
            glVertex3f(hs, -hs, -hs)
            glVertex3f(-hs, -hs, -hs)
            glVertex3f(-hs, hs, -hs)
            glVertex3f(hs, hs, -hs)

            # Cara izquierda (x negativa)
            glVertex3f(-hs, -hs, -hs)
            glVertex3f(-hs, -hs, hs)
            glVertex3f(-hs, hs, hs)
            glVertex3f(-hs, hs, -hs)

            # Cara derecha (x positiva)
            glVertex3f(hs, -hs, hs)
            glVertex3f(hs, -hs, -hs)
            glVertex3f(hs, hs, -hs)
            glVertex3f(hs, hs, hs)

            # Cara superior (y positiva)
            glVertex3f(-hs, hs, hs)
            glVertex3f(hs, hs, hs)
            glVertex3f(hs, hs, -hs)
            glVertex3f(-hs, hs, -hs)

            # Cara inferior (y negativa)
            glVertex3f(-hs, -hs, -hs)
            glVertex3f(hs, -hs, -hs)
            glVertex3f(hs, -hs, hs)
            glVertex3f(-hs, -hs, hs)

            glEnd()

        transformar(
            t_x=x,
            t_y=y,
            t_z=z,
            angulo=0.0,
            eje_x=0.0,
            eje_y=1.0,
            eje_z=0.0,
            sx=TAMANO_CELDA,
            sy=TAMANO_CELDA,
            sz=TAMANO_CELDA,
            objeto=_dibujar_cubo_unitario,
        )


