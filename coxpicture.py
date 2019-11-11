#!/bin/python
# -*- coding=utf-8 - *-

import numpy as np
import cv2

def get_key(strr):
    str = ''
    for i in range(len(strr)):
        str = str+'{0:08b}'.format(ord(strr[i]))
    return str

def embed(path,watercode,newpath):
    #读取图片，取y分量，再dct,取出dct后的交流分量排序
    image_array = cv2.cv2.imread(path)
    #没有参数，读取的是rgb色彩空间
    image_yuv=cv2.cv2.cvtColor(image_array,cv2.cv2.COLOR_BGR2YCR_CB) 
    #此处转化为Ycbcr色彩空间
    #cv2.cv2.cvtColor( )#进行色彩空间的转换
    #opencv中有多种色彩空间，包括 RGB、HSI、HSL、HSV、HSB、YCrCb、CIE XYZ、CIE Lab8种，使用中经常要遇到色彩空间的转化，以便生成mask图等操作
    image_y=image_yuv[:,:,0]#
    image_y=image_array[:,:,0]
    image_yfloat=np.float32(image_y)
    #image_yfloat=np.float32(image_array)
    #在此处很奇怪，一直报错说是多维数组无法dct，还有就是数据类型需要是浮点数，但此时只需要改成浮点数就可以正常dct了
    image_ydct=cv2.cv2.dct(image_yfloat)
    image_yflatten=image_ydct.flatten()
    index=np.argsort(-(image_yflatten[1:]))
    #argsort()函数是将x中的元素从小到大排列，提取其对应的index(索引)，然后输出到y
    #第一个是直流分量，我们只对交流分量进行排序
    image_yac=image_yflatten[1:]
   
   #嵌入水印
    i=0
    a=30#水印强度
    for w in watercode:
          w=int(w)
          image_yac[index[i]]=image_yac[index[i]]+a*w #x'=x+wa
          i += 1
   
   #嵌入水印后的y分量赋值回去，重新变成矩阵，idct,y分量代替旧的值，然后存储
    image_yflatten[1:]=image_yac
    image_reshape=np.reshape(image_yflatten,image_array.shape)
    image_newy=cv2.cv2.idct(image_reshape)
    i=0
    image_array[:,:,0]=image_newy
    image_array=cv2.cv2.cvtColor(image_yuv,cv2.cv2.COLOR_YCR_CB2BGR) 
    cv2.cv2.imwrite(newpath,image_array)

def extract(path,newpath):
    #将待检测的图像和原图像进行DCT变换
    newarray = cv2.cv2.imread(newpath)  
    newyuv = cv2.cv2.cvtColor(newarray,cv2.cv2.COLOR_BGR2YCR_CB) 
    newy=newyuv[:,:,0]
    newy=np.float32(newy)
    newydct=cv2.cv2.dct(newy)
    newydctflatten=newydct.flatten()
    newyac=newydctflatten[1:]
    newindex=np.argsort(-(newydctflatten[1:])) 

    oldarray=cv2.cv2.imread(path,cv2.cv2.IMREAD_COLOR)
    oldyuv=cv2.cv2.cvtColor(oldarray,cv2.cv2.COLOR_BGR2YCR_CB)
    oldy=oldyuv[:,:,0]
    oldy=np.float32(oldy)
    oldydct=cv2.cv2.dct(oldy)
    oldydctflatten=oldydct.flatten()
    oldyac=oldydctflatten[1:]
    oldindex=np.argsort(-(oldydctflatten[1:])) 

   #提取水印
    watercodebin=''
    a=30#水印强度
    for j in range(len(oldindex)):
        w=(newyac[oldindex[j]]-oldyac[oldindex[j]])/a
        watercodebin+=str(int(w))

    watermark=''
    for j in range(0,len(oldyac)):
        char_bin='0b'
        for k in range(j*8,j*8+8):
            char_bin+=watercodebin[k]
        if int(char_bin,2)==0:
            break
        else:
            char=chr(int(char_bin,2))
            watermark+=char
    print(watermark)
if __name__=='__main__':
        pictureurl='C:\\Users\\karen\\Desktop\\water\\lenacolor.bmp'
        newpictureurl='C:\\Users\\karen\\Desktop\\water\\lenawatered.bmp'
        key=get_key('chao')
        embed(pictureurl,key,newpictureurl)
        extract(pictureurl,newpictureurl)