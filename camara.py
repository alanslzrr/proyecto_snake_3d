"""
Proyecto Snake 3D - camara.py

En este módulo definimos una cámara orbital sencilla, heredada y adaptada a
nuestra versión del proyecto basada en el mundo cúbico/voxel.

Aunque en la versión actual del juego priorizamos una cámara fija y la rotación
global del mundo, mantenemos esta cámara como infraestructura reutilizable para:

- Explorar la escena 3D durante el desarrollo (modo depuración).
- Tomar capturas con diferentes encuadres del cubo planetario.
- Contar con una base preparada para futuros modos de cámara (libre o tercera
  persona) si decidimos reintroducir control con ratón y teclado.

La cámara orbita alrededor del origen utilizando coordenadas esféricas
parametrizadas por `pitch`, `yaw` y `radio`.
"""

import numpy as np


MIN_PITCH = -90.0  # Ángulo mínimo permitido para la inclinación (pitch)
MAX_PITCH = 90.0   # Ángulo máximo permitido para la inclinación (pitch)


class Camara:
    """
    Cámara orbital para la escena 3D del juego.

    Gestiona una posición de cámara que describe una órbita alrededor del
    origen, lo que nos permite inspeccionar el mundo cúbico y la serpiente
    desde distintos ángulos cuando activamos este modo de visualización.
    """

    def __init__(self, pitch: float = 0.0, yaw: float = 0.0, roll: float = 0.0, radio: float = 10.0) -> None:
        """
        Creamos la cámara con unos valores iniciales pensados como vista general
        cómoda del centro de la escena.

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
        Calcula y actualiza la posición de la cámara en el espacio 3D a partir
        de `pitch`, `yaw` y `radio`.

        Utilizamos un modelo orbital sencillo: la cámara describe una órbita
        alrededor del origen, lo que resulta suficiente para inspeccionar el
        cubo planetario y validar la correcta colocación de los elementos en la
        escena.
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
        """
        Ajustamos el ángulo de inclinación vertical (pitch) respetando los
        límites definidos para evitar giros completos que resultarían poco
        útiles a nivel de visualización.
        """
        self.pitch = float(np.clip(self.pitch + incremento, MIN_PITCH, MAX_PITCH))

    def ajustar_yaw(self, incremento: float) -> None:
        """
        Ajustamos el ángulo de rotación horizontal (yaw).

        En este caso permitimos vueltas completas, ya que resulta natural poder
        rodear por completo el mundo cúbico.
        """
        self.yaw += incremento

    def ajustar_roll(self, incremento: float) -> None:
        """
        Ajustamos el roll (rotación sobre el eje de visión) para poder inclinar
        lateralmente la escena cuando buscamos encuadres más expresivos o
        queremos enfatizar el carácter planetario del cubo.
        """
        self.roll += incremento

    def ajustar_radio(self, incremento: float, min_radio: float, max_radio: float) -> None:
        """
        Acercamos o alejamos la cámara respetando un mínimo y un máximo
        razonables, de manera que siempre mantengamos una distancia útil para
        inspeccionar el cubo y la serpiente sin atravesar la geometría.
        """
        self.radio = float(np.clip(self.radio + incremento, min_radio, max_radio))

    # ---------------------------------------------------------------------
    # Estados predefinidos
    # ---------------------------------------------------------------------

    def reset(self) -> None:
        """Restablecemos los parámetros de la cámara a su estado inicial."""
        self.pitch = self.pitch_inicial
        self.yaw = self.yaw_inicial
        self.roll = self.roll_inicial
        self.radio = self.radio_inicial
        self.actualizar_camara()

    def set_capture(self) -> None:
        """
        Colocamos la cámara en una posición cómoda para tomar capturas del
        mundo cúbico, inspirada en la configuración que utilizábamos en el
        proyecto de referencia `SHADER`.
        """
        self.pitch = 45.0
        self.yaw = 45.0
        self.roll = 0.0
        self.radio = 11.0
        self.actualizar_camara()


