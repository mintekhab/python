#!/usr/bin/python
#s = "vyyjrasomf"
#counter = 0 
#for char in s:
#    if char == 'a' or char == 'e' \
#    or char == 'i' or char == 'o' \
#    or char == 'u' :
#       counter += 1
#print ("Number of vowels: ",counter)

# long_str = s[0]
# last_sub = s[0]
# for letter in s[1:]:
#     if long_str[-1] <= letter :
#        long_str = long_str + letter
#        print ("if char : " +letter)
#        print ("if string : " + long_str)
#     else:
#         print ("else char : " +letter)
#         if len(last_sub) < len(long_str):
#             print ("last_sub :" , last_sub)
#             print (len(last_sub))
#             print ("long_str :" , long_str)
#             print (len(long_str))
#             last_sub = long_str
#         long_str = letter
#         print ("else string : " + long_str)
#     print ("last string : " + last_sub)
# if len(last_sub) < len(long_str):
#    print (long_str)
# else:
#    print (last_sub)   

x = 23
epsilon = 0.01
step = 0.1
guess = 0.0

while abs(guess**2-x) >= epsilon:
    if guess <= x:
        guess += step
    else:
        break

if abs(guess**2 - x) >= epsilon:
    print('failed')
else:
    print('succeeded: ' + str(guess))