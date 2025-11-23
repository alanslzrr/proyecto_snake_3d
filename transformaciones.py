"""
Proyecto Snake 3D - transformaciones.py

En este módulo agrupamos funciones auxiliares para aplicar transformaciones
geométricas en el espacio 3D utilizando la pila de matrices de OpenGL.

Nuestro objetivo es encapsular el patrón clásico:

- Traslación al punto deseado.
- Rotación opcional alrededor de los ejes X, Y y Z.
- Escalado independiente en cada eje.

De este modo, los módulos que dibujan geometría (tablero, segmentos de la
serpiente, etc.) pueden delegar en una única función el conjunto completo de
transformaciones sin duplicar llamadas a `glTranslatef`, `glRotatef` y
`glScalef`, manteniendo el código más legible y coherente.
"""

from OpenGL.GL import (
    glTranslatef,
    glRotatef,
    glScalef,
    glPushMatrix,
    glPopMatrix,
)

def transformar(
    t_x: float, t_y: float, t_z: float,
    ang_x: float = 0.0, ang_y: float = 0.0, ang_z: float = 0.0,
    s_x: float = 1.0, s_y: float = 1.0, s_z: float = 1.0,
    objeto_dibujado = None
) -> None:
    """
    Aplica una secuencia completa de transformaciones a la pila de matrices
    actual: traslación → rotación (opcional) → escalado.

    Args:
        t_x, t_y, t_z:
            Traslación en cada eje antes de aplicar cualquier otra
            transformación.
        ang_x, ang_y, ang_z:
            Ángulos de rotación (en grados) alrededor de los ejes X, Y y Z. Si
            un ángulo es 0.0, omitimos la rotación correspondiente.
        s_x, s_y, s_z:
            Factores de escalado en cada eje.
        objeto_dibujado:
            Función sin argumentos que se encarga de emitir la geometría con
            llamadas a OpenGL (por ejemplo, un cubo unitario centrado en el
            origen).

    Encapsulamos la lógica de `glPushMatrix`/`glPopMatrix` para garantizar que
    las transformaciones aplicadas a un objeto no afecten al resto de la
    escena.
    """
    glPushMatrix()
    
    glTranslatef(t_x, t_y, t_z)
    
    if ang_x != 0: glRotatef(ang_x, 1, 0, 0)
    if ang_y != 0: glRotatef(ang_y, 0, 1, 0)
    if ang_z != 0: glRotatef(ang_z, 0, 0, 1)
    
    glScalef(s_x, s_y, s_z)
    
    if objeto_dibujado:
        objeto_dibujado()
        
    glPopMatrix()
