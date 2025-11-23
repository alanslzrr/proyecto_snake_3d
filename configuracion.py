"""
Proyecto Snake 3D - configuracion.py

En este módulo concentramos toda la configuración global del proyecto, actuando
como punto único de verdad para constantes visuales, geométricas y de control.

Hemos adaptado estas constantes a la nueva versión del juego basada en un
“Cubo Planetario” de estilo vóxel, en el que la serpiente se desplaza sobre la
superficie de un cubo gigante que rota en bloque. Desde aquí parametrizamos:

- La paleta de colores (incluyendo canal alpha para transparencias).
- Las dimensiones discretas del mundo cúbico y el tamaño de cada celda.
- El sistema de proyección y la ventana de renderizado.
- La frecuencia objetivo de actualización y la velocidad de rotación global
  del mundo.

Este diseño centralizado nos permite ajustar el comportamiento visual y
geométrico del juego de forma coherente en todos los módulos.
"""

# ---------------------------------------------------------------------------
# Colores base (R, G, B, A) - Añadimos Alpha para transparencias
# ---------------------------------------------------------------------------

# Cubos vacíos del interior del mundo cúbico
# (tono azulado translúcido para reforzar la estética de “cubo de cristal”).
COLOR_CUBO_VACIO = (0.2, 0.2, 0.5, 0.15)

# Borde de los cubos vacíos
# (azul algo más intenso para que la rejilla interna sea legible).
COLOR_BORDE_VACIO = (0.3, 0.3, 0.7, 0.3)

# Colores sólidos para entidades jugables y de entorno.
# Usamos RGBA normalizado en el rango [0.0, 1.0].
COLOR_SERPIENTE_CABEZA = (0.0, 1.0, 0.0, 1.0)   # Verde brillante para la cabeza
COLOR_SERPIENTE_CUERPO = (0.0, 0.8, 0.0, 1.0)   # Verde ligeramente más oscuro
COLOR_COMIDA           = (1.0, 0.0, 0.0, 1.0)   # Rojo intenso para resaltar la comida
COLOR_FONDO            = (0.05, 0.05, 0.05, 1.0)  # Fondo casi negro para centrar la atención en el cubo

# ---------------------------------------------------------------------------
# Parámetros del Mundo Cúbico
# ---------------------------------------------------------------------------

# Dimensiones del cubo grande (N x N x N).
# Por ejemplo, si es 10, obtenemos un volumen de 10×10×10 celdas discretas.
GRID_SIZE = 10

# Tamaño visual (en unidades de mundo) de cada minicubo (celda).
TAMANO_CELDA = 1.0

# Espacio entre celdas (pequeña separación para efecto rejilla si lo activamos).
ESPACIO_CELDA = 0.0

# Desplazamiento necesario para centrar el cubo grande en el origen (0, 0, 0).
OFFSET_GRID = (GRID_SIZE * TAMANO_CELDA) / 2.0

# ---------------------------------------------------------------------------
# Ventana y proyección en perspectiva
# ---------------------------------------------------------------------------

SCREEN_WIDTH        = 800
SCREEN_HEIGHT       = 600
SCREEN_ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT

# Campo de visión vertical de la cámara (en grados).
# Un valor ligeramente angular nos permite abarcar bien el volumen del cubo.
FOV        = 60
NEAR_PLANE = 0.1
FAR_PLANE  = 100.0

# ---------------------------------------------------------------------------
# Control y velocidad de actualización
# ---------------------------------------------------------------------------

FPS = 60

# Velocidad de rotación global del mundo (en grados/segundo) al responder
# a las teclas de dirección. Ajustando este valor controlamos la suavidad
# y rapidez con la que el cubo planetario reacciona al input del usuario.
VELOCIDAD_ROTACION_MUNDO = 90.0

# --- FASE 4: Configuración de Movimiento de la Serpiente ---
#
# Tiempo entre pasos de la serpiente (en segundos).
# 0.15 = 150ms. Cuanto menor sea el número, más rápida es la serpiente.
TIEMPO_PASO = 0.15

# Vectores de Dirección (x, y, z)
# Nota: En la cara frontal (Z positiva), 'Arriba' es +Y, 'Derecha' es +X.
DIR_UP    = (0, 1, 0)
DIR_DOWN  = (0, -1, 0)
DIR_LEFT  = (-1, 0, 0)
DIR_RIGHT = (1, 0, 0)
DIR_STOP  = (0, 0, 0)  # Estado inicial o de pausa