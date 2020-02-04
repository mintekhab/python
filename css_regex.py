import re

i = 11
if i >0 and i < 50:
    lst = ["#BED","{","color: #FfFdF8; background-color:#aef;","font-size: 123px;","background: -webkit-linear-gradient(top, #f9f9f9, #fff);","}","#CAB","{","background-color: #ABC;","border: 2px dashed #fff;","}"]
    for i_iter in range (i):
        inpstr = lst[i_iter]
        match = re.findall(r'(?<!^)(#(?:[\da-f]{3}){1,2})',inpstr,re.IGNORECASE)
        for elem in match:
            print (elem)
else:
    pass