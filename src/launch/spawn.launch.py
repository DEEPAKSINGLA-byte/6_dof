import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    
    pkg_share = get_package_share_directory('6_dof')
    urdf_path = os.path.join(pkg_share, 'urdf', 'robot.urdf')

    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')

    declare_x_position_cmd = DeclareLaunchArgument(
        'x_pose', default_value='0.0',
        description='X position to spawn the robot')

    declare_y_position_cmd = DeclareLaunchArgument(
        'y_pose', default_value='0.0',
        description='Y position to spawn the robot')

    start_gazebo_ros_spawner_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'six_dof_arm',  
            '-file', urdf_path,
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.05'            
        ],
        output='screen',
    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        output='screen',
    )
    bridge_config_path = os.path.join(
        get_package_share_directory('6_dof'),
        'config',            
        '6_dof_bridge.yaml'
    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_config_path
        }],
        output='screen',
    )

    ld = LaunchDescription()

    # Add actions
    ld.add_action(declare_x_position_cmd)
    ld.add_action(declare_y_position_cmd)
    ld.add_action(start_gazebo_ros_spawner_cmd)
    ld.add_action(start_gazebo_ros_bridge_cmd)

    return ld
