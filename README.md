## weixin_crawler 已经私有化,源码一直处于维护中

获取最新源码请加入知识星球, 入口二维码在最底部
感谢[这些](readme_img/thanks.md)小伙伴对weixin_crawler的实际支持
开源社群因为你们必将更加精彩

## What is weixin_crawler?

weixin_crawler是一款使用Scrapy、Flask、Echarts、Elasticsearch等实现的微信公众号文章爬虫，自带分析报告([报告样例](readme_img/report_example.png))和全文检索功能，几百万的文档都能瞬间搜索。weixin_crawler设计的初衷是尽可能多、尽可能快地爬取微信公众的历史发文

weixin_crawler尚处于维护之中, 方案有效, 请放心尝试. weixin_crawler is under maintaining, the code works greatly free to explore please

如果你想先看看这个项目是否有趣，这段不足3分钟的介绍视频一定是你需要的
If you want to check if weixin_crawler is interesting or powerful enougth, this video will help to save time
https://www.youtube.com/watch?v=CbfLRCV7oeU&t=8s

## 写在最开始

如果你的时间有限，不是以技术研究为主要目的，只是需要采集公众号的数据，从而可以专注自己做更擅长、更能创造价值的事情。不妨试试商用软件WCplus3.0，由weixin_crawler作者设计并实现，同时支持Mac和Window系统 https://shimo.im/docs/dA7ejdOQuPwo7NZV/ 

## 主要特点

1. 使用Python3编写

   Python3 is used

2. 爬虫框架为Scrapy并且实际用到了Scrapy的诸多特性，是深入学习Scrapy的不错开源项目

   Made full use of scrapy, if you are struggling with scrapy this repo helps to spark

3. 利用Flask、Flask-socketio、Vue实现了高可用性的UI界面。功能强大实用，是新媒体运营等岗位不错的数据助手

   Flask、Flask-socketio、Vue are used to build a full stack project crawler 

4. 得益于Scrapy、MongoDB、Elasticsearch的使用，数据爬取、存储、索引均简单高效

   Thanks to scrapy mongodb elasticsearch weixin_crawler is not only a crawler but also a search engine

5. 支持微信公众号的全部历史发文爬取

   Able to crawl all the history articles of any weixin official account

6. 支持微信公众号文章的阅读量、点赞量、赞赏量、评论量等数据的爬取

   Able to crawl the reading data

7. 自带面向单个公众号的数据分析报告

   Released with report module based on sigle official account

8. 利用Elasticsearch实现了全文检索，支持多种搜索和模式和排序模式，针对搜索结果提供了趋势分析图表

   It is also a search engine

9. 支持对公众号进行分组，可利用分组数据限定搜索范围

   Able to group official account which can be used to define searching range

10. 原创手机自动化操作方法，可实现爬虫无人监管

    Whith the help of adb, weixin_crawler is able to opereate Android phone automatically, which means it can work without any human monitoring

11. 支持多微信APP同时采集, 理论上采集速度可线性增加

    Mutiple weixin app is supported to imporove crawling speed linearly

## 使用到的主要工具

| 语言  |         | Python3.6                                     |
| --- | ------- | --------------------------------------------- |
| 前端  | web框架   | Flask / Flask-socketio / gevent               |
|     | js/css库 | Vue / Jquery / W3css / Echarts / Front-awsome |
| 后端  | 爬虫      | Scrapy                                        |
|     | 存储      | Mongodb / Redis                               |
|     | 索引      | Elasticsearch                                 |

## 运行方法

weixin_crawler已经在Win/Mac/Linux系统下运行成功, 建议优先使用win系统尝试
weixin_crawler could work on win/mac/linux, although it is suggested to try on win os firstly

> #### Insatall  mongodb / redis / elasticsearch and run them in the background
> 
> 1. downlaod mongodb / redis / elasticsearch from their official sites and install them
> 
> 2. run them at the same time under the default configuration. In this case mongodb is localhost:27017 redis is localhost:6379(or you have to config in weixin_crawler/project/configs/auth.py)
> 
> 3. Inorder to tokenize Chinese, *elasticsearch-analysis-ik* have to be installed for Elasticsearch
> 
> #### Install proxy server and run proxy.js
> 
> 1. install nodejs and then npm install anyproxy and redis in weixin_crawler/proxy
> 
> 2. cd to weixin_crawler/proxy and run node proxy.js
> 
> 3. install anyproxy https CA in both computer and phone side
> 
> 4. if you are not sure how to use anyproxy, [here ](https://github.com/alibaba/anyproxy)is the doc
> 
> #### Install the needed python packages
> 
> 1. NOTE: you may can not simply type pip install -r requirements.txt to install every package, twisted is one of them which is needed by scrapy. When you get some problems about installing python package(twisted for instance), [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/) always have a solution——downlod the right version package to your drive and run $ pip install package_name
> 
> 2. I am not sure if your python enviroment will throw other package not found error, just install any package that is needed
> 
> #### Some source code have to be modified(maybe it is not reasonable)
> 
> 1. scrapy Python36\Lib\site-packages\scrapy\http\request\ \__init\__.py  --> weixin_crawler\source_code\request\\__init\__.py
> 
> 2. scrapy Python36\Lib\site-packages\scrapy\http\response\ \__init\__.py --> weixin_crawler\source_code\response\\\__init\__.py
> 
> 3. pyecharts Python36\Lib\site-packages\pyecharts\base.py --> weixin_crawler\source_code\base.py. In this case function get_echarts_options is added in line 106
> 
> #### If you want weixin_crawler work automatically those steps are necessary or you shoud operate the phone to get the request data that will be detected by Anyproxy manual
> 
> 1. Install adb and add it to your path(windows for example)
> 
> 2. install android emulator(NOX suggested) or plugin your phone and make sure you can operate them with abd from command line tools
> 
> 3. If mutiple phone are connected to your computer you have to find out their adb ports which will be used to add crawler
> 
> 4. adb does not support Chinese input, this is a bad news for weixin official account searching. In order to input Chinese, adb keyboard has to be installed in your android phone and set it as the default input method, more is [here](https://github.com/senzhk/ADBKeyBoard)
> 
> Why could weixin_crawler work automatically? Here is the reason:
> 
> - If you want to crawl a wechat official account, you have to search the account in you phone and click its "全部消息" then you will get a message list , if you roll down more lists will be loaded.  Anyone of the messages in the list could be taped if you want to crawl this account's reading data
> - If a nickname of a wechat official account is given, then wexin_crawler operate the wechat app installed in a phone, at the same time anyproxy is 'listening background'...Anyway weixin_crawler get all the request data requested by wechat app, then it is the show time for scrapy
> - As you supposed, in order to let weixin_crawler operate wechat app we have to tell adb where to click swap and input,  most of them are defined in weixin_crawler/project/phone_operate/config.py. BTW phone_operate is responsible for wechat operate just like human beings, its eyes are baidu OCR API and predefined location tap area, its fingers are adb
> 
> #### Run the main.py
> 
> $ cd weixin_crawler/project/
> 
> $ python(3) ./main.py
> 
> Now open the browser and everything you want would be in localhost:5000.
> 
> In this long step list you may get stucked, join our community for help, tell us what you have done and what kind of error you have found.
> 
> Let's go to explore the world in localhost:5000 together

## 功能展示

UI主界面

![1](readme_img/爬虫主界面.gif)

添加公众号爬取任务和已经爬取的公众号列表

![1](readme_img/公众号.png)

爬虫界面

![](readme_img/caiji.png)

设置界面

![ ](readme_img/设置.png)

公众号历史文章列表

![ ](readme_img/历史文章列表.gif)

报告

![ ](readme_img/报告.gif)

搜索

![ ](readme_img/搜索.gif)


| 作者微信(备注请以wc开头) | 加入知识星球 |
| ----------------------- | ------------------------- |
| ![ ](readme_img/wq.jpg) | ![ ](readme_img/知识星球.png) |
