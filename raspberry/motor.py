import cv2
import socket
import numpy as np
import time
import threading
from gpiozero import Robot
from gpiozero import Motor

dc_motorL = Motor(forward=12, backward=16)
dc_motorR = Motor(forward=20, backward=21)

TCP_IP = '000.000.000.00'
TCP_PORT = 50001s
motor_control = "4"
prev_motor_control = "4"
startTime = time.time()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
print('connect')

capture = cv2.VideoCapture(0)
capture2 = cv2.VideoCapture(1)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
prev_time = 0

def motor():
    global motor_control
    print(motor_control)
    if(motor_control[0]=="2"):
        print('left')
        dc_motorR.backward(speed=0.3)
        dc_motorL.forward(speed=1)
    elif(motor_control[0]=="1"):
        print('right')
        dc_motorR.backward(speed=1)
        dc_motorL.forward(speed=0.3)
    elif(motor_control[0]=="3"):
        print('go')
        dc_motorR.backward(speed=1)
        dc_motorL.forward(speed=1)

    elif(motor_control[0]=="4"):
        print('stop')
        dc_motorL.stop()
        dc_motorR.stop()
    elif(motor_control[0] =="5"):
        print('OCR')
        dc_motorL.stop()
        dc_motorR.stop()
    elif(motor_control[0] =="6"):
        print('stop for moment')
        dc_motorL.stop()
        dc_motorR.stop()
        time.sleep(2)
    else:
        print('else')
        dc_motorL.stop()
        dc_motorR.stop()
        time.sleep(1)

def send(sock):
    while True:
        global prev_time, motor_control
        if(motor_control=="5"):
            ret, frame = capture2.read()
        else:
            ret, frame = capture.read()
        current_time = time.time() - prev_time
        if (ret is True) and (current_time > 1./5):
            prev_time = time.time()

            result, frame = cv2.imencode('.jpg', frame, encode_param)
            data = np.array(frame)
            stringData = data.tobytes()

            sock.sendall((str(len(stringData))).encode().ljust(16) + stringData)


def receive(sock):
    while True:
        global motor_control, prev_motor_control
        recvData = sock.recv(1024)
        if recvData:
            motor_control = recvData.decode('utf-8')
            if(motor_control != prev_motor_control):
                motor()
            prev_motor_control = motor_control

sender = threading.Thread(target=send, args=(sock,))
receiver = threading.Thread(target= receive, args= (sock,))

sender. start()
receiver.start()

while True:
    time.sleep(1)
    pass

