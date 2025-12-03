# Computación Gráfica
## Informe Final – Snake 3D: Vóxel Planetario
**Grupo 3**

**Integrantes:**
* Yago Ramos Sánchez
* Alan Ariel Salazar
* Mario Tuset Gende
* Miguel Ángel Lorenzo Fossati
* Yésica Ramírez Bernal

---

## Participación del equipo

El responsable del equipo, ubicado en la primera fila, garantiza el cumplimiento de lo establecido en el contrato de enseñanza-aprendizaje.

| Nombre | Participación |
| :--- | :--- |
| **Yago Ramos Sánchez** | **SI** |
| Alan Ariel Salazar | SI |
| Mario Tuset Gende | SI |
| Miguel Ángel Lorenzo Fossati | SI |
| Yésica Ramírez Bernal | SI |

---

## 1. Resumen

"Snake 3D: Vóxel Planetario" reinterpreta el clásico Snake en un entorno cúbico semitransparente donde la serpiente recorre la superficie de un planeta hecho de vóxeles. Diseñamos un mundo que rota automáticamente 90° cada vez que la cabeza cruza un borde, manteniendo siempre una vista frontal coherente y evitando cámaras complejas. 

Trabajamos con PyOpenGL y Pygame, combinando diseño modular, matrices jerárquicas y renderizado híbrido (opaco + translúcido). Esto nos permitió separar la lógica discreta del tablero y la serpiente, sincronizar la rotación global con el movimiento local y garantizar la estabilidad visual del "cubo de cristal".

El resultado es un prototipo estable a 60 FPS gracias al uso de Display Lists, optimizaciones de transparencia y una arquitectura orientada a objetos que facilita la incorporación de cámaras múltiples, UI y mecánicas completas de crecimiento, colisiones y puntuación.

## 2. Introducción

El propósito de este proyecto es implantar de forma práctica los conceptos teóricos de representación, transformación y visualización de objetos en espacio 2D y 3D. Inicialmente, la idea era crear un generador interactivo de patrones y mandalas en 2D empleando transformaciones geométricas sencillas y primitivas básicas. Sin embargo, tras la retroalimentación del profesor y buscando un mayor desafío técnico, decidimos cambiar totalmente nuestra propuesta hacia algo más ambicioso: la implementación de un videojuego Snake en 3D con técnicas de navegación espacial sobre un cubo rotacional, que denominamos **Snake 3D: Vóxel Planetario**.

El juego clásico Snake, que surge en los años 70 y se populariza en dispositivos móviles a finales de la década de los 90, sirve como ejemplo ideal de aplicación interactiva en tiempo real para probar principios fundamentales de la programación gráfica. Su implementación tradicional en 2D restringe el desarrollo de técnicas avanzadas; por ello, en este proyecto lo llevamos más allá trasladando la mecánica a un ambiente cúbico tridimensional. Cuando la cabeza de la serpiente llega al borde del cubo, este gira automáticamente 90° conservando una visual frontal fija. Este enfoque elimina la necesidad de sistemas complejos de cámara seguidora y aun así genera la ilusión de un mundo cúbico sin límites.

Uno de los problemas principales fue garantizar que la serpiente se moviera de forma continua sobre las caras del cubo, manteniendo la consistencia visual y lógica durante las transiciones. Para ello, separamos la interacción del jugador en sistemas de coordenadas locales y globales: sobre la superficie local de la cara se realiza el movimiento de la serpiente, mientras que la lógica de transición genera rotaciones del cubo, requiriendo una gestión precisa de la pila de matrices de transformación (Modelo y Vista).

La relevancia de este proyecto radica en que combina prácticamente todos los bloques temáticos del curso en un caso de estudio interactivo y visualmente atractivo, sirviendo como puente entre la teoría y su aplicación práctica. El proyecto nos obligó a dominar transformaciones geométricas compuestas, gestionar la pila de matrices de OpenGL, manipular buffers, optimizar renderizados de alto conteo poligonal y coordinar lógica de juego con visualización. Todo ello en un escenario interactivo que expone errores de diseño en cuestión de segundos, lo que representa un laboratorio perfecto para los temas del curso.

## 3. Objetivos

### Objetivo general
Construir un videojuego Snake tridimensional que ocurra sobre la superficie de un cubo voxelizado, aplicando transformaciones globales para mantener la continuidad visual y lógica mientras se demuestra el dominio del pipeline gráfico de la asignatura.

### Objetivos específicos

1. **Mundo cúbico transparente:** Modelar un tablero formado por vóxeles translúcidos empleando el modelo de color RGBA estudiado en clase, con control preciso del *depth buffer* y del orden de renderizado para evitar errores visuales durante las rotaciones y transiciones.

2. **Serpiente 3D segmentada:** Representar la serpiente como una entidad segmentada con coordenadas 3D $(x, y, z)$ sobre la cara frontal del cubo. Incorporar movimiento discreto en las 6 caras, incluyendo verificación de movimientos, prevención de giros no válidos (180°), manejo del crecimiento gradual al recoger comida y detección de colisiones con el propio cuerpo.

3. **Rotación global suave:** Separar los controles de movimiento de la serpiente de la rotación del mundo, permitiendo inspección libre del entorno. Al pasar de una cara a otra, implementar rotaciones globales suaves de 90° mediante interpolación y transformación jerárquica sobre la matriz modelo-vista.

4. **Transición entre caras:** Diseñar el algoritmo que permita un paso suave de la serpiente entre caras del cubo, ajustando coordenadas y reorientando todos los segmentos de manera automática cuando la cabeza cruza un borde.

5. **Objetos interactivos:** Elaborar un sistema que produzca comida de forma aleatoria únicamente en las celdas superficiales del cubo ($x$, $y$ o $z$ en 0 o $N-1$). Manejar la detección de colisiones, efectos de interacción y sincronización con las rotaciones planetarias.

6. **Renderizado:** Aplicar materiales, técnicas de *Alpha Blending* e iluminación básica para optimizar la estética. Emplear técnicas de optimización como *Display Lists* para mejorar la representación de miles de primitivas por frame, sosteniendo 60 FPS.

7. **Experiencia completa:** Incorporar UI con puntuación en tiempo real, estados de juego (menú, jugando, game over), cámaras alternativas (isométrica, frontal, seguimiento, primera persona) y retroalimentación visual (flash al comer).

## 4. Marco teórico

### 4.1 El género Snake y su contexto histórico

El juego Snake pertenece a un género de videojuegos de acción donde el jugador controla a una serpiente, que representa una línea de crecimiento, y debe evitar chocar contra obstáculos o su propia cola mientras alcanza la comida para seguir creciendo y aumentar la puntuación. Históricamente, este tipo de juego se popularizó en máquinas recreativas y ordenadores en los años 70 y 80, pasando más adelante a dispositivos móviles a finales de los 90, consolidándose como el ejemplo clásico de interacción en tiempo real controlada por teclado o botones direccionales (Wikipedia contributors, 2025). Desde el punto de vista de computación gráfica y diseño de videojuegos, Snake combina un modelo geométrico sencillo (segmentos sobre una rejilla) con una lógica de actualización cíclica (bucle del juego: entrada → actualización → renderizado) y reglas de colisión simples.

### 4.2 Del plano 2D al mundo cúbico 3D

En este proyecto reinterpretamos el modelo tradicional pasando de un plano 2D a un mundo cúbico tridimensional, donde la serpiente se desplaza por las distintas caras de un cubo formado por una malla de vóxeles semitransparentes. Este enfoque obliga a replantear varios conceptos fundamentales:

* Los bordes del plano 2D pasan a ser aristas de un cubo con 6 caras, donde la continuidad del movimiento debe mantenerse al pasar a otra cara.
* La percepción del jugador depende de la rotación del cubo, introduciendo un vínculo directo entre el modelo matemático del espacio (rotaciones y cambios de base) y la ilusión de un mundo infinito.
* El concepto de que la serpiente avanza por las diferentes caras y el cubo gira automáticamente 90 grados para mantener contacto visual claro con ella representa la mecánica central del juego.

### 4.3 Pipeline gráfico y OpenGL

El pipeline gráfico moderno implementado por APIs como OpenGL transforma primitivas geométricas definidas en un espacio de objeto en una imagen 2D final mediante una secuencia de etapas: transformación por las matrices del modelo, vista y proyección; recorte al volumen de visión; proyección en coordenadas del dispositivo normalizadas; y rasterización de triángulos o cuadriláteros en fragmentos de pantalla (Shreiner et al., 2023).

Utilizamos **PyOpenGL** como interfaz hacia el pipeline de OpenGL. Aunque Python gestiona la lógica de alto nivel, el renderizado se delega a la GPU, lo que garantiza un buen rendimiento incluso cuando se dibujan cientos de cubos por fotograma. Aunque la asignatura profundiza en el pipeline programable (Vertex y Fragment Shaders), en este proyecto empleamos el pipeline fijo optimizado mediante **Display Lists**; de haber utilizado shaders, habríamos descrito los vértices del cubo y los gradientes de color directamente en GPU, pero el coste de emitir miles de draw calls desde Python justificó la alternativa.

### 4.4 Representación volumétrica mediante vóxeles

Los vóxeles (*volumetric pixels*) se definen como la unidad cúbica mínima de una matriz tridimensional uniforme que representa volumen. Es la forma análoga al píxel en 2D, pero extendida a tres dimensiones. Cada vóxel ocupa una celda de una rejilla $N \times N \times N$ y puede asociarse a propiedades como color, opacidad o tipo de material, lo que permite modelar volúmenes complejos como conjuntos de pequeños cubos discretos en vez de superficies continuas descritas por mallas poligonales.

La elección de un tablero voxelizado responde a la necesidad de representar un espacio discreto que comparta sistema de coordenadas con la serpiente y los objetos. Esto permite tratar el tablero y la serpiente en un mismo sistema de coordenadas discretas $(x, y, z)$, simplificando la detección de colisiones y la generación de comida. La representación voxelizada trae consigo implicaciones de rendimiento y diseño visual, ya que se generan cientos o miles de cubos pequeños por fotograma, y la transparencia introduce problemas de orden de dibujo y de lectura de profundidad.

### 4.5 Transformaciones geométricas en coordenadas homogéneas

Las transformaciones en 3D se formulan en coordenadas homogéneas mediante matrices $4 \times 4$, lo que permite expresar traslaciones, rotaciones y escalados como productos matriciales que pueden componerse de forma jerárquica. En OpenGL, el producto de la matriz de modelo, la matriz de vista y la matriz de proyección determina la transformación completa desde el espacio de objeto al de pantalla.

En línea con los apuntes de la asignatura, gestionamos dichas transformaciones mediante la pila de matrices (`glPushMatrix`/`glPopMatrix`): el cubo actúa como nodo padre y la serpiente como nodo hijo, por lo que cada giro se formula como una multiplicación matricial que preserva la coherencia espacial. Aplicamos el principio de relatividad del movimiento estudiado para cámaras virtuales: en lugar de girar una cámara con ángulos de Euler o cuaterniones, invertimos la transformación y rotamos el mundo, obteniendo el mismo resultado visual con menor complejidad numérica.

### 4.6 Transparencia y gestión del Depth Buffer

La transparencia se gestiona en OpenGL mediante *Alpha Blending*, combinando el color de la fuente y el del destino según una función de mezcla que depende del canal alfa, mediante configuraciones como `glBlendFunc`. Sin embargo, para conseguir resultados visuales correctos es necesario considerar el orden de dibujo y la interacción con el *depth buffer*, ya que la geometría translúcida puede ocultar indebidamente objetos si se renderiza en un orden incorrecto.

La estrategia teórica consiste en dibujar primero toda la parte opaca con pruebas de profundidad y escrituras activadas, continuando con el renderizado de la geometría translúcida sin escritura de profundidad. En nuestro juego, este principio se aplica de forma directa: se dibuja primero la serpiente como geometría opaca, escribiendo en el *depth buffer*, y a continuación se desactiva la escritura de profundidad (`glDepthMask(GL_FALSE)`) antes de renderizar el tablero de vóxeles semitransparentes, de forma que el cubo se superpone visualmente sin hacer desaparecer partes de la serpiente durante las rotaciones.

### 4.7 Bucle de juego en tiempo real

Desde el punto de vista de ingeniería de videojuegos, todo se integra en un bucle de juego en tiempo real estructurado en:
1. **Captura de entrada:** lectura del estado del teclado
2. **Actualización lógica:** movimiento discreto, detección de colisiones, gestión de estados
3. **Renderizado:** dibujo de la escena con las transformaciones aplicadas

Esta estructura permite separar la frecuencia de actualización de la lógica de la de refresco de pantalla, garantizando una experiencia fluida independientemente del hardware.

### 4.8 Decisiones de diseño: texturas, shaders y optimización

Durante la planificación del proyecto evaluamos varias técnicas que, aunque forman parte del temario de la asignatura, decidimos conscientemente no implementar. Creemos importante explicar el razonamiento detrás de estas decisiones, ya que reflejan un proceso de ingeniería donde el contexto del problema guía las soluciones técnicas.

**¿Por qué no utilizamos texturas?**

Las texturas en OpenGL permiten mapear imágenes sobre superficies poligonales, añadiendo detalle visual sin incrementar la complejidad geométrica. Sin embargo, en nuestro caso particular, el uso de texturas no aportaba valor significativo al proyecto por varias razones:

* **Estética minimalista intencionada:** El estilo visual "vóxel" que buscábamos se basa precisamente en cubos de colores sólidos y uniformes. Añadir texturas habría roto la coherencia estética del "cubo de cristal" translúcido.
* **Complejidad de gestión:** Cada textura requiere carga desde disco, generación de objetos de textura en GPU (`glGenTextures`, `glBindTexture`), configuración de parámetros de filtrado y wrapping, y gestión del ciclo de vida. Con miles de vóxeles renderizándose por frame, esta sobrecarga habría complicado innecesariamente el código.
* **Impacto en rendimiento:** El *texture sampling* añade ciclos de GPU, y la gestión de múltiples texturas puede fragmentar la memoria de vídeo. Dado que la fluidez de la experiencia de juego era vital para nosotros (un Snake que no responda a 60 FPS se siente "roto"), priorizamos la simplicidad.
* **Coordenadas UV innecesarias:** Mapear texturas sobre cubos requiere definir coordenadas UV para cada vértice. En un mundo procedural donde los cubos se generan dinámicamente, esto añadiría complejidad sin beneficio visual.

En lugar de texturas, optamos por definir los colores directamente en `configuracion.py` como constantes RGBA, lo que nos dio control total sobre la paleta visual y simplificó enormemente el pipeline de renderizado.

**¿Por qué Display Lists en lugar de Shaders y VBOs?**

El temario de la asignatura enfatiza el pipeline programable moderno (Vertex Shaders, Fragment Shaders, VBOs, VAOs). Reconocemos que esta es la dirección de la industria, pero en el contexto específico de Python + PyOpenGL, las Display Lists ofrecían ventajas prácticas:

* **Overhead de Python:** Cada llamada a una función de OpenGL desde Python implica un cruce de frontera entre el intérprete y la librería nativa. Con shaders y VBOs, seguiríamos necesitando emitir comandos de dibujo por cada entidad. Las Display Lists precompilan *todos* los comandos en la GPU, reduciendo el overhead a una única llamada por frame.
* **Prototipado rápido:** El pipeline fijo con `glBegin`/`glEnd` es más intuitivo para experimentar con geometría. Pudimos iterar rápidamente sobre el diseño visual sin preocuparnos por la gestión de buffers.
* **Resultado equivalente:** Para nuestro caso de uso (geometría estática del tablero), las Display Lists logran el mismo objetivo que un VBO estático: la geometría reside en la GPU y se renderiza sin transferencias por frame.

Esta decisión no implica desconocimiento del pipeline moderno; al contrario, entendemos que en un entorno de producción con C++ o un motor gráfico, los shaders serían la opción correcta. Simplemente adaptamos la solución al contexto real del proyecto.

## 5. Metodología

Este proyecto Snake 3D se ha diseñado a través de un método iterativo e incremental con revisiones semanales. Cada ciclo se centró en un bloque funcional (tablero, serpiente, rotaciones, UI) y concluyó con pruebas en tiempo real para detectar artefactos gráficos o lógicos. El enfoque prioriza la modularidad, un uso claro del código y la aplicación práctica de transformaciones 3D, transparencia y animación con OpenGL.

### 5.1 Lenguaje y librerías

Se ha elegido **Python** como lenguaje principal por su claridad sintáctica y rapidez de prototipado. Las librerías utilizadas son:
* **Pygame:** Gestión de la ventana, entrada del usuario y bucle de juego.
* **PyOpenGL:** Interfaz hacia el pipeline de OpenGL, permitiendo que las partes críticas del renderizado se ejecuten directamente sobre la GPU.

### 5.2 Arquitectura modular

Adoptamos un enfoque orientado a objetos con separación clara de responsabilidades:

| Módulo | Responsabilidad |
|--------|-----------------|
| `main.py` | Punto de entrada e inicialización |
| `game.py` | Bucle principal, máquina de estados y render loop |
| `tablero.py` | Generación y renderizado del mundo vóxel (optimizado con Display Lists) |
| `snake.py` | Lógica de la entidad, movimiento y colisiones |
| `comida.py` | Generación aleatoria de comida en celdas superficiales |
| `camara.py` | Configuración de los diferentes modos de cámara |
| `luces.py` | Configuración de la iluminación OpenGL |
| `input_handler.py` | Abstracción de la lectura del teclado |
| `text_renderer.py` | Renderizado de texto 2D sobre la escena 3D |
| `configuracion.py` | Constantes globales (tamaños, colores, tiempos) |
| `transformaciones.py` | Funciones auxiliares para rotaciones matemáticas |

Esta separación nos permitió trabajar en características aisladas sin romper la lógica general.

### 5.3 Pipeline gráfico y técnicas de renderizado

Aunque el temario enfatiza el pipeline programable (Shaders, VBO/VAO), en Python el costo de emitir miles de draw calls impone un límite práctico. Por ello utilizamos **Display Lists** del pipeline fijo para precompilar la geometría en GPU. Esta decisión, aunque menos moderna, reproduce la eficiencia buscada logrando 60 FPS estables.

El modelado por vóxeles implica dibujar cientos de cubos pequeños por fotograma. Para gestionar esta carga:
* Precompilamos la geometría del tablero en Display Lists durante la inicialización.
* Eliminamos los cubos internos, dibujando solo el "cascarón" superficial.
* Aplicamos un gap entre vóxeles para mejorar la legibilidad visual.

**Colores procedurales en lugar de texturas:** Definimos toda la paleta de colores en `configuracion.py` como tuplas RGBA. La serpiente usa verde brillante, la comida rojo intenso, y el tablero un azul translúcido. Este enfoque nos permite ajustar la estética instantáneamente sin gestionar archivos externos, y evita el overhead del *texture sampling* en cada fragmento. Para un juego donde la claridad visual y la respuesta inmediata son prioritarias, esta simplicidad resultó ser una ventaja, no una limitación.

### 5.4 Gestión de transformaciones y rotación del mundo

Empleamos `glPushMatrix`/`glPopMatrix` para aislar cada entidad. La pila de matrices permite componer transformaciones jerárquicamente sin que una afecte a otra.

Para la animación de rotación de 90° al cambiar de cara:
* Se detecta cuándo la cabeza intenta salir del rango válido.
* Se calcula el eje y ángulo de rotación necesarios.
* Se interpola suavemente el ángulo durante un tiempo configurable (`TIEMPO_ROTACION_AUTO`).
* Los segmentos de la serpiente y la comida rotan matemáticamente para mantener coherencia lógica.

### 5.5 Transparencia, profundidad y renderizado híbrido

La gestión de transparencias sigue un orden estricto:
1. **Primero:** Dibujar geometría opaca (serpiente, comida) con escritura en *depth buffer* activada.
2. **Después:** Desactivar escritura de profundidad (`glDepthMask(GL_FALSE)`).
3. **Finalmente:** Dibujar geometría translúcida (tablero vóxel) con *alpha blending*.

Este orden garantiza que el cubo de cristal no oculte visualmente a la serpiente.

### 5.6 Sistema de coordenadas híbrido

* **Coordenadas discretas (lógica):** La serpiente, la comida y las colisiones operan en índices enteros $(x, y, z)$ dentro del rango $[0, N-1]$.
* **Coordenadas continuas (renderizado):** Las posiciones se transforman a coordenadas de mundo mediante un *stride* que considera el tamaño del vóxel y el espaciado entre celdas.

Esta dualidad simplifica la lógica del juego mientras permite un renderizado flexible.

### 5.7 Desarrollo iterativo por fases

Cada fase terminó con:
* Un entregable funcional (ejecutable).
* Capturas visuales (GIF) para documentar el progreso.
* Mediciones de FPS para validar fluidez.
* Actualización del README y este informe.

Este enfoque facilitó detectar regresiones, mantener la motivación del equipo y asegurar trazabilidad entre decisiones técnicas y resultados.

## 6. Desarrollo del proyecto

El proyecto cobró vida a través de una secuencia lógica de avances organizados en fases. A continuación, describimos cada etapa con los retos enfrentados y las soluciones implementadas.

### 6.1 Fases 0-2: Del plano al volumen

Comenzamos configurando el entorno OpenGL, activando *blending* y construyendo el primer cubo voxelizado isométrico. En `configuracion.py` definimos las propiedades del "Mundo Cúbico":
* `GRID_SIZE` para el tamaño del cubo (ej. 10×10×10, luego ampliado a 15×15×15).
* Colores con canal Alpha (RGBA) para soportar transparencias.
* Ajuste del FOV de la cámara para abarcar el volumen completo.

La clase `Tablero` pasó de dibujar un simple `GL_QUAD` a iterar en tres dimensiones $(x, y, z)$, renderizando cubos unitarios con un color azulado y un valor Alpha bajo (0.15), creando el efecto de "cubo de cristal". También dibujamos las aristas en modo *wireframe* para que la cuadrícula 3D fuera visualmente legible.

### 6.2 Fases 3-4: Movimiento sobre la cara frontal

Una vez tuvimos el mundo, colocamos a la serpiente. El reto fue migrar de coordenadas 2D a 3D. Actualizamos la clase `Segmento` para almacenar $(x, y, z)$ completas y programamos la lógica para que la serpiente apareciera en la cara frontal del cubo (la cara con Z positivo máximo).

![Fase 3 - Serpiente en cara frontal](FasesCompletadas/Hasta_Fase3.gif)

Implementamos el movimiento discreto clásico del Snake: cada cierto intervalo de tiempo (`TIEMPO_PASO = 150ms`), la serpiente avanza una celda en la dirección indicada. Separamos claramente los controles:
* **Flechas del teclado:** Controlan la dirección de la serpiente, con validación para prevenir giros de 180°.
* **El mundo rota automáticamente** para seguir a la serpiente cuando cruza un borde.

El mapeo de flechas se mantiene en el plano local visible, de modo que tras cada giro los controles siguen siendo consistentes con la percepción del jugador.

![Fase 4 - Movimiento discreto funcionando](FasesCompletadas/Hasta_Fase4.gif)

### 6.3 Fase 5: Transición automática de caras

Este fue el punto de inflexión del proyecto. Implementamos el concepto de "frente infinito": la serpiente siempre cree que está en la cara frontal, y cuando cruza un borde, rotamos su sistema de coordenadas y animamos el mundo para que la nueva cara se convierta en el frente visible.

![Fase 5 - Transición automática entre caras](FasesCompletadas/Hasta_Fase5.gif)

**Implementación en dos frentes:**

1. **Lado lógico (`snake.py`):** Cada vez que un segmento intenta salir del rango $(0..N-1)$, devolvemos el eje y el ángulo de rotación necesarios. Antes de movernos, aplicamos una rotación matemática a todos los segmentos para reacomodarlos sobre la "nueva" cara frontal.

2. **Lado visual (`main.py`):** Convertimos el bucle principal en una mini máquina de estados. Cuando se detecta una transición, "congelamos" el input del usuario, retrocedemos un frame la rotación para evitar el típico "pop" y luego interpolamos durante `TIEMPO_ROTACION_AUTO` hasta alinear el cubo suavemente.

**Problema del Depth Buffer:** En nuestro primer intento, la serpiente desaparecía al cruzar las esquinas. El cristal se dibujaba primero, escribía en el *depth buffer* y OpenGL descartaba los segmentos que quedaban "dentro" del cubo. La solución fue cambiar el orden de renderizado:
* Dibujar **primero la serpiente** (opaca).
* Desactivar la escritura en profundidad (`glDepthMask(GL_FALSE)`).
* Dibujar el tablero translúcido encima.

### 6.4 Fase 6: Mecánicas de juego

Cerramos el ciclo de juego básico añadiendo la comida. La clase `Comida` genera posiciones aleatorias con una restricción clave: **siempre en la superficie** del cubo ($x$, $y$ o $z$ deben ser 0 o $N-1$), validando que no aparezca sobre el cuerpo de la serpiente.

**Reto matemático: Rotación solidaria.** Al igual que la serpiente, la comida tiene coordenadas lógicas. Cuando la serpiente cruza un borde y el mundo rota 90°, **la comida también debe rotar sus coordenadas** internamente. Si no lo hiciéramos, al girar el cubo la comida parecería moverse de sitio o flotar en el vacío.

Implementamos el crecimiento mediante el método `crecer()` que duplica el último segmento de la cola, y la detección de autocolisión verificando si la coordenada destino de la cabeza coincide con algún segmento del cuerpo.

### 6.5 Fases 7-9: Pulido visual y rendimiento

Activamos el pipeline de iluminación de OpenGL configurando `GL_LIGHT0` y `GL_COLOR_MATERIAL` para dar volumen y brillo a la escena. Refactorizamos el código de un script monolítico a una arquitectura orientada a objetos con `game.py` e `input_handler.py`.

![Fase 7 - Iluminación y arquitectura](FasesCompletadas/Hasta_Fase7.gif)

Implementamos una máquina de estados con tres fases: `MENU` → `JUGANDO` → `GAMEOVER`. Creamos `text_renderer.py` para mostrar instrucciones y puntuación sobre la escena 3D.

**Problema crítico de rendimiento:** Al dibujar 3,375 cubos individuales ($15^3$) en cada frame, Python generaba un cuello de botella masivo. El juego sufría de *lag* severo con FPS muy por debajo de 60.

**Solución: Display Lists.** Implementamos esta técnica de OpenGL que permite "grabar" toda la geometría del tablero en la memoria de la GPU una sola vez durante la inicialización. A partir de entonces, renderizar el tablero requiere una única llamada (`glCallList`) que ejecuta todos los comandos pregrabados. El resultado fue espectacular: pasamos de *lag* constante a **60 FPS estables**.

También implementamos:
* **Caché de texturas de texto** para evitar regenerar las texturas en cada frame.
* **Feedback visual (flash)** al comer: incremento temporal de la luz ambiental y un overlay 2D blanco semitransparente.

![Fase 9 - UI, estados y feedback visual](FasesCompletadas/Hasta_Fase9.gif)

### 6.6 Fase 10: Sistema de cámaras

Añadimos un sistema de cámaras seleccionables para que el jugador pudiera elegir la perspectiva que mejor se adaptara a su estilo:

* **Cámara 1 (Isométrica):** Vista diagonal clásica que muestra tres caras del cubo simultáneamente. Utiliza proyección ortogonal para mantener el tamaño aparente constante.
* **Cámara 2 (Frontal):** Vista frontal ligeramente elevada, centrada en la cara activa. Proyección en perspectiva.
* **Cámara 3 (Seguimiento / Third Person):** Cámara dinámica que sigue la posición de la cabeza de la serpiente.
* **Cámara 4 (Primera Persona / FPS):** La cámara se sitúa sobre la cabeza de la serpiente, mirando hacia adelante en la dirección del movimiento.

Esta adición requirió actualizar `configuracion.py` para definir los vectores de posición de cada cámara y modificar `game.py` para alterar dinámicamente los parámetros de `gluLookAt`.

![Fase 10 - Sistema de 4 cámaras](FasesCompletadas/Hasta_Fase10.gif)

### 6.7 Fase 11: Estética y legibilidad

Refinamos la estética del mundo para mejorar la legibilidad visual:

* **Gap entre vóxeles:** Introdujimos un espaciado físico (`ESPACIO_CELDA = 0.2`) para que cada celda sea distinguible.
* **Eliminación de cubos internos:** Dado que la serpiente solo se mueve por la superficie, los vóxeles del núcleo eran innecesarios. Al dibujar solo el "cascarón", limpiamos visualmente el centro y mejoramos el rendimiento.
* **Ajuste de colores:** Incrementamos la opacidad de las caras al 15% y cambiamos el color de los bordes a un cyan brillante con mayor opacidad (0.6).
* **Bordes engrosados:** Aumentamos `glLineWidth` para facilitar la navegación espacial.

El resultado es un tablero mucho más legible y estético, donde cada celda es una entidad distinta que parece flotar en el espacio.

Cada fase dejó un entregable funcional, lo que facilitó detectar regresiones y mantener la motivación del equipo.

## 7. Resultados

El resultado final es **"Snake 3D: Vóxel Planetario"**, un videojuego completo que cumple con creces la propuesta inicial. A continuación, detallamos los logros alcanzados en cada dimensión del proyecto.

### 7.1 Rendimiento

* **60 FPS constantes** en un cubo 15×15×15 gracias a Display Lists y eliminación de geometría innecesaria.
* **Tiempo de carga mínimo:** La precompilación de la geometría en Display Lists ocurre una sola vez al inicio.
* **Sin caídas de rendimiento** durante las rotaciones animadas ni al crecer la serpiente.

### 7.2 Funcionalidad técnica

| Característica | Estado | Implementación |
|----------------|--------|----------------|
| Mundo vóxel 3D | ✓ | Cubo 15×15×15 con transparencias |
| Movimiento en 6 caras | ✓ | Transición automática al cruzar bordes |
| Rotación suave del mundo | ✓ | Interpolación durante `TIEMPO_ROTACION_AUTO` |
| Generación de comida superficial | ✓ | Solo en celdas donde $x$, $y$ o $z$ = 0 o $N-1$ |
| Autocolisión | ✓ | Game Over al chocar con el propio cuerpo |
| Iluminación OpenGL | ✓ | `GL_LIGHT0` con materiales |
| Sistema de puntuación | ✓ | 8 puntos por comida |
| Interfaz de usuario | ✓ | Texto 2D sobre escena 3D |
| Múltiples cámaras | ✓ | 4 modos: isométrica, frontal, seguimiento, FPS |
| Feedback visual | ✓ | Flash al comer (3D + overlay 2D) |

### 7.3 Experiencia de usuario

* **Control responsivo:** La serpiente responde inmediatamente a las flechas del teclado.
* **Instrucciones claras:** El menú inicial muestra los controles y la cámara seleccionada.
* **Reinicio instantáneo:** Al morir, pulsar 'R' reinicia la partida sin demora.
* **Feedback visual inmediato:** El flash al comer mejora el "game feel".

### 7.4 Arquitectura y escalabilidad

* **Código modular:** 15 archivos Python con responsabilidades claramente separadas.
* **Fácil extensión:** La arquitectura permite añadir nuevas cámaras, skins o mecánicas sin reescribir el núcleo.
* **Documentación integrada:** README técnico y este informe final actualizados en cada fase.

### 7.5 Demostración académica

El prototipo cubre de forma práctica los siguientes temas del curso:
* Transformaciones geométricas compuestas (rotación, traslación).
* Coordenadas homogéneas y matrices $4 \times 4$.
* Pipeline gráfico de OpenGL (aunque con Display Lists en lugar de shaders).
* Gestión del *depth buffer* y *alpha blending*.
* Iluminación básica con `GL_LIGHT0`.
* Animación en tiempo real con interpolación.
* Proyecciones ortogonal y en perspectiva.

No solo buscamos un comprensión teórica, sino capacidad para aplicar estos conceptos en un entorno interactivo.

## 8. Conclusiones

La versión voxel planetaria de Snake nos permitió convertir conceptos de computación gráfica en decisiones concretas: desde entender por qué el orden de dibujo afecta la transparencia hasta medir el impacto de optimizar con Display Lists. Superamos el objetivo inicial de un simple tablero 3D y entregamos un juego completo con interfaz, estados y experiencia pulida.

### 8.1 Grado de consecución de los objetivos

Todos los objetivos planteados fueron alcanzados satisfactoriamente:

| Objetivo | Estado | Observaciones |
|----------|--------|---------------|
| Mundo cúbico transparente | ✓ Completado | Cubo 15×15×15 con alpha blending y depth buffer controlado |
| Serpiente 3D segmentada | ✓ Completado | Movimiento en 6 caras, colisiones, crecimiento |
| Rotación global suave | ✓ Completado | Interpolación de 90° sin saltos visuales |
| Transición entre caras | ✓ Completado | Reorientación automática de segmentos y comida |
| Objetos interactivos | ✓ Completado | Comida superficial sincronizada con rotaciones |
| Renderizado avanzado | ✓ Completado | 60 FPS estables con Display Lists |
| Experiencia completa | ✓ Completado | UI, estados, 4 cámaras, feedback visual |

### 8.2 Lecciones aprendidas

Confirmamos que la modularidad acelera los cambios (por ejemplo, la sustitución del tablero completo tras un error sintáctico) y que las pruebas frecuentes evitan que los problemas de profundidad o rendimiento lleguen al final del ciclo. Entre las lecciones más importantes:

* **La matemática es la base de todo:** Las matrices de transformación, las coordenadas homogéneas y las rotaciones no son conceptos abstractos; son las herramientas que hacen posible cualquier aplicación gráfica 3D.
* **El orden de renderizado importa:** La gestión del *depth buffer* y el *alpha blending* requiere comprensión profunda del pipeline. Un orden incorrecto hace que objetos desaparezcan misteriosamente.
* **La optimización no es opcional:** Python + OpenGL puede generar cuellos de botella severos. Las Display Lists demostraron ser una solución elegante y efectiva.
* **Saber qué NO implementar es tan importante como saber qué implementar:** Decidir conscientemente no usar texturas ni shaders no fue por desconocimiento, sino por análisis del contexto. Un buen ingeniero adapta las herramientas al problema, no al revés. En nuestro caso, la fluidez del juego era prioritaria, y las técnicas más simples cumplían el objetivo sin añadir complejidad innecesaria.

### 8.3 Relevancia en el contexto de la asignatura

El proyecto demuestra que los conceptos estudiados durante el curso tienen aplicación directa en el desarrollo de software interactivo. Las transformaciones 3D, la gestión del pipeline gráfico, la iluminación y las técnicas de optimización no son solo teoría; son las herramientas que permiten crear experiencias visuales inmersivas.

### 8.4 Trabajo futuro

El proyecto queda listo para futuras extensiones sin comprometer la base lograda:
* Implementar obstáculos estáticos sobre la superficie del cubo.
* Añadir modos de dificultad con velocidades variables.
* Explorar técnicas de renderizado más modernas (shaders, VBOs).
* Incorporar efectos de sonido y música.
* Desarrollar modos cooperativos o competitivos.

En definitiva, creemos haber logrado cumplir los objetivos académicos, creando una pieza de software funcional y estética a nuestro gusto que demuestra que con una metodología ordenada es posible construir mundos tridimensionales complejos e interactivos.

## 9. Bibliografía

* Foley, J. D., van Dam, A., Feiner, S. K., & Hughes, J. F. (1996). *Computer Graphics: Principles and Practice* (2nd ed.). Addison-Wesley.

* PyOpenGL Developers. (2024). *PyOpenGL Documentation*. https://pyopengl.sourceforge.net/

* Pygame Community. (2024). *Pygame Documentation*. https://www.pygame.org/docs/

* Shreiner, D., Sellers, G., Kessenich, J., & Licea-Kane, B. (2023). *OpenGL Programming Guide: The Official Guide to Learning OpenGL* (10th ed.). Addison-Wesley.

* Wikipedia contributors. (2025, November 23). *Snake (video game genre)*. Wikipedia, The Free Encyclopedia. https://en.wikipedia.org/w/index.php?title=Snake_(video_game_genre)&oldid=1323825146

* Woo, M., Neider, J., Davis, T., & Shreiner, D. (1999). *OpenGL Programming Guide: The Official Guide to Learning OpenGL* (3rd ed.). Addison-Wesley.
