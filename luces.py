"""
Proyecto Snake 3D: Vóxel Planetario - luces.py

Este módulo gestiona el sistema de iluminación de nuestra escena 3D. La luz
es fundamental para dar volumen y profundidad a los objetos, transformando
formas planas en elementos tridimensionales convincentes.

Implementamos una luz direccional (GL_LIGHT0) posicionada en la esquina
superior derecha frontal de la escena. Esta configuración crea sombras suaves
y resalta los bordes del cubo planetario, mejorando significativamente la
lectura espacial del juego.

Además de la iluminación estática, este módulo gestiona el efecto de
"Flash" que se activa cuando la serpiente come. Este feedback visual
refuerza la sensación de logro del jugador mediante un destello de luz
que ilumina momentáneamente toda la escena.
"""

from OpenGL.GL import *


class Iluminacion:
    """
    Clase que encapsula la configuración de iluminación OpenGL y el sistema
    de efectos visuales dinámicos (flash al comer).
    
    La iluminación se compone de tres elementos:
    - Luz ambiental: Iluminación base que afecta a todos los objetos.
    - Luz difusa: Componente direccional que crea degradados de sombra.
    - Luz especular: Brillos puntuales que dan sensación de material pulido.
    """
    def __init__(self):
        # Luz direccional desde la esquina superior derecha frontal
        self.luz_posicion = [10.0, 10.0, 10.0, 1.0]
        
        # Configuración base de intensidad
        self.base_ambiental = [0.3, 0.3, 0.3, 1.0]
        self.base_difusa = [0.8, 0.8, 0.8, 1.0]
        
        # Estado actual (puede variar por el flash)
        self.luz_ambiental = list(self.base_ambiental)
        self.luz_difusa = list(self.base_difusa)
        self.luz_especular = [1.0, 1.0, 1.0, 1.0]
        
        # Variables para el efecto Flash
        self.flash_intensity = 0.0
        self.flash_decay = 2.0 # Más lento (0.5s) para que sea visible


    def trigger_flash(self):
        """Dispara un flash de luz blanca intensa."""
        self.flash_intensity = 1.0

    def update(self, dt):
        """Actualiza la intensidad del flash frame a frame."""
        if self.flash_intensity > 0:
            self.flash_intensity -= self.flash_decay * dt
            if self.flash_intensity < 0:
                self.flash_intensity = 0
            
            # Mezclamos el color base con blanco puro según la intensidad del flash
            # Ambiental: 0.3 -> 1.0
            # Difusa: 0.8 -> 1.0
            
            fi = self.flash_intensity
            self.luz_ambiental = [
                min(1.0, self.base_ambiental[0] + fi * 0.7),
                min(1.0, self.base_ambiental[1] + fi * 0.7),
                min(1.0, self.base_ambiental[2] + fi * 0.7),
                1.0
            ]
            self.luz_difusa = [
                min(1.0, self.base_difusa[0] + fi * 0.2),
                min(1.0, self.base_difusa[1] + fi * 0.2),
                min(1.0, self.base_difusa[2] + fi * 0.2),
                1.0
            ]
        else:
            # Restaurar valores base si no hay flash (optimización)
            self.luz_ambiental = list(self.base_ambiental)
            self.luz_difusa = list(self.base_difusa)

    def activar(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        glLightfv(GL_LIGHT0, GL_POSITION, self.luz_posicion)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.luz_ambiental)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.luz_difusa)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.luz_especular)
        
        # Configuración de material para que los colores de los objetos reaccionen a la luz
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Brillo especular
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
