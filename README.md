# Task 3 
## 6-DOF Robotic Arm Control using ROS2 and Gazebo Sim

---

## Overview

This project demonstrates simulation and control of a 6-DOF robotic arm in Gazebo Sim using ROS2. The robot is spawned using a URDF model, controlled through ros2_control, and commanded via custom teleoperation and control nodes. Velocity commands are converted into joint position commands and sent to a Joint Trajectory Controller.

---

## Objectives

- Load 6-DOF arm URDF into Gazebo Sim  
- Bridge Gazebo and ROS2 topics  
- Configure ros2_control interfaces  
- Load controllers  
- Send velocity commands  
- Convert velocity to joint positions  
- Move robotic arm joints  

---


---

## Key Components

- URDF model of 6-DOF arm  
- Launch file (robo.launch.py)  
- robot_state_publisher launch file  
- spawn launch file  
- bridge.yaml (ROS2 ↔ Gazebo topics)  
- ros2_control.yaml (controllers & interfaces)  
- teleop_node.py  
- control_node.py  

---

## System Requirements

- Ubuntu 22.04  
- ROS2 Humble  
- Gazebo Sim (gz)  
- ros2_control  
- controller_manager  

---

## Environment setup

source /opt/ros/humble/setup.bash
source install/setup.bash

--- 

## Workflow

1. Launch robot in Gazebo
2. Load controllers
3. Start teleop node
4. Start control node
5. Move arm

---

## Doing the actual work

### Launch Robot in Gazebo (Terminal 1)

- cd 6_dof
- source install/setup.bash
- ros2 launch 6_dof robo.launch.py

### Load Controllers (Terminal 2)

- ros2 run controller_manager spawner joint_state_broadcaster \
 --param-file /home/deepak/6_dof/config/ros2_control.yaml \
 --ros-args -p use_sim_time:=true

- ros2 run controller_manager spawner joint_trajectory_controller \
 --param-file /home/deepak/6_dof/config/ros2_control.yaml \
 --ros-args -p use_sim_time:=true

### Start Teleoperation Node (Terminal 3)

- cd 6_dof
- source install/setup.bash
- python3 src/teleop_node.py

### Start Control Node (Terminal 4)
- cd 6_dof
- source install/setup.bash
- python3 src/control_node.py

---

### Topics used

- /cmd_vel
- /joint_states
- /joint_trajectory_controller/joint_trajectory

## Demo Video link
https://youtu.be/sbDG4Flq-o8
