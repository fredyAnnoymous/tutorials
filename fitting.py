#!/usr/local/env python
#coding:utf-8
"""
Create data is 2017-05-03;
@author: ZZK
@function:
plot the line of data ,and calculate the parameter of (RSSI=-10*lg(d) - A)
@Python Version: python2.7

""" 
import numpy as np
import MySQLdb
import matplotlib.pyplot as plt  
import math
from scipy import optimize


def mysql_connect(x,y,d):
    conn = MySQLdb.connect(host='59.110.153.188',user='fredy',passwd='123456',port=3306,db='python')
    cur = conn.cursor()
    sql = 'select RSSI from test where Distance={}'.format(d)
    cur.execute(sql)
    data = cur.fetchall()
    x.append(d)
    sum = 0
    for i in range(len(data)):
	sum = sum + float(data[i][0])
    aver = sum / (len(data))
    y.append(aver)
    cur.close()
    conn.close()
"""
def plot_scatter(x,y):
    x = np.array(x)
    y = np.array(y)
    plt.title('RSSI and Distance')
    plt.scatter(x,y,c='b',marker='o',s=6)
    plt.ylabel('RSSI(dB)')
    plt.ylim(-100,-30)
    plt.xlabel('Distance(m)')
    plt.xlim(0,6)
    plt.legend()
    plt.show()    
"""

if __name__ == '__main__':
    x = []
    y = []
    z = []
    distance = ['0.5','1.0','2.0','3.0','4.0']
    for i in range(len(distance)):
	mysql_connect(x,y,distance[i])
    rssi = np.array(y)
    for d in x:
	z.append(math.log10(float(d)))
    z = np.array(z)
	
    def residuals(p):
	k,b = p 
	return rssi-10*k*z-b
    r = optimize.leastsq(residuals,[1,0])
    k,b = r[0]
    y_t = z * k * 10 + b
    plt.title('RSSI And Distance')
#    plt.plot(x,rssi,label="RSSI and Distance")
    plt.plot(x,rssi,"b--",label='reference')
    plt.scatter(x,y)
    plt.plot(x,y_t,label='fitting line')
    plt.legend()
    plt.show()

#    r = optimize.leastsq(residuals,[1,0])
#    k,b = r[0]
    print "The parameter n is {}".format(k)
    print "The parameter A is {}".format(b)
