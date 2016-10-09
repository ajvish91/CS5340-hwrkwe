import PIL.Image
import cv2
import xml.etree.ElementTree as ET
import numpy as np
from seqlearn.datasets import load_conll
from seqlearn.hmm import MultinomialHMM
from seqlearn.evaluation import bio_f_score

# The feature extractor: So far does nothing but splits the pixels of the image by spaces
def features(sequence, i):
    split_sequence = sequence[i].split(" ")
    # print i
    for pixel in split_sequence:
    	# print pixel + "lol"
    	yield pixel

# Reads image from dataset and stores it as a numpy array
myimage = cv2.imread("Datasets/sentences/a01/a01-000u/a01-000u-s00-00.png", 0)

# Captures the jpeg file and extracts METADATA
jpgfile = PIL.Image.open('Datasets/sentences/a01/a01-000u/a01-000u-s00-00.png')

# The METADATA is an XML, hence parsing
myxml = ET.fromstring(jpgfile.info["Description"])

# Gets the text corresponding to the file a01-000u-s00-00.png
sentence = myxml.find("handwritten-part")[0].attrib["text"]

# Saves the image into a TXT file
np.savetxt("test.txt", myimage, fmt="%1.2f", newline=" ",
           header='[', footer='] [' + sentence + ']', comments='')

# Extracts features from the datasets
X_train, y_train, lengths_train = load_conll("test.txt", features)

# Models it as an HMM
clf = MultinomialHMM()
clf.fit(X_train, y_train, lengths_train)

print X_train, y_train

# Validation after training
X_test, y_test, lengths_test = load_conll("test.txt", features)
y_pred = clf.predict(X_test, lengths_test)

# Final score
print(bio_f_score(y_test, y_pred))
