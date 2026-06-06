import rclpy
from std_msgs.msg import String
import time
import socket

global node, wifi_config

def init_wifi_transmitter(ip, port):
    global wifi_config
    wifi_config = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    wifi_config.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    wifi_config.settimeout(3.0)

    node.get_logger().info(f"Intentando conectar al ESP32...")

    try:
        wifi_config.connect((ip,port))
        wifi_config.settimeout(None)
        node.get_logger().info(f"Conectado a {ip}:{port}")
    except socket.timeout:
        node.get_logger().error(f"¡TIEMPO DE ESPERA AGOTADO!: El ESP32 ({ip}) no respondió en 3 segundos.")
    except Exception as e:
        node.get_logger().error(f"Error crítico de red al conectar: {e}")
        raise SystemExit(e)


def cmd_motores_callback(msg):
    global wifi_config, node

    #Recibe el topico a partir del publicador joy
    comando = msg.data.strip()

    #imprime el comando en el monitor
    print(f'Recibido del publicador: {comando}')
    #Lo convierte en un string con un fin de linea
    comando_endl = f"{comando}\n"

    #Envia el comando a ESP32 ya codificado, genera un log para poder monitorear datos enviados
    wifi_config.sendall(comando_endl.encode('utf-8'))
    node.get_logger().info(f" Enviado a ESP32: {comando}")

def cmd_stop (msg):
    
    comando = msg.data.strip()
    print(f'Recibido del publicador: {comando}')

    #Solo se envian comandos cuando esta cerca a objeto
    if comando in ["OBJETO_DETECTADO"]:
        comando_endl = f"{comando}\n"
        #Enviar el comando a ESP32
        wifi_config.sendall(comando_endl.encode('utf-8'))
        node.get_logger().info(f" Enviado a ESP32: {comando}")


def main():
    global wifi_config, node

    rclpy.init()

    node = rclpy.create_node('wifi_transmitter')

    sub_joy = node.create_subscription(String, 'direccion_joy', cmd_motores_callback, 10)
    sub_sensor_us = node.create_subscription(String, 'objeto_a_la_vista', cmd_stop, 10)

    #Se debe cambiar el valor de la IP y el puerto
    node.declare_parameter('ip', '10.166.109.128')
    node.declare_parameter('port', 8080)

    ip = node.get_parameter('ip').get_parameter_value().string_value
    port = node.get_parameter('port').get_parameter_value().integer_value

    #Configurar la conexión WiFi
    init_wifi_transmitter(ip,port)

    #Mantener el nodo corriendo
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
    