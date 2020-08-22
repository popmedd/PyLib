# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 17:35:46 2020

@author: Administrator
"""


import time
from websocket import create_connection
import sqlite3
import pandas as pd
# from_engine('postgresql+psycopg2://postgres:123456@localhost:5432/bitmex_chat')
# wss://stream.binance.com:9443
# wss://www.bitmex.com/realtime?subscribe=chat
# wss://api.huobi.pro/ws
# wss://api-aws.huobi.pro/ws


url = "wss://www.bitmex.com/realtime?subscribe=quoteBin1m"

import json
import sqlite3

def connDB():
    conn = sqlite3.connect("test2.db")
    return conn

def initTable():
    sql = "create table bitmex (id INTEGER  primary key, timestamp TXT, symbol TEXT,bidSize INTEGER,bidPrice REAL, askPrice REAL)"
    conn=connDB()
    cursor = conn.cursor()
    cursor.execute(sql)  
    conn.commit()
    conn.close()

def save(jsonData):
    conn=connDB()
    cursor = conn.cursor()
    for data in jsonData:
        sql = """
        insert into bitmex (id, timestamp,symbol,bidSize,bidPrice,askPrice) values 
        (null,'%s','%s',%s,%s,%s)
        """% (data['timestamp'],data['symbol'],data['bidSize'],data['bidPrice'],data['askPrice'])
        print(sql)
        cursor.execute(sql)
    conn.commit()
    conn.close()
    

if __name__ == "__main__":

     
    while True:  # 一直链接，直到连接上就退出循环
        time.sleep(5)
        try:
            ws = create_connection(url, http_proxy_host="127.0.0.1", http_proxy_port=10809)
            print(ws)
            break
        except Exception as e:
            print('连接异常：', e)
            continue
    while True:  # 连接上，退出第一个循环之后，此循环用于一直获取数据
        # response =int(ws.recv())[['data']]
        # response =ws.recv()
        
        # print(response)
        #首次运行放开下面代码创建数据表
        initTable()
        jsonDataStr=ws.recv()['data']
        jsonData = json.loads(jsonDataStr)
        save(jsonData)            

