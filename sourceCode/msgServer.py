# python 내장 소켓 모듈
from socket import *
# python 내장 스레드 모듈
from _thread import *
from time import sleep

# 메신저 서버 클래스
class msgServer:
    """
        __init__: 메신저 서버(msgServer) 생성자
        PORT: 소켓에 바인딩할 포트
    """
    def __init__(self,PORT):
        # AF_INET: IPv4 주소체계
        # SOCK_STREAM: TCP 통신
        self.sSock = socket(AF_INET, SOCK_STREAM)
        self.clientList = []

        # bind: 소켓과 네트워크 인터페이스를 연결하는 작업
        # '': Any Host (like 0.0.0.0)
        # port: 인자로 전달된 port에 서버 소켓 연결
        self.sSock.bind(('', PORT))

        # self.sSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        # listen: 다른 네트워크 연결을 기다리는 대기열 생성 (Queue 형식)
        self.sSock.listen()

    """
        connectWait: 클라이언트 접속을 대기하다가 연결 요청이 들어오면 연결을 처리(accept)하는 함수
    """
    def connectWait(self):
        print("[클라이언트 접속 대기중..]")

        # 무한 루프를 돌면서 클라이언트 연결 요청 대기
        while True:
            # 두개의 클라이언트가 접속하면 더이상 연결하지 않음
            if (len(self.clientList) == 2):
                pass

            # 아직 두개의 클라이언트가 연결되지 않았다면
            else:
                # accept: listen 대기열에 연결 요청이 생성되면 해당 소켓과 연결
                # cSock: 연결된 클라이언트의 소켓 정보
                # cAddr: 연결된 클라이언트의 주소 정보
                cSock, cAddr = self.sSock.accept()

                # 클라이언트 정보를 clientList 변수에 튜플 형태로 저장
                self.clientList.append((cSock, cAddr))

                # 만약, 접속된 클라이언트가 2명이 아니라면(clientList 길이가 2가 아니라면)
                if(len(self.clientList) != 2):
                    # 현재 연결된 클라이언트에게 [*] 상대방 접속을 기다리는 중... 메시지 전송
                    self.waitMsg(cSock)
                    # 전송 후, 1초 동안 기다림
                    sleep(1)

                # 만약, 접속된 클라이언트가 2명이라면
                else:
                    # 모든 클라이언트가 접속되었음을 각 클라이언트에게 알리고
                    self.startMsg()

                    # 각 클라이언트의 메시지를 비동기적으로 처리할 수 있도록 각 스레드에 recvClientMsg 맵핑
                    for client in self.clientList:
                        # start_new_thread: 새로운 스레드 시작
                        # recvClientMsg: 클라이언트에게 수신한 메시지를 처리하는 함수
                        # client[0]: 49번 라인에서 저장한 클라이언트 소켓 정보(cSock)
                        # client[1]: 49번 라인에서 저장한 클라이언트 주소 정보(cAddr)
                        start_new_thread(self.recvClientMsg, (client[0], client[1]))


    """
        recvClientMsg: 클라이언트에게 수신한 메시지를 처리하는 함수
        cSock: 클라이언트 소켓 정보
        cAddr: 클라이언트 주소 정보
    """
    def recvClientMsg(self, cSock, cAddr):
        print("\n[*] 클라이언트 접속 정보")
        print("     > IP: " + cAddr[0])
        print("     > PORT: " + str(cAddr[1]))

        # 무한 루프를 돌면서
        while True:
            # 클라이언트에서 수신되는 데이터를 1024Bytes 만큼 계속 읽어들임
            msg = cSock.recv(1024).decode("utf-8")

            # 클라이언트 리스트에서 현재 클라이언트 인덱스 가져오기
            idx = self.clientList.index((cSock, cAddr))

            # 만약, 수신된 데이터가 exit 라면 클라이언트가 퇴장한 것이므로,
            if (msg == "exit"):
                print("[*] 클라이언트 퇴장 정보")
                print("     > IP: " + cAddr[0])
                print("     > PORT: " + str(cAddr[1]))

                # 해당 인덱스 클라이언트 리스트에서 제거 후, 해당 스레드 종료
                self.clientList.pop(idx)
                exit()
                break

            # 위의 경우가 아니라면, 수신된 메시지를 상대방 클라이언트에게 전달
            else:
                if (msg):
                    print("[{PORT}]".format(PORT=str(cAddr[1])), end=' ')
                    # sendClientMsg: idx정보를 기반으로 상대 클라이언트 소켓으로 수신된 메시지(msg)를 전송하는 함수
                    self.sendClientMsg(idx, msg)

        # 클라이언트 소켓 제거
        cSock.close()

    """
       sendClientMsg: idx정보를 기반으로 상대 클라이언트 소켓으로 수신된 메시지(msg)를 전송하는 함수
       idx: msg를 전송한 클라이언트 인덱스
       msg: 클라이언트가 전송한 메시지
    """
    def sendClientMsg(self,idx,msg):
        # 만약, 클라이언트 인덱스가 1이라면,
        if(idx == 1):
            # currentClient(현재 클라이언트)에 1번 클라이언트 정보 저장 (로깅용)
            currentClient = self.clientList[1]
            # targetClient(상대 클라이언트)에 0번 클라이언트 정보 저장
            targetClient = self.clientList[0]

        # 위의 경우가 아니라면,
        else:
            # currentClient(현재 클라이언트)에 0번 클라이언트 정보 저장 (로깅용)
            currentClient = self.clientList[0]
            # targetClient(상대 클라이언트)에 1번 클라이언트 정보 저장
            targetClient = self.clientList[1]

        # 서버 로깅용으로 위에서 저장한 값 출력
        print("[{currentClient}]->[{targetClient}]".format(
            currentClient=currentClient[1],
            targetClient=targetClient[1]
        ))

        # targetClient에 저장된 클라이언트 소켓으로 메시지 전송
        # 0: 소켓 정보, 1: 주소 정보
        targetClient[0].sendall(msg.encode())

    """
        waitMsg: 현재 연결된 클라이언트에게 [*] 상대방 접속을 기다리는 중... 메시지 전송
        client: 현재 연결된 클라이언트 소켓 정보
    """
    def waitMsg(self,client):
        client.sendall("[*] 상대방 접속을 기다리는 중...".encode())


    """
        startMsg: 모든 클라이언트가 접속되었음을 각 클라이언트에게 알림
    """
    def startMsg(self):
        for client in self.clientList:
            client[0].sendall("[*] 모든 사용자가 입장했습니다.".encode())
        
    """
        close: 서버 소켓 종료
    """
    def close(self):
        self.sSock.close()

if __name__ == "__main__":
    mServer = msgServer(8888)
    mServer.connectWait()
    mServer.close()