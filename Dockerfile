# image는 Docker Hub에서 제공하는 python:3 사용 
FROM python:3

# sourceCode 디렉터리에 위치한 msgServer.py를 컨테이너 내부로 복사
COPY sourceCode/msgServer.py msgServer.py

# image가 실행되면 아래 명령어 시작 (python msgServer.py / 메시지 서버 시작)
CMD python msgServer.py
