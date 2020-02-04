import email.utils
import re

i = 13
if i >0 and i < 100:
    lst = ["vin <vineet@>","vineet <vineet@gmail.com>","vineet <vineet@gma.il.co.m>","vineet <vineet@gma-il.co-m>","vineet <vineet@gma,il.co@m>", \
           "vineet <vineet@gmail,com>","vineet <.vin@gmail.com>","vineet <vin-nii@gmail.com>","vineet <v__i_n-n_ii@gmail.com>",
           "this <is@valid.com>" ,"this <is_som@radom.stuff>","this <is_it@valid.com>","this <_is@notvalid.com>"]
    for i_iter in range (i):
        inpstr = lst[i_iter]
        emailaddr = email.utils.parseaddr(inpstr)[1]
        if emailaddr is None:
            break
        match = re.search(r'^[a-z]+[\w.-]+@[a-zA-Z]+\.+?[a-zA-Z]{1,3}$',emailaddr)
        if match:
            print (match.group())
else:
    pass