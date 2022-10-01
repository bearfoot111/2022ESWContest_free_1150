# Text Recognition model
## 1. East Text Detection + Tesseract OCR
> **East Text Detection** : 

> **Tesseract OCR** : 
### 적용 과정
> East Text Detection은 input 이미지 사이즈가 32의 배수여야 하므로 사이즈를 조절
```
(origH, origW) = image.shape[:2]
 
rW = origW / float(frame_size)
rH = origH / float(frame_size)
newW = int(origW / rH)
center = int(newW / 2)
start = center - int(frame_size / 2)

image = cv2.resize(image, (newW, frame_size)) 
```
> East Text Detection model을 적용하여 text의 ROI를 구함
```
layerNames = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
net = cv2.dnn.readNet(east_decorator)
net.setInput(blob_image)
(scores, geometry) = net.forward(layerNames)
(numRows, numCols) = scores.shape[2:4]
for y in range(0, numRows):
        # extract the scores (probabilities)
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        for x in range(0, numCols):
        
                (offsetX, offsetY) = (x * 4.0, y * 4.0)

                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                rects.append((startX, startY, endX, endY))
```
> Tesseract OCR을 적용하여 text ROI에서 인식되는 text를 반환
```
config = ("-l kor+eng --oem 1 --psm 12")
text = pytesseract.image_to_string(image, config=config)
````
자세한 과정은 2022ESWContest_free_1150/2022ESWContest/server/ocr_model/Tesseract&easyOCR.ipynb 
## 2. EasyOCR
> **Text Detection** : CRAFT

> **Text Recognition** : ResNet + LSTM + CTC
### 적용 과정
```
reader = easyocr.Reader(['en', 'ko'], gpu=True)
result = reader.readtext(gray)
for res in result:
        text += res[1] + " "
```
## 3. model 적용 결과 비교
<img src="https://user-images.githubusercontent.com/109569066/193410836-bcbedd09-1c20-4e63-a9cf-7ae97cb6428d.png" width="500" />

> 실생활 이미지에 각각의 model을 적용하였을  EasyOCR이 Tesseract보다 성능이 우수하였다.
