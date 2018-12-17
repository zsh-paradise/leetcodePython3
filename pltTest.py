# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
labels='frogs','hogs','dogs','logs'
sizes=15,20,45,10
colors='yellowgreen','gold','lightskyblue','lightcoral'
explode=0,0.1,0,0
#饼状图
#plt.pie(sizes,explode=explode,labels=labels,colors=colors,autopct='%1.1f%%',shadow=True,startangle=50)
#plt.axis('equal')
#plt.show()

t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
x =[2013,2014,2015,2016,2017]
#总资产
y1=[30991.21,40151.36,45206.88,58958.77,56938.96]
#货币资金
y2 =[4301.32+825.02,4680.23+690.27,4294.93+943.62,5204.71+1780.72,4380.71+501.49]
#固定资产
y3=[160.90,191.61,199.34,192.50,192.65]
#无形资产
y4=[40,39.01,39.49,38.03,37.04]
#贷款和垫款
y5=[15248.03,17590.94,19818.55,23818.79,27149.57]
#吸收存款
y6=[21249.78,24063.08,27021.66,30506.69,29360.21]
#股东权益
y7=[1948.77,2363.30,2965.77,3368.20,3721.90]
#解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
lines = plt.plot(x, y1, 'r--', x,y5,'c*',x,y6,'y.')

plt.xticks(range(2013,2018,1))
plt.title(u'负债摘要图1')
plt.xlabel(u'年份')
plt.ylabel(u'资金（亿元）')
plt.legend((u'总资产', u'贷款和垫款', u'吸收存款'),
           loc='lower right')
plt.show()


plt.plot( x,y3, 'b', x, y4, 'g')
plt.xticks(range(2013,2018,1))
plt.title(u'负债摘要图2')
plt.xlabel(u'年份')
plt.ylabel(u'资金（亿元）')
plt.legend((u'固定资产', u'无形资产'),
           loc='center right')
plt.show()

plt.plot( x,y3, 'b')
plt.xticks(range(2013,2018,1))
plt.title(u'货币资金')
plt.xlabel(u'年份')
plt.ylabel(u'资金（亿元）')

plt.show()
# mu, sigma = 100, 15
# x = mu + sigma * np.random.randn(10000)
#
# # 数据的直方图
# n, bins, patches = plt.hist(x, 50, normed=1, facecolor='g', alpha=0.75)
#

# plt.xlabel('Smarts')
# plt.ylabel('Probability')
# #添加标题
# plt.title('Histogram of IQ')
# #添加文字
# plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
# plt.axis([40, 160, 0, 0.03])
# plt.grid(True)
# plt.show()