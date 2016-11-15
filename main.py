import cv2
import preprocess
import segmentbeautify
import xmloperations
import hmm
from os import listdir
from os.path import isfile, join

words_hmm = []
filepath = "Datasets/formsA-D/"
i = 0
onlyfiles = [f for f in listdir(
    filepath) if isfile(join(filepath, f))]
for file in onlyfiles:
    img = cv2.imread(filepath + file, 0)
    # cv2.namedWindow("Main image", cv2.WINDOW_NORMAL)
    # cv2.imshow("Main image", img)
    lines = xmloperations.machinePrintedPart(filepath + file)
    img = preprocess.samplePage(img)
    # cv2.namedWindow("Sampled image", cv2.WINDOW_NORMAL)
    # cv2.imshow("Sampled image", img)
    img = preprocess.binarize(img)
    # cv2.namedWindow("Binarized image", cv2.WINDOW_NORMAL)
    # cv2.imshow("Binarized image", img)
    img = preprocess.removeSaltnPepperNoise(img)
    # cv2.namedWindow("Denoised image", cv2.WINDOW_NORMAL)
    # cv2.imshow("Denoised image", img)

    # edge_image = cv2.bitwise_not(img)
    # edge_image = preprocess.detectEdge(edge_image)

    # cv2.namedWindow("Edge image", cv2.WINDOW_NORMAL)
    # cv2.imshow("Edge image", edge_image)

    img = preprocess.detectSkew(img)
    words_hmm = words_hmm + segmentbeautify.extractLines(img, file, lines)
    # cv2.waitKey(100000)
    i += 1
    if 0.2 * len(onlyfiles) < i:
        break

hmm.createTXT(words_hmm)
print "written"
clf = hmm.trainHMM("test.txt")
print "trained"
hmm.testHMM(clf, "test.txt")
print "tested"
