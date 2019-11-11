#!/bin/python
# -*- coding=utf8 - *-
import cv2
import numpy as np

    #cv2.imread()：读入图片，共两个参数，
    # 第一个参数为要读入的图片文件名，
    # 第二个参数为如何读取图片，包括cv2.IMREAD_COLOR：读入一副彩色图片；cv2.IMREAD_GRAYSCALE：
    # 以灰度模式读入图片；cv2.IMREAD_UNCHANGED：读入一幅图片，并包括其alpha通道。

#flatten返回一个折叠成一维的数组。但是该函数只能适用于numpy对象，即array或者mat，普通的list列表是不行的。

  #获取要隐藏的文件内容并转化为二进制,开头八位二进制表示水印的字符长度
def get_key(strr):
    str = ''
    a=len(strr)
    str=str+'{0:08b}'.format(a)
    for i in range(len(strr)):
         #逐个字节将要隐藏的文件内容转换为二进制，并拼接起来
         #1.先用ord()函数将s的内容逐个转换为ascii码,
         # ord() 函数是 chr() 函数（对于8位的ASCII字符串）或 unichr() 函数（对于Unicode对象）的配对函数，
         # 它以一个字符（长度为1的字符串）作为参数，返回对应的 ASCII 数值，或者 Unicode 数值，
         # 如果所给的 Unicode 字符超出了你的 Python 定义范围，则会引发一个 TypeError 的异常。
         #2.使用bin()函数将十进制的ascii码转换为二进制
         #3.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空
         #4.又由于ascii码转换二进制后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位
        #a=(bin(ord(strr[i])).replace('0b',''))
        str = str+'{0:08b}'.format(ord(strr[i]))
    return str

#嵌入水印
def embed(picturepath,code,newpath):
     image_array = cv2.imread(picturepath, cv2.IMREAD_COLOR)
     im_array_flatten = image_array.flatten()
     length=len(code)
     codelist=list(code)
     n=0
     for c in codelist:
         if c=='0':
            if im_array_flatten[n]%2!=0:
                im_array_flatten[n]-=1
         elif c=='1':
            if im_array_flatten[n]%2!=1:
                 im_array_flatten[n]+=1
         n+=1
     reshape= np.reshape(im_array_flatten,image_array.shape)
     cv2.cv2.imwrite(newpath, reshape)
#waitKey()函数的功能是不断刷新图像，频率时间为delay，单位为ms。返回值为当前键盘按键值。
if __name__=='__main__':
        pictureurl='C:\\Users\\76419\\Desktop\\picture.bmp'
        #\是错误的
        newpictureurl='C:\\Users\\76419\\Desktop\\newpicture.bmp'
        key=get_key('I am chao haha')#将嵌入信息转化为二进制
        embed(pictureurl,key,newpictureurl)#嵌入水印
