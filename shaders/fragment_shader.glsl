// Proyecto Snake 3D - shaders/fragment_shader.glsl
//
// Objetivo general:
// - Definir el shader de fragmentos responsable de calcular el color final de cada
//   píxel de la escena, integrando información de texturas e iluminación.
//
// Objetivos específicos:
// - Aplicar un modelo de iluminación sencillo (por ejemplo, basado en componentes
//   ambiente, difusa y especular) para mejorar la percepción de volumen en la
//   serpiente, el tablero y la comida.
// - Combinar la iluminación con las texturas asignadas a cada objeto.
// - Mantener el código suficientemente claro como para poder extenderlo con
//   efectos adicionales en fases posteriores.
//
// Este shader se inspira en la estructura del `fragment_shader.glsl` de nuestra referencia en 'shader',
// adaptando los parámetros y cálculos a los requisitos del proyecto Snake 3D.


