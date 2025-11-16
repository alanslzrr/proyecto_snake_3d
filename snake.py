"""
Proyecto Snake 3D - snake.py

En este módulo agrupamos la serpiente como entidad lógica del juego.

En la Fase 3 nuestro objetivo no es todavía moverla, sino conseguir:

- Una serpiente básica construida a partir de varios `Segmento`.
- Situarla sobre el tablero utilizando coordenadas de celda.
- Poder dibujarla de forma consistente en la escena 3D.

Más adelante, en fases posteriores, añadiremos aquí la lógica de movimiento,
crecimiento y colisiones. Por ahora nos quedamos con una serpiente estática
que nos sirve para validar el modelo de datos y el sistema de dibujo.
"""

from __future__ import annotations

from typing import List

from configuracion import (
    TABLERO_ANCHO,
    TABLERO_LARGO,
    COLOR_SERPIENTE_CABEZA,
    COLOR_SERPIENTE_CUERPO,
)
from segmento import Segmento
from tablero import Tablero


class Snake:
    """
    Representación básica de la serpiente como lista de segmentos.

    En esta fase mantenemos la serpiente estática: elegimos una posición
    cómoda sobre el tablero y generamos una pequeña cadena de segmentos
    alineados. El objetivo es que se vea claramente en pantalla y que
    nos acostumbremos a trabajar con coordenadas de celda.
    """

    def __init__(self, tablero: Tablero, longitud_inicial: int = 3) -> None:
        self.tablero = tablero
        self.longitud_inicial = max(1, longitud_inicial)

        self.segmentos: List[Segmento] = []
        self._crear_serpiente_inicial()

    # ------------------------------------------------------------------
    # Construcción inicial
    # ------------------------------------------------------------------

    def _crear_serpiente_inicial(self) -> None:
        """
        Creamos una serpiente muy sencilla en el centro del tablero.

        Colocamos la cabeza en el centro y vamos añadiendo segmentos hacia
        atrás en el eje Z. Todavía no nos preocupamos por la dirección real
        de movimiento, eso llegará en la siguiente fase.
        """
        centro_x = TABLERO_ANCHO // 2
        centro_z = TABLERO_LARGO // 2

        # Cabeza
        self.segmentos.append(
            Segmento(
                celda_x=centro_x,
                celda_z=centro_z,
                color=COLOR_SERPIENTE_CABEZA,
            )
        )

        # Cuerpo inicial, alineado detrás de la cabeza en el eje Z
        for i in range(1, self.longitud_inicial):
            self.segmentos.append(
                Segmento(
                    celda_x=centro_x,
                    celda_z=centro_z - i,
                    color=COLOR_SERPIENTE_CUERPO,
                )
            )

    # ------------------------------------------------------------------
    # Dibujado
    # ------------------------------------------------------------------

    def dibujar(self) -> None:
        """
        Recorremos todos los segmentos y los dibujamos sobre el tablero actual.

        De momento no hay noción de "cabeza activa" más allá del color, ya que
        la serpiente permanece quieta. En cuanto tengamos movimiento, este
        método seguirá siendo válido: la lista de segmentos será la que vaya
        cambiando con el tiempo.
        """
        for segmento in self.segmentos:
            segmento.dibujar(self.tablero)


