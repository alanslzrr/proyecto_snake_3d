"""
Proyecto Snake 3D - configuracion.py

En este módulo concentramos toda la configuración global del proyecto: tamaños de ventana,
parámetros de proyección, constantes de tiempo, colores base y opciones de interacción.

La idea es mantener un único punto de verdad para estos valores, reutilizando la misma
filosofía que ya teníamos en `SHADER/configuracion.py` y añadiendo algunas constantes
específicas del juego (como el tamaño lógico del tablero).
"""

# ---------------------------------------------------------------------------
# Colores base
# ---------------------------------------------------------------------------

# Definición de colores en formato RGB normalizado (0.0 - 1.0)
COLOR_ROJO      = (1.0, 0.0, 0.0)
COLOR_VERDE     = (0.0, 1.0, 0.0)
COLOR_AZUL      = (0.0, 0.0, 1.0)
COLOR_AMARILLO  = (1.0, 1.0, 0.0)
COLOR_NARANJA   = (1.0, 0.5, 0.0)
COLOR_BLANCO    = (1.0, 1.0, 1.0)
COLOR_NEGRO     = (0.0, 0.0, 0.0)

# ---------------------------------------------------------------------------
# Ventana y proyección
# ---------------------------------------------------------------------------

# Tamaño de la ventana principal del juego
SCREEN_WIDTH        = 1280
SCREEN_HEIGHT       = 720
SCREEN_ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT

# Parámetros de la proyección en perspectiva
FOV        = 45     # Campo de visión vertical de la cámara (en grados)
NEAR_PLANE = 0.1    # Plano cercano de recorte
FAR_PLANE  = 50.0   # Plano lejano de recorte

# ---------------------------------------------------------------------------
# Bucle de juego
# ---------------------------------------------------------------------------

FPS                     = 60
MILLISECONDS_PER_SECOND = 1000.0

# ---------------------------------------------------------------------------
# Interacción con la cámara
# ---------------------------------------------------------------------------

BOTON_IZQUIERDO_RATON = 1      # ID del botón izquierdo del ratón en Pygame
SENSIBILIDAD_ROTACION = 0.2    # Sensibilidad de rotación con el ratón
SENSIBILIDAD_ZOOM     = 0.3    # Sensibilidad de zoom con la rueda del ratón
RADIO_MAX             = 15.0   # Distancia máxima de la cámara al origen
RADIO_MIN             = 1.0    # Distancia mínima de la cámara al origen
INVERTIR_CONTROLES    = -1     # 1 o -1 según prefiramos invertir el sentido
VELOCIDAD_ROTACION    = 135.0  # Grados por segundo al rotar con el teclado
VELOCIDAD_ZOOM        = 10.0   # Unidades por segundo al hacer zoom con el teclado

# ---------------------------------------------------------------------------
# Ejes y rejilla auxiliar
# ---------------------------------------------------------------------------

LONGITUD_EJE         = 4                 # Longitud de cada eje
EJE_X_MIN            = -LONGITUD_EJE
EJE_X_MAX            = LONGITUD_EJE
EJE_Y_MIN            = -LONGITUD_EJE
EJE_Y_MAX            = LONGITUD_EJE
EJE_Z_MIN            = -LONGITUD_EJE
EJE_Z_MAX            = LONGITUD_EJE
COLOR_EJE_X          = COLOR_ROJO
COLOR_EJE_Y          = COLOR_VERDE
COLOR_EJE_Z          = COLOR_AZUL
EJE_FLECHA_BASE      = 0.1
EJE_FLECHA_PUNTA     = 0.0
EJE_FLECHA_LONGITUD  = 0.3
EJE_FLECHA_REBANADAS = 10
EJE_FLECHA_PILAS     = 10

REJILLA_COLOR  = COLOR_BLANCO
REJILLA_TAMANO = 3      # Se dibujan líneas desde -N hasta N en X y Z
REJILLA_PASO   = 1.0    # Distancia entre líneas de la rejilla

# ---------------------------------------------------------------------------
# Parámetros lógicos del juego Snake (tablero y serpiente)
# ---------------------------------------------------------------------------

# Dimensiones lógicas del tablero (celdas). Estos valores se usarán más adelante
# cuando implementemos `tablero.py` y la lógica de posicionamiento de la serpiente.
TABLERO_ANCHO  = 10
TABLERO_LARGO  = 10
TABLERO_ALTO   = 1      # De momento trabajamos en un plano XZ con una altura fija

# Tamaño de cada celda en unidades del mundo 3D
TAMANO_CELDA = 1.0


# ---------------------------------------------------------------------------
# Apariencia del tablero 3D
# ---------------------------------------------------------------------------

# Colores del tablero. Usamos un patrón sencillo de dos tonos para que se
# distingan bien las celdas, y un color de borde para delimitar el área jugable.
COLOR_TABLERO_BASE  = (0.15, 0.15, 0.15)
COLOR_TABLERO_ALT   = (0.20, 0.20, 0.20)
COLOR_TABLERO_BORDE = (1.0, 1.0, 1.0)


# ---------------------------------------------------------------------------
# Apariencia de la serpiente
# ---------------------------------------------------------------------------

# Colores de los segmentos de la serpiente. De momento sólo necesitamos dos:
# uno para la "cabeza" y otro para el resto del cuerpo. Más adelante podremos
# afinar estos valores o incluso hacerlos configurables.
COLOR_SERPIENTE_CABEZA = (0.0, 0.9, 0.4)
COLOR_SERPIENTE_CUERPO = (0.0, 0.6, 0.25)


