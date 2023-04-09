"""
You can enter your code here and it will automatically open Stack Overflow pages related to any errors it encounters. 
This is a helpful way to quickly access potential solutions to any problems you might encounter in your code.

"""
# ex: TypeError: 'str' object does not support item assignment
x = None
s = input()
x = s[0]
i = 1
while i<=len(s):
    s[i-1]=s[i]
    i += 1
s[len(s)]=x
print(s, end = '')
