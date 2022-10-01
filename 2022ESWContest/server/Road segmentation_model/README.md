# Road Segmentation 
 
<img src="https://user-images.githubusercontent.com/109472852/193393158-bdd7c0b2-eb4d-4844-873c-754813118866.jpg" width="600" />


* ## 모델 구조  
UNET은 이미지 분할을 목적으로 제안된 End-to-End 방식의 Fully-Convolutional Network 기반 모델이다. 이미지의 전반적인 정보를 얻기 위한 네트워크와 정확한 Localization을 위한 네트워크가 대칭 형태로 구성되어 있다. 활성화 함수는 ReLU를 사용하며, FCN 보다 확장된 개념의 Up-sampling을 적용하여 적은 양의 학습 데이터만으로 우수한 성능을 보일 수 있다.   

개발에서 사용된 모델은 UNET에  PSPNET의 pyramid pooling module을 추가한 구조로, PSPNET 의 장점인 global context information이 활용된다. global context information이란 픽셀값의 클래스를 분류할 때 근처의 local 정보들만 이용하는 것이 아니라 더 넓은 영역, 즉 global을 활용하는 것이다. 이와 같이 PSPNET을 접목한 PSPUNET은 UNET 모델만을 사용했을 때보다 정확도가 높고 속도가 빠르다. 아래는 간단한 demo 버전의 성능 분석표이다. 
|model|accuracy|loss|mloU|FPS|Size|
|---|---|---|---|---|---|
|PSPUnet|90.2%|0.3160|74.5%|24.8|39.6MB|
|UNet|89.1%|0.3520|70.9%|22.7|131MB|

* ## 사용 모델
demo 버전인만큼 epoh가 10, 정확도가 90%로 가볍게 훈련된 모델이 사용되었다. 아래 표와 같이 epoh 값을 높게 부여할 수록 정확도가 증가하는 것을 확인하여 본 개발에서는 epoh를 50으로 조정한 새로운 훈련 모델을 생성하였다. 
<img src="https://user-images.githubusercontent.com/109569066/193413463-fa19a318-1f85-4e72-a9c8-ef42c881619e.png" width="600" />

* ## 적용 과정
> road segmentation model load 및 적용
```
model = pspunet((IMG_HEIGHT, IMG_WIDTH ,3), n_classes)
model.load_weights("pspunet_weight.h5")

frame = cv2.imread('image.jpg')

frame = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame = frame[tf.newaxis, ...]
frame = frame/255
pre = model.predict(frame)
pre = create_mask(pre).numpy()

frame2 = frame/2
frame2[0][(pre==1).all(axis=2)] += [0, 0, 0]
frame2[0][(pre==2).all(axis=2)] += [0.5, 0.5,0]
frame2[0][(pre==3).all(axis=2)] += [0.2, 0.7, 0.5]
frame2[0][(pre==4).all(axis=2)] += [0, 0.5, 0.5]
frame2[0][(pre==5).all(axis=2)] += [0, 0, 0.5]
frame2[0][(pre==6).all(axis=2)] += [0.5, 0, 0]
```
> road segmentation model 적용 이후 output을 이미지로 반환하는 과정
```
frame2 = tf.squeeze(frame2)
frame2 = frame2.numpy()
frame2 = frame2*255
frame2 = np.uint8(frame2)
frame2 = to_pil_image(frame2)
frame2 = np.array(frame2)
frame2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2BGR)
```

* ## 개발 환경


  ubuntu 18.04, tensorflow 2.0.0, opencv-python 4.2.0.32, numpy 1.18.2


[detail & original author](https://github.com/JunHyeok96/Road-Segmentation)


