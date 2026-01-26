cmake_minimum_required(VERSION 3.8)
project(6_dof)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)

# =========================================================
# INSTALL RULES
# This copies your folders to the "install" directory
# so ROS can find them when you run launch files.
# =========================================================
install(
  DIRECTORY src/launch src/urdf config
  DESTINATION share/${PROJECT_NAME}
)

# If you have meshes (stl/dae files), uncomment the line below:
# install(DIRECTORY meshes DESTINATION share/${PROJECT_NAME})

ament_package()
