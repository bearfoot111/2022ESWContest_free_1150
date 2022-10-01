# Ultrasonicwave


<img src="https://user-images.githubusercontent.com/109472852/193396751-b2765428-2a0f-4d6c-b92c-2c3be187fb52.png" height="300px" width="300px">


* #### 아두이노 초음파센서 HC-SR04<br>
<br>

Echo Pin의 High 펄스 간격 = 펄스가 반사되고 물체에 부딪힌 후 돌아오기까지의 시간이므로, 아래의 코드와 같이<br>
<br>

> Echo Pin의 High 펄스 간격 / 2 = 장애물과의 거리 값<br>
<br>

과 같은 식을 도출할 수 있다. 


```
        check_time = stop - start
        distance = check_time * 34300 / 2
        print("Distance : %.1f cm" % distance)
```

장애물과의 거리가 40cm 이하일 경우, sever로 "stop!!!"이라는 메세지를 보낸다.

```
        if(distance<=40):
            print("stop!!!")
            sock2.sendall('Stop!'.encode())
        else:
            print("RUN!")
            sock2.sendall('Run!'.encode())
        time.sleep(1)
```


# Motor

server로부터 받은 전역변수 motor_control에 저장된 값에 따라 모터를 제어한다. 정리된 표와 코드는 다음과 같다.  
<br>


| motor_control | 모터 동작 |
| :----: | :-----: |
| 1 |우회전|
| 2 |좌회전|
| 3 |직진|
| 4 |정지|
| 5 |간판 인식 실행|
| 6 |정지 점자블록 인식->정지|  


<br>
<br>


```
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
```
