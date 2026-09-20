## =========================================================
# launch 설정
# - 여러 개의 노드를 한꺼번에 실행하도록 설정
# - 1. 실행할 노드 관련 정보를 LaunchDescription에 저장
# - 2. launch.py 파일에 대한 정보 설정
#       * package.xml - 해당 패키지 구동에 필요한 패키지 정보 제공 
#       * setup.py - launch 폴더 등록하고 ROS2의 share 사용 알림
#                    data_files 항목에 설정 추가
## =========================================================
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. 시뮬레이터 노드
        Node(
            package='turtlesim', 
            executable='turtlesim_node'
        ),
        
        # 2. 키보드 제어 노드 (터미널 분리 설정 추가)
        Node(
            package='turtlesim', 
            executable='turtle_teleop_key', 
            output='screen', 
            prefix='xterm -e', 
            emulate_tty=True    
        ), 
    ])