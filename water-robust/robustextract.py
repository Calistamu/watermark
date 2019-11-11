import numpy as np
import cv2

def extract(newpath):
    image_array=cv2.cv2.imread(newpath)
    image_yuv=cv2.cv2.cvtColor(image_array,cv2.cv2.COLOR_BGR2YCR_CB)
    image_y=image_array[:,:,0]
    hanglength=image_y.shape[0]
    lielength=image_y.shape[1]

#提取水印
    watercode=''
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
            arraydct=cv2.cv2.dct(array_float)
            #arraydct=cv2.dct(array_needdct)
            a=arraydct[1,0]
            b=arraydct[2,0]
            if a>b:
                watercode=watercode+'1'
            elif a<=b:
                watercode=watercode+'0'
        if flaghang==1:
            break
#水印缩减成原来的水印     
    j=0
    count1=0
    count0=0
    watercodeshort=''
    for i in watercode:
        if i=='1':
            count1+=1
            j+=1
        elif i=='0':
            count0+=1
            j+=1
        if j==5:
            if count1>count0:
                watercodeshort=watercodeshort+'1'
            else:
                watercodeshort=watercodeshort+'0'
            j=0
            count1=0
            count0=0
    #水印转化为字符
    j=0
    watermark=''
    for i in watercodeshort:
       w=''
       w=w+i
       j+=1
       if(j==8):
        j=0
        char=chr(int(w,2))  
        watermark+=char
        w=''
    
    print(watermark)

if __name__=='__main__':
        newpictureurl='C:\\Users\\karen\\Documents\\GitHub\\lenawatered.bmp'
        extract(newpictureurl)