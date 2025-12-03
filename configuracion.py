"""
Proyecto Snake 3D: Vóxel Planetario - configuracion.py

Este módulo es el "panel de control" de todo el proyecto. Aquí centralizamos
todas las constantes y parámetros que definen el comportamiento visual,
geométrico y de control del juego.

La filosofía es simple: cualquier valor que pueda necesitar ajuste durante
el desarrollo o para personalizar la experiencia de juego debe estar aquí,
en un único lugar. Esto nos permite:

- Ajustar rápidamente el tamaño del cubo, los colores o la velocidad.
- Mantener coherencia entre todos los módulos que usan estos valores.
- Documentar claramente qué significa cada parámetro.

Organizamos la configuración en secciones temáticas:
1. Paleta de colores (incluyendo canal alpha para transparencias).
2. Dimensiones del mundo cúbico y tamaño de cada celda.
3. Configuración de la ventana y proyección.
4. Parámetros de control y velocidad.
5. Configuración de las diferentes cámaras.
"""

# ---------------------------------------------------------------------------
# Colores base (R, G, B, A) - Añadimos Alpha para transparencias
# ---------------------------------------------------------------------------

# Cubos vacíos del interior del mundo cúbico
# (tono azulado translúcido para reforzar la estética de “cubo de cristal”).
# Relleno: Casi inexistente. Solo una pequeñísima sugerencia de materia azulada.
COLOR_CUBO_VACIO = (0.0, 0.1, 0.3, 0.015)

# Borde: Azul eléctrico vibrante.
# Mantenemos tu color azul base pero aumentamos el Alpha para que defina mucho más la forma.
COLOR_BORDE_VACIO = (0.3, 0.3, 1.0, 0.4)

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
# Dimensiones del cubo grande (N x N x N).
# Aumentamos a 15 para dar más espacio de juego (Fase 9).
GRID_SIZE = 15

# Tamaño visual (en unidades de mundo) de cada minicubo (celda).
TAMANO_CELDA = 1.0

# Espacio entre celdas (pequeña separación para efecto rejilla si lo activamos).
# Fase 11: Aumentamos el espacio para separar los vóxeles.
ESPACIO_CELDA = 0.2

# Desplazamiento necesario para centrar el cubo grande en el origen (0, 0, 0).
# Calculamos el ancho total: N celdas + (N-1) espacios.
ANCHO_TOTAL = (GRID_SIZE * TAMANO_CELDA) + ((GRID_SIZE - 1) * ESPACIO_CELDA)
OFFSET_GRID = ANCHO_TOTAL / 2.0

# ---------------------------------------------------------------------------
# Ventana y proyección en perspectiva
# ---------------------------------------------------------------------------

# Ampliamos la resolución para una mejor experiencia (Fase 9 -> Fase 10 Ajuste).
SCREEN_WIDTH        = 1280
SCREEN_HEIGHT       = 960
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
# Puntuación (Fase 9)
PUNTOS_POR_COMIDA = 8

# Velocidad de rotación global del mundo (en grados/segundo) al responder
# a las teclas de dirección. Ajustando este valor controlamos la suavidad
# y rapidez con la que el cubo planetario reacciona al input del usuario.
VELOCIDAD_ROTACION_MUNDO = 90.0

# --- FASE 4: Configuración de Movimiento de la Serpiente ---
#
# Tiempo entre pasos de la serpiente (en segundos).
# 0.15 = 150ms. Cuanto menor sea el número, más rápida es la serpiente.
TIEMPO_PASO = 0.15

# --- FASE 5: Configuración de Rotación Automática ---
#
# Tiempo (en segundos) que tarda el mundo en completar una rotación de 90º
# cuando la serpiente atraviesa el borde de una cara y debemos "reorientar"
# la escena para seguir con la ilusión del “frente infinito”.
TIEMPO_ROTACION_AUTO = 0.4

# Vectores de Dirección (x, y, z)
# Nota: En la cara frontal (Z positiva), 'Arriba' es +Y, 'Derecha' es +X.
DIR_UP    = (0, 1, 0)
DIR_DOWN  = (0, -1, 0)
DIR_LEFT  = (-1, 0, 0)
DIR_RIGHT = (1, 0, 0)
DIR_STOP  = (0, 0, 0)  # Estado inicial o de pausa

# --- FASE 10: Configuración de Cámaras (Ajuste de Proximidad) ---
#
# Definimos los multiplicadores de distancia para las distintas cámaras.
# La distancia base se calcula como GRID_SIZE * 2.5
#
# Cámara 1 (Default): Isométrica (Diagonal)
# Ajustada para estar más cerca y ver los detalles del vóxel.
CAMARA_1_POS = (0.85, 0.7, 0.85) # (x, y, z) multiplicadores

# Cámara 2: Frontal Inclinada
# De frente (X=0), elevada ligeramente y mucho más cerca en Z
# para una experiencia inmersiva "casi dentro" del cubo.
CAMARA_2_POS = (0.0, 0.4, 0.9)

# Cámara 3: Tercera Persona (Seguimiento)
# Offset relativo a la cabeza de la serpiente.
# (0, 0, 12) significa 12 unidades "atrás" (en Z) de la cabeza.
CAMARA_3_OFFSET = (0.0, 0.0, 12.0)

# Cámara 4: Primera Persona (Snake View)
# "Encima de la cabeza" (Offset en Z, la normal)
# "Mirando al frente" (Usaremos el vector de dirección de la serpiente)
CAMARA_4_ALTURA = 1.5 # Altura sobre la cabeza (eje Z local)
CAMARA_4_DISTANCIA_MIRA = 5.0 # Qué tan lejos mira hacia adelante