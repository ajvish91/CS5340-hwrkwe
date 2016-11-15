import cv2
import numpy as np
import conncomp


def extractLines(img, file, lines_text):
    # Word extraction from machine-# printed area
    word_text = lines_text.split(" ")
    word_counter = 0
    # print word_text, len(word_text)
    word_array = []

    # Performing Vertical Profile Projection
    vertical = conncomp.verticalProfileProjection(img)
    histogram = vertical["histogram"]
    zero_count = vertical["zero_count"]
    non_zero_count = vertical["non_zero_count"]
    avg_line_spacing = vertical["avg_line_spacing"]
    avg_line_height = vertical["avg_line_height"]

    # Initializing counters
    zero_counter = 0
    non_zero_counter = 0
    i = 0

    # Initializing Line Array
    lines = np.empty(non_zero_count.shape)

    while ((i < img.shape[0]) and
           (zero_counter < len(zero_count)) and
           (non_zero_counter < len(non_zero_count)) and
           (word_counter < len(word_text))):
        # print "Word Counter 1", word_counter
        if histogram[i] == 0:
            i += zero_count[zero_counter]
            zero_counter += 1
        else:
            line = img[i:i + non_zero_count[non_zero_counter],
                       0:img.shape[1] - 1]
            if line.shape[0] < avg_line_height - 30:
                print "Not a line"
            elif avg_line_height * 5 < line.shape[0]:
                this_line = line.shape[0]
                if avg_line_height is None or avg_line_height == 0:
                    avg_line_height = 2
                number_of_lines = int(this_line / avg_line_height)
                print number_of_lines
                sub_lines = np.vsplit(line, number_of_lines)
                for sub_line in sub_lines:
                    cv2.imwrite("lines/line_" + str(non_zero_counter) + file,
                                sub_line)
                    # print "Word Counter 2", word_counter, len(word_array)
                    line_imagefile = cv2.imread("lines/line_" +
                                                str(non_zero_counter) +
                                                file, 0)
                    inc, new_words = extractWords(line_imagefile,
                                                  file, word_text,
                                                  word_counter)
                    word_counter = inc
                    for word_found in new_words:
                        word_array.append(word_found)
                    # print "Word Counter 3", word_counter, len(word_array)
            else:
                cv2.imwrite("lines/line_" + str(non_zero_counter) + file,
                            line)
                # print "Word Counter 2", word_counter, len(word_array)
                line_imagefile = cv2.imread("lines/line_" +
                                            str(non_zero_counter) + file, 0)
                inc, new_words = extractWords(line_imagefile,
                                              file, word_text, word_counter)
                word_counter = inc
                for word_found in new_words:
                    word_array.append(word_found)
                # print "Word Counter 3", word_counter, len(word_array)
            i += non_zero_count[non_zero_counter]
            non_zero_counter += 1
    # print len(word_array)
    word_map = zip(word_array, word_text)
    return word_map


def extractWords(img, file, word_text, word_counter):
    # Get horizontal profile of the line
    horizontal = conncomp.horizontalProfileProjection(img)
    histogram = horizontal["histogram"]
    zero_count = horizontal["zero_count"]
    non_zero_count = horizontal["non_zero_count"]
    avg_word_spacing = horizontal["avg_word_spacing"]
    avg_word_width = horizontal["avg_word_width"]

    # Initializing the counters
    zero_counter = 0
    non_zero_counter = 0
    i = 0

    # Word Array accumulator
    word_array = []

    # print avg_word_width, avg_word_spacing
    while ((i < img.shape[1]) and
           (zero_counter < len(zero_count)) and
           (non_zero_counter < len(non_zero_count)) and
           (word_counter < len(word_text))):
        if histogram[i] == 0:
            if zero_count[zero_counter] < avg_word_spacing - 50:
                i += non_zero_count[non_zero_counter]
                non_zero_counter += 1
            i += zero_count[zero_counter]
            zero_counter += 1
        else:
            word = img[0:img.shape[0] - 1,
                       i:i + non_zero_count[non_zero_counter]]
            if (word.shape[1] < avg_word_width / 2.5 or
                    zero_count[zero_counter - 1] < avg_word_spacing / 2):
                word = np.hstack((img[0:img.shape[0] - 1, i -
                                      zero_count[zero_counter - 1] -
                                      non_zero_count[non_zero_counter - 1]:
                                      i - zero_count[zero_counter - 1]],
                                  word))
                word[:, word.shape[1] / 2] = 125
                # cv2.imwrite("words/word_" + str(word_counter) +
                #             word_text[word_counter - 1] + file,
                #             word)
                # print "small word"
                if len(word_array) == 0:
                    word_array.append(word / 255)
                else:
                    word_array[-1] = word / 255
                # print "not a word", word_text[word_counter]
            else:
                # print word_text[word_counter]
                # cv2.imwrite("words/word_" + str(word_counter) +
                #             word_text[word_counter] + file,
                #             word)
                word_array.append(word / 255)
                word_counter += 1
            # # print words.shape
            # print "non_zero_counter ", non_zero_counter
            i += non_zero_count[non_zero_counter]
            non_zero_counter += 1
    # cv2.namedWindow("word", cv2.WINDOW_NORMAL)
    # cv2.imshow("word", test)
    # print "This is my word array length for this line ", len(word_array)
    return word_counter, word_array
