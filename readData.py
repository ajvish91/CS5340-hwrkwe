import PIL.Image
import cv2
import xml.etree.ElementTree as ET
import os
import numpy as np
from seqlearn.datasets import load_conll
from seqlearn.hmm import MultinomialHMM
from seqlearn.evaluation import bio_f_score


# Recursively extracts filenames from a directory and its subdirectory
def list_files(dir):
    r = []
    subdirs = [x[0] for x in os.walk(dir)]
    for subdir in subdirs:
        files = os.walk(subdir).next()[2]
        if (len(files) > 0):
            for file in files:
                r.append(subdir + "/" + file)
    return r

# Gets the features from test.txt
def features(sequence, i):
    split_sequence = sequence[i].split(" ")
    # print i
    print len(split_sequence)
    yield str(sequence)


# An image directory
IMAGE_DIRECTORY = "Datasets/sentences/a01/a01-000x/"
my_images = []


# Reads image from dataset and stores it as a numpy array
for i in range(0, 2):
    for j in range(0, 3):
        myimage = cv2.imread(
            IMAGE_DIRECTORY + "a01-000x-s0" + str(i) +
            "-0" + str(j) + ".png", 0)
        (thresh, im_bw) = cv2.threshold(myimage, 128,
                                        255, cv2.THRESH_BINARY |
                                        cv2.THRESH_OTSU)
        my_images.append(im_bw / 255)
myimage = cv2.imread(
    IMAGE_DIRECTORY + "a01-000x-s01-03.png", 0)
(thresh, im_bw) = cv2.threshold(myimage, 128,
                                255, cv2.THRESH_BINARY |
                                cv2.THRESH_OTSU)
my_images.append(im_bw / 255)
# cv2.imwrite("bw.jpg", im_bw)
print len(my_images)

# Captures the jpeg file and extracts METADATA
jpgfile = PIL.Image.open(IMAGE_DIRECTORY + "/a01-000x-s01-00.png")

# The METADATA is an XML, hence parsing
myxml = ET.fromstring(jpgfile.info["Description"])

print jpgfile.info["Description"]

# Gets the text corresponding to the file a01-000u-s00-00.png
sentence = myxml.find("handwritten-part")[0].attrib["text"]

# Gets <lines from the xml
lines = myxml.findall("./handwritten-part/line")
# Initialize image iterator
i = 0

# Maps the line to a word
line_mapping = [[], [], [], [], [], [], [], [], []]

for line in lines:
    lower = line.find("./lower-contour")
    upper = line.find("./upper-contour")
    my_image = my_images[i]
    print "image shape: ", my_image.shape
    x1 = []
    x2 = []
    if lower is not None:
	#get lower contour values
        for point in lower.findall("./point"):
            x1.append(int(point.attrib["x"]))
    if upper is not None:
        for point in upper.findall("./point"):
            x2.append(int(point.attrib["x"]))
    # Get words in a line
    words = line.findall("./word")
    for word in words:
        print "The Word: ****", word.attrib["text"], "****"
        word_width = 0
        x = int(word.findall("./cmp")[0].attrib["x"])
        print "starts at ", x
        for ch in word.findall("./cmp"):
            word_width += int(ch.attrib["width"])
        print "word width: ", word_width
        if len(x1) == 0:
            print "minimum = ", x2[0]
            offset = x - x2[0]
        else:
            print "minimum = ", x1[0]
            offset = x - x1[0]
        if offset <= 0:
            offset = 0
        print "offset ", offset
        word_image = my_image[
            :, offset:offset + word_width]
        my_word = {
            "matrix": word_image,
            "word": word.attrib["text"]
        }
        line_mapping[i].append(my_word)
        # cv2.imwrite("line" + str(i) + "-" +
        #             str(len(line_mapping[i]) - 1) + "-" +
        #             my_word["word"] + ".jpg",
        #             my_word["matrix"] * 255)
        print my_word["matrix"].shape
    print '\n'
    # Go to the next image
    i += 1


# Saves the image into a TXT file
for line in line_mapping:
    for word in line:
        if word["matrix"].shape[1] == 0:
            print "Zero matrix... Skipping..."
        else:
            f_handle = file('test.txt', 'a')
            np.savetxt(f_handle, word['matrix'], delimiter=" ",
                       fmt="%i", newline=" ",
                       header='', footer="" + word["word"] + "\n\n",
                       comments='')
            f_handle.close()

# # Extracts features from the datasets
X_train, y_train, lengths_train = load_conll("test.txt", features)

# # Models it as an HMM
clf = MultinomialHMM()
clf.fit(X_train, y_train, lengths_train)

print X_train, y_train

# Validation after training
X_test, y_test, lengths_test = load_conll("test.txt", features)
y_pred = clf.predict(X_test, lengths_test)

print y_pred
# # Final score
# print(bio_f_score(y_test, y_pred))
