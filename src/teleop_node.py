#!/usr/bin/env python3
import sys
import select
import termios
import tty
import os
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile

msg = """
Control Your 6-DOF Arm Joints!
Each pair moves a specific joint positive/negative.

Joint 1: q / a  (Mapped to Linear X)
Joint 2: w / s  (Mapped to Linear Y)
Joint 3: e / d  (Mapped to Linear Z)
Joint 4: r / f  (Mapped to Angular X)
Joint 5: t / g  (Mapped to Angular Y)
Joint 6: y / h  (Mapped to Angular Z)

SPACE or 'x' : Stop all movement
CTRL-C       : Quit
"""

settings = termios.tcgetattr(sys.stdin)

def get_key():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    rclpy.init()
    node = rclpy.create_node('teleop_joint_keyboard')
    
    qos = QoSProfile(depth=10)
    pub = node.create_publisher(Twist, 'cmd_vel', qos)

    lx = 0.0 
    ly = 0.0 
    lz = 0.0 
    ax = 0.0 
    ay = 0.0 
    az = 0.0 
    
    speed = 0.5 

    try:
        print(msg)
        while(1):
            key = get_key()
            
            lx = 0.0; ly = 0.0; lz = 0.0; ax = 0.0; ay = 0.0; az = 0.0

            if key == 'q': lx = speed
            elif key == 'a': lx = -speed
            
            elif key == 'w': ly = speed
            elif key == 's': ly = -speed
            
            elif key == 'e': lz = speed
            elif key == 'd': lz = -speed
            
            elif key == 'r': ax = speed
            elif key == 'f': ax = -speed
            
            elif key == 't': ay = speed
            elif key == 'g': ay = -speed
            
            elif key == 'y': az = speed
            elif key == 'h': az = -speed

            elif key == '\x03': # CTRL-C
                break

            twist = Twist()
            twist.linear.x = lx
            twist.linear.y = ly
            twist.linear.z = lz
            twist.angular.x = ax
            twist.angular.y = ay
            twist.angular.z = az

            pub.publish(twist)

    except Exception as e:
        print(e)

    finally:
        twist = Twist()
        pub.publish(twist)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
