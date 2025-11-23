"""
Proyecto Snake 3D - main.py (Versión Vóxel / Cubo Rotatorio)

En este archivo implementamos el punto de entrada de la aplicación y el bucle
principal del juego en su versión “Cubo Planetario”.

Desde aquí orquestamos:

- La creación de la ventana de Pygame con contexto OpenGL.
- La configuración básica del pipeline (proyección en perspectiva y color de
  fondo).
- La instanciación del mundo cúbico (`Tablero`) y de la serpiente (`Snake`).
- La gestión del bucle de juego, incluyendo la lectura del teclado y la
  aplicación de una rotación global al mundo en función del input del usuario.

En esta fase del proyecto todavía no movemos la serpiente de forma autónoma:
utilizamos la rotación del cubo completo para inspeccionar visualmente la
estructura de vóxeles y validar las transformaciones geométricas compuestas.
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt

from configuracion import *
from tablero import Tablero
from snake import Snake

def main():
    pygame.init()
    display = (SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Snake 3D - Fase 4: Movimiento Crawler")

    # Configuración básica de OpenGL: prueba de profundidad y color de fondo.
    glEnable(GL_DEPTH_TEST)
    glClearColor(*COLOR_FONDO) # Fondo oscuro

    # Configuración de la proyección en perspectiva. Utilizamos los parámetros
    # centralizados en `configuracion.py` para garantizar coherencia visual.
    glMatrixMode(GL_PROJECTION)
    gluPerspective(FOV, SCREEN_ASPECT_RATIO, NEAR_PLANE, FAR_PLANE)

    glMatrixMode(GL_MODELVIEW)
    
    # Inicializamos los objetos principales de la escena:
    # - `Tablero`: mundo cúbico volumétrico (rejilla de vóxeles).
    # - `Snake`: serpiente adherida inicialmente a una de las caras del cubo.
    tablero = Tablero()
    snake = Snake(tablero)
    
    # Variables de rotación del mundo (acumulamos la rotación en función de la
    # entrada del usuario con las teclas WASD para inspeccionar el cubo).
    rot_x = 0.0
    rot_y = 0.0
    
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(FPS) / 1000.0  # Delta time en segundos

        # 1. Entrada (input)
        #    Aquí gestionamos eventos de ventana y teclado.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            # --- INPUT SERPIENTE (Eventos discretos para evitar doble giro) ---
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    snake.cambiar_direccion(DIR_UP)
                elif event.key == K_DOWN:
                    snake.cambiar_direccion(DIR_DOWN)
                elif event.key == K_LEFT:
                    snake.cambiar_direccion(DIR_LEFT)
                elif event.key == K_RIGHT:
                    snake.cambiar_direccion(DIR_RIGHT)

        # Control de rotación del cubo gigante mediante teclas WASD.
        # Cada tecla modifica el ángulo acumulado en el eje correspondiente.
        keys = pygame.key.get_pressed()
        if keys[K_a]:  # Izquierda
            rot_y -= VELOCIDAD_ROTACION_MUNDO * dt
        if keys[K_d]:  # Derecha
            rot_y += VELOCIDAD_ROTACION_MUNDO * dt
        if keys[K_w]:  # Arriba
            rot_x -= VELOCIDAD_ROTACION_MUNDO * dt
        if keys[K_s]:  # Abajo
            rot_x += VELOCIDAD_ROTACION_MUNDO * dt

        # 2. Actualización de la lógica de la serpiente en función del tiempo.
        snake.actualizar(dt)

        # 3. Renderizado
        #    Limpiamos los buffers, colocamos la cámara en una posición fija
        #    tipo isométrica y aplicamos la rotación global del mundo antes de
        #    dibujar el tablero y la serpiente.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Cámara fija: miramos al origen desde una esquina (vista isométrica
        # aproximada) para apreciar el volumen completo del cubo de vóxeles.
        distancia_camara = GRID_SIZE * 2.5
        gluLookAt(distancia_camara, distancia_camara * 0.8, distancia_camara, 
                  0, 0, 0, 
                  0, 1, 0)

        # --- Aplicamos la rotación global al mundo cúbico ---
        glPushMatrix()
        glRotatef(rot_x, 1, 0, 0) # Rotación eje X (Arriba/Abajo)
        glRotatef(rot_y, 0, 1, 0) # Rotación eje Y (Izquierda/Derecha)

        # Dibujamos el contenido del mundo:
        # primero la estructura volumétrica del tablero y, a continuación, la
        # serpiente sobre la cara frontal.
        tablero.dibujar()
        snake.dibujar()

        glPopMatrix()

        pygame.display.flip()

if __name__ == "__main__":
    main()