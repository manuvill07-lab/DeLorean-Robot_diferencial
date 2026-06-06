# DeLorean-Robot_diferencial
Sistema de control para un robot diferencial utilizando ROS2 (Python) y un código para el microcontrolador ESP32, permitiendo controlar el movimiento del carro mediante comunicación inalámbrica por WiFi.

**Organizacion del sistema:**
  Se cuenta con 3 nodos dentro de 3 paquetes que se comunican mediante el sistema operativo de ROS2 - distro Jazzy:

  **-motores_joy (paquete) - executable_joy (ejecutable) - joystick_node (nodo):** 
    Es un publicador que recibe los datos del joystick (Unicamente el izquierdo) y los traduce a comandos tipo String enviados en el topico 'direccion_joy'.
      **-¿Como funciona?:** Dependiendo del movimiento del joystick que llega al nodo como un mensaje tipo joy (debido a que esta conectado al paquete joy), se determina si el movimiento es:
          A --> avanzar
          R --> retroceder
          I --> girar a la izquierda
          D --> girar a la derecha
          F --> frenar (si no se esta moviendo el joystick)
          
  **-pub_sensor_us (paquete) - executable_sensor_us (ejecutable) - ultrasonic_sensor_publisher (nodo):**
    Es un publicador que recibe los datos del sensor ultrasonico desde la ESP32 via WiFi y dependiendo de la distancia emite un mensaje tipo String en el topico 'objeto_a_la_vista'.
        **-¿Como funciona?:** Una vez este conectada la ESP32 a ROS2, se recibe la distancia calculada hacia algun objeto. Si esta es menor a 10, el mensaje enviado seria: "OBJETO_DETECTADO". En cualquier otra situacion 
        envia el mensaje "VIA_LIBRE".

  **-bridge (paquete) - executable_bridge (ejecutable) - 'wifi_transmitter'(nodo):**
    Es el subscriptor a los dos nodos publicadores. Recibe los topicos de ambos nodos anteriores, los procesa y envia un comando a la ESP32 por WiFi cada vez que le llega un mensaje. Es el puente entre ROS2 y la ESP32.
        **-¿Como funciona?:** Cada vez que reciben un topico se llama el callback respectivo.
            + cmd_motores_callback(msg): Recibe los mensajes de direccion_joy
            + cmd_stop_callback (msg): Recibe los mensajes de objeto_a_la_vista
          Para ambos casos una vez se guarda el mensaje en una variable, se genera un string con un final de linea para facilitar la lectura de estos en la ESP32 y este string se codifica 'utf-8' para enviar al 
          microcontrolador.

Ademas, se cuenta con el codigo de **Platformio**, el cual se compila al microcontrolador. De este es importante conectar el WiFi al microcontrolador y obtener la IP para reemplazar en el launch de ROS2 ubicado en el bridge.
En este codigo realizado en platformio con framework Arduino, se controlan los motores a partir de los mensajes que recibe del bridge y al mismo tiempo envia los datos del sensor ultrasonico, en donde ya se ha calculado la distancia 

**Ejecutar el proyecto:**
  1). Se debe conectar la ESP32 con el computador mediante el microUSB. Hay que llenar en el setup los siguientes datos de la funcion de WiFi.begin("nombre_red","contraseña") para conectar la ESP32 por WiFi.
  Se debe compilar el codigo de Platformio primero para obtener la IP del microcontrolador.
  
      NOTA: Una vez se compile deberia salir el monitor serial en donde muestra la IP una vez se conecte al WiFi, sin embargo a veces el monitor solo muestra ruido. Se debe reiniciar la ESP32 desde la placa para que vuelva
      a intentar conectarse.
	  
  2). Teniendo la IP se puede reemplazar en el launch file ubicado en el bridge. Se debe poner la IP en el parametro correspondiente del paquete bridge y pub_sensor_us.
      NOTA: Si el launch file no corre (nos sucedio a nosotros al principio), se debe cambiar la IP en los parametros de los dos ejecutables tambien.
  3). Se debe hacer compilar de nuevo el proyecto (colcon build) y activar el workspace en la terminal (source install/setup.bash) porque se acabaron de cambiar datos en el paso 2.
  4). Para correr los nodos hay un launch file ubicado en el paquete bridge con el nombre car_launch.py. Para correr el launch file en la terminal luego de haber realizado el paso 3 se debe poner el comando:
        **ros2 launch bridge car_launch.py**
  5). Ya deberia estar corriendo el launch file, en la terminal es posible ver los datos que se estan enviando por el WiFi transmitter al ESP32, y si el ESP32 sigue conectado al computador, en su monitor serial se pueden ver
  reflejados los comandos tambien. Se puede desconectar el robot diferencial y con el joystick deberia moverse por WiFi.

      
        
