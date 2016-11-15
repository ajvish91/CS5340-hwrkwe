from seqlearn.datasets import load_conll
from seqlearn.hmm import MultinomialHMM
from seqlearn.evaluation import whole_sequence_accuracy
import numpy as np


# Gets the features from test.txt
def features(sequence, i):
    split_sequence = sequence[i].split(" ")
    # print sequence[i], i
    for ele in (split_sequence):
        yield ele
    # yield sequence[i]


def createTXT(words):
    # Saves the image into a TXT file
    for word in words:
        f_handle = file('test.txt', 'a')
        np.savetxt(f_handle, word[0].flatten(), delimiter=" ",
                   fmt="%i", newline=" ",
                   header='', footer="" + word[1] + "\n\n",
                   comments='')
        f_handle.close()
    return "test.txt"


def trainHMM(data):
    # # Extracts features from the datasets
    X_train, y_train, lengths_train = load_conll(data, features)

    # # Models it as an HMM
    clf = MultinomialHMM(decode='viterbi', alpha=0.2)
    clf.fit(X_train, y_train, lengths_train)

    # print X_train, y_train
    return clf


def testHMM(clf, data):
    # Validation after training
    X_test, y_test, lengths_test = load_conll(data, features)
    y_pred = clf.predict(X_test, lengths_test)

    print y_pred
    # # Final score
    print(whole_sequence_accuracy(y_test, y_pred, lengths_test))
