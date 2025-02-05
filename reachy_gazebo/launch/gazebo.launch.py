from launch.launch_description import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument,
    OpaqueFunction,
)
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource


def launch_setup(context, *args, **kwargs):

    robot_config = LaunchConfiguration("robot_config", default="full_kit")
    world = LaunchConfiguration("world")

    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("gazebo_ros"),
                    "launch",
                    "gazebo.launch.py",
                ]
            )
        ),
        launch_arguments={
            "world": world,
            "verbose": "false",
        }.items(),
    )

    # Note: Environment variable GAZEBO_MODEL_PATH is extended as in
    # ROS2 control demos via environment hook https://github.com/ros-controls/ros2_control_demos/tree/master/ros2_control_demo_description/rrbot_description
    # Also see https://colcon.readthedocs.io/en/released/developer/environment.html#dsv-files
    # Gazebo launch scripts append GAZEBO_MODEL_PATH with known paths, see https://github.com/ros-simulation/gazebo_ros_pkgs/blob/ab1ae5c05eda62674b36df74eb3be8c93cdc8761/gazebo_ros/launch/gzclient.launch.py#L26
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic",
            "robot_description",
            "-entity",
            LaunchConfiguration("robot_name"),
            "-x",
            LaunchConfiguration("x_pose"),
            "-y",
            LaunchConfiguration("y_pose"),
            "-z",
            "0.084",
        ],
        output="screen",
    )

    fake_gz_interface = Node(
        package="reachy_gazebo",
        executable="fake_gz_interface",
        output="screen",
        parameters=[{"robot_config": f"{robot_config.perform(context)}"}],
    )

    return [
        gazebo,
        fake_gz_interface,
        spawn_entity,
    ]


def generate_launch_description():

    cucr_worlds_small_house_dir = FindPackageShare(
        package="cucr_worlds_small_house"
    ).find("cucr_worlds_small_house")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "robot_name", default_value="reachy", description="Set robot name."
            ),
            DeclareLaunchArgument(
                "robot_config",
                default_value="full_kit",
                description="Robot configuration.",
            ),
            DeclareLaunchArgument(
                "world",
                default_value=[
                    cucr_worlds_small_house_dir + "/worlds/small_house.world"
                ],
                description="Path of the world to show.",
            ),
            DeclareLaunchArgument(
                "x_pose",
                default_value="0",
                description="X position for robot spawn.",
            ),
            DeclareLaunchArgument(
                "y_pose",
                default_value="0",
                description="Y position for robot spawn.",
            ),
            OpaqueFunction(function=launch_setup),
        ]
    )
