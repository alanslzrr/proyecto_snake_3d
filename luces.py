"""
Proyecto Snake 3D - luces.py

Seguimos el mismo enfoque que en `SHADER/luces.py`: una pequeña clase que
se encarga de enviar los parámetros de iluminación al programa de shaders.
"""

from OpenGL.GL import (
    glUseProgram,
    glGetUniformLocation,
    glUniform3f,
    glUniform1f,
)


class Iluminacion:
    """
    Representamos una única fuente de luz con componentes ambiente, difusa,
    especular y un exponente de brillo para los reflejos especulares.
    """

    def __init__(self) -> None:
        # Valores iniciales de la luz, heredados del proyecto de referencia.
        self.light_ambient = (0.1, 0.1, 0.1)
        self.light_diffuse = (0.8, 0.8, 0.8)
        self.light_specular = (0.5, 0.5, 0.5)
        self.light_shininess = 32.0

    def aplicar(self, shader_program: int, light_pos: tuple[float, float, float], view_pos: tuple[float, float, float]) -> None:
        """
        Enviamos los parámetros de la luz al programa de shaders.

        Args:
            shader_program: ID del programa de shaders activo.
            light_pos: posición de la luz en el mundo.
            view_pos: posición de la cámara, necesaria para el cálculo especular.
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


