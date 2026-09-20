## ------------------------------------------------------------
## [토픽 방식] 발행 노드 클래스 정의 및 발행
## ------------------------------------------------------------
## - 이미지 데이터 발생 구조
##  * 타입: sensor_msgs/msg/Image
## ------------------------------------------------------------
## 모듈 로딩
## ------------------------------------------------------------
import rclpy                          # 개발 언어 파이썬 라이브러리
from rclpy.node import Node           # 노드 클래스 패키지
from sensor_msgs.msg import Image     # 카메라 이미지 메시지 패키지


## ------------------------------------------------------------
## 전역 변수
## ------------------------------------------------------------
NODE_NAME = "image_pub"               # 노드명
TOPIC_NAME = "/camera/image"           # 토픽명
QUEUE_SIZE = 10                       # 메시지 저장 공간 크기


## ------------------------------------------------------------
## 클래스이름 : ImagePublisher
## 부모클래스 : Node
## 클래스역할 : 1초마다 camera/image 토픽에 빈 이미지를 발행한다 (구조 이해용, cv_bridge 미사용)
## 클래스속성 : pub(Publisher), timer(1초 주기 Timer)
## 클래스기능 : timer_callback — Timer가 1초마다 자동으로 호출하는 콜백
## ------------------------------------------------------------
class ImagePublisher(Node):

    # __init__ : 노드를 초기화하고 Publisher·Timer를 준비한다
    def __init__(self):
        super().__init__(NODE_NAME)
        self.pub = self.create_publisher(Image, TOPIC_NAME, QUEUE_SIZE)
        self.timer = self.create_timer(1.0, self.timer_callback)

    # timer_callback : 1초마다 자동 호출 — 필드를 채운 Image를 발행한다
    def timer_callback(self):
        # 이미지 데이터 준비
        msg = Image()
        msg.header.frame_id = 'camera'
        msg.height = 10
        msg.width = 10
        msg.encoding = 'mono8'                     # 흑백 1채널
        msg.step = msg.width                       # 가로 한 줄의 바이트 수
        msg.data = [0] * (msg.height * msg.width)  # 전부 0(검은색)으로 채운 가짜 값
        
        # 이미지 데이터 발행
        self.pub.publish(msg)
        
        # 디버깅/확인용
        self.get_logger().info(f'발행: {msg.width}x{msg.height}, data 길이={len(msg.data)}')
        

## ------------------------------------------------------------
# Entry point 함수: 토픽 발행 기능
## ------------------------------------------------------------
def main(args=None):
    # ROS 통신 초기화
    rclpy.init(args=args)
    
    # 토픽 발행 인스턴스 생성
    node = ImagePublisher()

    # 지정된 간격으로 토픽 발행
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('종료됨!')
        # pass
    finally:
        # ROS 통신 종료 및 자원 반납
        node.destroy_node()
        rclpy.shutdown()


## ------------------------------------------------------------
## 실행 여부에 따른 처리 부분
## ------------------------------------------------------------
if __name__ == '__main__':
    main()
