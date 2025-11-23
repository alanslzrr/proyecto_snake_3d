"""
Proyecto Snake 3D - utilidades.py

En este módulo agrupamos funciones de apoyo visual que nos ayudan a entender la
escena 3D mientras desarrollamos y depuramos el juego: ejes de coordenadas y
rejilla sobre el plano XZ.

La idea es muy similar a la de `SHADER/utilidades.py`: disponer de elementos
geométricos simples que nos permitan:

- Verificar rápidamente la orientación de la escena.
- Localizar el origen y los rangos de los ejes.
- Superponer una rejilla de referencia cuando sea útil comparar con el mundo
  cúbico de vóxeles.

Aun cuando en la versión de “Cubo Planetario” la referencia principal pasa a
ser el propio tablero volumétrico, estas utilidades siguen siendo valiosas
durante el desarrollo para contrastar transformaciones y ángulos de cámara.
"""

from OpenGL.GL import (
    glBegin,
    glEnd,
    glColor3f,
    glVertex3f,
    GL_LINES,
)
from OpenGL.GLU import (
    gluNewQuadric,
    gluCylinder,
)

from configuracion import (
    EJE_X_MIN,
    EJE_X_MAX,
    EJE_Y_MIN,
    EJE_Y_MAX,
    EJE_Z_MIN,
    EJE_Z_MAX,
    COLOR_EJE_X,
    COLOR_EJE_Y,
    COLOR_EJE_Z,
    EJE_FLECHA_BASE,
    EJE_FLECHA_PUNTA,
    EJE_FLECHA_LONGITUD,
    EJE_FLECHA_REBANADAS,
    EJE_FLECHA_PILAS,
    REJILLA_COLOR,
    REJILLA_TAMANO,
    REJILLA_PASO,
)


def dibujar_elementos_auxiliares(ejes: bool = False, rejilla: bool = False) -> None:
    """
    Dibuja ejes y/o rejilla según las opciones indicadas.

    Durante las primeras fases del proyecto, y en particular mientras iteramos
    la configuración de cámara y transformaciones globales, estos elementos nos
    sirven para comprobar que el origen está donde esperamos y que no se
    producen inversiones de ejes no deseadas.
    """
    if ejes:
        dibujar_ejes()
    if rejilla:
        dibujar_rejilla()


def dibujar_ejes() -> None:
    """
    Dibuja los tres ejes principales X, Y y Z con sus respectivas flechas en el
    extremo positivo.
    """
    dibujar_eje_con_flecha(EJE_X_MIN, 0, 0, EJE_X_MAX, 0, 0, COLOR_EJE_X, rotacion=(90, 0, 1, 0))
    dibujar_eje_con_flecha(0, EJE_Y_MIN, 0, 0, EJE_Y_MAX, 0, COLOR_EJE_Y, rotacion=(-90, 1, 0, 0))
    dibujar_eje_con_flecha(0, 0, EJE_Z_MIN, 0, 0, EJE_Z_MAX, COLOR_EJE_Z)


def dibujar_eje_con_flecha(
    x1: float,
    y1: float,
    z1: float,
    x2: float,
    y2: float,
    z2: float,
    color: tuple[float, float, float],
    rotacion: tuple[float, float, float, float] | None = None,
) -> None:
    """
    Dibuja un eje como segmento entre dos puntos y añade una pequeña flecha en
    el extremo positivo para indicar la dirección.
    """
    dibujar_segmento(x1, y1, z1, x2, y2, z2, color)
    glColor3f(*color)
    # Posicionamos la flecha en el extremo
    from OpenGL.GL import glPushMatrix, glPopMatrix, glTranslatef, glRotatef  # import local para no contaminar arriba

    glPushMatrix()
    glTranslatef(x2, y2, z2)
    if rotacion:
        glRotatef(*rotacion)
    dibujar_cono()
    glPopMatrix()


def dibujar_segmento(
    x1: float,
    y1: float,
    z1: float,
    x2: float,
    y2: float,
    z2: float,
    color: tuple[float, float, float],
) -> None:
    """Dibuja un segmento sencillo entre dos puntos en el espacio 3D."""
    glBegin(GL_LINES)
    glColor3f(*color)
    glVertex3f(x1, y1, z1)
    glVertex3f(x2, y2, z2)
    glEnd()


def dibujar_cono() -> None:
    """
    Dibuja un cono muy simple que utilizamos como punta de flecha para los
    ejes de referencia.
    """
    cone = gluNewQuadric()
    gluCylinder(
        cone,
        EJE_FLECHA_BASE,
        EJE_FLECHA_PUNTA,
        EJE_FLECHA_LONGITUD,
        EJE_FLECHA_REBANADAS,
        EJE_FLECHA_PILAS,
    )


def dibujar_rejilla() -> None:
    """
    Dibuja una rejilla en el plano XZ.

    Esta rejilla nos sirve como referencia visual del “suelo” y es
    especialmente útil para contrastar posiciones relativas cuando combinamos
    el mundo plano de depuración con el mundo cúbico volumétrico.
    """
    glColor3f(*REJILLA_COLOR)
    glBegin(GL_LINES)
    for i in range(-REJILLA_TAMANO, REJILLA_TAMANO + 1):
        # Líneas paralelas al eje X
        dibujar_linea(-REJILLA_TAMANO, 0, i, REJILLA_TAMANO, 0, i)
        # Líneas paralelas al eje Z
        dibujar_linea(i, 0, -REJILLA_TAMANO, i, 0, REJILLA_TAMANO)
    glEnd()


def dibujar_linea(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> None:
    """
    Dibuja una línea en el plano XZ escalada por el paso de la rejilla, a
    partir de dos puntos expresados en coordenadas discretas de la rejilla.
    """
    glVertex3f(x1 * REJILLA_PASO, y1, z1 * REJILLA_PASO)
    glVertex3f(x2 * REJILLA_PASO, y2, z2 * REJILLA_PASO)



