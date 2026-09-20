import rclpy                              # 개발 언어 파이썬 라이브러리
from rclpy.node import Node               # 노드 클래스 패키지
from sensor_msgs.msg import LaserScan     # LiDAR 거리 메시지 패키지

NODE_NAME = "laserscan_pub"                # 노드명
TOPIC_NAME = "scan"                        # 토픽명
QUEUE_SIZE = 10                            # 메시지 저장 공간 크기


## ------------------------------------------------------------
## 클래스이름 : LaserScanPublisher
## 부모클래스 : Node
## 클래스기능 : 1초마다 scan 토픽에 가짜 LaserScan 메시지를 발행한다 (구조 이해용)
## 속성 / 필드  : pub(Publisher), timer(1초 주기 Timer)
## 메    서    드  : timer_callback — Timer가 1초마다 자동으로 호출하는 콜백
## ------------------------------------------------------------
class LaserScanPublisher(Node):

    # __init__ : 노드를 초기화하고 Publisher·Timer를 준비한다
    def __init__(self):
        super().__init__(NODE_NAME)
        self.pub = self.create_publisher(LaserScan, TOPIC_NAME, QUEUE_SIZE)
        self.timer = self.create_timer(1.0, self.timer_callback)

    # timer_callback : 1초마다 자동 호출 — 필드를 채운 LaserScan을 발행한다
    def timer_callback(self):
        # 레이저 센서 데이터 준비 <- 실제 센서값들
        msg = LaserScan()
        msg.header.frame_id = 'laser'
        msg.angle_min = -3.14
        msg.angle_max = 3.14
        msg.angle_increment = 0.0175
        msg.range_min = 0.1
        msg.range_max = 10.0
        msg.ranges = [3.0] * 360          # 360개 각도 모두 3.0m로 가정 (가짜 값)
        
        # 토픽 발생 및 로그 출력
        self.pub.publish(msg)
        self.get_logger().info(f'발행: ranges 개수={len(msg.ranges)}, 첫 값={msg.ranges[0]}')


# main : 노드를 생성해 spin(대기·실행)시키고, 종료 시 자원을 정리한다
def main(args=None):
    rclpy.init(args=args)
    node = LaserScanPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
