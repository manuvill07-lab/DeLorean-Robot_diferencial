# DeLorean-Robot_diferencial
Sistema de control para un robot diferencial utilizando ROS2 (Python) y un código para el microcontrolador ESP32, permitiendo controlar el movimiento del carro mediante comunicación inalámbrica por WiFi.

**Organizacion del sistema:**
---
  Se cuenta con 3 nodos dentro de 3 paquetes que se comunican mediante el sistema operativo de ROS2 - distro Jazzy:

  ### 1. motores_joy (Paquete) - Ejecutable: executable_joy - Nodo: joystick_node
  ---

**- Descripción:** Es un nodo publicador que captura los datos de un Joystick físico (utilizando únicamente la palanca izquierda) y los traduce a comandos de dirección.

**- Tópico publicado:** direccion_joy (Mensajes de tipo std_msgs/String)

**- ¿Cómo funciona?:** El nodo se suscribe al paquete estándar joy. Dependiendo del movimiento del joystick que llega al nodo como un mensaje tipo joy (debido a que esta conectado al paquete joy), se determina si el movimiento es:

* A $\rightarrow$ Avanzar

* R $\rightarrow$ Retroceder

* I $\rightarrow$ Girar a la izquierda

* D $\rightarrow$ Girar a la derecha

* F $\rightarrow$ Frenar / Detener (cuando se suelta la palanca)

### 2. pub_sensor_us (Paquete) - Ejecutable: executable_sensor_us - Nodo: ultrasonic_sensor_publisher
---

**- Descripción:** Nodo publicador encargado de recibir la distancia calculada del sensor ultrasónico desde el ESP32 vía WiFi, evaluarla y publicarla en la red ROS 2.

**- Tópico publicado:** objeto_a_la_vista (Mensajes de tipo std_msgs/String)

**- ¿Cómo funciona?:**
Una vez este conectada la ESP32 a ROS2, se recibe la distancia calculada hacia algun objeto. La distancia determina el mensaje que se envia:

* Si distancia $< 10.0\text{ cm}$ $\rightarrow$ OBJETO_DETECTADO

* Si distancia $\ge 10.0\text{ cm}$ $\rightarrow$ VIA_LIBRE

### 3. bridge (Paquete) - Ejecutable: executable_bridge - Nodo: wifi_transmitter
---

**- Descripción:** Es el subscriptor a los dos nodos publicadores. Recibe los topicos de ambos nodos anteriores, los procesa y envia un comando a la ESP32 por WiFi cada vez que le llega un mensaje. Es el puente entre ROS2 y la ESP32.

**- Tópicos suscritos:** direccion_joy y objeto_a_la_vista

**- ¿Cómo funciona?:**
El nodo escucha constantemente ambos tópicos. Cada vez que llega un mensaje, dispara su función callback correspondiente:

* cmd_motores_callback(msg): Recibe comandos de dirección de direccion_joy.

* cmd_stop(msg): Recibe el estado del entorno de objeto_a_la_vista.

Los comandos se procesan, se les añade un salto de línea (\n) para que el microcontrolador pueda determinar hasta donde llega un mensaje y se codifican en formato utf-8 antes de ser transmitidos vía WiFi.

### FIRMWARE - PLATFORMIO:
---

Ademas, se cuenta con el codigo de **Platformio**, el cual se compila al microcontrolador.
En este codigo realizado en platformio con framework Arduino, se controlan los motores a partir de los mensajes que recibe del bridge y al mismo tiempo envia los datos del sensor ultrasonico, en donde ya se ha calculado la distancia 

**Ejecutar el proyecto:**
---

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

Proyecto en funcionamiento
---

https://github.com/user-attachments/assets/88bcc1ab-ae02-4027-befd-f140cc389cc6

https://github.com/user-attachments/assets/3ec41700-bc81-4f12-99fe-9bd598a9c4ae


    
        
