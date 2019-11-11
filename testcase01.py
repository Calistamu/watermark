f=open('C:\\Users\\76419\\source\\repos\\Project1\\Project1\\testcasedis.txt','r')
lines=f.readlines()
f.close()
for line in lines:
    if line.find('call')!=-1:
        print(line)