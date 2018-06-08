# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 14:37:57 2018
@author: shengjiex@qq.com
存储日线：把所有数据存储到一个工作表里
数据库叫day,工作表用：price
只保存了创业板最近两年的数据，大约30w行。
获取一次数据需要5s钟，太慢了。
创建date和sid的索引应该可以快很多
db.price.createIndex({date:-1,sid:1},{'unique':true,'dropDups':true})
db.price.createIndex({sid:1,date:-1},{'unique':true,'dropDups':true})
db.price.getIndexes()
更新操作：
我获取所有股票数据，然后挨个股票更新日期，
首先获得最新日期，然后在最新的日期上加1，得到
notes:
如何复权，获取的数据应不复权
"""
#import numpy as np
import tushare as ts
import pandas as pd
import json
from pymongo import MongoClient
import logging
import  datetime
import time

logger = logging.getLogger("day")
# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
#最常用的是StreamHandler和FileHandler, Handler用于向不同的输出端打log。
file_handler = logging.FileHandler("day.log")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.setLevel(logging.WARNING)


class config:
    def __init__(self):
        self.database='day'
        self.collection='price'
        
class MongoBase:
    def __init__(self,database,collection):
        self.database=database
        self.collection=collection
        self.OpenDB()
    def OpenDB(self):
        self.Client = MongoClient('localhost',27017)#接口
        self.db = self.Client[self.database]#数据库
        self.col=self.db[self.collection]#colle
    def closeDB(self):
        self.Client.close()
       

class tushare_mongo:
    def __init__(self,col):
        self.col=col##mongodb.collection
        self.filter_stocks_save()
        
    def get_stocks_list_save(self):
        '''获取tushare里的股票列表'''
        self.stocks=ts.get_stock_basics().index.values
        
    def filter_stocks_save(self):
        '''筛选需要保存的股票列表'''
        self.get_stocks_list_save()
        #self.stocks=[i for i in self.stocks if i.startswith('0')]
        
    def get_day_in_tushare(self,sid,start,end):
        '''从tushare获取一只股票的不复权日线数据 '''
        #for mongo
        p=ts.get_h_data(sid,start,end,autype=None)
        de=[time.localtime(i.astype(datetime.datetime)/1e9) for i in p.index.values]
        date=['{:4}-{:0>2}-{:0>2}'.format(n[0],n[1],n[2]) for n in de]
        p['date']=date
        p['sid']=[sid]*p.shape[0] 
        return  p

    def get_hist_day_in_tushare(self,sid,start,end):
        '''从tushare获取一只股票的不复权日线数据 '''
        #for mongo
        p=ts.get_hist_data(sid,start,end)
        p['date']=p.index.values
        p['sid']=[sid]*p.shape[0] 
        return  p
    
    def save_one_to_mong_day(self,sid,start,end):
        '''保存一只股票的日线数据到mongodb'''
        try:
            day_bar=self.get_day_in_tushare(sid,start,end)            
            if day_bar.shape[0]!=0:
                day_bar_mongo=json.loads(day_bar.T.to_json()).values()
                self.col.insert_many(day_bar_mongo)
                logger.info('save_stocks:sid:{},start:{},end:{}--ok!'.format(sid,start,end))
        except:
            logger.warning('save_stocks:sid:{},start:{},end:{}--failed!'.format(sid,start,end))

    def save_many_to_mongo_day(self,start,end):
        '''保存self.stocks内的股票到mongodb'''
        for sid in self.stocks:
            self.save_one_to_mong_day(sid,start,end)
                    
    def read_one_day_m(self,sid,start,end,fields):
        '''从mongodb读取一只股票的日线数据'''
        if isinstance(fields,list):
            if 'date' not in fields:
                fields.append('date')            
            __field={}#for projection
            for i in fields:
                __field[i]=1
        elif fields==None:
            __field=fields
        else:
            pass
        #__field={'date':1,'sid':1,'open':1}
        query={'sid':sid,'date':{'$gte':start,'$lte':end}}
        try:
            if __field==None:
                data=pd.DataFrame(list(self.col.find(query)))
            else:
                data=pd.DataFrame(list(self.col.find(query,__field)))
            del data['_id']
            data.set_index('date',drop=True, append=False, inplace=True)
            logger.info('read:{}--done!'.format(sid))
        except Exception as e:
            data=[0]
            logger.warning('read:{}--failed {}'.format(sid,e))            
        return data
        
    def read_from_mongo_day(self,stocks,start,end,fields=None):
        '''从mongodb读取日线数据，stocks可以是list，也可以是str'''
        stocks_bar={}
        if isinstance(stocks,str):
            stocks=[stocks]
        for sid in stocks:
            day_bar=self.read_one_day_m(sid,start,end,fields=fields)
            stocks_bar[sid]=day_bar
        return stocks_bar

    
    def get_stocks_in_m(self): 
        '''从monggodb获取所有已经存在的股票'''
        agg=[{'$group':{'_id':'$sid','sid':{'$first':'$sid'}}}]
        sids=list(self.col.aggregate(agg))
        sids=[i['sid'] for i in sids]
        return sids
    
    def update(self):
        '''更新monggodb中所有的股票日线数据到今天'''
        stocks=self.get_stocks_in_m()
        end=self.now()
        last_day=self.get_last_day_for_sid()
        for sid in stocks:
            start=self.another_day(last_day[sid],1)
            if start<end:
                self.save_one_to_mong_day(sid,start,end)
                                                
    def get_last_day_for_sid(self):
        '''获取所有股票的最近一个日期'''
        agg=[{'$group':{'_id':'$sid','date':{'$max':'$date'}}}]
        aggs=self.col.aggregate(agg)
        aggs=pd.DataFrame().from_dict(list(aggs))
        aggs.set_index('_id',drop=True, append=False, inplace=True)
        return aggs

    def another_day(self,current,nextd=1):
        '''2013-01-01'''
        current=[int(i) for i in current.split('-')]
        n=datetime.datetime(*current)+datetime.timedelta(nextd)
        return '{:4}-{:0>2}-{:0>2}'.format(n.year,n.month,n.day)
            
    def now(self):
        '''获取程序运行是的时间，2012-01-01'''
        n=datetime.datetime.now()
        return '{:4}-{:0>2}-{:0>2}'.format(n.year,n.month,n.day)
    def dropDups(self):
        '''删除重复的数据，可能会很慢'''
        projection={'_id':1,'date':1,'sid':1}
        aggs=self.col.find({},projection)
        aggs=pd.DataFrame().from_dict(list(aggs))  
        #按照股票分组，然后按照日期分组，最后找到，分组内个数大于1的股票和日期
        aggs_count=aggs.groupby(by='sid').apply(lambda x:x.groupby(by='date').apply(lambda x:x.count()))
        id_gt2=aggs_count[aggs_count.sid>1].sid
        for _del_ in id_gt2.index:
            '''('300001', '2016-11-02')'''
            for times in range(id_gt2[_del_]-1):
                #如果有两个，只需要删除一次。
                query={'date':'{}'.format(_del_[1]),'sid':'{}'.format(_del_[0])}
                self.col.delete_one(query)
        
    def autotype(self):
        '''打算用来处理复权，但是好像费内存的样子'''        
        pass
    
def day_bar_to_mongo(st,ed):
    '''保存日线数据到mongo'''
    c=config()
    mongo=MongoBase(c.database,c.collection)  
    #save  
    day=tushare_mongo(mongo.col)
    day.save_many_to_mongo_day(st,ed)    
    mongo.closeDB()      
    
def get_price(sids,start,end,fields):
    c=config()
    mongo=MongoBase(c.database,c.collection)  
    #read   
    day=tushare_mongo(mongo.col)
    #sids=day.get_stocks_in_m()
    price=day.read_from_mongo_day(sids,st,ed,fields)  
    mongo.closeDB() 
    return price 
 
        
st='2014-01-02'
ed='2018-03-28'
fields=None
#fields=['sid','open','close']
day_bar_to_mongo(st,ed)
#c=get_price('000605',st,ed,fields)

logger.removeHandler(file_handler)        
            
            

            
            
            