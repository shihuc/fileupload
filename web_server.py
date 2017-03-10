#!/usr/bin/env python
#-*- coding:utf-8 -*-
#__author__ "shihuc"

import tornado.ioloop
import tornado.web
import os
import json
import multiprocessing

import aibusiness

procPool = multiprocessing.Pool()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("uploadAI.html")

class UploadHandler(tornado.web.RequestHandler):

    def post(self,*args,**kwargs):
        file_metas=self.request.files['tkai_file']    			   #提取表单中‘name’为‘tkai_file’的文件元数据
        timestamp = self.get_argument("sequence")
        xsrf = self.get_argument("_xsrf")

        res = {} 
        #注意，只会有一个文件在每次http请求中
        for meta in file_metas:
            filename=meta['filename']
            procPool.apply_async(aibusiness.doWriteImageJob, (filename, meta['body'],))
            p = multiprocessing.Process(target=aibusiness.doRecJob, args=(timestamp, meta['body'],))
            p.start()
            p.join()
        retVal = aibusiness.reportResult(timestamp)
        print "timestamp: %s, xrsf: %s, res: %s, filename: %s\r\n" % (timestamp, xsrf, retVal, filename)
        res['result'] = retVal
        self.write(json.dumps(res))
        
        

settings = {
    'template_path': 'page',          # html文件
    'static_path': 'resource',        # 静态文件（css,js,img）
    'static_url_prefix': '/resource/',# 静态文件前缀
    'cookie_secret': 'shihuc',        # cookie自定义字符串加盐
    'xsrf_cookies': True              # 防止跨站伪造
}

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),(r"/upload", UploadHandler)
    ], default_host='',transforms=None, **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(9909)
    tornado.ioloop.IOLoop.current().start()
    procPool.close()
