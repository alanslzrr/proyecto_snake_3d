"""
Proyecto Snake 3D - game.py

Este módulo contiene la clase principal `Game`, que actúa como el "Director"
de la aplicación.

Responsabilidades:
1. Inicializar subsistemas (Pygame, OpenGL).
2. Instanciar entidades (Snake, Tablero, Comida, Luces).
3. Gestionar el Bucle Principal (Game Loop):
   - Input (vía InputHandler)
   - Update (Lógica de juego y animaciones)
   - Render (Dibujado de la escena)

Esta refactorización nos permite tener un `main.py` limpio y facilita la
expansión futura (ej. añadir menús o estados de pausa).
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt

from configuracion import *
from tablero import Tablero
from snake import Snake
from comida import Comida
from luces import Iluminacion
from input_handler import InputHandler

from text_renderer import TextRenderer

# Estados del juego
ESTADO_MENU = 0
ESTADO_JUGANDO = 1
ESTADO_GAMEOVER = 2

class Game:
    def __init__(self):
        # 1. Inicialización de Pygame y Ventana
        pygame.init()
        display = (SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Snake 3D: Vóxel Planetario")

        # 2. Configuración OpenGL
        self._configurar_opengl()

        # 3. Instanciación de Entidades
        self.input = InputHandler()
        self.luces = Iluminacion()
        self.text_renderer = TextRenderer() # Nuevo renderizador de texto
        
        # Inicializamos entidades del juego (se reiniciarán al empezar)
        self.tablero = Tablero()
        self.snake = None
        self.comida = None
        
        # 4. Estado del Juego
        self.clock = pygame.time.Clock()
        self.running = True
        self.estado = ESTADO_MENU
        self.score = 0
        
        # Variables de rotación del mundo
        self.rot_x = 0.0
        self.rot_y = 0.0

        # Variables de animación automática (transición de caras)
        self.animando = False
        self.tiempo_animacion = 0.0
        self.inicio_rot = {'x': 0.0, 'y': 0.0}
        self.meta_rot = {'x': 0.0, 'y': 0.0}

        # Fase 10: Estado de la cámara
        self.camara_actual = 1

    def _configurar_opengl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glClearColor(*COLOR_FONDO)
        
        glMatrixMode(GL_PROJECTION)
        gluPerspective(FOV, SCREEN_ASPECT_RATIO, NEAR_PLANE, FAR_PLANE)
        glMatrixMode(GL_MODELVIEW)

    def reset_game(self):
        """Reinicia la partida: serpiente, comida y puntuación."""
        self.snake = Snake(self.tablero)
        self.comida = Comida(self.snake)
        self.score = 0
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.animando = False

    def run(self):
        """
        Inicia el bucle principal del juego.
        """
        self.luces.activar()
        
        # Inicializamos objetos para que se vean en el menú de fondo (opcional)
        self.reset_game()

        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self._procesar_input()
            self._actualizar(dt)
            self._renderizar()
        
        pygame.quit()

    def _procesar_input(self):
        self.input.procesar_eventos()
        
        if self.input.salir:
            self.running = False
            return

        if self.estado == ESTADO_MENU:
            if self.input.accion_start:
                self.reset_game()
                self.estado = ESTADO_JUGANDO
        
        elif self.estado == ESTADO_GAMEOVER:
            if self.input.accion_restart:
                self.reset_game()
                self.estado = ESTADO_JUGANDO

        elif self.estado == ESTADO_JUGANDO:
            # Si estamos animando una transición automática, ignoramos el input de movimiento
            if not self.animando:
                # Input para la serpiente
                if self.input.direccion_snake:
                    self.snake.cambiar_direccion(self.input.direccion_snake)
                
                # --- OPTIMIZACION: Eliminada rotacion manual WASD ---
        
        # Fase 10: Cambio de cámara (Permitido en cualquier estado o restringido según diseño)
        # El usuario pidió "antes de presionar S o R", es decir en MENU o GAMEOVER.
        # Pero para mejor UX, lo permitiremos siempre o al menos en MENU/GAMEOVER.
        if self.estado in [ESTADO_MENU, ESTADO_GAMEOVER]:
            if self.input.camara_1:
                self.camara_actual = 1
            elif self.input.camara_2:
                self.camara_actual = 2
            elif self.input.camara_3:
                self.camara_actual = 3
            elif self.input.camara_4:
                self.camara_actual = 4

    def _actualizar(self, dt):
        self.luces.update(dt) # Actualizar luces (flash) siempre
        
        if self.estado == ESTADO_JUGANDO:
            if self.animando:
                self._actualizar_animacion(dt)
            else:
                self._actualizar_juego(dt)
        
        # En MENU y GAMEOVER podemos rotar el mundo suavemente como efecto visual
        elif self.estado == ESTADO_MENU or self.estado == ESTADO_GAMEOVER:
            self.rot_y += 10.0 * dt # Rotación automática de fondo

    def _actualizar_animacion(self, dt):
        self.tiempo_animacion += dt
        t = min(self.tiempo_animacion / TIEMPO_ROTACION_AUTO, 1.0)
        
        # Interpolación lineal (o suavizada si quisiéramos)
        self.rot_x = self.inicio_rot['x'] + (self.meta_rot['x'] - self.inicio_rot['x']) * t
        self.rot_y = self.inicio_rot['y'] + (self.meta_rot['y'] - self.inicio_rot['y']) * t

        if t >= 1.0:
            self.animando = False
            self.rot_x = self.meta_rot['x']
            self.rot_y = self.meta_rot['y']

    def _actualizar_juego(self, dt):
        # 1. Rotación manual (ELIMINADA)
        # --- OPTIMIZACION: Eliminada logica WASD ---

        # 2. Actualizar lógica de la serpiente
        eje_transicion, angulo_transicion = self.snake.actualizar(dt)
        
        # Verificar muerte
        if not self.snake.vivo:
            self.estado = ESTADO_GAMEOVER
            return

        # 3. Detectar transiciones de cara (Rotación Automática)
        if eje_transicion:
            self._iniciar_transicion(eje_transicion, angulo_transicion)
        
        # 4. Detectar colisión con comida
        head = self.snake.segmentos[0]
        if self.comida.posicion and \
           head.x == self.comida.posicion.x and \
           head.y == self.comida.posicion.y and \
           head.z == self.comida.posicion.z:
            
            self.snake.crecer()
            self.score += PUNTOS_POR_COMIDA # Sumar puntos
            self.comida.generar_nueva_posicion()
            self.luces.trigger_flash() # Disparar flash visual

    def _iniciar_transicion(self, eje, angulo):
        self.animando = True
        self.tiempo_animacion = 0.0
        
        # Rotamos la comida solidariamente
        self.comida.rotar_coordenadas(eje, angulo)

        # Preparamos la interpolación visual
        # Ajuste de "pop": retrocedemos la vista para compensar el salto lógico
        if eje == 'x':
            self.inicio_rot['x'] = self.rot_x - angulo
            self.inicio_rot['y'] = self.rot_y
            self.rot_x = self.inicio_rot['x'] # Aplicar instantáneamente para evitar glitch
            
            self.meta_rot['x'] = self.inicio_rot['x'] + angulo
            self.meta_rot['y'] = self.rot_y
            
        elif eje == 'y':
            self.inicio_rot['x'] = self.rot_x
            self.inicio_rot['y'] = self.rot_y - angulo
            self.rot_y = self.inicio_rot['y']
            
            self.meta_rot['x'] = self.rot_x
            self.meta_rot['y'] = self.inicio_rot['y'] + angulo

    def _renderizar(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Cámara
        dist = GRID_SIZE * 2.5
        
        if self.camara_actual == 1:
            # Cámara 1: Default (Isométrica)
            cx = dist * CAMARA_1_POS[0]
            cy = dist * CAMARA_1_POS[1]
            cz = dist * CAMARA_1_POS[2]
        elif self.camara_actual == 2:
            # Cámara 2: Frontal
            cx = dist * CAMARA_2_POS[0]
            cy = dist * CAMARA_2_POS[1]
            cz = dist * CAMARA_2_POS[2]
        
        elif self.camara_actual == 3:
            # Cámara 3: Tercera Persona (Dinámica)
            # Sigue a la cabeza de la serpiente
            if self.snake and self.snake.segmentos:
                head = self.snake.segmentos[0]
                # Obtenemos la posición real en el mundo
                hx, hy, hz = self.tablero.obtener_posicion_mundo(head.x, head.y, head.z)
                
                # La cámara se posiciona con un offset relativo a la cabeza
                cx = hx + CAMARA_3_OFFSET[0]
                cy = hy + CAMARA_3_OFFSET[1]
                cz = hz + CAMARA_3_OFFSET[2]
                
                # Miramos hacia la cabeza
                gluLookAt(cx, cy, cz, hx, hy, hz, 0, 1, 0)
                
                # IMPORTANTE: Retornamos aquí porque ya llamamos a gluLookAt
                # y no queremos ejecutar el gluLookAt genérico de abajo.
                self._renderizar_escena()
                return

        elif self.camara_actual == 4:
            # Cámara 4: Primera Persona (Snake View)
            if self.snake and self.snake.segmentos:
                head = self.snake.segmentos[0]
                hx, hy, hz = self.tablero.obtener_posicion_mundo(head.x, head.y, head.z)
                
                # Dirección de la serpiente
                dx, dy, dz = self.snake.direccion
                
                # Posición Cámara: Sobre la cabeza (Z+)
                # Nota: Asumimos que la serpiente siempre está en la cara Z+ (lógica del juego)
                cx = hx
                cy = hy
                cz = hz + CAMARA_4_ALTURA
                
                # Punto de Mira: Hacia adelante en la dirección de movimiento
                lx = hx + (dx * CAMARA_4_DISTANCIA_MIRA)
                ly = hy + (dy * CAMARA_4_DISTANCIA_MIRA)
                lz = hz # Miramos a la altura de la cabeza (o podríamos mirar un poco abajo)
                
                # Vector Arriba (Up Vector): La normal de la cara (Z+)
                # Esto mantiene el "suelo" (la cara del cubo) abajo en la pantalla.
                gluLookAt(cx, cy, cz, lx, ly, lz, 0, 0, 1)
                
                self._renderizar_escena()
                return

        gluLookAt(cx, cy, cz, 0, 0, 0, 0, 1, 0)
        self._renderizar_escena()

    def _renderizar_escena(self):
        """
        Dibuja los objetos de la escena (luces, mundo, entidades).
        Separado de _renderizar para reutilizarlo con distintas cámaras.
        """
        # Actualizar luces (necesario para el efecto flash en objetos)
        self.luces.activar()

        # Aplicar rotación del mundo
        glPushMatrix()
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)

        # Dibujar entidades
        if self.snake: self.snake.dibujar()
        if self.comida: self.comida.dibujar(self.tablero)
        self.tablero.dibujar()

        glPopMatrix()
        
        # --- RENDERIZADO DE UI (2D) ---
        if self.estado == ESTADO_MENU:
            self.text_renderer.dibujar_texto("SNAKE 3D PLANETARIO", 20, 20, "large")
            self.text_renderer.dibujar_texto("Press 'S' to Start", 20, 80, "small")
            self.text_renderer.dibujar_texto("Select Camera: '1' (Iso) / '2' (Front) / '3' (Follow) / '4' (FPS)", 20, 120, "small")
            self.text_renderer.dibujar_texto("Controls: Arrows to Move", 20, 160, "small")
            
        elif self.estado == ESTADO_JUGANDO:
            self.text_renderer.dibujar_texto(f"Score: {self.score}", 20, 20, "large")
            
        elif self.estado == ESTADO_GAMEOVER:
            self.text_renderer.dibujar_texto("GAME OVER", 20, 20, "large")
            self.text_renderer.dibujar_texto(f"Final Score: {self.score}", 20, 80, "large")
            self.text_renderer.dibujar_texto("Press 'R' to Restart", 20, 140, "small")

        # --- EFECTO FLASH (Overlay 2D) ---
        # Implementación Híbrida:
        # Además de alterar las luces 3D, dibujamos un quad blanco semitransparente
        # sobre toda la pantalla (espacio de pantalla 2D).
        # Esto garantiza que el jugador perciba el "impacto" visual incluso si
        # está mirando una zona oscura o si los materiales 3D no reaccionan mucho.
        if self.luces.flash_intensity > 0:
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
            
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            
            glDisable(GL_DEPTH_TEST)
            glDisable(GL_LIGHTING) # Importante: color puro sin luces
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            # Intensidad visual (ajustada para que no sea totalmente ciega)
            alpha = self.luces.flash_intensity * 0.6 
            glColor4f(1.0, 1.0, 1.0, alpha)
            
            glBegin(GL_QUADS)
            glVertex2f(0, 0)
            glVertex2f(SCREEN_WIDTH, 0)
            glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT)
            glVertex2f(0, SCREEN_HEIGHT)
            glEnd()
            
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)
            glDisable(GL_BLEND)
            
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()
