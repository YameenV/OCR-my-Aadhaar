from numpy import NaN, nan
import pytesseract as tess
import cv2
import re
import numpy as np
import time

def ocrHandler(img):
    print("ocrHandler")
    gamma = adjustGamma(img)
    thress_img = preProcessing(gamma)
    text = textExtracting(thress_img, 0, gamma)
    print(text, 0)
    firstData = textProcessing(text)
    result = dataEvaluation(firstData, 1)

    if result == True:
        text = textExtracting(thress_img, 1, gamma)
        print(text)
        secondData = textProcessing(text)
        result = dataEvaluation(firstData, 0, *secondData)
        if result == True:
            return secondData

    return firstData

def adjustGamma(image, gamma=1.2):
    print("adjustGamma")
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


def preProcessing(img): 
    print("preProcessing")
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    dilated_img = cv2.dilate(gray, np.ones((7,7), np.uint8))
    bg_img = cv2.bilateralFilter(dilated_img,50,75,75)
    diff_img = 255 - cv2.absdiff(gray, bg_img)
    norm_img = diff_img.copy()
    cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    _, thr_img = cv2.threshold(norm_img,0 ,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    return thr_img
    

def textExtracting(thress_img, flag, img):
    print("textExtracting", flag)
    if flag == 0:
        data = tess.image_to_string(thress_img, lang='eng+hin')
        return data
    if flag == 1:
        data = tess.image_to_string(img, lang='eng+hin')
        return data
        

def textProcessing(data):
    print("textProcessing")
    adharNumber = ''

    x = re.search(r"[2-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}", data)
    y = re.search(r"[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}", data)
    z = re.search(r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}", data)

    gender = "Female" if "female" in data.lower() else "Male" if "male" in data.lower() else ""

    birthDate = z.group(0) if z != None else ''

    if x == None and y == None:
        adharNumber = ''
    elif x == None:
        adharNumber = y.group(0)
    elif y == None:
        adharNumber = x.group(0)
    
    return {"adharno" : adharNumber, "birthdate" : birthDate, "gender": gender}

def dataEvaluation(firstData, flag, *secondData):
    print("dataEvaluation", flag)
    firstScore  = 0
    for i in firstData:
        if len(firstData[i]) > 0:
            firstScore += 1
    if firstScore <= 2:
        return True

    if flag == 0:
        secondScore  = 0
        for i in secondData:
            if len(secondData[i]) > 0:
                secondScore += 1
            if secondScore >= firstScore:
                return True

    return False