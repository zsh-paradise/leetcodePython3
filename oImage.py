import numpy as np
import matplotlib.pyplot as plt


x =np.arange(0,5,0.1)
y =(np.log2(x))*x
z = np.sqrt(x)
q = x

font1 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 9,
}
plt.plot(x,y,label ='$log2(n)*n$')
plt.plot(x,z,label ='$sqrt(n)$')
plt.plot(x,q,label ='$n$')
hl=plt.legend(loc='upper right', prop=font1, frameon=False)

plt.show()