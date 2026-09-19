# 토픽 수신 클래스
# 실행: ros2 run robot_nodes listener (heartbeat와 다른 터미널에서!)
# 핵심 문장: 콜백을 직접 부르지 않음. 메시지가 도착하면 ROS2가 대신 호출!

from std_msgs.msg import String
import rclpy
from rclpy.node import Node


## -----------------------------------------------------
## 클래스이름 : Listener
## 클래스역할 : /system/heartbeat 토픽을 구독(Subscribe)하는 노드 클래스
##            도착한 메시지를 '받음: alive:N' 로그로 보여주는 ROS2 노드
## 부모클래스 : Node
## 클래스속성 : sub - Subscription 객체 (String, /system/heartbeat, 큐 10)
## 오버라이딩 : __init__(): 인스턴스 속성 초기화
## 클래스기능 : callback(): 토픽 수신 시 자동 실행되는 메소드
## -----------------------------------------------------
class Listener(Node):

    ## ------------
    ## 메서드기능 : 부모(Node) 초기화로 노드 이름 'listener' 등록 후
    ##              구독할 토픽과 콜백 함수를 지정
    ## 메서드이름 : __init__
    ## 매개변수들 : self
    ## 메서드결과 : 없음 (속성 초기화)
    ## ------------
    def __init__(self):
        super().__init__('listener')                    # 부모 준비 먼저 (super)
        self.sub = self.create_subscription(String, '/system/heartbeat', self.callback, 10)  # 도착하면 callback 자동 호출

    ## ------------
    ## 메서드기능 : 수신한 메시지의 data를 '받음:' 로그로 출력
    ##            (직접 호출하지 않음. 메시지 도착 시 ROS2가 자동 호출하는 콜백)
    ## 메서드이름 : callback
    ## 매개변수들 : self
    ##            msg - 수신한 메시지 객체 (std_msgs.msg.String)
    ## 메서드결과 : 없음 (터미널 로그 출력)
    ## ------------
    def callback(self, msg):
        self.get_logger().info(f'받음: {msg.data}')


## ------------
## 함수기능   : rclpy 초기화 → 노드 생성 → spin으로 콜백 실행 유지
##              → 종료(Ctrl+C) 시 노드·통신 자원 정리
## 함수이름   : main
## 매개변수들 : args - ROS 실행 인자 (기본값 None)
## 함수결과   : 없음
## ------------
def main(args=None):
    # ROS Node 및 통신 초기화
    rclpy.init(args=args)
    
    # 인스턴스 노드 생성
    node = Listener()
    
    # 무한반복으로 수신
    try:
        rclpy.spin(node)
    # 키보드 인터럽트 발생 시 종료
    except KeyboardInterrupt:
        pass
    finally:
        # 통신 종료에 따른 정리. 즉, 컴퓨터 자원 반납
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
