
import cv2 as cv
import numpy as np
import math
from PIL import Image,ImageDraw

def loadImage(path):
    return cv.imread(path)

def saveImage(path, image):
    return cv.imwrite(path,image) 

def circleAverage(image, center, r):
    total = np.uint32([0,0,0])
    count = 0
    for i in range(center[0]-r, center[0]+r):
        for j in range(center[1]-r, center[1] + r):
            if (center[0] - i) ** 2 + (center[1] - j) ** 2 <= r**2:
                total += image[i,j]
                count += 1
    return np.uint8(total // count)

def paintCircle(image, center, r, color):
    p_rad = np.deg2rad([150.,90,30.,-30.,-90.,-150.,150.]) 
    X = np.cos(p_rad)*r + center[1]
    Y = np.sin(p_rad)*r + center[0]
    polygon = tuple(zip(X,Y))

    hex = Image.new('L', (image.shape[1], image.shape[0]), 0)
    ImageDraw.Draw(hex).polygon(polygon, outline=1, fill=1)
    hex = np.array(hex)
    image[:,:,0] += hex*color[0]
    image[:,:,1] += hex*color[1]
    image[:,:,2] += hex*color[2]


def calcKMeansImage(image, k):
    unsegmented_image = cv.cvtColor(image,cv.COLOR_BGR2YCrCb)
    pixel_values = unsegmented_image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, (centers) = cv.kmeans(pixel_values, k, None, criteria, 50, cv.KMEANS_PP_CENTERS)
    centers = np.uint8(centers)
    labels = labels.flatten()
    segmentedImage = centers[labels.flatten()]
    segmentedImage = segmentedImage.reshape(unsegmented_image.shape)
    segmentedImage = cv.cvtColor(segmentedImage,cv.COLOR_YCrCb2BGR)
    return segmentedImage

def calcHexagonImage(image, innerR, k):
    outerR = int((innerR * 2) / math.sqrt(3))
    height = image.shape[0]
    width = image.shape[1]

    rows = int((height - 2*outerR) / (1.5*outerR) + 1)
    cols = int((width - 2*innerR) / (2*innerR))

    avgs = np.zeros((rows, cols, 3), np.uint8)
    i = 0
    offset = False
    for y in range(outerR, height - outerR, int(1.5*outerR)):
        offsetX = innerR if offset else 0
        j = 0
        for x in range(innerR + offsetX, width - innerR - offsetX, 2*innerR):
            avg = circleAverage(image, (y,x), innerR)
            avgs[i,j] = avg
            j += 1
        offset = not offset
        i += 1

    avgs = calcKMeansImage(avgs,k)

    innerRR = 10
    outerRR = int((innerRR * 2) / math.sqrt(3))
    newwidth = int(cols * 2 * innerRR)
    newheight = int((rows - 1) * (outerRR * 3/2 ) + (outerRR *2))
    hexagonImage = np.zeros((newheight, newwidth, 3), np.uint8)
    hexImage = Image.new('RGB', (newwidth,newheight), 0)

    p_rad = np.deg2rad([150.,90,30.,-30.,-90.,-150.,150.]) 
    X = np.cos(p_rad)*outerRR
    Y = np.sin(p_rad)*outerRR
    offset = False
    for y in range(rows):
        offsetX = innerRR if offset else 0
        for x in range(cols):
            cX = X + innerRR + offsetX + 2 * innerRR * x
            cY = Y + outerRR + int(1.5*outerRR) * y
            polygon = tuple(zip(cX,cY))

            ImageDraw.Draw(hexImage).polygon(polygon, outline=tuple(avgs[y,x]), fill=tuple(avgs[y,x]))
        offset = not offset
    
    hexImage = np.array(hexImage)

    print(cols,rows)

    return hexImage


