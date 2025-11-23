# Computación Gráfica

**Proyecto de la Asignatura - Avance de Proyecto**

# Juego Snake 3D: Versión Vóxel Planetario

## Grupo 3

### Integrantes:

1. Yago Ramos Sánchez
2. Alan Ariel Salazar
3. Mario Tuset Gende
4. Miguel Ángel Lorenzo Fossati
5. Yésica Ramírez Bernal

---

## 1. Título

**Juego Snake 3D: Simulación Interactiva en Espacio Cúbico Rotacional**

Tras una revisión profunda de la propuesta y buscando un mayor desafío técnico y visual, hemos evolucionado nuestro título y enfoque. Pasamos de un tablero plano tradicional a una propuesta de **"Mundo Cúbico" (estilo Vóxel)**. En esta simulación, la serpiente se desplaza por las caras de un cubo tridimensional que rota sobre su propio eje, creando una mecánica de juego donde el entorno gira para adaptarse a la posición del jugador, en lugar de mover una cámara alrededor de un plano estático.

---

## 2. Resumen

Durante la fase inicial del proyecto, evaluamos las herramientas disponibles y comenzamos con un enfoque clásico de Snake sobre un plano. Sin embargo, al analizar referentes visuales más modernos y mecánicas de juego más inmersivas (inspirados en conceptos de "gravedad local" o juegos particulares como *Snake 3D Cube*), decidimos pivotar el desarrollo hacia un sistema de **renderizado volumétrico**.

En este nuevo enfoque, el tablero no es una superficie plana, sino un volumen de $N \times N \times N$ celdas (vóxeles). Esto nos ha llevado a replantear la arquitectura gráfica:
1.  **Visualización**: Pasamos de dibujar un simple `GL_QUAD` a renderizar una estructura de múltiples cubos semitransparentes que dan volumen a la escena.
2.  **Cámara y Transformaciones**: En lugar de orbitar la cámara alrededor de la escena, hemos fijado la cámara (como primer objetivo, luego plantearemos hacer nuevas funciones para que la cámara pueda moverse hacia primera persona) y aplicamos transformaciones de rotación global a todo el "mundo" basándonos en el input del usuario.
3.  **Pipeline**: Seguimos utilizando el pipeline moderno con OpenGL y Python, pero ahora gestionando la profundidad y la transparencia (Alpha Blending) para lograr un efecto de "cubo de cristal".

Este documento detalla cómo hemos adaptado nuestra base de código inicial para soportar este nuevo paradigma y los avances logrados hasta la Fase 3.

---

## 3. Objetivos

### Objetivo General

Desarrollar un videojuego Snake 3D "planetario" donde la serpiente se mueve sobre la superficie de un cubo gigante rotatorio. El objetivo es dominar las transformaciones geométricas compuestas (rotación del mundo + traslación local) y el manejo de estructuras de datos tridimensionales.

### Objetivos Específicos (Actualizados)

1.  **Renderizado Volumétrico (Vóxel)**: Implementar un sistema que dibuje un cubo formado por pequeñas celdas cúbicas, gestionando correctamente la transparencia para ver el interior de la estructura.
2.  **Sistema de Coordenadas 3D**: Migrar de un sistema 2D lógico `(x, z)` a un sistema completamente 3D `(x, y, z)` que permita ubicar segmentos en cualquiera de las 6 caras del cubo.
3.  **Transformación Global del Mundo**: Implementar una lógica de control donde las teclas de dirección no mueven "la cámara", sino que rotan la matriz del modelo completo (el mundo gira ante los ojos del jugador).
4.  **Gestión de Transparencias**: Utilizar *Alpha Blending* en OpenGL para lograr estética de cristal/vidrio en los cubos vacíos.
5.  **Lógica de Movimiento en Superficie**: Desarrollar (en fases futuras) el algoritmo que permita a la serpiente transitar de una cara a otra, rotando el cubo 90 grados suavemente al cruzar un borde.

---

## 4. Metodología

### Reestructuración del Enfoque

Nuestro cambio de diseño implicó una refactorización de los componentes que ya teníamos. Mantenemos la modularidad, pero cambiamos la responsabilidad de las clases principales:

* **`main.py`**: Ahora gestiona la **Matriz de Rotación Global**. Es el encargado de escuchar las flechas del teclado y aplicar `glRotate` a toda la escena antes de dibujar nada.
* **`tablero.py`**: Ya no es un plano. Ahora es un bucle tridimensional que dibuja cubos en las posiciones $(x, y, z)$ usando materiales translúcidos.
* **`snake.py`**: La serpiente se inicializa ahora en una de las caras del cubo (por ejemplo, la cara frontal Z), y sus segmentos tienen coordenadas espaciales completas.

### Tecnologías 

Mantenemos **Python 3**, **Pygame** y **PyOpenGL**. Sin embargo, hemos añadido el uso intensivo de:
* **`glBlendFunc`**: Para manejar las transparencias de los cubos inactivos.
* **`glPushMatrix` / `glPopMatrix`**: Esencial ahora que dibujamos cientos de pequeños cubos; necesitamos aislar la transformación de cada uno para que no afecte al siguiente.

---

## 5. Desarrollo y Avances del Proyecto

Debido al cambio de enfoque, hemos reescrito gran parte de la lógica de las fases 2 y 3. A continuación, documentamos el estado actual del proyecto tras esta refactorización.

### Fase 0: Estructura y Configuración (Mantenido)

Conservamos la estructura de archivos modular (`main.py`, `configuracion.py`, `transformaciones.py`, etc.). Sin embargo, hemos actualizado `configuracion.py` para definir las propiedades del nuevo "Mundo Cúbico":
* Definimos `GRID_SIZE` (tamaño del cubo, ej. 10x10x10).
* Añadimos colores con canal Alpha (RGBA) para soportar transparencias (`COLOR_CUBO_VACIO`).
* Ajustamos el FOV de la cámara para abarcar el volumen completo del cubo desde una perspectiva isométrica.

### Fase 1: Ventana y Renderizado Base (Adaptado)

En esta fase, validamos que podíamos abrir la ventana OpenGL y configurar el contexto para transparencias.
* Activamos `GL_BLEND` para permitir que los objetos se vean a través de otros.
* Cambiamos la posición de la cámara: ahora está **fija** en una posición diagonal, mirando hacia el centro del mundo $(0,0,0)$. Ya no usamos la cámara orbital con el ratón de la versión anterior, ya que el control pasará a ser la rotación del cubo con el teclado.

### Fase 2: El "Mundo de Cristal" (Refactorización Completa)

Aquí es donde el proyecto cambió radicalmente. Abandonamos la rejilla plana y construimos el **Tablero Volumétrico**.

* **Implementación**: La clase `Tablero` ahora itera en tres dimensiones ($x, y, z$).
* **Visualización**: Para cada posición de la rejilla, dibujamos un cubo unitario.
    * Si la celda está vacía, se dibuja con un color azulado y un valor Alpha bajo (0.15), creando un efecto de "fantasma" o cristal.
    * Dibujamos también las aristas (wireframe) de cada celda para que la cuadrícula 3D sea legible visualmente.
* **Resultado**: Al ejecutar esta fase, obtenemos un cubo gigante flotando en el espacio, con una estructura interna visible que da una gran sensación de profundidad.

 
### Fase 3: La Serpiente en el Vóxel (Completada)

Una vez tuvimos el cubo volumétrico, necesitábamos colocar a la serpiente sobre él.

* **Coordenadas 3D**: Actualizamos la clase `Segmento` para almacenar $(x, y, z)$. Antes solo guardaba $(x, z)$.
* **Inicialización**: Programamos la lógica para que la serpiente aparezca inicialmente en la **cara frontal** del cubo (la cara con Z positivo máximo).
* **Interacción Básica**: Implementamos en el `main.py` la lógica para que, al presionar las flechas del teclado, se modifiquen las variables de rotación global del mundo (`rot_x`, `rot_y`).

**Estado Actual**: Tenemos un sistema funcional donde vemos el cubo de cristal translúcido y una serpiente verde adherida a su superficie. Podemos usar las flechas del teclado para rotar el cubo completo y examinar la serpiente desde cualquier ángulo, validando que las transformaciones jerárquicas funcionan correctamente.

![Fase 3 - Tablero 3D](FasesCompletadas/Hasta_Fase3.gif)

Con este gid del estado actual, podemos validar que hemos alcanzado el hito de la **Fase 3**.

Hasta este punto logramos renderizar la estructura volumétrica del mundo (el "cubo de cristal") utilizando  el *Alpha Blending* para las transparencias, lo que nos permite visualizar la profundidad interna del tablero sin perder la definición de la forma cúbica, en ciertos angulos la transparencia se nos va pero lo puliremos cuando hagamos que la serpiente se mueva junto con el cubo.  

Por el momento, la serpiente se posiciona correctamente sobre la superficie (en este caso, en la cara frontal) y hemos comprobado que la lógica de **rotación global del mundo** funciona de manera fluida y estable. Al interactuar con las flechas del teclado, el cubo gira suavemente respondiendo al input sin presentar vibraciones (*jitter*) ni caídas de rendimiento, lo que confirma que nuestra gestión de la pila de matrices (`glPushMatrix`/`glPopMatrix`) está funcionando muy bien.

---

## 6. Próximos Pasos

Dado que hemos cambiado la mecánica base, hemos redefinido las siguientes fases para lograr el objetivo del "Snake Planetario".

### Fase 4: Movimiento "Crawler"
El próximo desafío es hacer que la serpiente se mueva automáticamente.
* Implementar vectores de dirección 3D.
* Detectar cuando la serpiente llega a un borde del cubo ($x > limite$, etc.).

### Fase 5: Transición de Caras y Rotación Automática
Esta será la fase más compleja y visualmente impactante.
* Implementar la lógica: *"Si la serpiente cruza el borde derecho, el mundo debe rotar 90 grados hacia la izquierda"*.
* Suavizar esta rotación para que no sea instantánea, sino una animación fluida que reoriente la nueva cara hacia el frente de la cámara.

### Fase 6: Comida y Crecimiento 3D
* Generar comida (cubos rojos) aleatoriamente, pero asegurando que aparezcan solo en las **caras superficiales** del cubo grande, nunca en el interior hueco.

### Fase 7: Pulido Visual
* Añadir efectos de iluminación para resaltar los bordes.
* Ajustar los colores y la opacidad para mejorar la jugabilidad.

---

## 7. Bibliografía Preliminar

*[Esta sección se completará con las referencias bibliográficas consultadas durante el desarrollo del proyecto, en formato APA 7. Incluirá libros, artículos, documentación oficial, tutoriales y cualquier otra fuente utilizada.]*

---

**Última actualización**: 23 de Noviembre