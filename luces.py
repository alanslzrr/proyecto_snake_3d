"""
Proyecto Snake 3D - luces.py

En este módulo encapsulamos la configuración de iluminación que enviamos a los
shaders del pipeline moderno de OpenGL.

Reutilizamos y adaptamos el enfoque del proyecto de referencia `SHADER`,
manteniendo una interfaz sencilla que agrupa los parámetros de luz más
relevantes (componente ambiente, difusa, especular y brillo) y los expone en
forma de una única clase lista para ser usada por el resto del proyecto.

Aunque en la versión actual del Snake planetario todavía no explotamos todos
los efectos de iluminación posibles, dejamos esta infraestructura preparada para
realzar, en fases posteriores, el volumen del cubo de vóxeles y la presencia de
la serpiente sobre su superficie.
"""

from OpenGL.GL import (
    glUseProgram,
    glGetUniformLocation,
    glUniform3f,
    glUniform1f,
)


class Iluminacion:
    """
    Representa una única fuente de luz puntual con componentes ambiente,
    difusa y especular, además de un exponente de brillo para controlar la
    intensidad de los reflejos especulares en los shaders.

    Centralizar estos parámetros en una clase nos permite ajustar de forma
    coherente la atmósfera visual de la escena (cubo, serpiente y elementos
    auxiliares) sin dispersar configuraciones por el código.
    """

    def __init__(self) -> None:
        # Valores iniciales de la luz, heredados del proyecto de referencia.
        self.light_ambient = (0.1, 0.1, 0.1)
        self.light_diffuse = (0.8, 0.8, 0.8)
        self.light_specular = (0.5, 0.5, 0.5)
        self.light_shininess = 32.0

    def aplicar(self, shader_program: int, light_pos: tuple[float, float, float], view_pos: tuple[float, float, float]) -> None:
        """
        Envía los parámetros de la luz al programa de shaders activo.

        Args:
            shader_program:
                ID del programa de shaders sobre el que vamos a aplicar la
                configuración de iluminación.
            light_pos:
                Posición de la luz en coordenadas de mundo, utilizada por el
                shader para calcular direcciones de iluminación.
            view_pos:
                Posición de la cámara en el mundo, necesaria para calcular el
                componente especular en el modelo de iluminación.
        """
        glUseProgram(shader_program)

        loc_pos = glGetUniformLocation(shader_program, "lightPos")
        loc_view = glGetUniformLocation(shader_program, "viewPos")
        loc_amb = glGetUniformLocation(shader_program, "lightAmbient")
        loc_diff = glGetUniformLocation(shader_program, "lightDiffuse")
        loc_spec = glGetUniformLocation(shader_program, "lightSpecular")
        loc_shin = glGetUniformLocation(shader_program, "lightShininess")

        glUniform3f(loc_pos, *light_pos)
        glUniform3f(loc_view, *view_pos)
        glUniform3f(loc_amb, *self.light_ambient)
        glUniform3f(loc_diff, *self.light_diffuse)
        glUniform3f(loc_spec, *self.light_specular)
        glUniform1f(loc_shin, self.light_shininess)

        glUseProgram(0)


