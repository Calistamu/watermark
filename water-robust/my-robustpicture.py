#!/bin/python
# -*- coding=utf-8 - *-
import numpy as np
import cv2

def get_key(strr):
    str = ''
    for i in range(len(strr)):
        str = str+'{0:08b}'.format(ord(strr[i]))
    s=''
    for i in str:
        for j in range(5):
            s=s+i
    return s

def embed(path,watercode,newpath):
    image_array = cv2.imread(path)
   # image_yuv=cv2.cvtColor(image_array,cv2.cv2.COLOR_BGR2YCR_CB) 
    image_y=image_array[:,:,0]
    hanglength=image_y.shape[0]
    lielength=image_y.shape[1]
    flaghang=0

    k=0
    for i in range(0,hanglength,8):
        for j in range(0,lielength,8):
            if i+8>hanglength:
                flaghang=1
                break
            if j+8>lielength:
                break
            array=np.zeros((8,8))#生成一个8*8的数组
            array_needdct=image_y[i:i+8,j:j+8].copy()#拷贝数组
            array_float=np.float32(array_needdct)
            arraydct=cv2.dct(array_float)
            #水印嵌入
            a=arraydct[1,0]
            b=arraydct[2,0]
            intk=int(watercode[k])
            if k==len(watercode)-1:
                flaghang=1
                break
            else :
                k+=1
            if intk==1:
             if abs(a-b)>5:
               if a<=b:
                   arraydct[1,0],arraydct[2,0]=arraydct[2,0],arraydct[1,0]
               else:
                   if a>b:
                       a+=6
                   else :
                        b+=6
                        arraydct[1,0],arraydct[2,0]=arraydct[2,0],arraydct[1,0]
            elif intk==0:
              if abs(a-b)>5:
               if a>b:
                    arraydct[1,0],arraydct[2,0]=arraydct[2,0],arraydct[1,0]
               else:
                   if a<b:
                        b+=6
                   else:
                       a+=6
                       arraydct[1,0],arraydct[2,0]=arraydct[2,0],arraydct[1,0]
            arrayidct=cv2.idct(arraydct)
            image_y[i:i+8,j:j+8]=arrayidct.copy()
        if flaghang==1:
            break
    image_array[:,:,0]=image_y
   # image_newarray=cv2.cvtColor(image_array,cv2.cv2.COLOR_BGR2YCR_CB) 
    cv2.imwrite(newpath,image_array)

if __name__=='__main__':
        pictureurl='C:\\Users\\76419\\Desktop\\picture.bmp'
        newpictureurl='C:\\Users\\76419\\Desktop\\newpicture.bmp'
        key=get_key('chao')
        embed(pictureurl,key,newpictureurl)