# fileupload
one demo which is based on tornado, to simulate the process flow about image recognization.

一个图片上传的例子，基于tornado 4.0测试通过。注意一下：</br>
1. 前端是基于bootstrap-fileinput插件，配置的方式是异步ajax上传。</br>
2. 模拟真实的APP场景下，一张一张的图片上传，若图片识别效果合适，就返回OK，否则返回NOK，只有OK的时候，跳出弹出框"Result is acceptable"。</br>
3. 我处理每次上传的图片，用生成随机数代替你们的图像识别过程。随机数取值范围0-9。</br>
4. 随机数大于2的个数不小于80%则认为识别结果OK。</br>
5. 图像上传写图片的过程是用的进程池，图像识别的过程是单独起进程。</br>
6. 前端通过时间戳来标记一个识别过程。只有识别OK了，相应的记录数据会从多进程共享dict数据结构中删除。</br>

项目启动，直接执行python web_server.py，在浏览器输入http://host:9909/ 即可测试。 后台会打印出一些基本的日志信息。</br>

