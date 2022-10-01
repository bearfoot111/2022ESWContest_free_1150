# Text Recognition model
# 1. Tesseract OCR
> **Text Detection** : east text detection

> **Text Recognition** : Tesseract-OCR Engine
# 2. EasyOCR
> **Text Detection** : CRAFT

> **Text Recognition** : ResNet + LSTM + CTC
### 적용 과정
```
reader = easyocr.Reader(['en', 'ko'], gpu=True)
result = reader.readtext(gray)
for res in result:
        text += res[1] + " "
```



