"""
Proyecto Snake 3D - usuario.py

De momento reutilizamos la misma lógica de entrada que en `SHADER/usuario.py`
para controlar la cámara con ratón y teclado. Más adelante ampliaremos este
archivo con las teclas específicas del juego (giro de la serpiente, reinicio,
cambio de modo de cámara, etc.).
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
    Procesamos los eventos de ratón para rotar y hacer zoom con la cámara.

    Esta función es prácticamente un calco de la que hemos usado en SHADER: nos
    permite orbitar alrededor de la escena de forma muy cómoda mientras
    desarrollamos el resto de componentes del juego.
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
    Leemos el estado del teclado para ajustar la cámara.

    Mantendremos estos controles tal cual durante las primeras fases, y en
    cuanto tengamos la serpiente en marcha añadiremos aquí las teclas de
    movimiento del juego.
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


