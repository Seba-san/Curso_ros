# Ejercicio 3
En este ejercicio usted posee un robot atrapado en un laberinto 2D. El objetivo es lograr salir en la menor cantidad de pasos posibles.
Para esto, el robot cuenta con un sensor de obstaculos. Los posibles obstaculos son: Pared (1.0) y Caja (0.5). El espacio libre el sensor devuelve un 0.0, 
si usted esta en la salida el sensor devuelve 1000.0 y si esta en el punto de partida devuelve -1.0. 

Por ejemplo, si tiene esta situación:
     
          libre

     caja   R    pared

          pared
          
El sensor publicará una vez por segundo en el topic /sensor, el siguiente mensaje:

    echoes: [0.0, 1.0, 1.0, 0.5]

Lee los datos en sentido horario. Primero lee el que esta en el Norte, luego en el Este, luego Sur y por último Oeste.

Para moverse sobre el mapa usted tendra que publicar en el topic /robot_velocity. Donde el valor de las variables significan:
- linear.x > 0 Moverse un paso para la derecha
- linear.x <  0 Moverse un paso para la izquierda
- linear.y > 0 Moverse un paso para arriba
- linear.y <  0 Moverse un paso para abajo


Por otro lado usted cuenta con asistencias (servicios) que le dan habilidades especiales:
- /velocidad : Permite moverse 2 lugares en una dirección y cuenta como un movimiento.
- /saltar_caja : Permite saltar una caja.
- /pasar_paredes :  Permite pasar al otro lado de una pared
- /ayuda : El siguiente movimiento no suma en la cantidad de pasos. Solo se puede usar una vez

El objetivo didáctico del ejercicio es que cada jugador cree su propio nodo que se subscriba al topic /sensor, que publique en el topic /robot_velocity y que llame a alguna de las asistencias (servicios) cuando lo requiera.
Además se recomienda usar el ejemplo que se vio en la primer clase para poder operar el robot o bien usar el package: "teleop_twist_keyboard"

Para instalarlo hacer:
        
        sudo apt-get install ros-${ROS_DISTRO}-teleop-twist-keyboard
        
y para ejecutarlo hacer:

        rosrun teleop_twist_keyboard teleop_twist_keyboard.py
        
seguramente va a ser necesario que agregue procesamiento extra entre el topic /cmd_vel (donde publica teleop_twist_keyboard) y donde se requiere la informacion /robot_velocity.

Por último los mensajes de error, info y warnings los puede ver en /rosout, o en rqt_console o en el std_out. Usando todas las asistencias se pueden hacer todos los mapas
en 2 movimientos. La idea es que solo se pueda usar un solo tipo de asistencia y la ayuda, bajo estas condiciones va a depender del tipo de asistencia, pero se puede completar cada mapa en al menos 10 movimientos.

    
