import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import String

global node, pub

def joy_callback(msg:Joy):

    global pub

    comando = String()

    eje_x = msg.axes[0]
    eje_y = msg.axes[1]

    if eje_x > 0.5:
        comando.data = "I"

    elif eje_x < -0.5:
        comando.data = "D"

    elif eje_y > 0.5:
        comando.data = "A"

    elif eje_y < -0.5:
        comando.data = "R"
    else:
        comando.data = "F"


    pub.publish(comando)


def main():

    global node, pub

    rclpy.init()

    node = Node("joystick_node")

    pub = node.create_publisher(String,"direccion_joy",10)

    node.create_subscription(Joy,"/joy",joy_callback,10)

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()