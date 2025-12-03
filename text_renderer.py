"""
Proyecto Snake 3D: Vóxel Planetario - text_renderer.py

Este módulo resuelve un problema clásico en aplicaciones OpenGL: ¿cómo
mostramos texto 2D (puntuación, instrucciones, mensajes) sobre una escena 3D?

La solución que implementamos sigue estos pasos:

1. Utilizamos pygame.font para renderizar el texto a una superficie 2D.
2. Convertimos esa superficie a datos de píxeles compatibles con OpenGL.
3. Cambiamos temporalmente a proyección ortogonal (2D).
4. Dibujamos los píxeles del texto directamente en pantalla con glDrawPixels.
5. Restauramos la proyección 3D para continuar con el renderizado normal.

Para optimizar el rendimiento, implementamos un sistema de caché que evita
regenerar las texturas de texto en cada frame. Los textos estáticos (como
"Press S to Start") se generan una sola vez y se reutilizan, mientras que
los textos dinámicos (como la puntuación) se actualizan solo cuando cambian.

Esta técnica nos permite mantener los 60 FPS estables sin sacrificar la
claridad visual de la interfaz de usuario.
"""

import pygame
from OpenGL.GL import *
from configuracion import SCREEN_WIDTH, SCREEN_HEIGHT

class TextRenderer:
    def __init__(self):
        self.font_large = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 24)
        self.color_text = (255, 255, 255, 255) # Blanco
        
        # --- OPTIMIZACION: Cache de texturas ---
        # Diccionario: (texto, tamano) -> (width, height, text_data)
        self.cache = {}

    def dibujar_texto(self, texto, x, y, tamano="small"):
        """
        Dibuja texto en la posición (x, y) de la pantalla.
        Usa caché para evitar renderizar la fuente en cada frame.
        """
        clave_cache = (texto, tamano)
        
        if clave_cache in self.cache:
            width, height, text_data = self.cache[clave_cache]
        else:
            # Si no está en caché, generamos
            font = self.font_large if tamano == "large" else self.font_small
            text_surface = font.render(texto, True, self.color_text, (0,0,0,0)) # Fondo transparente
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            width, height = text_surface.get_rect().size
            
            # Guardamos en caché
            self.cache[clave_cache] = (width, height, text_data)

        # Configurar proyección ortogonal para UI 2D
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Desactivar profundidad y luces (aunque ya no hay luces globales)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Posicionar raster (OpenGL empieza abajo-izquierda, Pygame arriba-izquierda)
        glRasterPos2i(x, SCREEN_HEIGHT - y - height)
        
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        # Restaurar estado
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
