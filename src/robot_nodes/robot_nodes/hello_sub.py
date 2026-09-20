import rclpy                          # 개발 언어 파이썬 라이브러리
from rclpy.node import Node           # 노드 클래스 패키지
from std_msgs.msg import String       # 문자열 메시지 패키지

NODE_NAME = "hello_sub"               # 노드명
TOPIC_NAME = "greeting"                # 토픽명 (hello_pub과 반드시 동일해야 함)
QUEUE_SIZE = 10                        # 메시지 저장 공간 크기


## ------------------------------------------------------------
## 클래스이름 : HelloSubscriber
## 부모클래스 : Node
## 클래스기능 : greeting 토픽을 구독해 도착한 메시지를 로그로 출력한다
## 속성 / 필드  : sub(Subscription)
## 메    서    드  : listener_callback — 메시지 도착 시 ROS2가 자동으로 호출하는 콜백
## ------------------------------------------------------------
class HelloSubscriber(Node):

    # __init__ : 노드를 초기화하고 greeting 토픽을 구독한다
    def __init__(self):
        super().__init__(NODE_NAME)
        self.sub = self.create_subscription(
            String, TOPIC_NAME, self.listener_callback, QUEUE_SIZE)

    # listener_callback : 메시지 도착 시 자동 호출 — 받은 데이터를 로그로 출력한다
    def listener_callback(self, msg):
        self.get_logger().info(f'수신: {msg.data}')


# main : 노드를 생성해 spin(대기·실행)시키고, 종료 시 자원을 정리한다
def main(args=None):
    rclpy.init(args=args)
    node = HelloSubscriber()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
