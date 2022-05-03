# socket 모듈을 import
from socket import *

# serverName을 “localhost”로 지정한 후 serverPort를 12000으로 설정
# Server를 위한 TCP 소켓을 생성하고 Server와의 connection을 setup
serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# 어떤 HTTP 프로토콜 request를 요청할 것인지 입력 받고 Server로 전달
method = input("HTTP Protocol Method: ")
clientSocket.send(method.encode())

# Server가 보낸 응답을 reponse 변수에 저장하고 decode한 결과를 출력
response = clientSocket.recv(1024)
print(response.decode())

# Server와의 connection을 끊기
clientSocket.close()
