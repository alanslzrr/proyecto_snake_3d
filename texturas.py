"""
Proyecto Snake 3D - texturas.py

En este módulo centralizamos la carga de texturas utilizando Pygame y OpenGL.
La implementación es prácticamente la misma que en `SHADER/texturas.py`, ya que
esa versión cubre justo lo que necesitamos para el proyecto.
"""

import pygame
from OpenGL.GL import (
    glGenTextures,
    glBindTexture,
    glTexImage2D,
    glTexParameteri,
    GL_TEXTURE_2D,
    GL_RGB,
    GL_UNSIGNED_BYTE,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_REPEAT,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER,
    GL_LINEAR,
)


def cargar_textura(ruta_textura: str) -> int:
    """
    Cargamos una textura desde disco y la registramos en OpenGL.

    De momento mantenemos una función muy simple que devuelve el ID de la textura.
    Si más adelante vemos que repetimos muchas cargas, podremos montar una pequeña
    caché sobre esta misma función.
    """
    # Cargamos la imagen con Pygame.
    textura_surface = pygame.image.load(ruta_textura)

    # Convertimos la imagen a una cadena de bytes en formato RGB.
    textura_data = pygame.image.tostring(textura_surface, "RGB", 1)

    # Creamos el identificador de textura en OpenGL y la asociamos.
    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    # Subimos los datos de la textura a la GPU.
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGB,
        textura_surface.get_width(),
        textura_surface.get_height(),
        0,
        GL_RGB,
        GL_UNSIGNED_BYTE,
        textura_data,
    )

    # Configuramos el comportamiento de la textura.
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return int(textura_id)


