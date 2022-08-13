import cv2
import os
import numpy as np



img = cv2.imread('gauge-2.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#그레이함수로 변환
gray = cv2.GaussianBlur(gray,(5, 5),0)#블러처리

mser = cv2.MSER_create()#그레이 영상에서 글자 영역 검출
regions,_ = mser.detectRegions(gray)

clone = img.copy()#원본이미지 복사


hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
#검출된 영역에서 convexhull 검출

remove1 = []
#사각영역 검출하고 보여주기
for i,c1 in enumerate(hulls):

    x, y, w, h = cv2.boundingRect(c1)
    r1_start = (x, y)
    r1_end = (x+w, y+h)

    for j,c2 in enumerate(hulls):
        
        if i == j:
            continue

        x, y, w, h = cv2.boundingRect(c2)
        r2_start = (x, y)
        r2_end = (x+w, y+h)

#일단 직사각형 제거해야 할 듯
#원판 찾고 잘라서 그 안에서 찾기

#큰 사각형 안에 작은 사각형이 있을 경우 제거

        if r1_start[0]> r2_start[0] and r1_start[1] > r2_start[1] and r1_end[0] < r2_end[0] and r1_end[1] < r2_end[1]:
            remove1.append(i)


for j,cnt in enumerate(hulls):
    if j in remove1: continue
    x, y, w, h = cv2.boundingRect(cnt)
    margin = 10
    #숫자 외곽에 여유공간 주기
    cv2.rectangle(clone, (x-margin, y-margin), (x + w + margin, y + h + margin), (0, 255, 0), 1)

cv2.imshow('mser', clone)
cv2.waitKey(0)


mask = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)

for j,cnt in enumerate(hulls):
    if j in remove1: continue
    x, y, w, h = cv2.boundingRect(cnt)
    margin = 10
    cv2.rectangle(mask, (x-margin, y-margin), (x + w + margin, y + h + margin), (255, 255, 255), -1)

text_only = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("text only", text_only)
cv2.waitKey(0)

#https://webnautes.tistory.com/1449
