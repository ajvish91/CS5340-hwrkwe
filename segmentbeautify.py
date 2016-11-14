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


def verticalProfileProjection(img, file, lines_text):
    word_text = lines_text.split(" ")
    word_counter = 0
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
    # print avg_line_spacing, avg_line_height
    # print len(zero_count), len(non_zero_count)
    zero_counter = 0
    non_zero_counter = 0
    lines = np.empty(non_zero_count.shape)
    print img.shape[0]
    i = 0
    while i < img.shape[0] and zero_counter < len(zero_count) and non_zero_counter < len(non_zero_count):
        if count[i] == 0:
            i += zero_count[zero_counter]
            zero_counter += 1
        else:
            line = img[i:i + non_zero_count[non_zero_counter],
                       0:img.shape[1] - 1]
            if line.shape[0] < avg_line_height - 30:
                print "Not a line"
            elif avg_line_height + avg_line_spacing < line.shape[0]:
                this_line = line.shape[0]
                number_of_lines = this_line / avg_line_height
                sub_lines = np.split(line, number_of_lines)
                for sub_line in sub_lines:
                    cv2.imwrite("lines/line_" + str(non_zero_counter) + file,
                                sub_line)
                    word_counter += horizontalProfileProjection(cv2.imread(
                        "lines/line_" + file + str(non_zero_counter) + ".jpg"),
                        file, word_text, word_counter)
            else:
                cv2.imwrite("lines/line_" + str(non_zero_counter) + file,
                            line)
                word_counter += horizontalProfileProjection(cv2.imread(
                    "lines/line_" + file + str(non_zero_counter) + ".jpg"),
                    file, word_text, word_counter)
            # print lines.shape
            i += non_zero_count[non_zero_counter]
            non_zero_counter += 1
    # cv2.namedWindow("line", cv2.WINDOW_NORMAL)
    # cv2.imshow("line", test)
    return lines


def horizontalProfileProjection(img, file, word_text, word_counter):
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
    # print avg_word_spacing, avg_word_width
    # print len(zero_count), len(non_zero_count)
    zero_counter = 0
    non_zero_counter = 0
    # print img.shape[0]
    i = 0
    while i < img.shape[1] and zero_counter < len(zero_count) and non_zero_counter < len(non_zero_count):
        if count[i] == 0:
            i += zero_count[zero_counter]
            zero_counter += 1
        else:
            if word_counter == len(word_text):
                word_counter -= 1
            word = img[0:img.shape[0] - 1,
                       i:i + non_zero_count[non_zero_counter]]
            if word.shape[1] < avg_word_width - 100:
                print "not a word"
            else:
                print word_text[word_counter]
                cv2.imwrite("words/word_" + file + str(non_zero_counter) +
                            word_text[word_counter] + ".jpg",
                            word)
                word_counter += 1
            # print words.shape
            i += non_zero_count[non_zero_counter]
            non_zero_counter += 1
    # cv2.namedWindow("word", cv2.WINDOW_NORMAL)
    # cv2.imshow("word", test)
    return word_counter
