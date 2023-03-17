# Ejercicio 2
Asuma que hay un *archivo* encriptado el cual contiene información importante para usted. Afortudanamente existe un nodo de ROS que es capaz 
de desencriptarlo. Siga las siguientes instrucciones para comenzar el ejercicio.

> No se por qué pero se requieren 2 archivos distintos dependiendo si se corre en ros MELODIC o es ros NOETIC, por esto hay dos carpetas separadas. Siga los sigiuentes comandos teniendo en cuenta la version de ROS que esta utilizando usted.

En una terminal hacer:

` source ~/iniciar`

` roscore`

Y en otra hacer:

` source ~/iniciar`

` cd Curso_ros/ej2/`

` cd TU_VERSION_DE_ROS`

` python ej2.py`


si todo funciona bien deberia aparecer el siguiente mensaje en la terminal:
> [INFO] [1679061049.074380]: Iniciando el ejercicio 2. Para comenzar debes publicar en el topic correcto tu nombre en minusculas.

Este ejercicio tiene 2 niveles de deficultad: 
- Obtener el código guardado dentro del archivo encriptado
- Desencriptar todo el archivo
