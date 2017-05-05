#!/usr/bin/env python
#coding:utf-8
"""
Create data is: 2017-02-27
@author: ZZK
@function:
Get the data from BLE, store the data into database;
It is the first step.
@Python Version: python2.7
"""
import MySQLdb
from bluepy.btle import Scanner, DefaultDelegate
import time

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

def mysql_connect(addr,rssi,distance,time):
    conn = MySQLdb.connect(host='59.110.153.188',user='fredy',passwd='123456',db='python',port=3306)
    cur = conn.cursor()
    try:
#	cur = conn.cursor()
#	cur.execute('create database if not exists python')
#	conn.select_db('python')
	cur.execute('DROP TABLE IF EXISTS TEST')
#	cur.execute('create table test(Device varchar(30),RSSI(dB) varchar(10),Distance varchar(10), Time varchar(50))')
	sql = """create table test (
			Device varchar(30),
			RSSI   varchar(10),
			Distance varchar(10),
			Time varchar(50))"""
	cur.execute(sql)
	#cur.commit()
    except:
	pass		
    value = [addr,rssi,distance,time]
    cur.execute('insert into test values(%s,%s,%s,%s)',value)
    print 'ok'
    conn.commit()
    cur.close()
    conn.close()	

if __name__ == '__main__':
    number = 0
    while(1):
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(5.0)
#	time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	distance = "0.5"
	if number <= 50:
#	    number = number + 1
            for dev in devices:
#	    time = str(time)
		number = number + 1
	        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print "Device %s (%s), RSSI=%d dB, Distance=%s m, Time(m)=%s" % (dev.addr, dev.addrType, dev.rssi, distance, t)
                mysql_connect(dev.addr,dev.rssi,distance,t)
	        for (adtype, desc, value) in dev.getScanData():
                    print "  %s = %s" % (desc, value)
	else:
	    print "date collect finally"	 
	    break


