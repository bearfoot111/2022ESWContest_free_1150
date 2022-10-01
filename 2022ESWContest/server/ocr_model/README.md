# EasyOCR
> input 이미지에 EasyOCR 적용
```
reader = easyocr.Reader(['en', 'ko'], gpu=True)
result = reader.readtext(gray)
for res in result:
        text += res[1] + " "
```

![dyery_page-0001](https://user-images.githubusercontent.com/109472852/193394022-4ecd9755-2c33-41e0-bb6a-32099e3d0eb6.jpg)


