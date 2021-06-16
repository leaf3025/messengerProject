# python 내장 소켓 모듈
from socket import *
# python 내장 스레드 모듈
from _thread import *


# 메신저 클라이언트 클래스
class msgClient:
    """
        __init__: 메신저 클라이언트(msgClient) 생성자
        IP: 메신저 서버의 IP주소
        PORT: 메신저 서버의 PORT
    """

    def __init__(self, IP, PORT):
        # 소켓 설정
        # AF_INET: IPv4 사용
        # SOCK_STREAM: TCP 통신
        self.cSock = socket(AF_INET, SOCK_STREAM)

        # 서버와 연결(connect)
        self.cSock.connect((IP, PORT))

    """
        recvMsg: 소켓으로 넘어오는 데이터를 수신하는 함수
    """

    def recvMsg(self):
        # 무한 루프를 돌면서
        while True:
            # 1024Bytes 만큼 데이터를 계속 읽어 들인다.
            msg = self.cSock.recv(1024).decode("utf-8")

            # 만약, 넘어온 데이터(상대방이 입력한 메시지)가 exit면 상대방이 종료했다는 뜻
            if (msg == "exit"):
                print("\n[*] 상대방이 퇴장했습니다.\n")

            # 상대방이 접속하지 않았으면, 서버에서 [*] 상대방 접속을 기다리는 중... 메시지가 넘어온다.
            # 이에 대한 출력 처리
            elif (msg == "[*] 상대방 접속을 기다리는 중..."):
                print("\n[*] 상대방 접속을 기다리는 중...\n")

            # 위의 경우가 아니라면, 상대방에게서 온 메시지 출력
            else:
                print("\n< " + msg)

    """
        chat: 서버 연결 후, 스레드로 recvMsg()를 실행하고 메시지를 보낼 수 있는 상태로 전환
    """

    def chat(self):
        # start_new_thread: _thread 모듈 함수로 새로운 스레드를 시작하는 함수
        # recvMsg()함수를 스레드에 올려서 비동기적인 메시지 수신이 가능하도록 한다.
        start_new_thread(self.recvMsg, ())

        # 무한 루프를 돌면서
        while True:
            # 상대방에게 보낼 메시지 입력
            msg = input("> ")

            # 만약, 입력한 메시지가 exit면 해당 메시지를 상대방에게 보내고, thread 종료 후 반복문을 빠져나간다.
            if (msg == "exit"):
                self.cSock.sendall(msg.encode())
                exit()
                break

            # 위의 경우가 아니라면, 상대방에게 입력한 메시지를 보낸다.
            else:
                self.cSock.sendall(msg.encode())

        # 반복문이 종료되면 소켓을 닫고 프로그램을 종료한다.
        self.cSock.close()


if __name__ == "__main__":
    # msgClient 객체를 생성하면서, 서버(127.0.0.1:8888)와 연결(connect)
    mClient = msgClient("127.0.0.1", 8888)
    # 채팅 로직 시작
    mClient.chat()