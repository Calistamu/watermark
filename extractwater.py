#!/bin/python
# -*- coding=utf8 - *-
import cv2
import numpy as np

def extract(embed_path):
    im_array = cv2.imread(embed_path, cv2.IMREAD_COLOR)
    im_array_flatten = im_array.flatten()

    length_bin_string = '0b'
    for i in range(0, 8):
        if im_array_flatten[i] & 1 == 0:
            length_bin_string += '0'
        else:
            length_bin_string += '1'

    watermark_length = int(length_bin_string, 2)

    watermark = ''
    for i in range(watermark_length):
        char_bin_string = '0b'
        for j in range(8 * (i + 1), 8 * (i + 1) + 8):
            if im_array_flatten[j] & 1 == 0:
                char_bin_string += '0'
            else:
                char_bin_string += '1'

        char = chr(int(char_bin_string, 2))

        watermark += char

    print(watermark)

if __name__ == '__main__':
    extract('C:\\Users\\76419\\Desktop\\newpicture.bmp')