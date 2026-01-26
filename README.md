I obtained the urdf for the 6_dof arm and first opened it in the gz sim using launch file
The launch file include two other launch files(robot_state_publisher and spawn) and spawn includes the bridge.yaml path that helps in making communicating for the topics of gz and ros2
we also have the ros2_control.yaml file that is used to tell the joints and command interfaces and state interfaces
we have the teleopnode.py that is used to publish on cmd_vel(twist message type)
and we have control_node.py that takes the twist message type and gives the joint position on the joint trajectory controller topic that is moved to make the arm moves

TO USE THIS REPO
FIRST CLONE THIS REPO AND COLCON BUILD 

TERMINAL 1
cd 6_dof
source install/setup.bash
ros2 launch 6_dof robo.launch.py

Terminal 2 (loading the controllers)
ros2 run controller_manager spawner joint_state_broadcaster --param-file /home/deepak/6_dof/config/ros2_control.yaml --ros-args -p use_sim_time:=true

ros2 run controller_manager spawner joint_trajectory_controller --param-file /home/deepak/6_dof/config/ros2_control.yaml --ros-args -p use_sim_time:=true

Terminal 3
cd 6_dof
source install/setup.bash
python3 src/teleop_node.py

Terminal 4
cd 6_dof
source install/setup.bash
python3 src/control_node.py
