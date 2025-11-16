"""
Proyecto Snake 3D - transformaciones.py

Aquí agrupamos funciones auxiliares para aplicar traslaciones, rotaciones y escalados
en el espacio 3D. La implementación parte directamente de `SHADER/transformaciones.py`,
que ya nos resolvía muy bien esta parte del trabajo.
"""

from OpenGL.GL import (
    glTranslatef,
    glRotatef,
    glScalef,
    glPushMatrix,
    glPopMatrix,
)


def trasladar(x: float, y: float, z: float) -> None:
    """Aplicamos una traslación sencilla en el espacio 3D."""
    glTranslatef(x, y, z)


def rotar(angulo: float, x: float, y: float, z: float) -> None:
    """Rotamos alrededor del eje definido por (x, y, z)."""
    glRotatef(angulo, x, y, z)


def escalar(sx: float, sy: float, sz: float) -> None:
    """Escalamos un objeto de forma independiente en cada eje."""
    glScalef(sx, sy, sz)


def transformar(
    t_x: float,
    t_y: float,
    t_z: float,
    angulo: float,
    eje_x: float,
    eje_y: float,
    eje_z: float,
    sx: float,
    sy: float,
    sz: float,
    objeto,
) -> None:
    """
    Encapsulamos el patrón clásico de transformación:
    1. Trasladar
    2. Rotar
    3. Escalar

    `objeto` debe ser una función que se encargue de dibujar con OpenGL.
    """
    glPushMatrix()

    trasladar(t_x, t_y, t_z)
    rotar(angulo, eje_x, eje_y, eje_z)
    escalar(sx, sy, sz)

    objeto()

    glPopMatrix()


