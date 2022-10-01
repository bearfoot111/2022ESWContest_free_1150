# Team 맨발에서일인자까지1


## 팀원
| 이름 | 메일 |역할|
| ---- | ----- |------|
| 백민정 | b75391@naver.com |전체 기획 총괄<br/>TCP/IP 통신망 구축<br/>Flutter 앱 UI 개발<br/>3D 프린팅 도안 제작<br/>server-client 간 multi processing 구축<br/>보고서 작성 |
| 안진혁 | hijin99@konkuk.ac.kr  |server-client 간 multi processing 구축<br/>TCP/IP 통신망 구축<br/>GPU SERVER 원격 제어 환경 구축<br/>라즈베리 파이 multi threading 구현<br/>Road Segmentation 구현|
| 김채현 | baekchae1120@konkuk.ac.kr  |Road Segmentation 모델 학습<br/>라즈베리 파이 client 코드 개발<br/>TCP/IP 통신망 구축<br/>시연 영상 편집<br/>보고서 작성|
| 하채리 | hacherry05@naver.com  |YOLO 학습 모델 최적화<br/>Text detection 구현<br/>TCP/IP 통신망 구축<br/>라즈베리 파이 multi threading 구현<br/>보고서 작성 |
| 오희빈 | dhgmlqls0527@naver.com  |YOLO 학습 모델 최적화<br/>Text detection 구현<br/>3D 프린팅 도안 제작<br/>TTS 앱 연동 구축<br/>보고서 작성|


## 개발 요약
<img src="https://user-images.githubusercontent.com/109563514/193400087-e9d4057b-1b94-4feb-8f6f-5a26ceacc13a.png" width="600" />


## 2022ESWContest (최종 folder) 구성
```bash
│  
├─ server
│  │  server.py
│  ├─ ocr_model
│  │     README.md
│  │     Tesseract&easyOCR.ipynb
│  │     frozen_east_text_detection.pb
│  │     
│  ├─ yolo_model
│  │  │  train_yolo.md
│  │  │  best_block_.pt
│  │  │  yolov5_block.ipynb
│  │  │  
│  │  ├─ dataset  
│  │  │  │  README.dataset.txt  
│  │  │  │  README.roboflow.txt
│  │  │  │  data.yaml
│  │  │  └─ train
│  │  │     ├─ images
│  │  │     └─ labels
│  │  │     
│  │  └─ test_result 
│  │  
│  └─ Road segmentation_model
│     │  README.md
│     │  train.ipynb
│     ├──data_loader
│     │   │  data_loader
│     │   │  display.py
│     │   │  split_train_test.py
│     │   └─ __pycache__
│     │      display.cpython-39.pyc
│     │     
│     └─ model
│         │  pspunet.py
│         │  pspunet_weight.h5
│         └─ __pycache__
│            pspunet.cpython-39.pyc
│           
├─ raspberry
│     README.md
│     ultra.py
│     motor.py
│     
└─ app
   README.md
   main.dart
   count_provider.dart
   first_page.dart
```

## 서버 구성도
<img src="https://user-images.githubusercontent.com/109569066/193387203-a40715e7-c304-4977-a9f5-2686e74e9b16.png" width="700" />

## 주요 함수 흐름도
<img src="https://user-images.githubusercontent.com/109563514/193400589-2ced53a0-b95e-445c-93a5-bbdf20f51834.png" width="600" />

## 사용한 model
> **YOLO** : 자세한 내용은 2022ESWContest/server/yolo_model/README.md 참고

> **Road Segmentation** : 자세한 내용은 2022ESWContest/server/Road segmentation_model/README.md 참고

> **EasyOCR** : 자세한 내용은 2022ESWContest/server/ocr_model/README.md 참고

## 앱 구성 및 사용법
### 1. 서버와 연결상태 확인
| [1] | [2] |
| ---- | ---- |
| ![image](https://user-images.githubusercontent.com/109563514/193395903-c960ade6-7115-43aa-b98c-394fd629af58.png)  | 
![image](https://user-images.githubusercontent.com/109563514/193395048-995965eb-00d9-4c94-9b12-ee693f5f203c.png) |
 
>**[1] 서버와 연결된 상태**
>- 앱을 실행하면 자동으로 서버와 연결된다.

>**[2]서버와 연결이 끊긴 상태**
>- Connect 버튼을 누르면 서버와 연결을 다시 시도하게 된다.

</br></br>
### 2. 버튼 누르기
![image](https://user-images.githubusercontent.com/109563514/193397068-c334d25d-b57e-49f3-84b5-b8c0c0248c5f.png)
>**Run 버튼을 누른 상태**
>- 안내로봇의 motor 작동이 시작된다.
>- Stop 버튼으로 활성화된다.

![image](https://user-images.githubusercontent.com/109563514/193397207-e8a9f58a-3290-49a5-a922-24d263ce3200.png)
>**Stop 버튼을 누른 상태**
>- 안내로봇의 motor 작동이 멈추게된다.
>- Run 버튼으로 활성화된다.

![image](https://user-images.githubusercontent.com/109563514/193397219-2ad26037-159f-4d91-9e96-147fc41e865d.png)
>**Run OCR 버튼을 누른 상태**
>- 안내로봇의 motor 작동을 멈추고 주변 문자인식을 실행한다.
>- 인식된 문자들이 가운데 메세지창에 뜨면서 음성으로도 출력된다.
>- Stop OCR 버튼으로 활성화된다.

![image](https://user-images.githubusercontent.com/109563514/193397258-3da81758-a57e-4960-8d99-2497ea356de1.png)
>**Stop OCR 버튼을 누른 상태**
>- 주변 문자인식을 멈춘다.
>- Run OCR 버튼으로 활성화된다.

</br></br>
### 3. 설정창 사용하기
![image](https://user-images.githubusercontent.com/109563514/193397457-6a68bea9-5733-4c9c-8253-9df743527746.png)
>왼쪽 상단의 메뉴를 클릭한다.

![image](https://user-images.githubusercontent.com/109563514/193397379-bed0dddf-eec8-426b-ac37-6421cbc8a616.png)
>**메뉴바를 누른 상태**
>- 설정바가 있다.

![image](https://user-images.githubusercontent.com/109563514/193397411-402a7547-019d-4406-99a9-6617d4faf808.png)
>**설정 바를 누른 상태**
>- 안내 음성의 volume, pitch, speechrate을 조절할 수 있다.


## 개발환경
>**사용PC**
>- CPU : ntel(R) Xeon(R) CPU W-2223
>- VGA : RTX3080
>- HDD : SSD 1TB
>- CUDA 11.2
>- CUDNN 8.0.5

>**사용라이브러리**
>- numpy 1.16.2
>- opencv2 4.1.0
>- Pytorch 1.10.0
>- Tensorflow 2.9.0
>- CUDNN 8.0.5


## Hardware 구성
### 안내 로봇 사진
<img src="https://user-images.githubusercontent.com/109563514/193400318-38a4d737-6fc8-4129-9c8b-c910c3982f18.png" width="500" />

### 라즈베리파이 카메라모듈 거치대 3d모델
![image](https://user-images.githubusercontent.com/109563514/193400450-7f08c308-3d5d-4e6e-b2b6-7173f375fb80.png)

### 라즈베리파이 basket 3d모델
![image](https://user-images.githubusercontent.com/109563514/193400487-b5c53fe8-8ceb-4f7f-87c1-376f7ce9e90b.png)

### 차체 mdf 도안
<img src="https://user-images.githubusercontent.com/109563514/193400503-490ffc67-2d2f-4d23-af84-efab9ae59b2e.png" width="500" />

