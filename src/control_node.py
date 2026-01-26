#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState

class RobotControlNode(Node):
    def __init__(self):
        super().__init__('robot_control_node')
        
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)
        self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        self.joint_state_sub = self.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10)

        self.current_joints = [0.0] * 6
        self.JOINT_MAX = 3.14
        self.JOINT_MIN = -3.14

        self.get_logger().info("Control Node Running. Waiting for joint states...")

    def joint_state_callback(self, msg):
        target_order = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'finger_left_joint', 'finger_right_joint']
        
        current_state_dict = dict(zip(msg.name, msg.position))
        
        new_joints = []
        for name in target_order:
            if name in current_state_dict:
                new_joints.append(current_state_dict[name])
            else:
                new_joints.append(0.0) 
        
        self.current_joints = new_joints

    def cmd_vel_callback(self, msg):
        traj = JointTrajectory()
        traj.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        
        point = JointTrajectoryPoint()
        scale = 0.1

        new_pos = list(self.current_joints) 
        
        new_pos[0] += msg.linear.x * scale 
        new_pos[1] += msg.linear.y * scale 
        new_pos[2] += msg.linear.z * scale 
        new_pos[3] += msg.angular.x * scale 
        new_pos[4] += msg.angular.y * scale 
        new_pos[5] += msg.angular.z * scale 
        
        for i in range(6):
            new_pos[i] = max(self.JOINT_MIN, min(self.JOINT_MAX, new_pos[i]))

        point.positions = new_pos[0:6]
        point.time_from_start.sec = 0
        point.time_from_start.nanosec = 100000000 
        
        traj.points = [point]
        self.publisher_.publish(traj)

def main(args=None):
    rclpy.init(args=args)
    node = RobotControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
