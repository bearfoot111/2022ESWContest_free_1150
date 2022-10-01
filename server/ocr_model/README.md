# Easy OCR

* CRAFT 를 사용한 text detection.   
-CRAFT는 VGG16 기반 U-Net으로 구성되어 문자영역을 분할인식(Semantic Segmentation)하여 문자의 위치를 검출하는 네트워크를 말한다. ResNet은 기본적으로 VGG19의 구조를 뼈대로 하며 거기에 컨볼루션 층들을 추가해서 깊게 만든 후에, shortcut들을 추가한다.  
CTC는 EasyOCR에서 출력부분에서 사용된다. 훈련데이터에 문장의 시퀀스에 따라 클래스만 나열되어있고 이미지 내에서 각 클래스의 위치정보는 없는 unsegmented 시퀀스 데이터의 학습이 가능한 알고리즘이다.

![dyery_page-0001](https://user-images.githubusercontent.com/109472852/193394022-4ecd9755-2c33-41e0-bb6a-32099e3d0eb6.jpg)


