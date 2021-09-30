import pytesseract as tess
import cv2
import re

def readImage(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgbi = cv2.bilateralFilter(imgGray,1,75,75)

    return threshold(imgbi)

def threshold(image):  
    a,b = 1,1
    c,d = 0,0
    for i in range(0,24):
        a += 10
        b += 6
        imgthress = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, a,b)
        test = tess.image_to_string(imgthress, lang='eng+hin')
        #print(test)
        x = re.search(r"[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}", test)
        if x != None:
            c = a
            d = b
            #print('djajsdfj sjdh',c, d)
            break
    return {"adharno" : x.group(0)}