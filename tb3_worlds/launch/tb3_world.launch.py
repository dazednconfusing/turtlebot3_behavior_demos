from os.path import join

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    tb3_gazebo_dir = get_package_share_directory("turtlebot3_gz")
    gazebo_ros_dir = get_package_share_directory("ros_gz")

    use_sim_time = LaunchConfiguration("use_sim_time", default="true")
    x_pose = LaunchConfiguration("x_pose", default="0.0")
    y_pose = LaunchConfiguration("y_pose", default="0.0")

    tb3_world_dir = get_package_share_directory("tb3_worlds")
    default_map = join(tb3_world_dir, "maps", "sim_house_map.yaml")
    default_world = join(tb3_world_dir, "worlds", "sim_house.world")

    # Start Gazebo server and client
    gazebo_spawn_world = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-file', default_world],
        )

    # Spawn the turtlebot
    spawn_turtlebot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            join(tb3_gazebo_dir, "launch", "gz_sim.launch.py")
        )
    )

    return LaunchDescription(
        [
            gazebo_spawn_world,
            spawn_turtlebot,
        ]
    )
