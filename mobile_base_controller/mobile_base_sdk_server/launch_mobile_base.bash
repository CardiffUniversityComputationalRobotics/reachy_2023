#!/bin/bash
# source ROS2 Foxy setup file.
# shellcheck disable=SC1091


# Env setup
source /opt/ros/humble/setup.bash
source /home/reachy/reachy_ws/install/setup.bash
source /usr/share/gazebo/setup.bash
source /usr/share/colcon_cd/function/colcon_cd.sh
export _colcon_cd_root=~/ros2_install
export LC_NUMERIC="en_US.UTF-8"
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
source "$HOME/.cargo/env"
export PATH=$PATH:$HOME/.local/bin


zuuu_model=$(reachy-identify-zuuu-model 2>&1)
# Start the ROS2 launch file
if [ $zuuu_model != none ];
then
    echo "Starting mobile base launch file."
    ros2 launch mobile_base_sdk_server run_mobile_base_sdk_server_and_hal.launch.py
else
    echo "No mobile base found in this Reachy model."
fi
