#!/bin/python
# -*- coding=utf-8 - *-
import cv2
import numpy as np
import math

def DCT(im):
    h, w = im.shape[:2]
    new_arry = np.zeros((h,w), np.float32)
    new_arry[:h, :w] = im
    im_dct=cv2.cv2.dct(new_arry)
    return im_dct

def bin_value(value, bitsize):
    binval = bin(value)[2:]
    if len(binval) > bitsize:
        print("Larger than the expected size")
    while len(binval) < bitsize:
        binval = "0" + binval
    return binval

def embed(image_path,watermark,intensity):
    im_array = cv2.cv2.imread(image_path)
    imyuv=cv2.cv2.cvtColor(im_array,cv2.cv2.COLOR_BGR2YCR_CB)
    #im=imyuv.astype('float32')#转成float32是dct必要条件
    im_Y=imyuv[:,:,0]
    im_temp=DCT(im_Y)
    im_dct=im_temp.flatten()
    im_X=im_dct[1:]
    index=np.argsort(-(im_X))#注意需要取绝对值后再降序排列，其中(-x)与(x,-1)最终效果不同？
    '''
    for i in range(0,20):
        print(im_dct[index[i]+1])
    print('***************************')
    '''
    i=0
    for char in watermark:
        binval=bin_value(ord(char), 8)
        for c in binval:
            #print(im_X[index[i]])
            c=int(c)
            im_X[index[i]]=im_X[index[i]]+intensity*c
            #print(im_X[index[i]])
            i += 1
    im_dct[1:]=im_X
    '''
    for i in range(0,20):
        print(im_dct[index[i]+1])
    '''
    im_reshape=np.reshape(im_dct,im_Y.shape)
   
    im_Y_idct=cv2.cv2.idct(im_reshape)
    i=0
    imyuv[:,:,0]=im_Y_idct
    im_array=cv2.cv2.cvtColor(imyuv,cv2.cv2.COLOR_YCR_CB2BGR) 
    cv2.cv2.imwrite("2.png",im_array)

if __name__ == '__main__':
    embed('1.png','Weasley',20)


    '''
    rownum=int(im_Y.shape[0]/8)#8*8分块的行数
	colnum=int(im_Y.shape[1]/8)#8*8分块的列数

    j=0
    for i in range(0,64):
        w=int(watermark[i])
    '''