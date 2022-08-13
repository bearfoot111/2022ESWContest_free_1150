import cv2
import numpy as np


def main():
    img=cv2.imread('line2.jpg')
    #lin.jpg도 해볼 수 있음
    #crop_img=img[60:120,0:160]
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    #여기 밑에 blur 다음 숫자 바꿔주면 임계점 바꿀 수 있음
    #현재 200보다 작은 값은 0, 200보다 큰 값은 255로 바꾸는 중
    ret,thresh1=cv2.threshold(blur,200,255,cv2.THRESH_BINARY_INV)
    cv2.imshow('thresh1',thresh1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__=='__main__':
    main()




