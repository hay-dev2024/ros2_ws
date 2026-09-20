"""8일차 실습 — day8_world.sdf 실행 + ROS2<->Gazebo 브리지 기동.

사용:
    ros2 launch robot_gazebo sim.launch.py
"""
## ----------------------------------------------------------------------------------
## 모듈 로딩
## ----------------------------------------------------------------------------------
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

## ----------------------------------------------------------------------------------
## 함수기능 : 여러개 노드 실행을 위한 설정 객체 즉, LaunchDescription 인스턴스 생성 및 반환
## ----------------------------------------------------------------------------------
def generate_launch_description():
    # 노드 실행을 위한 설정 파일 경로 추출
    pkg_share = get_package_share_directory('robot_gazebo')
    world_path = os.path.join(pkg_share, 'worlds', 'day8_world.sdf')
    bridge_config = os.path.join(pkg_share, 'config', 'bridge.yaml')

    # WSL2 등 GPU 렌더링이 불안정한 환경에서 Gazebo 창이 비거나
    # gpu_lidar 값이 전부 0.0으로 나오는 문제를 예방 — 소프트웨어 렌더링 강제
    # force_software_render = SetEnvironmentVariable('LIBGL_ALWAYS_SOFTWARE', '1')

    # 가제보 시뮬레이션 launch 파일 경로 추출
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r {world_path}'}.items(),
    )

    # 가제보와 ROS 코드 연동 설정
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        parameters=[{'config_file': bridge_config}],
        output='screen',
    )

    # return LaunchDescription([force_software_render, gz_sim, bridge])
    return LaunchDescription([gz_sim, bridge])
