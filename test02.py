import pefile#用于解析pe文件
import capstone#用于反汇编
f=open('C:\\Users\\76419\\source\\repos\\Project1\\Project1\\testcasedis.txt','r')
lines=f.readlines()
f.close()
function_list=[]
call_ins=[]j4
for line in lines:
    #观察反汇编的结果，发现有三种call语句
    #call 0x123abc
    #call DWDRD PTR ds:0x123abc
    if line.find('call')!=-1:
        #find方法返回字符串的位置，如果没有则为-1
        call_to=line[line.index('call        0x')+len('call        0x'):].strip()
        call_from=line[:line.index(':')].strip()
        #index() 函数用于从列表中找出某个值第一个匹配项的索引位置。
        #strip()去掉前后端多余的空白字符
        call_ins.append((call_from,call_to))
for call_from,call_to in call_ins:
    function_list.append(call_to)

#set去重复，sort排序
function_list=list(set(function_list))
fundtion_list.sort()

function_call_relation=[]

for call_from,call_to in call_ins:
    for i in range(len(function_list)-1):
        if call_from>=function_list[i]and call_from<function_list:
            function_call_relation.append((function_list[i],call_to))

function_call_relation=list(set(function_call_relation))

for caller,callee in function_call_relation:
    print(caller,'->',callee)

print('共%i个函数'%len(function_list))
print('共%i次调用'%len(call_ins))
print('共%i个调用关系'%len(function_call_relation))
    