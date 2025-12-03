"""
Proyecto Snake 3D: Vóxel Planetario - main.py

Este archivo es el punto de entrada de nuestra aplicación. Tras la
refactorización realizada en las fases finales del proyecto, hemos conseguido
que este módulo sea extremadamente limpio y conciso.

Toda la complejidad del juego —la inicialización de OpenGL, la gestión de
estados, el bucle principal, el renderizado— está encapsulada en la clase
`Game`. De este modo, `main.py` actúa simplemente como el interruptor que
enciende el motor del juego.

Esta separación nos permite:
- Mantener un código legible y fácil de entender.
- Facilitar la depuración al tener un único punto de entrada claro.
- Preparar el terreno para futuras extensiones (por ejemplo, argumentos de
  línea de comandos o modos de ejecución alternativos).
"""

from game import Game

def main():
    juego = Game()
    juego.run()

if __name__ == "__main__":
    main()