# YOLO
## YOLOv5
YOLO는 Object Detection에서 빠른 영상처리 속도와 준수한 성능을 모두 가지고 있는 모델이다. 로봇의 특성상 카메라에서 받아들이는 영상을 바로 처리해야 하므로 Real-Time Model이 필요하다. 따라서 성능이 더 좋은 DINO 혹은 SwinV2-G보다는 실시간성이 보장되는 YOLOv5를 사용하게 되었다.
>yolov5 pretrained model 종류
<img src="https://user-images.githubusercontent.com/109569066/193399694-a1de8d2d-315f-42ba-895c-24337ab54c42.png" width="600" />

## 적용 과정
<img src="https://user-images.githubusercontent.com/109569066/193397458-1f8abb3f-f0fb-46fe-9a6a-b89f1622de3f.png" width="600" />

1. yolo를 이용해 사용자 지정 데이터를 학습시키기 위하여 이미지를 수집
2. roboflow를 사용하여 해당 이미지의 관심 개체에 label을 지정
3. yolov5의 pretrained model 중 yolov5s을 선택하여 학습
4. weight 파일인 best.pt를 생성
5. weight 파일을 이용해 실제 사진/영상에 yolo를 적용
---
## 학습 과정

### 학습 데이터
> **Image Data** : 2022ESWCOntest/server/yolo_model/dataset/train/images

> **Label Data** : 2022ESWCOntest/server/yolo_model/dataset/train/labels

> **roboflow Data** : https://universe.roboflow.com/object-detection/block-kpj3b

> **yaml** : 2022ESWCOntest/server/yolo_model/dataset/data.yaml

### train
```
!python train.py --img 416 --batch 16 --epochs 50 --data /content/dataset/data.yaml --cfg ./models/yolov5s.yaml --weights yolov5s.pt --name block_yolov5s_results
```
> 자세한 train 과정은 2022ESWCOntest/server/yolo_model/yolov5_block.ipynb 참고

### train summary
| Class | Images | Labels | P | R | mAP@.5 | mAP@.5:.95 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| all | 21 | 139 | 0.83 | 0.733 | 0.794 | 0.576 |
| go | 21 | 88 | 0.774 | 0.858 | 0.898 | 0.67 |
| stop | 21 | 51 | 0.885 | 0.608 | 0.689 | 0.482 |

YOLOv5s summary: 213 layers, 7015519 parameters, 0 gradients, 15.8 GFLOPs

---
## 학습 결과 비교
<img src="https://user-images.githubusercontent.com/109569066/193401139-b71b9a93-7f22-43cf-8928-9936e6589023.png" width="500" />
(1)은 주로 수직에서 바라보는 점자블록의 이미지를, (2)는 상대적으로 수평에서 바라보는 점자블록의 이미지를 학습한 경우이다.

로봇의 시점에서 촬영한 video에 학습한 model을 적용하였을 때 (2)가 (1)보다 더 많은 점자블록을 높은 확률로 인식하였다.

---
## 적용
>학습된 yolov5 model을 load
```
model = torch.hub.load('yolov5', 'custom', path='best_block_.pt', source='local')
```
>(model의 inference setting) gpu로 yolo를 실행하며 신뢰도를 0.4로 설정
```
model.to('cuda:0')
model.conf = 0.4
```
>input 이미지에 yolo를 적용
```
results = model(frame)
```
>yolo 적용 결과 output 이미지
```
frame = np.squeeze(results.render())
```
  
>yolo 적용 결과 output 좌표
```
arr = results.xyxy[0].to('cuda:0')

#      xmin    ymin    xmax   ymax  confidence  class    name
# 0  749.50   43.50  1148.0  704.5    0.874023      0      go
# 1  433.50  433.50   517.5  714.5    0.687988      1    stop
# 2  114.75  195.75  1095.0  708.0    0.624512      1    stop
# 3  986.00  304.00  1028.0  420.0    0.586865      0      go
```

