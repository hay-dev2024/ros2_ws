## ------------------------------------------------------------
## [토픽 방식] 발행 노드 클래스 정의 및 발행
## ------------------------------------------------------------
## - 센서 데이터 발생 구조
##  * 타입: sensor_msgs/msg/Imu
##  * 구성: 가속도계 - 직선가속도(급정지/급가속), 자이로스코프 - 회전가속도, 지자기계 - 방위
## ------------------------------------------------------------
## 모듈 로딩
## ------------------------------------------------------------
import rclpy                      # 개발 언어 파이썬 라이브러리
from rclpy.node import Node       # 노드 클래스 패키지
from sensor_msgs.msg import Imu   # 자세·가속도 메시지 패키지

## ------------------------------------------------------------
## 전역 변수
## ------------------------------------------------------------
NODE_NAME = "imu_pub"              # 노드명
TOPIC_NAME = "imu"                 # 토픽명
QUEUE_SIZE = 10                    # 메시지 저장 공간 크기


## ------------------------------------------------------------
## 클래스이름 : ImuPublisher
## 부모클래스 : Node
## 클래스역할 : 1초마다 imu 토픽에 가짜 Imu 메시지를 발행한다 (구조 이해용, 정지 상태 가정)
## 클래스속성 : pub(Publisher), timer(1초 주기 Timer)
## 클래스기능 : timer_callback — Timer가 1초마다 자동으로 호출하는 콜백
## ------------------------------------------------------------
class ImuPublisher(Node):

    # __init__ : 노드를 초기화하고 Publisher·Timer를 준비한다
    def __init__(self):
        super().__init__(NODE_NAME)
        self.pub = self.create_publisher(Imu, TOPIC_NAME, QUEUE_SIZE)
        self.timer = self.create_timer(1.0, self.timer_callback)

    # timer_callback : 1초마다 자동 호출 — 필드를 채운 Imu를 발행한다
    def timer_callback(self):
        # IMU 센서 데이터 준비 - 실제 측정된 센서값 저장
        msg = Imu()
        msg.header.frame_id = 'imu_link'
        msg.orientation.w = 1.0              # w - 회전. 회전 없음(단위 쿼터니언) 가정
        msg.angular_velocity.x = 0.0         # 회전 속도 없음 가정
        msg.linear_acceleration.z = 9.8      # 중력가속도만 있다고 가정(정지 상태)
        
        # IMU 센서 정보 발행
        self.pub.publish(msg)
        self.get_logger().info(f'발행: linear_acceleration.z={msg.linear_acceleration.z}')


## ------------------------------------------------------------
# Entry point 함수: 토픽 발행 기능
## ------------------------------------------------------------
def main(args=None):
    rclpy.init(args=args)
    node = ImuPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
