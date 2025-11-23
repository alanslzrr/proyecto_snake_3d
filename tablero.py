"""
Proyecto Snake 3D - tablero.py

En este módulo representamos el “Mundo Cúbico” sobre el que se desarrolla
nuestra versión planetaria del Snake 3D.

El tablero deja de ser un plano tradicional para convertirse en:

- Un volumen tridimensional discreto de tamaño `GRID_SIZE × GRID_SIZE × GRID_SIZE`.
- Una rejilla de celdas cúbicas (vóxeles) centrada en el origen del espacio 3D.
- Una estructura visual semitransparente que permite ver el interior del cubo y
  sirve como referencia espacial para la posición de la serpiente.

Nuestro objetivo en esta fase es proporcionar una representación volumétrica
clara y estable que nos permita razonar sobre coordenadas (x, y, z) y probar
las transformaciones geométricas globales del mundo (rotaciones completas del
cubo) antes de introducir la lógica de movimiento sobre la superficie.
"""

from OpenGL.GL import (
    glBegin, glEnd, glColor4f, glVertex3f,
    glEnable, glDisable, glBlendFunc, glLineWidth,
    GL_QUADS, GL_LINES, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
)
from configuracion import (
    GRID_SIZE, TAMANO_CELDA, OFFSET_GRID,
    COLOR_CUBO_VACIO, COLOR_BORDE_VACIO
)
from transformaciones import transformar

class Tablero:
    def __init__(self):
        self.size = GRID_SIZE
    
    def obtener_posicion_mundo(self, x: int, y: int, z: int) -> tuple:
        """
        Convierte coordenadas discretas de rejilla (0..N-1) en coordenadas de
        mundo centradas en el origen.

        De este modo, cualquier celda identificada por índices enteros (x, y, z)
        puede traducirse a una posición 3D continua, compatible con las
        transformaciones de OpenGL.
        """
        pos_x = (x * TAMANO_CELDA) - OFFSET_GRID + (TAMANO_CELDA / 2)
        pos_y = (y * TAMANO_CELDA) - OFFSET_GRID + (TAMANO_CELDA / 2)
        pos_z = (z * TAMANO_CELDA) - OFFSET_GRID + (TAMANO_CELDA / 2)
        return pos_x, pos_y, pos_z

    def dibujar(self):
        """
        Dibuja la estructura volumétrica completa del cubo gigante.

        Activamos `GL_BLEND` para que los minicubos que conforman el mundo
        tengan un relleno translúcido, manteniendo la sensación de “cubo de
        cristal” y permitiendo percibir la profundidad interna.

        Nota: En esta fase recorremos todas las celdas del volumen; en etapas
        posteriores podríamos optimizar este proceso dibujando únicamente las
        capas visibles o empleando técnicas más avanzadas de instancing.
        """
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Recorremos todo el volumen para dibujar la "rejilla de cristal"
        # Nota: Para optimizar en fases futuras, podríamos dibujar solo las caras externas
        # o usar Instancing, pero por ahora lo hacemos explícito para entender la lógica.
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    # Obtenemos coordenadas 3D reales
                    px, py, pz = self.obtener_posicion_mundo(x, y, z)
                    
                    # Dibujamos cada "celda vacía"
                    transformar(
                        t_x=px, t_y=py, t_z=pz,
                        s_x=TAMANO_CELDA, s_y=TAMANO_CELDA, s_z=TAMANO_CELDA,
                        objeto_dibujado=self._dibujar_cubo_cristal
                    )
        
        glDisable(GL_BLEND)

    def _dibujar_cubo_cristal(self):
        """
        Primitiva de un cubo unitario con relleno translúcido y bordes
        marcados.

        El relleno aporta la sensación volumétrica, mientras que el
        wireframe refuerza la lectura de la rejilla 3D cuando el cubo rota
        sobre sí mismo.
        """
        hs = 0.45 # Half size (un poco menos de 0.5 para ver separación entre celdas)
        
        # 1. Relleno translúcido
        glColor4f(*COLOR_CUBO_VACIO)
        glBegin(GL_QUADS)
        # ... (Definición de los vértices del cubo, omitido por brevedad estándar, 
        # es el mismo cubo de siempre pero con alpha)
        # Cara frontal
        glVertex3f(-hs, -hs,  hs); glVertex3f( hs, -hs,  hs)
        glVertex3f( hs,  hs,  hs); glVertex3f(-hs,  hs,  hs)
        # Cara trasera
        glVertex3f(-hs, -hs, -hs); glVertex3f(-hs,  hs, -hs)
        glVertex3f( hs,  hs, -hs); glVertex3f( hs, -hs, -hs)
        # Cara izquierda
        glVertex3f(-hs, -hs, -hs); glVertex3f(-hs, -hs,  hs)
        glVertex3f(-hs,  hs,  hs); glVertex3f(-hs,  hs, -hs)
        # Cara derecha
        glVertex3f( hs, -hs, -hs); glVertex3f( hs,  hs, -hs)
        glVertex3f( hs,  hs,  hs); glVertex3f( hs, -hs,  hs)
        # Cara arriba
        glVertex3f(-hs,  hs, -hs); glVertex3f(-hs,  hs,  hs)
        glVertex3f( hs,  hs,  hs); glVertex3f( hs,  hs, -hs)
        # Cara abajo
        glVertex3f(-hs, -hs, -hs); glVertex3f( hs, -hs, -hs)
        glVertex3f( hs, -hs,  hs); glVertex3f(-hs, -hs,  hs)
        glEnd()

        # 2. Bordes (Wireframe)
        glLineWidth(1.0)
        glColor4f(*COLOR_BORDE_VACIO)
        glBegin(GL_LINES)
        # Frontal
        glVertex3f(-hs,-hs, hs); glVertex3f( hs,-hs, hs)
        glVertex3f( hs,-hs, hs); glVertex3f( hs, hs, hs)
        glVertex3f( hs, hs, hs); glVertex3f(-hs, hs, hs)
        glVertex3f(-hs, hs, hs); glVertex3f(-hs,-hs, hs)
        # Trasera
        glVertex3f(-hs,-hs,-hs); glVertex3f( hs,-hs,-hs)
        glVertex3f( hs,-hs,-hs); glVertex3f( hs, hs,-hs)
        glVertex3f( hs, hs,-hs); glVertex3f(-hs, hs,-hs)
        glVertex3f(-hs, hs,-hs); glVertex3f(-hs,-hs,-hs)
        # Uniones
        glVertex3f(-hs,-hs, hs); glVertex3f(-hs,-hs,-hs)
        glVertex3f( hs,-hs, hs); glVertex3f( hs,-hs,-hs)
        glVertex3f( hs, hs, hs); glVertex3f( hs, hs,-hs)
        glVertex3f(-hs, hs, hs); glVertex3f(-hs, hs,-hs)
        glEnd()