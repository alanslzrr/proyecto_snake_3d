"""
Proyecto Snake 3D - main.py

En este archivo montamos el punto de entrada de la aplicación. Sobre la base
del proyecto de referencia `SHADER`, aquí orquestamos:

- La ventana de Pygame con contexto OpenGL.
- La cámara orbital principal.
- El tablero 3D centrado en el origen.
- Y, a partir de la Fase 3, una serpiente básica representada por varios cubos.

El objetivo es tener un bucle de juego claro sobre el que iremos añadiendo
funcionalidad (movimiento, comida, colisiones, etc.) de forma incremental.
"""


import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import (
    glClearColor,
    glEnable,
    glShadeModel,
    glClear,
    glMatrixMode,
    glLoadIdentity,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_MODELVIEW,
    GL_PROJECTION,
    GL_SMOOTH,
    glRotatef,
)
from OpenGL.GLU import gluPerspective, gluLookAt

from camara import Camara
from configuracion import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_ASPECT_RATIO,
    FOV,
    NEAR_PLANE,
    FAR_PLANE,
    FPS,
    MILLISECONDS_PER_SECOND,
)
from utilidades import dibujar_elementos_auxiliares
from tablero import Tablero
from snake import Snake
from usuario import procesar_eventos_raton, consultar_estado_teclado


def inicializar_escena() -> pygame.Surface:
    """
    Creamos la ventana, configuramos el contexto de OpenGL y dejamos lista
    la proyección en perspectiva.
    """
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Snake 3D - Fase 3: Serpiente básica sobre el tablero")

    # Color de fondo y ajustes básicos de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    # Matriz de proyección
    glMatrixMode(GL_PROJECTION)
    gluPerspective(FOV, SCREEN_ASPECT_RATIO, NEAR_PLANE, FAR_PLANE)

    # Matriz de vista/modelo
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    return screen


def crear_camara_inicial() -> Camara:
    """
    Creamos la cámara con una configuración cómoda para ver el origen, que de
    momento es donde vamos a centrar el tablero en fases posteriores.
    """
    camara = Camara(pitch=30.0, yaw=45.0, roll=0.0, radio=10.0)
    camara.actualizar_camara()
    return camara


def renderizar(camara: Camara, tablero: Tablero, snake: Snake) -> None:
    """
    Borramos el frame anterior, colocamos la cámara y dibujamos los elementos
    auxiliares (ejes y rejilla).
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Aplicamos el roll de la cámara antes de configurar la vista
    glRotatef(camara.roll, 0.0, 0.0, 1.0)

    cam_x, cam_y, cam_z = camara.obtener_posicion()
    # De momento miramos al origen (0, 0, 0), que será el centro del tablero
    gluLookAt(cam_x, cam_y, cam_z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Ejes para situarnos en la escena y el tablero 3D como superficie de juego
    dibujar_elementos_auxiliares(ejes=True, rejilla=False)
    tablero.dibujar()
    snake.dibujar()


def bucle_principal() -> None:
    """
    Bucle principal del juego.

    Por ahora sólo gestionamos la cámara y el dibujado de la escena base.
    La serpiente, el tablero y la comida se irán integrando sobre esta estructura.
    """
    screen = inicializar_escena()
    _ = screen  # De momento no usamos el objeto directamente, pero lo mantenemos por claridad.

    camara = crear_camara_inicial()
    tablero = Tablero()
    snake = Snake(tablero=tablero, longitud_inicial=3)

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        delta_time = clock.tick(FPS) / MILLISECONDS_PER_SECOND

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type in (
                pygame.MOUSEBUTTONDOWN,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEMOTION,
                pygame.MOUSEWHEEL,
            ):
                procesar_eventos_raton(evento, camara)

        consultar_estado_teclado(camara, delta_time)
        camara.actualizar_camara()

        renderizar(camara, tablero, snake)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    bucle_principal()


