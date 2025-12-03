"""
Proyecto Snake 3D - snake.py

Módulo principal de la lógica de la serpiente.

Fase 4:
- Implementamos el movimiento automático tipo "crawler" sobre la cara frontal.
- Gestionamos la cola de segmentos manteniendo el tamaño constante.
- Añadimos un control de rango de la rejilla lógica (sin cambio de cara aún).

Fase 5:
- Detectamos cruces de borde y aplicamos transiciones de cara manteniendo la
  ilusión del “frente infinito”.
- Rotamos las coordenadas discretas de todos los segmentos para que, tras la
  animación visual del cubo, la lógica continúe operando sobre la cara frontal.
"""

from configuracion import (
    GRID_SIZE,
    COLOR_SERPIENTE_CABEZA,
    COLOR_SERPIENTE_CUERPO,
    DIR_UP,
    DIR_DOWN,
    DIR_LEFT,
    DIR_RIGHT,
    DIR_STOP,
    TIEMPO_PASO,
)
from segmento import Segmento
from tablero import Tablero

class Snake:
    def __init__(self, tablero: Tablero):
        self.tablero = tablero
        self.segmentos = []

        # Estado de movimiento
        self.direccion = DIR_UP           # Dirección actual de movimiento
        self.proxima_direccion = DIR_UP   # Buffer para la siguiente entrada del usuario
        self.tiempo_acumulado = 0.0       # Acumulador para controlar la velocidad
        self.vivo = True                  # Bandera para detener la serpiente cuando haya autocolisión (fase futura)

        self._crear_inicial()

    def _crear_inicial(self):
        """
        Inicializa la serpiente sobre la cara frontal del cubo (Z positiva),
        colocando la cabeza en el centro y dos segmentos de cuerpo por debajo
        en el eje Y para que la cadena sea claramente visible.
        """
        z_face = GRID_SIZE - 1
        mid = GRID_SIZE // 2

        # Cabeza
        self.segmentos.append(Segmento(mid, mid, z_face, COLOR_SERPIENTE_CABEZA))

        # Cuerpo (2 segmentos hacia abajo)
        self.segmentos.append(Segmento(mid, mid - 1, z_face, COLOR_SERPIENTE_CUERPO))
        self.segmentos.append(Segmento(mid, mid - 2, z_face, COLOR_SERPIENTE_CUERPO))

    def cambiar_direccion(self, nueva_dir):
        """
        Actualiza la intención de giro.
        Evita que la serpiente gire 180 grados sobre sí misma instantáneamente.
        """
        # Si estamos parados o muertos, no hacemos nada (o podríamos reiniciar).
        if not self.vivo or self.direccion == DIR_STOP:
            return

        # Verificar opuestos para evitar giros de 180º.
        # Si sumamos los vectores de dirección opuestos (ej. 1 + -1), da 0.
        es_opuesto = (
            (self.direccion[0] + nueva_dir[0] == 0)
            and (self.direccion[1] + nueva_dir[1] == 0)
            and (self.direccion[2] + nueva_dir[2] == 0)
        )

        if not es_opuesto:
            self.proxima_direccion = nueva_dir

    def actualizar(self, dt: float):
        """
        Avanza la lógica de juego según el delta time.

        Returns:
            tuple[str | None, float]: información sobre la rotación solicitada.
            - ('x'|'y', +/-90.0) cuando hay transición de cara.
            - (None, 0.0) si no ocurre nada especial.
        """
        if not self.vivo:
            return (None, 0.0)

        self.tiempo_acumulado += dt

        rotacion_solicitada = (None, 0.0)

        # Si ha pasado suficiente tiempo, damos un "paso".
        if self.tiempo_acumulado >= TIEMPO_PASO:
            self.tiempo_acumulado = 0.0
            rotacion_solicitada = self.mover()

        return rotacion_solicitada

    def mover(self, crecer=False):
        """
        Calcula la nueva posición, gestiona transiciones de cara y actualiza los segmentos.
        :param crecer: Si es True, no eliminamos la cola (la serpiente crece).
        """
        # 1. Actualizamos la dirección oficial.
        self.direccion = self.proxima_direccion
        dx, dy, dz = self.direccion

        # 2. Obtenemos posición actual de la cabeza.
        cabeza = self.segmentos[0]
        nx = cabeza.x + dx
        ny = cabeza.y + dy
        nz = cabeza.z + dz

        # 3. Verificamos si debemos rotar el mundo (Fase 5).
        rotacion_eje, rotacion_angulo = self._verificar_transicion(nx, ny)

        if rotacion_eje is not None:
            # Ajustamos las coordenadas de todos los segmentos para mantener
            # la ilusión de que seguimos operando sobre la cara frontal.
            self._aplicar_transformacion_coordenadas(rotacion_eje, rotacion_angulo)

            # Recalculamos la posición objetivo de la cabeza en el nuevo marco.
            cabeza = self.segmentos[0]
            nx = cabeza.x + dx
            ny = cabeza.y + dy
            nz = cabeza.z + dz

        # 4. Control defensivo: evitamos acceder fuera de la rejilla
        # (solo debería ocurrir si en el futuro añadimos nuevas transiciones).
        if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
            return rotacion_eje, rotacion_angulo

        # --- FASE 8: Detección de Autocolisión ---
        # Verificamos si la nueva posición de la cabeza coincide con algún segmento del cuerpo.
        # Nota: No comprobamos el último segmento si no vamos a crecer, porque ese espacio quedará libre.
        # Sin embargo, para simplificar y ser robustos, comprobamos contra todos menos la cola actual
        # si no crecemos.
        
        # Enfoque simple: comprobamos contra todos los segmentos actuales.
        # Si la nueva cabeza (nx, ny, nz) está en self.segmentos, es choque.
        # Excepción: si no crecemos, la cola se va a ir, así que chocar contra la cola es válido (perseguirla).
        
        limite_comprobacion = len(self.segmentos)
        if not crecer:
            limite_comprobacion -= 1 # Ignoramos la cola actual porque se moverá
            
        for i in range(limite_comprobacion):
            seg = self.segmentos[i]
            if seg.x == nx and seg.y == ny and seg.z == nz:
                self.vivo = False
                print("Game Over: Autocolisión detectada")
                return rotacion_eje, rotacion_angulo

        # 5. Movimiento "crawler" (mover la serpiente).
        # a) Creamos nueva cabeza en la posición destino.
        nueva_cabeza = Segmento(nx, ny, nz, COLOR_SERPIENTE_CABEZA)

        # b) La cabeza antigua pasa a ser cuerpo.
        self.segmentos[0].color = COLOR_SERPIENTE_CUERPO

        # c) Insertamos la nueva cabeza al principio de la lista.
        self.segmentos.insert(0, nueva_cabeza)

        # d) Gestión de la cola (Crecimiento)
        if not crecer:
            # Si no crecemos, eliminamos la cola para mantener el tamaño.
            self.segmentos.pop()
        
        return rotacion_eje, rotacion_angulo

    def _verificar_transicion(self, nx, ny):
        """
        Detecta si la coordenada propuesta sale de la cara frontal y determina
        qué rotación del mundo es necesaria para seguir a la serpiente.

        Returns:
            tuple[str | None, float]: ('x'|'y', +/-90.0) o (None, 0.0).
        """
        limit = GRID_SIZE - 1

        # Caso 1: Salimos por la Derecha -> Mundo gira a la Izquierda (-90º en Y).
        if nx > limit:
            return ("y", -90.0)

        # Caso 2: Salimos por la Izquierda -> Mundo gira a la Derecha (+90º en Y).
        if nx < 0:
            return ("y", 90.0)

        # Caso 3: Salimos por Arriba -> Mundo gira hacia Abajo (+90º en X).
        if ny > limit:
            return ("x", 90.0)

        # Caso 4: Salimos por Abajo -> Mundo gira hacia Arriba (-90º en X).
        if ny < 0:
            return ("x", -90.0)

        return (None, 0.0)

    def _aplicar_transformacion_coordenadas(self, eje, angulo_mundo):
        """
        Aplica una rotación al sistema de coordenadas de todos los segmentos.

        Principio del “frente infinito”:
        Si el mundo gira visualmente -90º, rotamos las coordenadas de la serpiente
        +90º para que, matemáticamente, siga operando sobre la cara frontal.
        """
        N = GRID_SIZE - 1
        angulo_transformacion = -angulo_mundo  # Espejo respecto a la rotación visual.

        for seg in self.segmentos:
            x, y, z = seg.x, seg.y, seg.z

            if eje == "y":
                if angulo_transformacion == 90.0:
                    # Rotación +90º alrededor de Y (CCW).
                    seg.x = N - z
                    seg.z = x
                elif angulo_transformacion == -90.0:
                    # Rotación -90º alrededor de Y (CW).
                    seg.x = z
                    seg.z = N - x

            elif eje == "x":
                if angulo_transformacion == 90.0:
                    # Rotación +90º alrededor de X.
                    seg.y = z
                    seg.z = N - y
                elif angulo_transformacion == -90.0:
                    # Rotación -90º alrededor de X.
                    seg.y = N - z
                    seg.z = y

    def crecer(self):
        """
        Hace crecer a la serpiente añadiendo un nuevo segmento al final (cola).
        Se duplica el último segmento; en el siguiente movimiento se "desplegará".
        """
        cola = self.segmentos[-1]
        nuevo_segmento = Segmento(cola.x, cola.y, cola.z, COLOR_SERPIENTE_CUERPO)
        self.segmentos.append(nuevo_segmento)

    def dibujar(self):
        for seg in self.segmentos:
            seg.dibujar(self.tablero)