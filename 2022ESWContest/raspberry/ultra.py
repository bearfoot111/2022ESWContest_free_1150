import cv2
import socket
import numpy as np
import time
import threading
from gpiozero import Robot
from gpiozero import Motor
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24
print("초음파 거리 측정기")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("초음파 출력 초기화")
time.sleep(2)

TCP_IP = '000.000.000.00'
TCP_PORT = 50002

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2.connect((TCP_IP, TCP_PORT))
print('connect2')

def sendsensor(sock2):
    while True:
        GPIO.output(TRIG,True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        print("before echo")
        while GPIO.input(ECHO)==0:
            start = time.time()
        print("echo=0")
        while GPIO.input(ECHO)==1:
            stop = time.time()
        print("echo=1")

        check_time = stop - start
        distance = check_time * 34300 / 2
        print("Distance : %.1f cm" % distance)
        if(distance<=40):
            print("stop!!!")
            sock2.sendall('Stop!'.encode())
        else:
            print("RUN!")
            sock2.sendall('Run!'.encode())
        time.sleep(1)

sender2 = threading.Thread(target=sendsensor, args=(sock2,))
sender2.start()
while True:
    time.sleep(1)
    pass
