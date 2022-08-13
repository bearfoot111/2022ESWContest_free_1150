import cv2
import numpy as np


def main():
    img_copy=cv2.imread('line3.jpg')
    img=img_copy[60:150,0:700]
    #line.jpg도 해볼 수 있음
    #crop_img=img[60:120,0:160]
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    #여기 밑에 blur 다음 숫자 바꿔주면 임계점 바꿀 수 있음
    #현재 200보다 작은 값은 0, 200보다 큰 값은 255로 바꾸는 중
    ret,thresh1=cv2.threshold(blur,200,255,cv2.THRESH_BINARY_INV)
    cv2.imshow('thresh1',thresh1)
    cv2.waitKey(0) 
 

    mask = cv2.erode(thresh1, None, iterations=2)
    mask= cv2.dilate(mask,None,iterations=2)
    cv2.imshow('mask',mask)

    contours,hierarchy= cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)
    #무게중심 확인 후 선 중앙으로 가기 위한 보정 코드
    if len(contours) >0:
        c=max(contours, key=cv2.contourArea)
        M=cv2.moments(c)

        cx=int(M['m10']/M['m00'])
        cy=int(M['m01']/M['m00'])

        if cx>=95 and cx <=125:
            print("turn left!")
            #여기에 모터 왼쪽으로 가는 코드 넣기
        elif cx >= 39 and cx <= 65:
            print("turn right!")
            #여기에 모터 오른쪽으로 가는 코드 넣기
        else:
            print("go!")
            #직진 코드

        cv2.waitKey(0)
        cv2.destroyAllWindows()



if __name__=='__main__':
    main()




