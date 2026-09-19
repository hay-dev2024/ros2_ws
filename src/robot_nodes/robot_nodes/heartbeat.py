# ===============================================================
# 토픽 방식의 메시지 전송
# 실행:  ros2 run robot_nodes heartbeat   /   종료:  Ctrl+C
# ===============================================================
## -----------------------------------------------------
# 모듈 로딩
## -----------------------------------------------------
from std_msgs.msg import String   # 주고받을 메시지 타입
import rclpy                      # 파이썬 언어를 위한 ros 패키지
from rclpy.node import Node       # Node 클래스


## -----------------------------------------------------
## 클래스이름 : Heartbeat
## 클래스역할 : 1초마다 살아있음(alive:N)을 알리는 신호를
##              /system/heartbeat 토픽 이름으로 발행하는 ROS2 노드
## 부모클래스 : Node
## 클래스속성 : pub   - Publisher 객체 (String, /system/heartbeat, 큐 10)
##            seq   - 발행 순번 (0부터 1씩 증가)
##            timer - 1초 주기로 tick을 호출하는 Timer 객체
## 오버라이딩 : __init__(self) : 인스턴스 속성 초기화 
## 클래스기능 : tick(self)     : 1초 마다 메세지를 전송하는 메소드
## -----------------------------------------------------
class Heartbeat(Node):

    ## ------------
    ## 메서드기능 : 부모(Node) 초기화로 노드 이름 'heartbeat' 등록 후
    ##              Publisher·순번·Timer 속성 준비
    ## 메서드이름 : __init__
    ## 매개변수들 : self
    ## 메서드결과 : 없음 (속성 초기화)
    ## ------------
    def __init__(self):
        super().__init__('heartbeat')                   # 부모 준비 먼저 (super)
        self.pub = self.create_publisher(String, '/system/heartbeat', 10) # 문자열 메세지, 토픽이름, 메세지 저장크기
        self.seq = 0
        self.timer = self.create_timer(1.0, self.tick)  # 1초마다 tick 자동 호출

    ## ------------
    ## 메서드기능 : String 메시지 생성 → 토픽 발행 → 로그 출력 → 순번 증가
    ##              (직접 호출하지 않음. Timer가 1초마다 자동 호출하는 콜백)
    ## 메서드이름 : tick
    ## 매개변수들 : self
    ## 메서드결과 : 없음 (토픽 발행 + 터미널 로그 alive:N 출력)
    ## ------------
    def tick(self):
        # 메세지 담을 객체 생성 & 담기
        msg = String()
        msg.data = f'alive:{self.seq}'
        
        # 메세지 발송/전송
        self.pub.publish(msg)
        # 발송 로그 저장
        self.get_logger().info(msg.data)
        # 메세지 발송 카운트 증가
        self.seq += 1


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
    
    # 토픽 노드 인스턴스 생성 및 초기화
    node = Heartbeat()
    
    # 무한 루프 - 1초 간격으로 토픽 전송
    try:
        rclpy.spin(node)
    # 키보드 입력 발생 시 종료 - ctrl + c
    except KeyboardInterrupt:
        pass
    finally:
    # 무한 루프 및 키보드 입력에 따른 종료시 처리
        node.destroy_node()     # 실행 중인 노드 제거
        rclpy.try_shutdown()    # ROS 통신 종료
        

# 현재 py 파일이 실행될 때 동작하는 코드와
# import 될 때 구별을 위한 부분
if __name__ == '__main__':
    main()
