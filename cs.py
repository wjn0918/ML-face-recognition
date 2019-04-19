a = [1,2,3]
b = ['a','b','c']
c = zip(a,b)
e,f = zip(*c)
print(e)
e = list(e)
print(e)