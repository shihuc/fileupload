#!/usr/bin/env python
#-*- coding:utf-8 -*-
#__author__ "shihuc"

import os
import json
import random
import multiprocessing


#记录同一个业务请求对应的上传的图片数量，key是前端传来的timestamp，value是对应该
#timestamp值的图片处理结果，一个list。
timestamp_filecount_map = multiprocessing.Manager().dict()

procLock = multiprocessing.Lock()
procEvent = multiprocessing.Event()

upload_path=os.path.join(os.path.dirname(__file__),'uploadfiles')  #文件的暂存路径

def doWriteImageJob(filename, imgData):
       """ 1. Add your business logic here, write image data as file! 
       """
       #Below do result update
       filepath=os.path.join(upload_path,filename)
       with open(filepath,'wb') as up:                                #有些文件需要已二进制的形式存储，实际中可以更改
            up.write(imgData)      
 
def doRecJob(timestamp, imgData):
       """ 1. Add your business logic here, for example, image recognization! 
           2. After image rec process, you must update the timestamp_filecount_map
       to check the next final result in the next step.
       """
       #Here, do recognization, simulate the result by random
       procLock.acquire()
       result = random.randrange(0, 10, 1)
       #Below do result update
       res = []
       if timestamp_filecount_map.get(str(timestamp)) is None:
          res.append(result)
       else:
          res = timestamp_filecount_map.get(str(timestamp))
          res.append(result)
       timestamp_filecount_map[str(timestamp)] = res
       print timestamp_filecount_map
       procLock.release()      
       

def reportResult(timestamp):
       """ Add your business logic here, check whether the result is ok or not. 
       Here, I will simulate the logic that check the existing result whether it
       is accepted as OK, e.g. the present of image with same result is no less
       80%, which is defined to be OK.
       """ 
       #Here, simulation. check if all the result, if there is 80% image whose result 
       #is no less 2, then the final is OK.
       procLock.acquire()
       tempCnt = 0
       try:
           detail_info = timestamp_filecount_map.get(str(timestamp))
           if detail_info is None:
              return "OK"
           else:
              for elem in detail_info:
                 if elem >= 2:
                     tempCnt += 1
              if tempCnt >= len(detail_info) * 0.8:
                 del timestamp_filecount_map[str(timestamp)]             
                 return "OK"
              else:
                 return "NOK"
       finally:        
           procLock.release()   


