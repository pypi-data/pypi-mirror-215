import os,sys
import random
import pandas as pd
import numpy as np
from pathlib import Path
import time
from multiprocessing import shared_memory
import gzip,io,shutil,hashlib,threading
from datetime import datetime
from numba import njit,prange


from SharedData.Logger import Logger
import SharedData.SharedDataTableKeysJit as SharedDataTableKeysJit
from SharedData.SharedDataTableKeysJit import *


class SharedDataTableKeys:

    def __init__(self,table):
        self.table = table
        self.sharedData = self.table.sharedData
        
        self.initialized = False

        # primary key hash table        
        self.pkeycolumns = SharedDataTableKeys.get_pkeycolumns(self.sharedData.database)
        self.pkey = np.ndarray([])
        # date index
        self.dateiniidx = np.ndarray([])
        self.dateendidx = np.ndarray([])
        # date,portfolio index
        self.portiniidx = np.ndarray([]) # hash table
        self.portlist = np.ndarray([]) # linked list
        self.portlistcount = 0

    def initialize(self):
        # primary key & index functions
        self.create_pkey_func = None
        self.upsert_func = None
        self.get_loc_func = None

        create_pkey_fname = 'create_pkey_'+str.lower(self.sharedData.database) + '_jit'
        if hasattr(SharedDataTableKeysJit,create_pkey_fname):
            self.create_pkey_func = getattr(SharedDataTableKeysJit,create_pkey_fname)
        else:
            raise Exception('create_pkey function not found for database %s!' \
                % (self.sharedData.database))

        upsert_fname = 'upsert_'+str.lower(self.sharedData.database) + '_jit'
        if hasattr(SharedDataTableKeysJit,upsert_fname):
            self.upsert_func = getattr(SharedDataTableKeysJit,upsert_fname)
        else:
            raise Exception('upsert function not found for database %s!' \
                % (self.sharedData.database))

        get_loc_fname = 'get_loc_'+str.lower(self.sharedData.database) + '_jit'
        if hasattr(SharedDataTableKeysJit,get_loc_fname):
            self.get_loc_func = getattr(SharedDataTableKeysJit,get_loc_fname)
        else:
            raise Exception('get_loc function not found for database %s!' \
                % (self.sharedData.database))
        
        if (self.sharedData.database == 'Risk') | (self.sharedData.database == 'Positions'):
            self.get_date_portfolio_loc_func = getattr(SharedDataTableKeysJit,'get_date_portfolio_loc_jit')
        
        self.malloc()        

        self.initialized = True
    
    def malloc(self):
        path, shm_name = self.table.get_path(iswrite=True)
        keysize = int(self.table.records.size*5)
        keysize_bytes = int(keysize * 4)
        #date index
        dtunit = str(self.table.records.dtype[0]).split('[')[-1].split(']')[0]
        if dtunit=='D':
            self.dateunit = 1
        elif dtunit=='h':
            self.dateunit = 24
        elif dtunit=='m':
            self.dateunit = 24*60
        elif dtunit=='s':
            self.dateunit = 24*60*60
        elif dtunit=='ms':
            self.dateunit = 24*60*60*1000
        elif dtunit=='us':
            self.dateunit = 24*60*60*1000*1000
        elif dtunit=='ns':
            self.dateunit = 24*60*60*1000*1000*1000
        maxdate = np.datetime64('2050-01-01','D')
        dateidxsize = maxdate.astype(int)
        dateidxsize_bytes = int(dateidxsize * 4)
        #portiniidx        
        portlistsize = int(self.table.records.size*2)
        try:
            # test if shared memory already exists            
            self.create_map = 'map'
            self.pkeyshm = shared_memory.SharedMemory(name = shm_name+'#pkey',create=False)
            self.pkey = np.ndarray((keysize,),dtype=np.int32,buffer=self.pkeyshm.buf)      
            self.dateiniidxshm = shared_memory.SharedMemory(name = shm_name+'#dateiniidx',create=False)
            self.dateiniidx = np.ndarray((dateidxsize,),dtype=np.int32,buffer=self.dateiniidxshm.buf)
            self.dateendidxshm = shared_memory.SharedMemory(name = shm_name+'#dateendidx',create=False)
            self.dateendidx = np.ndarray((dateidxsize,),dtype=np.int32,buffer=self.dateendidxshm.buf)            
            if (self.sharedData.database == 'Risk') | (self.sharedData.database == 'Positions'):
                self.portiniidxshm = shared_memory.SharedMemory(name = shm_name+'#portiniidx',create=False)
                self.portiniidx = np.ndarray((keysize,),dtype=np.int32,buffer=self.portiniidxshm.buf)
                self.portendidxshm = shared_memory.SharedMemory(name = shm_name+'#portendidx',create=False)
                self.portendidx = np.ndarray((keysize,),dtype=np.int32,buffer=self.portendidxshm.buf)
                self.portlistshm = shared_memory.SharedMemory(name = shm_name+'#portlist',create=False)
                self.portlist = np.ndarray((portlistsize,),dtype=np.int32,buffer=self.portlistshm.buf)
                self.portlistcountshm = shared_memory.SharedMemory(name = shm_name+'#portlistcount',create=False)
                self.portlistcount = np.ndarray((1,),dtype=np.int32,buffer=self.portlistcountshm.buf)[0]                
        except:
            self.create_map = 'create'            
            self.pkeyshm = shared_memory.SharedMemory(name = shm_name+'#pkey',create=True,size=keysize_bytes)
            self.pkey = np.ndarray((keysize,),dtype=np.int32,buffer=self.pkeyshm.buf)
            self.pkey[:] = -1            
            self.dateiniidxshm = shared_memory.SharedMemory(name = shm_name+'#dateiniidx',create=True,size=dateidxsize_bytes)
            self.dateiniidx = np.ndarray((dateidxsize,),dtype=np.int32,buffer=self.dateiniidxshm.buf)
            self.dateiniidx[:]=-1
            self.dateendidxshm = shared_memory.SharedMemory(name = shm_name+'#dateendidx',create=True,size=dateidxsize_bytes)
            self.dateendidx = np.ndarray((dateidxsize,),dtype=np.int32,buffer=self.dateendidxshm.buf)
            self.dateendidx[:]=-1
            if (self.sharedData.database == 'Risk') | (self.sharedData.database == 'Positions'):
                self.portiniidxshm = shared_memory.SharedMemory(name = shm_name+'#portiniidx',create=True,size=keysize_bytes)
                self.portiniidx = np.ndarray((keysize,),dtype=np.int32,buffer=self.portiniidxshm.buf)
                self.portiniidx[:]=-1
                self.portendidxshm = shared_memory.SharedMemory(name = shm_name+'#portendidx',create=True,size=keysize_bytes)
                self.portendidx = np.ndarray((keysize,),dtype=np.int32,buffer=self.portendidxshm.buf)
                self.portendidx[:]=-1
                self.portlistshm = shared_memory.SharedMemory(name = shm_name+'#portlist',create=True,size=int(portlistsize*4))
                self.portlist = np.ndarray((portlistsize,),dtype=np.int32,buffer=self.portlistshm.buf)
                self.portlist[:]=-1
                self.portlistcountshm = shared_memory.SharedMemory(name = shm_name+'#portlistcount',create=True,size=int(4))
                self.portlistcount = np.ndarray((1,),dtype=np.int32,buffer=self.portlistcountshm.buf)[0]
                self.portlistcount=0
            self.create_pkey()
            
    def create_pkey(self):
        ti = time.time()
        if self.table.records.count>0:
            print('Creating pkey %s/%s/%s %i lines...' % \
                (self.sharedData.database,self.table.feeder,\
                self.table.dataset,self.table.records.count))
            arr = self.table.records
            if (self.sharedData.database == 'Risk') | (self.sharedData.database == 'Positions'):
                self.create_pkey_func(arr,self.table.records.count,\
                    self.pkey,self.dateiniidx,self.dateendidx,self.dateunit,\
                    self.portiniidx,self.portendidx,self.portlist,self.portlistcount,0)
                self.portlistcount=self.table.records.count
            else:
                self.create_pkey_func(arr,self.table.records.count,self.pkey,\
                    self.dateiniidx,self.dateendidx,self.dateunit,0)
            print('Creating pkey %s/%s/%s %i lines/s DONE!' % \
                (self.sharedData.database,self.table.feeder,\
                self.table.dataset,self.table.records.count/(time.time()-ti)))

    def update_pkey(self,start):
        arr = self.table.records[0:self.table.records.size]
        self.create_pkey_func(arr,self.table.records.count,self.pkey,start)
        
    @staticmethod
    def get_pkeycolumns(database):
        if database == 'MarketData':
            return ['date','symbol']
                
        elif database == 'Portfolios':
            return ['date','portfolio']

        elif database == 'Risk':
            return ['date','portfolio','riskfactor']
                
        elif database == 'Relationships':
            return ['date','riskfactor1','riskfactor2']
        
        elif database == 'Positions':
            return ['date','portfolio','symbol']
        
        elif database == 'Orders':
            return ['date','portfolio','symbol','clordid']
                
        elif database == 'Trades':
            return ['date','portfolio','symbol','tradeid']
                
        else:
            raise Exception('Database not implemented!')
        