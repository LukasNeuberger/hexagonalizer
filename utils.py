
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
    for y in range(int(center[0]-r), int(center[0]+r+1)):
        for x in range(int(center[1]-r), int(center[1] + r+1)):
            if (center[0] - y) ** 2 + (center[1] - x) ** 2 <= r**2:
                total += image[int(y),int(x)]
                count += 1
    return np.uint8(total // count)


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


def calcHexagonPattern(image, n):
    
    print('Calculating average color of hexagons')

    height = image.shape[0]
    width = image.shape[1]
    innerR = width / (2*n)
    outerR = (innerR * 2) / math.sqrt(3)

    rows = int((height - 2*outerR) / (1.5*outerR) + 1)
    cols = n

    pattern = np.zeros((rows, cols, 3), np.uint8)
    offset = False
    for row in range(rows):
        y = outerR + 1.5*outerR*row
        offsetX = innerR if offset else 0
        for col in range(cols):
            x = innerR + offsetX + 2*innerR*col
            if x + innerR <= width:
                avg = circleAverage(image, (y,x), innerR)
                pattern[row,col] = avg

        print('Calculating average color of hexagons progress: %0.1f' % (((row + 1)*cols) / (cols * rows) * 100))
        offset = not offset
    return pattern

def calcHexagonImage(pattern):
    
    print('Drawing hexagon image')

    cols = pattern.shape[1]
    rows = pattern.shape[0]

    innerRR = 20
    outerRR = (innerRR * 2) / math.sqrt(3)
    newwidth = int(cols * 2 * innerRR)
    newheight = int((rows - 1) * (outerRR * 1.5 ) + (outerRR *2))
    hexImage = Image.new('RGB', (newwidth, newheight), 0)

    p_rad = np.deg2rad([150.,90,30.,-30.,-90.,-150.,150.]) 
    hexX = np.cos(p_rad)*outerRR
    hexY = np.sin(p_rad)*outerRR
    offset = False
    for row in range(rows):
        y = hexY + outerRR + 1.5*outerRR * row
        offsetX = innerRR if offset else 0
        for col in range(cols):
            x = hexX + innerRR + offsetX + 2 * innerRR * col
            polygon = tuple(zip(x,y))
            ImageDraw.Draw(hexImage).polygon(polygon, outline=tuple(pattern[row,col]), fill=tuple(pattern[row,col]))

        print('Drawing hexagon image progress: %0.1f' % (((row+1)*cols) / (cols * rows) * 100))
        offset = not offset
    
    hexImage = np.array(hexImage)

    print(cols,rows, cols * rows)
    print('width: %fcm  height: %fcm' % (cols * 3, rows * (3 * 2) / math.sqrt(3)))

    return hexImage



def calcColors(colors, k):

    print('Reducing number of colors')

    return calcKMeansImage(colors, k)