### ROSBAG y TF
En este ejercicio lo que se busca es ejercitar la utilizacion de los archivos **.bag** y de la libreria **tf** o **tf2**.


Para esto se entrega una grabación realizada en simulación que consiste de un robot del tipo *pioneer2dx* (robot diferencial) moviendose dentro de un galpon.
El robot cuenta con un lidar dispuesto horizontalmente y el galpon tiene 5 conos equidistantes puesto sobre las paredes.

El objetivo del ejercicio es crear un nodo que publique un mensaje cuando el robot este cerca del punto de inicio (*hay que consultar el frame "chassis"*) y cuando 
pase de cuadrante. Demas ese mismo mensaje debe enviarse mediante el sistema de logwarn.

Los detalles se pueden ver en la clase grabada:  https://youtu.be/1up70MFh-_Y
