"""
Proyecto Snake 3D: Vóxel Planetario - input_handler.py

Este módulo actúa como el "traductor" entre el hardware del jugador y la
lógica del juego. Su responsabilidad es capturar las pulsaciones de teclas
y convertirlas en acciones semánticas que el resto del sistema pueda entender.

La filosofía de diseño es desacoplar completamente "qué tecla se pulsó" de
"qué debe ocurrir en el juego". Esto nos permite:

- Cambiar los controles fácilmente sin tocar la lógica del juego.
- Tener un código más limpio y mantenible.
- Facilitar futuras extensiones (gamepads, controles personalizables).

Funcionalidades implementadas:
- Detección del evento de cierre (QUIT, ESC).
- Mapeo de flechas a direcciones de la serpiente.
- Acciones de menú (S para iniciar, R para reiniciar).
- Selección de cámara (teclas 1-4).
"""

import pygame
from pygame.locals import *
from configuracion import DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT

class InputHandler:
    def __init__(self):
        self.salir = False
        
        # Buffer de acciones discretas (se limpian cada frame)
        self.direccion_snake = None 
        




    def procesar_eventos(self):
        """
        Lee la cola de eventos de Pygame y el estado del teclado.
        Debe llamarse una vez por frame.
        """
        # 1. Resetear acciones de un solo disparo (triggers)
        self.direccion_snake = None
        self.accion_start = False
        self.accion_restart = False
        self.camara_1 = False
        self.camara_2 = False
        self.camara_3 = False
        self.camara_4 = False


        # 2. Procesar cola de eventos (pulsaciones discretas)
        for event in pygame.event.get():
            if event.type == QUIT:
                self.salir = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.salir = True
                elif event.key == K_UP:
                    self.direccion_snake = DIR_UP
                elif event.key == K_DOWN:
                    self.direccion_snake = DIR_DOWN
                elif event.key == K_LEFT:
                    self.direccion_snake = DIR_LEFT
                elif event.key == K_RIGHT:
                    self.direccion_snake = DIR_RIGHT
                elif event.key == K_s:
                    self.accion_start = True
                elif event.key == K_r:
                    self.accion_restart = True
                elif event.key == K_1:
                    self.camara_1 = True
                elif event.key == K_2:
                    self.camara_2 = True
                elif event.key == K_3:
                    self.camara_3 = True
                elif event.key == K_4:
                    self.camara_4 = True

        # 3. Procesar estado continuo (teclas mantenidas para rotación manual)
        # --- OPTIMIZACION: Eliminado WASD por redundancia ---
        pass
