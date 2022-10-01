# YOLO
![about_yolo](https://user-images.githubusercontent.com/109569066/193397458-1f8abb3f-f0fb-46fe-9a6a-b89f1622de3f.png)

>1. yolo를 이용해 사용자 지정 데이터를 학습시키기 위하여 이미지를 수집
>2. roboflow를 사용하여 해당 이미지의 관심 개체에 label을 지정
>3. yolov5의 pretrained model 중 yolov5s을 선택하여 학습
>4. weight 파일인 best.pt를 생성
>5. weight 파일을 이용해 실제 사진/영상에 yolo를 적용

## 학습 과정



### 학습 데이터
> **Image Data** : 2022ESWCOntest/server/yolo_model/dataset/train/images

> **Label Data** : 2022ESWCOntest/server/yolo_model/dataset/train/labels

> **yaml** : 2022ESWCOntest/server/yolo_model/dataset/data.yaml

### yolov5의 pretrained model
Pretrained Checkpoints
Model	size
(pixels)	mAPval
0.5:0.95	mAPval
0.5	Speed
CPU b1
(ms)	Speed
V100 b1
(ms)	Speed
V100 b32
(ms)	params
(M)	FLOPs
@640 (B)
YOLOv5n	640	28.0	45.7	45	6.3	0.6	1.9	4.5
YOLOv5s	640	37.4	56.8	98	6.4	0.9	7.2	16.5
YOLOv5m	640	45.4	64.1	224	8.2	1.7	21.2	49.0
