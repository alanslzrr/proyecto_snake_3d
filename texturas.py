"""
Proyecto Snake 3D - texturas.py

En este módulo centralizamos la carga de texturas 2D utilizando Pygame y
OpenGL, siguiendo la misma filosofía que en `SHADER/texturas.py`.

Aunque en la versión actual del Snake planetario priorizamos una estética más
geométrica y translúcida (cubo de cristal y vóxeles de color plano), dejamos
preparada esta infraestructura de texturas para:

- Asignar materiales más ricos a la serpiente o a la comida en fases futuras.
- Incorporar detalles visuales en el mundo cúbico (por ejemplo, marcadores de
  zonas especiales sobre la superficie).
- Experimentar con efectos de iluminación y sombreado que combinen texturas y
  colores base.
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
    Carga una textura desde disco y la registra en OpenGL, devolviendo el
    identificador entero asociado.

    Mantenemos una función deliberadamente simple, suficiente para las
    necesidades actuales del proyecto. Si en fases posteriores detectamos
    cargas repetidas o un mayor número de recursos, podremos extender este
    módulo con una pequeña caché sobre esta misma función.
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



