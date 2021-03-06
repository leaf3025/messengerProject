## 1:1 메신저 프로그램 ##
> **요구 사항**
- 멀티 스레딩 활용
- 소켓 프로그래밍
- Docker를 활용한 서버 구축

        docker build -t msgserver:1.0 .
        docker run -d -p 8888:8888 msgserver:1.0
> **개요 및 목적**

CS구조의 1:1 메신저 프로그램 개발을 목적으로 한다.

두 개의 클라이언트가 서버에 연결요청을 하면, 서버는 중간에서 메시징 서비스를 중계한다.

> **설계 및 기능**

####클라이언트

메시지 전송(send)과 메시지 수신(recv)를 비동기적으로 처리하기 위해 멀티 스레드 활용

**메인 스레드**: 메시지 입력 및 전송(send) 처리

**자식 스레드**: 메시지 수신(recv) 및 출력 처리

####서버 
Docker Hub에서 제공하는 python:3으로 서버 구축 (Dockerfile 활용)

각 클라이언트의 연결과 메시지 릴레이를 비동기적으로 처리하기 위해 멀티 스레드 활용

**메인 스레드**: 각 클라이언트의 연결 요청 처리

**자식 스레드1**: 첫 번째 클라이언트 메시지 처리 (send/recv)

**자식 스레드2**: 두 번째 클라이언트 메시지 처리 (send/recv)

> **차이점**

단일 스레드일 경우, 메시지를 입력하고 발신(send)할 때 수신(recv)이 불가능하다.

멀티 스레드로 구현하면 수신(recv)/발신(send)의 비동기적인 처리가 가능해진다.


> **개발 스펙**
- python 3.7
- Docker
- python 내장 소켓 모듈
- python 내장 스레드 모듈


> **실행 화면**

도커빌드
<img width="1587" alt="dockerBuild" src="https://user-images.githubusercontent.com/70615588/122151129-f3c4a100-ce99-11eb-8114-414c8e820b9d.png">



클라이언트_접속_대기
<img width="561" alt="clientWait" src="https://user-images.githubusercontent.com/70615588/122151140-f921eb80-ce99-11eb-97b7-7f913603e45e.png">


채팅
<img width="1442" alt="chat" src="https://user-images.githubusercontent.com/70615588/122151146-fd4e0900-ce99-11eb-8199-58fd52ec81ba.png">

