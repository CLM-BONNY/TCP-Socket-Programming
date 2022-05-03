# socket 모듈, datetime 모듈을 import
from socket import *
from datetime import datetime

# serverName을 “localhost”로 지정한 후 serverPort를 12000으로 설정
# Client의 요청에 따른 TCP welcome 소켓을 생성하고 소켓에 포트번호를 부여
# Client로부터 들어오는 HTTP 프로토콜 request 요청을 한 번에 한 connection씩만 받기 시작하며 서버가 요청을 받을 준비가 되었다는 내용의 메시지를 출력
serverName = "localhost"
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

# HTTP 프로토콜 request의 응답 형식을 reponse 변수에 미리 담아 놓는다.
response = "HTTP/1.1 {header[0]} {header[1]}\nDate: {date}\nHost: {url}\n" \
           "Content-Type: text/html\nContent-Length:{len}\n\n{body}\n"

'''
GET 요청이 들어왔을 때 실행할 함수
1) Client로부터 온 요청에 이미 가지고 있는 index.html이 포함되어 있으면 변수 response에 200 OK와 각각의 값들을 넣는다.(파일 내용 포함)
2) Client로부터 온 요청에 이미 가지고 있는 index.html이 포함되어 있지 않으면 변수 response에 404 NOT FOUND를 넣는다.
3) Client에게 변수 response를 응답으로 보낸다. 
'''
def GET(connect):
    global response, serverName, method
    if "index.html" in method:
        with open("index.html", encoding="utf-8") as f:
            content = f.read()
        response = response.format(header=[200, "OK"], date=datetime.now(),
                                   url=serverName, len=len(content), body=content)
    else:
        response = "HTTP/1.1 400 NOT FOUND"
    connect.send(response.encode())


'''
HEAD 요청이 들어왔을 때 실행할 함수
1) Client로부터 온 요청에 이미 가지고 있는 index.html이 포함되어 있으면 변수 response에 200 OK와 각각의 값들을 넣는다. (파일 내용 미포함)
2) Client로부터 온 요청에 이미 가지고 있는 index.html이 포함되어 있지 않으면 변수 response에 404 NOT FOUND를 넣는다.
3) Client에게 변수 response를 응답으로 보낸다.
'''
def HEAD(connect):
    global response, serverName
    if "index.html" in method:
        with open("index.html", encoding="utf-8") as f:
            content = f.read()
        response = response.format(header=[200, "OK"], date=datetime.now(),
                                   url=serverName, len=len(content), body="")
    else:
        response = "HTTP/1.1 400 NOT FOUND"
    connect.send(response.encode())


'''
PUT 요청이 들어왔을 때 실행할 함수(P태그의 내용 변경하는 작업 실행, 없는 파일 이름으로 요청이 들어왔을 경우 새 파일 생성)
1) Client로부터 온 요청에 이미 가지고 있는 index.html이 포함되어 있으면 index.html 파일을 열고 내용을 읽어서 변수 line에 한번에 넣는다. index.html 파일을 다시 열고 반복문을 돌면서 파일을 다시 쓰고 해당 줄에 p태그가 있으면 멈춘다. Client로부터 온 요청에서 변경하기 원하는 파일 내용을 저장한 변수인 text로 p태그의 내용을 바꾼다.
2) Client로부터 온 요청에 이미 가지고 있는 index.html이 포함되어 있지 않으면 Client로부터 온 요청에서 파일명을 저장한 변수인 filename을 이름으로 하는 파일을 열고 Client로부터 온 요청에서 변경하기 원하는 파일 내용을 저장한 변수인 text를 파일 내용으로 한다.
3) 변수 response에 200 OK와 각각의 값들을 넣는다.(파일 내용 포함)
4) Client에게 변수 response를 응답으로 보낸다.
'''
def PUT(connect):
    global response, serverName, method
    method = method.split()
    filename = method[1]
    text = method[2]
    if "index.html" in method:
        with open("index.html", encoding="utf-8") as f:
            lines = f.readlines()

        with open("index.html", "w") as f:
            for line in lines:
                if "<p>" in line:
                    line = "    <p>" + text + "</p>\n"
                f.write(line)

        with open("index.html", encoding="utf-8") as f:
            content = f.read()

    else:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

        with open(filename, encoding="utf-8") as f:
            content = f.read()

    response = response.format(header=[200, "OK"], date=datetime.now(),
                               url=serverName, len=len(content), body=content)
    connect.send(response.encode())


'''
POST요청이 들어왔을 때 실행할 함수(새 파일 생성)
1) Client로부터 온 요청에서 파일명을 저장한 변수인 filename을 이름으로 하는 파일을 열고 Client로부터 온 요청에서 변경하기 원하는 파일 내용을 저장한 변수인 text를 파일 내용으로 한다.
2) 변수 response에 200 OK와 각각의 값들을 넣는다.(파일 내용 포함)
3) Client에게 변수 response를 응답으로 보낸다.
'''
def POST(connect):
    global response, serverName, method
    method = method.split()
    filename = method[1]
    text = method[2]

    with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

    with open(filename, encoding="utf-8") as f:
            content = f.read()

    response = response.format(header=[200, "OK"], date=datetime.now(),
                               url=serverName, len=len(content), body=content)
    connect.send(response.encode())

# 계속 반복문을 돌면서 Client로부터 들어올 HTTP 프로토콜 Request 요청, 새로운 소켓 생성을 대기
# 소켓으로부터 바이트 단위로 HTTP 프로토콜 Request 요청을 읽어서 method 변수에 저장
# GET/HEAD/PUT/POST 중 Client로부터 들어온 요청에 해당하는 함수를 실행
# 만약 다른 입력 값이 들어올 경우 다시 입력해달라는 메시지를 전송
while True:
    connectionSocket, addr = serverSocket.accept()
    method = connectionSocket.recv(1024).decode()
    if "GET" in method:
        GET(connectionSocket)
    elif "HEAD" in method:
        HEAD(connectionSocket)
    elif "PUT" in method:
        PUT(connectionSocket)
    elif "POST" in method:
        POST(connectionSocket)
    else:
        response = "Please enter another method"
        connectionSocket.send(response.encode())

# 이번에 연결된 Client와의 connect을 끊기
    connectionSocket.close()
