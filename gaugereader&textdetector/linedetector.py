import cv2 as cv
img = cv.imread(r'C:\Users\82109\Desktop\semi\img.jpg',0)
t = cv.imread(r'C:\Users\82109\Desktop\semi\t.png',0)
dst = cv.imread(r'C:\Users\82109\Desktop\semi\img.jpg') #컬러임

result = cv.matchTemplate(img, t, cv.TM_SQDIFF_NORMED)
minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)
x, y = minLoc
h, w = t.shape
dst = cv.rectangle(dst, (x, y), (x +  w, y + h) , (0, 0, 255), 2)

cv.imshow("result", dst)
cv.waitKey(0)
cv.destroyAllWindows()


