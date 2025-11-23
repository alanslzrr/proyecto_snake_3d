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

En esta fase añadimos la rotación automática del cubo cuando la serpiente
atraviesa un borde, manteniendo la ilusión del “frente infinito” sin sacrificar
la posibilidad de inspeccionar manualmente el mundo con las teclas WASD.

La lógica del bucle principal opera ahora con dos modos bien diferenciados:

1. Rotación manual controlada por el usuario (modo inspección).
2. Animación automática que interpola suavemente una rotación de 90º siempre que
   la serpiente solicita una transición de cara.
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
    pygame.display.set_caption("Snake 3D - Fase 5: Transición de Caras")

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

    # Variables que controlan la animación automática al cambiar de cara.
    animando = False
    tiempo_animacion = 0.0
    inicio_rot_x = rot_x
    inicio_rot_y = rot_y
    meta_rot_x = rot_x
    meta_rot_y = rot_y

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
            if not animando and event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    snake.cambiar_direccion(DIR_UP)
                elif event.key == K_DOWN:
                    snake.cambiar_direccion(DIR_DOWN)
                elif event.key == K_LEFT:
                    snake.cambiar_direccion(DIR_LEFT)
                elif event.key == K_RIGHT:
                    snake.cambiar_direccion(DIR_RIGHT)

        if animando:
            # 2.a Modo Animación: interpolamos hacia la meta calculada.
            tiempo_animacion += dt
            t = min(tiempo_animacion / TIEMPO_ROTACION_AUTO, 1.0)

            # Para depurar utilizamos interpolación lineal. Si queremos un
            # efecto más suave basta con activar una curva ease-out:
            # t_smooth = t * (2 - t)
            t_smooth = t

            rot_x = inicio_rot_x + (meta_rot_x - inicio_rot_x) * t_smooth
            rot_y = inicio_rot_y + (meta_rot_y - inicio_rot_y) * t_smooth

            if t >= 1.0:
                animando = False
                rot_x = meta_rot_x
                rot_y = meta_rot_y
        else:
            # 2.b Modo Manual: el usuario puede rotar y la serpiente avanza.
            keys = pygame.key.get_pressed()
            if keys[K_a]:  # Izquierda
                rot_y -= VELOCIDAD_ROTACION_MUNDO * dt
            if keys[K_d]:  # Derecha
                rot_y += VELOCIDAD_ROTACION_MUNDO * dt
            if keys[K_w]:  # Arriba
                rot_x -= VELOCIDAD_ROTACION_MUNDO * dt
            if keys[K_s]:  # Abajo
                rot_x += VELOCIDAD_ROTACION_MUNDO * dt

            eje_transicion, angulo_transicion = snake.actualizar(dt)

            if eje_transicion:
                # Iniciamos la animación automática solicitada por la serpiente.
                animando = True
                tiempo_animacion = 0.0

                target_change = angulo_transicion

                # Ajuste de "pop": retrocedemos instantáneamente la rotación visual
                # para que la serpiente no parezca teletransportarse y luego
                # interpolamos de nuevo hacia la postura final.
                if eje_transicion == 'x':
                    inicio_rot_x = rot_x - target_change
                    inicio_rot_y = rot_y
                    rot_x = inicio_rot_x
                    meta_rot_x = inicio_rot_x + target_change
                    meta_rot_y = rot_y
                elif eje_transicion == 'y':
                    inicio_rot_x = rot_x
                    inicio_rot_y = rot_y - target_change
                    rot_y = inicio_rot_y
                    meta_rot_x = rot_x
                    meta_rot_y = inicio_rot_y + target_change

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
        # Primero la serpiente (opaca) para asegurar que escriba en el depth buffer.
        # Después el tablero translúcido, que se mezcla sobre la escena sin ocultarla.
        snake.dibujar()
        tablero.dibujar()

        glPopMatrix()

        pygame.display.flip()

if __name__ == "__main__":
    main()