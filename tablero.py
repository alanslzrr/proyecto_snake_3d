"""
Proyecto Snake 3D - tablero.py

En este módulo definimos el tablero sobre el que se moverá la serpiente.

La idea en esta fase es tener:

- Una representación lógica en forma de rejilla de celdas (ancho x largo).
- Un mapeo claro entre índices de celda y coordenadas del mundo 3D.
- Un dibujado sencillo del tablero que sustituya a la rejilla genérica que
  usábamos en la Fase 1.

Más adelante añadiremos aquí comprobaciones de límites y utilidades para
colisiones con bordes, pero de momento nos centramos en la parte visual y
en el sistema de coordenadas.
"""

from OpenGL.GL import (
    glBegin,
    glEnd,
    glColor3f,
    glVertex3f,
    GL_QUADS,
    GL_LINES,
)

from configuracion import (
    TABLERO_ANCHO,
    TABLERO_LARGO,
    TAMANO_CELDA,
    COLOR_TABLERO_BASE,
    COLOR_TABLERO_ALT,
    COLOR_TABLERO_BORDE,
)


class Tablero:
    """
    Representa el tablero lógico y visual del juego.

    Trabajamos con un tablero de TABLERO_ANCHO x TABLERO_LARGO celdas, centrado
    en el origen del mundo 3D. Cada celda tiene un tamaño fijo TAMANO_CELDA.
    """

    def __init__(self) -> None:
        self.ancho = TABLERO_ANCHO
        self.largo = TABLERO_LARGO
        self.tamano_celda = TAMANO_CELDA

        # Calculamos estos desplazamientos una vez para reutilizarlos tanto
        # al dibujar como al mapear celdas a posiciones del mundo.
        self.offset_x = (self.ancho * self.tamano_celda) / 2.0
        self.offset_z = (self.largo * self.tamano_celda) / 2.0

    # ------------------------------------------------------------------
    # Mapeo de celdas lógicas a coordenadas de mundo
    # ------------------------------------------------------------------

    def obtener_posicion_mundo(self, celda_x: int, celda_z: int) -> tuple[float, float, float]:
        """
        Convertimos una celda (x, z) en su posición central en el mundo 3D.

        Usamos índices de celda en el rango [0, ancho) x [0, largo). Centrar
        el tablero en el origen nos facilita luego el uso de la cámara y de
        los ejes auxiliares.
        """
        x = (celda_x * self.tamano_celda) - self.offset_x + (self.tamano_celda / 2.0)
        z = (celda_z * self.tamano_celda) - self.offset_z + (self.tamano_celda / 2.0)
        y = 0.0
        return x, y, z

    # ------------------------------------------------------------------
    # Dibujado
    # ------------------------------------------------------------------

    def dibujar(self) -> None:
        """
        Dibujamos el tablero como una malla de celdas planas en el plano XZ.

        Usamos un patrón de dos colores para hacerlo más legible, y rematamos
        con un marco que deja muy claro dónde empieza y termina el área jugable.
        """
        self._dibujar_celdas()
        self._dibujar_borde()

    def _dibujar_celdas(self) -> None:
        """Dibujamos todas las celdas del tablero como quads en el plano XZ."""
        glBegin(GL_QUADS)
        for x in range(self.ancho):
            for z in range(self.largo):
                # Alternamos el color en función de la paridad de la celda
                if (x + z) % 2 == 0:
                    glColor3f(*COLOR_TABLERO_BASE)
                else:
                    glColor3f(*COLOR_TABLERO_ALT)

                x0 = (x * self.tamano_celda) - self.offset_x
                x1 = x0 + self.tamano_celda
                z0 = (z * self.tamano_celda) - self.offset_z
                z1 = z0 + self.tamano_celda
                y = 0.0

                glVertex3f(x0, y, z0)
                glVertex3f(x1, y, z0)
                glVertex3f(x1, y, z1)
                glVertex3f(x0, y, z1)
        glEnd()

    def _dibujar_borde(self) -> None:
        """Dibujamos un marco alrededor del tablero para remarcar sus límites."""
        glColor3f(*COLOR_TABLERO_BORDE)

        min_x = -self.offset_x
        max_x = self.offset_x
        min_z = -self.offset_z
        max_z = self.offset_z
        y = 0.001  # Lo elevamos un poco para evitar z-fighting con las celdas

        glBegin(GL_LINES)

        # Lado frontal (z mínimo)
        glVertex3f(min_x, y, min_z)
        glVertex3f(max_x, y, min_z)

        # Lado trasero (z máximo)
        glVertex3f(min_x, y, max_z)
        glVertex3f(max_x, y, max_z)

        # Lado izquierdo (x mínimo)
        glVertex3f(min_x, y, min_z)
        glVertex3f(min_x, y, max_z)

        # Lado derecho (x máximo)
        glVertex3f(max_x, y, min_z)
        glVertex3f(max_x, y, max_z)

        glEnd()


