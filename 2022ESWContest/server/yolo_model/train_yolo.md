# YOLO

### yolov5 pretrained model
| Model | mAP | Speed |
| ---- | ----- |------|
| YOLOv5n |	45.7 | 6.3 |
| YOLOv5s	| 56.8 | 6.4 |
| YOLOv5m |	64.1 | 8.2 |

<img src="https://user-images.githubusercontent.com/109569066/193399694-a1de8d2d-315f-42ba-895c-24337ab54c42.png" width="200" />

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

### train
```
!python train.py --img 416 --batch 16 --epochs 50 --data /content/dataset/data.yaml --cfg ./models/yolov5s.yaml --weights yolov5s.pt --name block_yolov5s_results
```
> 자세한 train 과정은 2022ESWCOntest/server/yolo_model/yolov5_block.ipynb 참고

## 적용 과정
>학습된 yolov5 model을 load
```
model = torch.hub.load('yolov5', 'custom', path='best_block_.pt', source='local')
```
>**model의 inference setting** : gpu로 yolo를 실행하며 신뢰도를 0.4로 설정
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
```
