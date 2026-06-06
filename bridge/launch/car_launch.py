from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        
        # 1. Nodo oficial JOY (Lee el control de Nintendo)
        Node(
            package='joy',
            executable='joy_node',
            name='joy_node_hardware',
            output='screen'
        ),

        # 2. Tu nodo de control (Traduce el control a comandos de texto)
        Node(
            package='motores_joy',        
            executable='executable_joy',   
            name='joystick_translator_node',
            output='screen'
        ),

        # 3. El nodo BRIDGE (Envía los comandos traducidos al ESP32)
        Node(
            package='bridge',         
            executable='executable_bridge', 
            name='serial_wifi_bridge_node',
            output='screen',
            parameters=[
                {'ip': '10.166.109.128'},
                {'port': 8080}
            ]
        ),

        # 4. Nodo de sensores ULTRASONIDO (Recibe las distancias del robot)
        Node(
            package='pub_sensor_us',     
            executable='executable_sensor_us', 
            name='ultrasonic_sensor_node',
            output='screen'
        )
    ])