import cv2
import numpy as np
import math


def binarize(img):
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret, binarized_img = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binarized_img


def removeSaltnPepperNoise(img):
    return cv2.medianBlur(img, 5)


def detectEdge(img):
    horizontalStructure = cv2.getStructuringElement(
        cv2.MORPH_RECT, (3, 3))

    cv2.erode(img, img, horizontalStructure, (-1, -1))
    cv2.dilate(img, img, horizontalStructure, (-1, -1))
    return img


def samplePage(img):
    page_width = img.shape[1]
    page_offset = 700
    page_height = img.shape[0] - page_offset
    page = img[page_offset: page_height - 100, 100:]
    print "Image has been sampled at ", page.shape[1], "x", page_width
    return page


def detectSkew(img):
    not_img = cv2.bitwise_not(img)
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(not_img, kernel, iterations=1)
# minLineLength = img.shape[1]  200
# maxLineGap = 30
# lines = cv2.HoughLinesP(not_img, 1, np.pi / 180,
#                         100, minLineLength, maxLineGap)
# if lines is not None:
#     angle = 0
#     for line in lines[0]:
#         print line
#         pt1 = (line[0], line[1])
#         pt2 = (line[2], line[3])
#         cv2.line(not_img, pt1, pt2, 125, 9)
#         angle += math.atan2(float(line[3]) - line[1],
#                             float(line[2]) - line[0])
#     angle /= len(lines[0])
#     print angle * np.pi / 180
    points_row, points_column = np.where(erosion == 255)
    points = zip(points_column, points_row)
    rect = cv2.minAreaRect(np.asarray(points))
    print rect
    box = cv2.cv.BoxPoints(rect)
    box = np.int0(box)
    print box
    cv2.drawContours(erosion, [box], 0, 125, 2)
    cv2.namedWindow("lined out", cv2.WINDOW_NORMAL)
    cv2.imwrite("lined_out.jpg", erosion)
    return img
