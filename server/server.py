import socket
import easyocr
import ctypes
import cv2
from matplotlib import pyplot as plt
import numpy as np
import time
import torch
import argparse
from multiprocessing import Process, Value, Array, Pool, Manager
import multiprocessing
from PIL import Image
from torchvision.transforms.functional import to_pil_image
import tensorflow as tf
from model.pspunet import pspunet
from data_loader.display import create_mask

stringData= ""
model = torch.hub.load('yolov5', 'custom', path='best_block_.pt', source='local')
model.to('cuda:0')
model.conf = 0.4

gpus = tf.config.experimental.list_physical_devices('GPU')

if gpus:
    try:
        tf.config.experimental.set_virtual_device_configuration(
       gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=500)])
    except RuntimeError as e:
        print(e)
        
IMG_WIDTH = 480
IMG_HEIGHT = 272
n_classes = 7

model1 = pspunet((IMG_HEIGHT, IMG_WIDTH ,3), n_classes)
model1.load_weights("pspunet_weight.h5")

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf
HOST = '000.000.000.00'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')

s.listen(2)
print('Socket now listening')

check = Value('i', 0)
sendresult = Value('i', 0)
ocr_check = Value('i', 0)
motor_move = Value('i', 0)
motor_move1 = Value('i', 0)
ocr_result = Array('c', 100)
ocr_result_check = Value('i', 0)
manager = Manager()
ocr_list_result = manager.dict()
ocr_count = Value('i', 0)
ocr_sound = Value('i', 0)
ocr_count_list = manager.list()
motor_stop = 0
stop_count = 10
prev_decode_data=""
decode_data=""

def road_seg(frame):
    frame = frame[tf.newaxis, ...]
    frame = frame/255
    pre = model1.predict(frame)
    pre = create_mask(pre).numpy()

    frame = frame/2
    frame[0][(pre==1).all(axis=2)] += [0, 0, 0]
    frame[0][(pre==2).all(axis=2)] += [0.5, 0.5,0]
    frame[0][(pre==3).all(axis=2)] += [0.2, 0.7, 0.5]
    #frame[0][(pre==4).all(axis=2)] += [0, 0.5, 0.5]
    frame[0][(pre==5).all(axis=2)] += [0, 0, 0.5]
    frame[0][(pre==6).all(axis=2)] += [0.5, 0, 0]

    frame = tf.squeeze(frame)
    frame = frame.numpy()
    frame = frame*255
    frame = np.uint8(frame)
    frame = to_pil_image(frame)
    frame = np.array(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

def yolo(frame):
    global stop_count
    global motor_stop
    results = model(frame)
    frame = np.squeeze(results.render())
    arr = results.xyxy[0].to('cuda:0')
    m = 0
    m_stop = 0
    index = -1
    index_stop = -1
    for i in range(len(arr)):
        if(arr[i][5]==0):
            if(arr[i][3]>m):
                m = arr[i][3]
                index = i
        else:
            if(arr[i][3]>m_stop):
                m_stop = arr[i][3]
                index_stop = i

    if(index!=-1):
        cx = (arr[index][0] + arr[index][2])/2
    else:
        cx = -1
    
    if(m_stop>m):
        if(motor_stop==0):
            stop_count -= 1
            cx = -2
            if(stop_count<0):
                motor_stop = 1
            
    else:
        motor_stop = 0
        stop_count = 10
        
    
    return frame, cx

def send(sock, check, sendresult):
    while True:
        if check.value==1:
            if(ocr_check.value ==1):
                sendresult.value=5
            sock.send(str(sendresult.value).encode('utf-8'))
            check.value=0
            
def app_check_recv(sock, ocr_check, motor_move, ocr_list_result, ocr_count):
    while True:
        global decode_data, prev_decode_data
        data = sock.recv(65535)
        decode_data = data.decode()
        if(decode_data!=prev_decode_data):
            print("app message : "+str(decode_data))
        if decode_data == "Stop":
            motor_move.value = 0
        elif decode_data == "run":
            motor_move.value = 1
        elif decode_data == "Run OCR":
            ocr_check.value = 1
            motor_move.value = 0
        elif decode_data == "Stop OCR":
            ocr_check.value = 0
            motor_move.value = 0
            ocr_list_result.clear()
            ocr_count.value = 0
        prev_decode_data = decode_data
            
def app_ocr_send(sock, ocr_list_result, ocr_check, ocr_result_check, ocr_count, ocr_sound, ocr_count_list):
    while True:
        if ocr_check.value == 1 and ocr_result_check.value == 1:
            if ocr_sound.value == 1:
                for i in ocr_count_list:
                    sock.send(ocr_list_result[i].encode(encoding='euc_kr'))
                    time.sleep(2)
                ocr_sound.value = 0
                ocr_count_list[:] = []
            ocr_result_check.value = 0

def ras_check_recv(sock, motor_move1):
    while True:
        global decode_data, prev_decode_data
        data = sock.recv(65535)
        decode_data = data.decode()
        if(prev_decode_data!=decode_data):
            if(decode_data=="Stop!"):
                print("raspberry message : obstacle detected")
            elif(decode_data=="Run!"):
                print("raspberry message : run")
        if decode_data == "Stop!":
            motor_move1.value = 0
        elif decode_data == "Run!":
            motor_move1.value = 1
        prev_decode_data = decode_data

conn, addr = s.accept()

sender = Process(target=app_ocr_send, args=(conn, ocr_list_result, ocr_check, ocr_result_check, ocr_count, ocr_sound, ocr_count_list))

sender.start()
recver = Process(target=app_check_recv, args=(conn, ocr_check, motor_move, ocr_list_result, ocr_count))


recver.start()


conn, addr = s.accept()
recver_ras = Process(target=ras_check_recv, args=(conn, motor_move1))
recver_ras.start()

conn, addr = s.accept()

sender_ras = Process(target=send, args=(conn, check, sendresult))

sender_ras.start()



count = 0

print('send and recv')
reader = easyocr.Reader(['en', 'ko'], gpu=True)
while True:
    if check.value==0:
        length = recvall(conn, 16)
        stringData = recvall(conn, int(length))
        data = np.frombuffer(stringData, dtype='uint8')
        frame2 = cv2.imdecode(data, cv2.IMREAD_COLOR)
        frame2 = cv2.resize(frame2, (IMG_WIDTH, IMG_HEIGHT))
        frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        frame_gray = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        count += 1
        if ocr_check.value == 1:
            if(count>20):
                result = reader.readtext(frame_gray)
                for res in result:
                    if res[1] in ocr_list_result.values():
                        pass
                    else:
                        ocr_count.value += 1
                        ocr_count_list.append(ocr_count.value)
                        ocr_list_result[ocr_count.value]=res[1]
                ocr_sound.value = 1
                ocr_result_check.value = 1
                count = 0
            frame2 = frame
            sendresult.value = 5
            check.value = 1
        else:
            if (motor_move.value != 0 and motor_move1.value != 0):
                frame2, cx = yolo(frame)

                if cx>=270:
                    sendresult.value = 1
                elif 0<=cx<= 210:
                    sendresult.value =2
                elif 210<cx<270:
                    sendresult.value =3
                elif cx==-1:
                    sendresult.value =3
                    frame2 = road_seg(frame)
                elif cx==-2:
                    sendresult.value = 6
                else:
                    sendresult.value =4
                check.value = 1
            else:
                sendresult.value = 4
                check.value = 1

        
        cv2.imshow('YOLO',frame2)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            s.close()
            break
        cv2.waitKey(1)
