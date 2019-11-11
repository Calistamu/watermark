import os
import re
#遍历文件夹
rootdir='E:/123'
list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
for i in range(0,len(list)):
    path=os.path.join(rootdir,list[i]) #把目录和文件名合成一个路径
    if os.path.isfile(path):
        pattern=re.compile(r'(\s*)+(\d+)+(\s*)+(\w+)+\s+(\s{3}|\w{8})+\s+(\w+)')
        f=open(path,"r")
        ffile=open(r'E:/functions.txt','w')
        lines=f.readlines()
        for line in lines:
            match_result=pattern.match(line)
            if match_result:
                print(line,file=ffile)
        
