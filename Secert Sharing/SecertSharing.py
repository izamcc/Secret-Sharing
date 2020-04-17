from binascii import hexlify , unhexlify
from scipy.interpolate import lagrange
import numpy as np
from numpy.polynomial.polynomial import Polynomial

#input your Secret
secret = int(input("what's u'r secres?  - "))

#create shares
nshares = int(input("Numper of Shares : "))
shares = {}
for i in range(nshares):
    index = i+1
    share = secret + (166*index) + (94*(pow(index,2)))
    shares.update({index:share})

#printing Shares
for k,v in shares.items():
    print(k,v)




#get X & Y vlues
intryx = []
intryy = []
for i in range(3):

    v = int(input('Share Numper - '))
    intryx.append(v)
    k = int(input('Share value - '))
    intryy.append(k)



#reconstruct
x = np.array(intryx)
y = np.array(intryy)
p = lagrange(x,y)
print(p)
p = Polynomial(p).coef
print(int(p[-1]))






