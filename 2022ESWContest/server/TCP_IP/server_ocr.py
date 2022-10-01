import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
import time
import socket

# socket에서 수신한 버퍼를 반환하는 함수
def recvall(sock, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf
HOST = '0.0.0.0' # cmd에서 확인한 IP주소
PORT = 50001 # port 번호

# 소켓 생성
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# 서버의 아이피와 포트번호 지정
s.bind((HOST, PORT))
print('Socket bind complete')

# 클라이언트의 접속을 기다린다. (클라이언트 연결을 1개까지 받는다)
s.listen(1)
print('Socket now listening')

# 연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
conn, addr = s.accept()
reader = easyocr.Reader(['en', 'ko'], gpu=True)
while True:
    # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = np.frombuffer(stringData, dtype='uint8')
    # data를 디코딩한다.
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    result = reader.readtext(gray)
    text = ""
    for res in result:
        text += res[1] + " "
    cv2.putText(frame, text, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
    cv2.imshow('ImageWindow', frame)
    cv2.waitKey(1)
