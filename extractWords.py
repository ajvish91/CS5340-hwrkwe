import cv2
import preprocess


# Get words from words.txt
words_mapping = []
with open("words.txt") as fp:
    for i, line in enumerate(fp):
        words_mapping.append(line)
labels = []
for label in words_mapping:
    label_split = label.rstrip("\n").split(" ")
    if label_split[0] != "a01-117-05-02":
        labels.append([label_split[0], label_split[-1]])
print labels

i = 0
filepath = "Datasets/words/"
target = open('sequence1.csv', "w")
for label in labels:
    if(113624 <= i):
        print label[1]
        navi = label[0].split("-")
        word = cv2.imread(filepath + navi[0] + "/" +
                          navi[0] + "-" + navi[1] +
                          "/" + label[0] + ".png", 0)
        cv2.imshow("original", word)
        word = preprocess.binarize(word)
        cv2.imshow("binarized", word)
        print word.shape
        word = preprocess.resizeImage(word)
        print word.shape
        word = preprocess.sharpen(word)
        word = cv2.bitwise_not(word)
        word = word / 255
        for row in range(word.shape[0]):
            for col in range(word.shape[1]):
                target.write(str(word[row, col]) + ",")
        target.write(label[1])
        target.write("\n")
    i += 1

target.close()
cv2.waitKey(10000)
