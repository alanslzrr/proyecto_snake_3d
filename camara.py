"""
Proyecto Snake 3D - camara.py

Esta clase de cámara está basada en la cámara orbital de `SHADER/camara.py`.
La usamos como cámara principal para explorar la escena 3D del juego: tablero,
serpiente y elementos auxiliares.
"""

import numpy as np


MIN_PITCH = -90.0  # Ángulo mínimo permitido para la inclinación (pitch)
MAX_PITCH = 90.0   # Ángulo máximo permitido para la inclinación (pitch)


class Camara:
    """Cámara orbital sencilla para la escena 3D del juego."""

    def __init__(self, pitch: float = 0.0, yaw: float = 0.0, roll: float = 0.0, radio: float = 10.0) -> None:
        """
        Creamos la cámara con unos valores iniciales que funcionan bien como vista general.

        Args:
            pitch: Ángulo inicial de inclinación vertical.
            yaw:   Ángulo inicial de rotación horizontal.
            roll:  Rotación lateral de la cámara.
            radio: Distancia al punto de interés (en nuestro caso, el origen).
        """
        # Guardamos los valores iniciales por si en algún momento queremos resetear la cámara.
        self.pitch_inicial = pitch
        self.yaw_inicial = yaw
        self.roll_inicial = roll
        self.radio_inicial = radio

        # Valores actuales
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.radio = radio

        # Posición calculada de la cámara en el espacio 3D
        self.cam_x, self.cam_y, self.cam_z = 0.0, 0.0, radio

    # ---------------------------------------------------------------------
    # Cálculo de posición
    # ---------------------------------------------------------------------

    def actualizar_camara(self) -> None:
        """
        Actualiza la posición de la cámara en el espacio a partir de pitch, yaw y radio.

        Usamos un modelo muy simple: la cámara describe una órbita alrededor del origen,
        lo suficiente para inspeccionar la escena durante las primeras fases del proyecto.
        """
        self.cam_x = self.radio * np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        self.cam_y = self.radio * np.sin(np.radians(self.pitch))
        self.cam_z = self.radio * np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))

    def obtener_posicion(self) -> tuple[float, float, float]:
        """Devolvemos la posición actual de la cámara para usarla en `gluLookAt`."""
        return self.cam_x, self.cam_y, self.cam_z

    # ---------------------------------------------------------------------
    # Controles básicos
    # ---------------------------------------------------------------------

    def ajustar_pitch(self, incremento: float) -> None:
        """Ajustamos el pitch respetando los límites para no dar la vuelta completa."""
        self.pitch = float(np.clip(self.pitch + incremento, MIN_PITCH, MAX_PITCH))

    def ajustar_yaw(self, incremento: float) -> None:
        """Ajustamos el yaw sin límites concretos (dejamos que pueda dar vueltas completas)."""
        self.yaw += incremento

    def ajustar_roll(self, incremento: float) -> None:
        """Ajustamos el roll para poder inclinar la escena lateralmente si lo necesitamos."""
        self.roll += incremento

    def ajustar_radio(self, incremento: float, min_radio: float, max_radio: float) -> None:
        """Acercamos o alejamos la cámara respetando un mínimo y un máximo razonables."""
        self.radio = float(np.clip(self.radio + incremento, min_radio, max_radio))

    # ---------------------------------------------------------------------
    # Estados predefinidos
    # ---------------------------------------------------------------------

    def reset(self) -> None:
        """Volvemos al estado inicial que hayamos definido para la cámara."""
        self.pitch = self.pitch_inicial
        self.yaw = self.yaw_inicial
        self.roll = self.roll_inicial
        self.radio = self.radio_inicial
        self.actualizar_camara()

    def set_capture(self) -> None:
        """
        Colocamos la cámara en una posición cómoda para tomar capturas
        (muy similar a la que usábamos en el proyecto de referencia SHADER).
        """
        self.pitch = 45.0
        self.yaw = 45.0
        self.roll = 0.0
        self.radio = 11.0
        self.actualizar_camara()


