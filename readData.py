import PIL.Image
import cv2
import xml.etree.ElementTree as ET

myimage = cv2.imread("Datasets/sentences/a01/a01-000u/a01-000u-s00-00.png")

jpgfile = PIL.Image.open('Datasets/sentences/a01/a01-000u/a01-000u-s00-00.png')

# print jpgfile.info
myxml = ET.fromstring(jpgfile.info["Description"])

print myxml.getchildren()
