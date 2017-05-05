#!/usr/bin/env python
#coding:utf-8
"""
Create data is : 2017-05-03;
@author: ZZK
@function:
Create the fingerprint maps databases, the parameter is position(x,y),RSSI(node0,node1,node2,node3),Proximity(node0,node1,node2,node3),time;

@Python Version:python2.7

"""

from bluepy.btle import Scanner, DefaultDelegate
import MySQLdb
import numpy as np
import tensorflow as tf
import math
import fitting
import scipy
import time

#define all the use data, create the formula of (rssi = -10*n*lgd + A)
#if BLE_NUM=4 , it shows rssi and proximity is a 4 vector.
n = fitting.k
A = fitting.b
BLE_NUM = 4
MAC_ADDR = {}
POSITION = '(0.5,0.5)'
RSSI = []
PROXIMITY = []

#define the class
                                                                                                                                                                             1,1           Top
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            pass
#            print "Discovered device", dev.addr
        elif isNewData:
            pass
#            print "Received new data from", dev.addr

#define all use the function 
def get_distance(n,A,rssi):
    return math.exp(-(A+rssi)/(10*n))


def get_mac_rssi():
    pass

#set proximity is nearest is 0;near is 1;far is 2;
def judge_proximity(distance):
    if distance <= 1.0:
        return '0.0'
    elif distance > 1.0 and distance <= 6.0:
        return '1.0'
    elif distance > 6.0:
        return '2.0'


def now_time():
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return now_time

def deposit_mysql(position,rssi,proximity,time,ble_num):
    conn = MySQLdb.connect(host='59.110.153.188',user='fredy',passwd='123456',db='python',
                                port=3306)
    cur = conn.cursor()
    value = [position,rssi,proximity,time,ble_num]
    try:
        cur.execute('insert into FingerPrintMaps values(%s,%s,%s,%s,%d)',value[0],value[1],value[2],value[3],value[4])
        print 'ok'
    except:
        print 'error'
    conn.commit()
    cur.close()
    conn.close()

#the main , use the same mac_addr collect the 20 time,and then get the average.
if __name__ == '__main__':
#    number = 20
    while(1):
        for i in range(21):
            scanner = Scanner().withDelegate(ScanDelegate())
            devices = scanner.scan(5.0)
            for dev in devices:
                if dev.addr in MAC_ADDR:
                    MAC_ADDR[dev.addr] = MAC_ADDR[dev.addr] + dev.rssi
                else:
                                                                               MAC_ADDR[dev.addr] = dev.rssi

        for addr in MAC_ADDR:
            MAC_ADDR[addr] = MAC_ADDR[addr] / 20
            RSSI.append(MAC_ADDR[addr])
            d = get_distance(n,A,float(MAC_ADDR[addr]))
            PROXIMITY.append(judge_proximity(d))

        deposit_mysql(position,RSSI,PROXIMITY,time=now_time(),ble_num)
        print 'finally the code'

