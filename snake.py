"""
Proyecto Snake 3D - snake.py

Módulo principal de la lógica de la serpiente.

Fase 4:
- Implementamos el movimiento automático tipo "crawler" sobre la cara frontal.
- Gestionamos la cola de segmentos manteniendo el tamaño constante.
- Añadimos un control de rango de la rejilla lógica (sin cambio de cara aún).
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
        """
        if not self.vivo:
            return

        self.tiempo_acumulado += dt

        # Si ha pasado suficiente tiempo, damos un "paso".
        if self.tiempo_acumulado >= TIEMPO_PASO:
            self.tiempo_acumulado = 0.0
            self.mover()

    def mover(self):
        """Calcula la nueva posición y actualiza los segmentos."""
        # 1. Actualizamos la dirección oficial.
        self.direccion = self.proxima_direccion
        dx, dy, dz = self.direccion

        # 2. Obtenemos posición actual de la cabeza.
        cabeza = self.segmentos[0]
        nx = cabeza.x + dx
        ny = cabeza.y + dy
        nz = cabeza.z + dz

        # 3. Control de rango discreto (FASE 4, DETALLE TÉCNICO).
        # A nivel conceptual, el cubo planetario no tiene "paredes" y la
        # serpiente solo debería poder perder por autocolisión. Este chequeo
        # simplemente garantiza que, a nivel de índices de la rejilla, no
        # intentemos acceder a posiciones fuera de rango mientras todavía no
        # está implementado el cambio de cara en la Fase 5.
        if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
            return

        # 4. Movimiento "crawler" (mover la serpiente).
        # a) Creamos nueva cabeza en la posición destino.
        nueva_cabeza = Segmento(nx, ny, nz, COLOR_SERPIENTE_CABEZA)

        # b) La cabeza antigua pasa a ser cuerpo.
        self.segmentos[0].color = COLOR_SERPIENTE_CUERPO

        # c) Insertamos la nueva cabeza al principio de la lista.
        self.segmentos.insert(0, nueva_cabeza)

        # d) Eliminamos la cola (para mantener el tamaño, a menos que comamos).
        #    En una fase posterior, si comemos, no haremos pop.
        self.segmentos.pop()

    def dibujar(self):
        for seg in self.segmentos:
            seg.dibujar(self.tablero)