// Proyecto Snake 3D - shaders/vertex_shader.glsl
//
// Objetivo general:
// - Definir el shader de vértices responsable de transformar las posiciones de los
//   vértices desde el espacio del modelo al espacio de pantalla, aplicando las
//   matrices de modelo, vista y proyección.
//
// Objetivos específicos:
// - Recibir atributos de vértice (posición, normal, coordenadas de textura) y
//   prepararlos para su uso en el shader de fragmentos.
// - Aplicar las transformaciones geométricas necesarias para situar la serpiente,
//   el tablero y los objetos de comida en la escena 3D.
// - Servir de base para el modelo de iluminación que se implementará en el fragment shader.
//
// Este shader se inspira en la estructura del `vertex_shader.glsl` de nuestra referencia en 'shader',
// pero se adaptará a las necesidades concretas del juego Snake 3D.


