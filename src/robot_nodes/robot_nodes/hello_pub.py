import rclpy                          # 개발 언어 파이썬 라이브러리
from rclpy.node import Node           # 노드 클래스 패키지
from std_msgs.msg import String       # 문자열 메시지 패키지

NODE_NAME = "hello_pub"               # 노드명
TOPIC_NAME = "greeting"                # 토픽명
QUEUE_SIZE = 10                        # 메시지 저장 공간 크기


## ------------------------------------------------------------
## 클래스이름 : HelloPublisher
## 부모클래스 : Node
## 클래스기능 : 1초마다 greeting 토픽에 문자열 메시지를 발행한다
## 속성 / 필드  : pub(Publisher), timer(1초 주기 Timer), count(발행 횟수)
## 메    서    드  : timer_callback — Timer가 1초마다 자동으로 호출하는 콜백
## ------------------------------------------------------------
class HelloPublisher(Node):

    # __init__ : 노드를 초기화하고 Publisher·Timer를 준비한다
    def __init__(self):
        super().__init__(NODE_NAME)
        self.pub = self.create_publisher(String, TOPIC_NAME, QUEUE_SIZE)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0

    # timer_callback : 1초마다 자동 호출 — 메시지를 만들어 발행한다
    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS2 {self.count}'
        self.pub.publish(msg)
        self.get_logger().info(f'발행: {msg.data}')
        self.count += 1


# main : 노드를 생성해 spin(대기·실행)시키고, 종료 시 자원을 정리한다
def main(args=None):
    rclpy.init(args=args)
    node = HelloPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
