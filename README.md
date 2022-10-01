# Team 맨발에서일인자까지1
## 팀원
| 이름 | 메일 |역할|
| ---- | ----- |------|
| 백민정 | b75391@naver.com |전체 기획 총괄<br/>TCP/IP 통신망 구축<br/>Flutter 앱 UI 개발<br/>3D 프린팅 도안 제작<br/>server-client 간 multi processing 구축<br/>보고서 작성 |
| 안진혁 | Content Cell  |server-client 간 multi processing 구축<br/>TCP/IP 통신망 구축<br/>GPU SERVER 원격 제어 환경 구축<br/>라즈베리 파이 multi threading 구현<br/>Road Segmentation 구현|
| 김채현 | baekchae1120@konkuk.ac.kr  |Road Segmentation 모델 학습<br/>라즈베리 파이 client 코드 개발<br/>TCP/IP 통신망 구축<br/>시연 영상 편집<br/>보고서 작성|
| 하채리 | hacherry05@naver.com  |YOLO 학습 모델 최적화<br/>Text detection 구현<br/>TCP/IP 통신망 구축<br/>라즈베리 파이 multi threading 구현<br/>보고서 작성 |
| 오희빈 | Content Cell  |YOLO 학습 모델 최적화<br/>Text detection 구현<br/>3D 프린팅 도안 제작<br/>TTS 앱 연동 구축<br/>보고서 작성|

## github Tree

```bash

│  README.md
│  
├─server
│  server.py
│  ├──ocr_model
│  ├──yolo_model
│  ├──Road segmentation_model
│      
├─raspberry
│  motor.py
│  ultra.py
└─app
   main.dart
   count_provider.dart
   first_page.dart
   
```

## 서버 구성도
![image](https://user-images.githubusercontent.com/109569066/193387203-a40715e7-c304-4977-a9f5-2686e74e9b16.png)

## YOLO
### 학습데이터
> ㅇㅇ
### 학습 방법
> .

## 앱 구성 및 사용법

### <첫화면>

#### 1. 서버와 연결상태 확인
![image](https://user-images.githubusercontent.com/109563514/193395903-c960ade6-7115-43aa-b98c-394fd629af58.png)  
>서버와 연결된 상태
>- 앱을 실행하면 자동으로 서버와 연결된다.

![image](https://user-images.githubusercontent.com/109563514/193395048-995965eb-00d9-4c94-9b12-ee693f5f203c.png)
>서버와 연결이 끊긴 상태
>- Connect 버튼을 누르면 서버와 연결을 다시 시도하게 된다.


</br></br>
#### 2. 버튼 누르기
![image](https://user-images.githubusercontent.com/109563514/193397068-c334d25d-b57e-49f3-84b5-b8c0c0248c5f.png)
>Run 버튼을 누른 상태
>- 안내로봇의 motor 작동이 시작된다.
>- Stop 버튼으로 활성화된다.

![image](https://user-images.githubusercontent.com/109563514/193397207-e8a9f58a-3290-49a5-a922-24d263ce3200.png)
>Stop 버튼을 누른 상태
>- 안내로봇의 motor 작동이 멈추게된다.
>- Run 버튼으로 활성화된다.

![image](https://user-images.githubusercontent.com/109563514/193397219-2ad26037-159f-4d91-9e96-147fc41e865d.png)
>Run OCR 버튼을 누른 상태
>- 안내로봇의 motor 작동을 멈추고 주변 문자인식을 실행한다.
>- 인식된 문자들이 가운데 메세지창에 뜨면서 음성으로도 출력된다.
>- Stop OCR 버튼으로 활성화된다.

![image](https://user-images.githubusercontent.com/109563514/193397258-3da81758-a57e-4960-8d99-2497ea356de1.png)
>Stop OCR 버튼을 누른 상태
>- 주변 문자인식을 멈춘다.
>- Run OCR 버튼으로 활성화된다.

</br></br>
#### 3. 설정창 사용하기
![image](https://user-images.githubusercontent.com/109563514/193397457-6a68bea9-5733-4c9c-8253-9df743527746.png)
>왼쪽 상단의 메뉴를 클릭한다.

![image](https://user-images.githubusercontent.com/109563514/193397379-bed0dddf-eec8-426b-ac37-6421cbc8a616.png)
>메뉴바를 누른 상태
>- 설정바가 있다.

![image](https://user-images.githubusercontent.com/109563514/193397411-402a7547-019d-4406-99a9-6617d4faf808.png)
>설정 바를 누른 상태
>- 안내 음성의 volume, pitch, speechrate을 조절할 수 있다.

