"""
Proyecto Snake 3D - usuario.py

En este módulo gestionamos la entrada del usuario pensada originalmente para
controlar una cámara orbital (ratón y teclado), siguiendo de cerca la lógica
del proyecto de referencia `SHADER/usuario.py`.

Aun cuando en la versión actual del Snake planetario hemos pasado a controlar
principalmente la rotación del mundo cúbico desde `main.py`, mantenemos este
archivo como infraestructura de entrada:

- Para seguir disponiendo de una cámara orbital de apoyo durante el desarrollo.
- Para facilitar la experimentación con distintos modos de cámara (por ejemplo,
  alternar entre vista fija y vista orbital).
- Como base sobre la que integraremos, en fases posteriores, teclas específicas
  del juego (reinicio, cambio de modo de cámara, atajos de depuración, etc.).
"""

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_q,
    K_a,
    K_e,
    K_d,
    K_r,
    K_c,
)

from configuracion import (
    BOTON_IZQUIERDO_RATON,
    SENSIBILIDAD_ROTACION,
    SENSIBILIDAD_ZOOM,
    RADIO_MIN,
    RADIO_MAX,
    INVERTIR_CONTROLES,
    VELOCIDAD_ROTACION,
    VELOCIDAD_ZOOM,
)


boton_izquierdo_presionado = False
ultimo_x, ultimo_y = 0, 0


def procesar_eventos_raton(evento: pygame.event.Event, camara) -> None:
    """
    Procesa los eventos de ratón para rotar y hacer zoom con la cámara orbital.

    Esta función reproduce la filosofía del proyecto `SHADER`: nos permite
    orbitar alrededor de la escena de forma cómoda mientras desarrollamos y
    validamos los distintos componentes del juego.
    """
    global boton_izquierdo_presionado, ultimo_x, ultimo_y

    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == BOTON_IZQUIERDO_RATON:
        boton_izquierdo_presionado = True
        ultimo_x, ultimo_y = evento.pos

    elif evento.type == pygame.MOUSEBUTTONUP and evento.button == BOTON_IZQUIERDO_RATON:
        boton_izquierdo_presionado = False

    elif evento.type == pygame.MOUSEMOTION and boton_izquierdo_presionado:
        dx = evento.pos[0] - ultimo_x
        dy = evento.pos[1] - ultimo_y

        camara.ajustar_yaw(dx * SENSIBILIDAD_ROTACION * INVERTIR_CONTROLES)
        camara.ajustar_pitch(-dy * SENSIBILIDAD_ROTACION * INVERTIR_CONTROLES)

        ultimo_x, ultimo_y = evento.pos

    elif evento.type == pygame.MOUSEWHEEL:
        camara.ajustar_radio(-evento.y * SENSIBILIDAD_ZOOM * INVERTIR_CONTROLES, RADIO_MIN, RADIO_MAX)


def consultar_estado_teclado(camara, delta_time: float) -> None:
    """
    Lee el estado del teclado y ajusta los parámetros de la cámara orbital.

    Mantenemos estos controles como soporte de desarrollo: mientras el modo
    principal de juego se basa en la rotación global del mundo cúbico, esta
    interfaz nos sigue resultando útil para inspeccionar la escena desde otros
    ángulos y preparar futuras ampliaciones de control.
    """
    keys = pygame.key.get_pressed()

    velocidad_rotacion = VELOCIDAD_ROTACION * delta_time * INVERTIR_CONTROLES
    velocidad_vertical = VELOCIDAD_ROTACION * delta_time
    velocidad_zoom = VELOCIDAD_ZOOM * delta_time * INVERTIR_CONTROLES

    if keys[K_UP]:
        camara.ajustar_pitch(-velocidad_vertical)
    if keys[K_DOWN]:
        camara.ajustar_pitch(velocidad_vertical)
    if keys[K_LEFT]:
        camara.ajustar_yaw(-velocidad_rotacion)
    if keys[K_RIGHT]:
        camara.ajustar_yaw(velocidad_rotacion)

    if keys[K_q]:
        camara.ajustar_radio(-velocidad_zoom, RADIO_MIN, RADIO_MAX)
    if keys[K_a]:
        camara.ajustar_radio(velocidad_zoom, RADIO_MIN, RADIO_MAX)

    if keys[K_e]:
        camara.ajustar_roll(velocidad_rotacion)
    if keys[K_d]:
        camara.ajustar_roll(-velocidad_rotacion)

    if keys[K_r]:
        camara.reset()
    if keys[K_c]:
        camara.set_capture()


