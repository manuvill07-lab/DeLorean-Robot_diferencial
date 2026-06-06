#SE ENCARGA DE PUBLICAR LOS DATOS DEL SENSOR ULTRASONICO A PARTIR DE LO QUE RECIBE POR WIFI DEL ESP32

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import socket

global node, pub, wifi_config

#Funcion que se llama cada vez que se ejecuta un nodo
def timer_callback():
    global node, pub, wifi_config

    try:
        # Se intenta leer el socket. Al ser no bloqueante, si no hay datos, falla.
        dato_rcb = wifi_config.recv(1024).decode('utf-8').strip()
    except BlockingIOError:
        # No hay datos en la red en este milisegundo, salimos de la funcion silenciosamente
        return
    except Exception as e:
        # Por si ocurre algún otro error de red inesperado
        return

    if dato_rcb:
        try:
            # Protegemos la conversion en caso de recibir caracteres invalidos
            distancia_str = dato_rcb
            distancia_atof = float(distancia_str)
        except ValueError:
            # Si el string no se puede convertir a float, ignoramos este ciclo
            return

        objeto_a_la_vista = String()

        #Define el comando a enviar al ESP32 dependiendo de la distancia medida por el sensor ultrasonico
        if(distancia_atof < 10.0):
            objeto_a_la_vista.data = "OBJETO_DETECTADO"
        else:
            objeto_a_la_vista.data = "VIA_LIBRE"

        #Publica el mensaje a ROS2 para que otros nodos puedan suscribirse a el
        pub.publish(objeto_a_la_vista)
        
        # Opcional: Se ajusto la impresion para ver el contenido del mensaje y no el objeto
        node.get_logger().info(f" Enviado a subscriptor: {objeto_a_la_vista.data}")


def wifi_setup(ip = '10.218.26.128', port = 8080):
    global wifi_config
    wifi_config = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wifi_config.connect((ip,port))

    wifi_config.setblocking(False)  # Establece el socket en modo no bloqueante
    node.get_logger().info(f"Conectado a {ip}:{port}")



def main():
    global node, pub
    rclpy.init()

    #Se crea el nodo
    node = rclpy.create_node('ultrasonic_sensor_publisher')

    #Se crea el publicador
    pub = node.create_publisher(String, 'objeto_a_la_vista', 10)

    #Se debe cambiar el valor de la IP y el puerto
    node.declare_parameter('ip', '10.166.109.128')
    node.declare_parameter('port', 8080)

    ip = node.get_parameter('ip').get_parameter_value().string_value
    port = node.get_parameter('port').get_parameter_value().integer_value

    wifi_setup(ip,port)

    node.create_timer(0.05, timer_callback)

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()