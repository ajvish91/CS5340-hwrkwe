from seqlearn.datasets import load_conll
from seqlearn.hmm import MultinomialHMM
from seqlearn.evaluation import whole_sequence_accuracy
import numpy as np


# Gets the features from test.txt
def features(sequence, i):
    split_sequence = sequence[i].split(" ")
    print sequence, i
    yield str(sequence)


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


def trainHMM(perc):
    # # Extracts features from the datasets
    X_train, y_train, lengths_train = load_conll("test.txt", features)

    # # Models it as an HMM
    clf = MultinomialHMM()
    clf.fit(X_train, y_train, lengths_train)

    # print X_train, y_train
    return clf


def testHMM(clf):
    # Validation after training
    X_test, y_test, lengths_test = load_conll("test.txt", features)
    y_pred = clf.predict(X_test, lengths_test)

    print y_pred
    # # Final score
    print(whole_sequence_accuracy(y_test, y_pred, lengths_test))
