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

def extract(image_path,embed_path,intensity):
    im_array = cv2.cv2.imread(image_path)
    imyuv=cv2.cv2.cvtColor(im_array,cv2.cv2.COLOR_BGR2YCR_CB)
    #im=imyuv.astype('float32')
    im_Y=imyuv[:,:,0]
    im_temp=DCT(im_Y)
    im_dct=im_temp.flatten()
    im_X=im_dct[1:]
    index=np.argsort(-(im_X))

    emb_array = cv2.cv2.imread(embed_path)
    embyuv=cv2.cv2.cvtColor(emb_array,cv2.cv2.COLOR_BGR2YCR_CB)
    #emb=embyuv.astype('float32')
    emb_Y=embyuv[:,:,0]
    emb_temp=DCT(emb_Y)
    emb_dct=emb_temp.flatten()
    '''
    for i in range(0,20):
        print(emb_dct[index[i]+1])
    '''
    emb_X=emb_dct[1:]

    wm_bin=''
    watermark=''

    for i in range(0,len(index)):
        #print(emb_X[index[i]],im_X[index[i]])
        w=(emb_X[index[i]]-im_X[index[i]])/intensity
        if int(w)!=0:
            w=1
        wm_bin+=str(int(w)) 
    #print(wm_bin) 

    for j in range(0,len(im_X)):
        char_bin='0b'
        for k in range(j*8,j*8+8):
            char_bin+=wm_bin[k]
        if int(char_bin,2)==0:
            break
        else:
            char=chr(int(char_bin,2))
            watermark+=char

    print(watermark)

if __name__ == '__main__':
    extract('1.png',"2.png",20)