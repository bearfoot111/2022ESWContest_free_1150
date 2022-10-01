# Text Recognition model
## 1. Tesseract OCR
> **Text Detection** : east text detection

> **Text Recognition** : Tesseract-OCR Engine
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
## 3. model 비교
<img src="https://user-images.githubusercontent.com/109569066/193405181-e7a6dae3-c95a-4b9e-b7d8-2b37eade5278.png" width="600" />
<img src="https://user-images.githubusercontent.com/109569066/193405210-90613832-6227-4c5c-9c28-8aea6dc4ffdd.png" width="600" />

