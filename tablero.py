"""
Proyecto Snake 3D: Vóxel Planetario - tablero.py

Este módulo representa el corazón visual del juego: el "Mundo Cúbico" sobre
el que la serpiente se desplaza. Lo que antes era un simple tablero plano
se ha transformado en una estructura tridimensional fascinante.

El tablero es ahora:
- Un volumen de GRID_SIZE × GRID_SIZE × GRID_SIZE celdas (vóxeles).
- Una rejilla centrada en el origen del espacio 3D.
- Una estructura semitransparente que permite ver el interior del cubo,
  creando el distintivo efecto de "cubo de cristal".

Para lograr un rendimiento óptimo (60 FPS con miles de cubos), implementamos
Display Lists de OpenGL. Esta técnica precompila todos los comandos de dibujo
del tablero en la memoria de la GPU durante la inicialización. Después, cada
frame solo requiere una única llamada para renderizar toda la estructura.

Además, como optimización adicional, solo dibujamos los vóxeles de la
superficie del cubo (las 6 caras externas), dejando el interior vacío.
Esto reduce drásticamente el número de polígonos sin afectar la jugabilidad,
ya que la serpiente solo se mueve por la superficie.
"""

from OpenGL.GL import (
    glBegin, glEnd, glColor4f, glVertex3f,
    glEnable, glDisable, glBlendFunc, glLineWidth, glDepthMask,
    GL_QUADS, GL_LINES, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
    GL_FALSE, GL_TRUE, GL_LIGHTING,
    glGenLists, glNewList, glEndList, glCallList, GL_COMPILE
)
from configuracion import (
    GRID_SIZE, TAMANO_CELDA, OFFSET_GRID,
    COLOR_CUBO_VACIO, COLOR_BORDE_VACIO, ESPACIO_CELDA
)
from transformaciones import transformar

class Tablero:
    def __init__(self):
        self.size = GRID_SIZE
        self.display_list_id = None
        self._compilar_lista()
    
    def _compilar_lista(self):
        """
        Compila la geometría del tablero en una Display List de OpenGL.
        Esto envía todos los comandos de dibujo a la GPU una sola vez.
        """
        self.display_list_id = glGenLists(1)
        glNewList(self.display_list_id, GL_COMPILE)
        
        # --- Lógica de dibujo original ---
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)
        
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    # Optimización Fase 11: Solo dibujamos los cubos de la superficie (hueco por dentro)
                    # Esto limpia visualmente el centro y mejora el rendimiento.
                    if x == 0 or x == self.size - 1 or \
                       y == 0 or y == self.size - 1 or \
                       z == 0 or z == self.size - 1:
                        
                        px, py, pz = self.obtener_posicion_mundo(x, y, z)
                        transformar(
                            t_x=px, t_y=py, t_z=pz,
                            s_x=TAMANO_CELDA, s_y=TAMANO_CELDA, s_z=TAMANO_CELDA,
                            objeto_dibujado=self._dibujar_cubo_cristal
                        )
        
        glDepthMask(GL_TRUE)
        glDisable(GL_BLEND)
        # ---------------------------------
        
        glEndList()

    def obtener_posicion_mundo(self, x: int, y: int, z: int) -> tuple:
        """
        Convierte coordenadas discretas de rejilla (0..N-1) en coordenadas de
        mundo centradas en el origen.

        De este modo, cualquier celda identificada por índices enteros (x, y, z)
        puede traducirse a una posición 3D continua, compatible con las
        transformaciones de OpenGL.
        """
        # Fase 11: Incluimos el espacio entre celdas en el cálculo de la posición.
        stride = TAMANO_CELDA + ESPACIO_CELDA
        
        pos_x = (x * stride) - OFFSET_GRID + (TAMANO_CELDA / 2)
        pos_y = (y * stride) - OFFSET_GRID + (TAMANO_CELDA / 2)
        pos_z = (z * stride) - OFFSET_GRID + (TAMANO_CELDA / 2)
        return pos_x, pos_y, pos_z

    def dibujar(self):
        """
        Dibuja el tablero invocando la Display List precompilada.
        Rendimiento: 1 llamada vs 170,000 llamadas.
        """
        if self.display_list_id:
            glCallList(self.display_list_id)

    def _dibujar_cubo_cristal(self):
        """
        Primitiva de un cubo unitario con relleno translúcido y bordes
        marcados.

        El relleno aporta la sensación volumétrica, mientras que el
        wireframe refuerza la lectura de la rejilla 3D cuando el cubo rota
        sobre sí mismo.
        """
        hs = 0.4 # Half size (Reducido a 0.4 para mayor separación visual entre celdas)
        
        # 1. Relleno translúcido
        glColor4f(*COLOR_CUBO_VACIO)
        glBegin(GL_QUADS)
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
        # Desactivamos iluminación para que las líneas se vean siempre nítidas
        glDisable(GL_LIGHTING)
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
        glEnable(GL_LIGHTING) # Reactivamos iluminación para el resto de la escena