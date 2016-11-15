import cv2
import numpy as np


def countZeroSequences(seq):
    zero_sequences = np.array([0])
    for i in seq:
        if i == 0:
            zero_sequences[len(zero_sequences) - 1] += 1
        elif i != 0 and zero_sequences[len(zero_sequences) - 1] != 0:
            zero_sequences = np.append(zero_sequences, 0)
        else:
            continue
    return zero_sequences


def countNonZeroSequences(seq):
    non_zero_sequences = np.array([0])
    for i in seq:
        if i != 0:
            non_zero_sequences[len(non_zero_sequences) - 1] += 1
        elif i == 0 and non_zero_sequences[len(non_zero_sequences) - 1] != 0:
            non_zero_sequences = np.append(non_zero_sequences, 0)
        else:
            continue
    return non_zero_sequences


def verticalProfileProjection(img):
    count = np.zeros(img.shape[0])
    test = cv2.bitwise_not(img)
    for i in range(test.shape[0]):
        count[i] = np.count_nonzero(test[i])
        if count[i] == 0:
            test[i, :] = 125
    zero_count = countZeroSequences(count)
    non_zero_count = countNonZeroSequences(count)
    avg_line_spacing = np.mean(zero_count[1:len(zero_count) - 1])
    avg_line_height = np.mean(non_zero_count)
    return {"histogram": count,
            "zero_count": zero_count,
            "non_zero_count": non_zero_count,
            "avg_line_spacing": avg_line_spacing,
            "avg_line_height": avg_line_height}


def horizontalProfileProjection(img):
    count = np.zeros(img.shape[1])
    test = cv2.bitwise_not(img)
    for i in range(test.shape[1]):
        count[i] = np.count_nonzero(test[:, i])
        if count[i] == 0:
            test[:, i] = 125
    zero_count = countZeroSequences(count)
    non_zero_count = countNonZeroSequences(count)
    # print zero_count, non_zero_count
    avg_word_spacing = np.mean(zero_count[1:len(zero_count) - 1])
    avg_word_width = np.mean(non_zero_count)
    return {"histogram": count,
            "zero_count": zero_count,
            "non_zero_count": non_zero_count,
            "avg_word_spacing": avg_word_spacing,
            "avg_word_width": avg_word_width}
