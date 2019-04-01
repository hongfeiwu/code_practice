![Image text](scrapy_architecture.png)

- Scrapy Engine
 引擎负责控制数据流在系统中所有组件中流动，并在相应动作发生时触发事件。 详细内容查看下面的数据流(Data Flow)部分
- 调度器(Scheduler)
  --调度器从引擎接受request并将他们入队，以便之后引擎请求他们时提供给引擎
- 下载器(Downloader)
  --下载器负责获取页面数据并提供给引擎，而后提供给spider
- Spiders
  --Spider是Scrapy用户编写用于分析response并提取item(即获取到的item)或额外跟进的URL的类。 每 个spider负责处理一个特定(或一些)网站
- Item Pipeline
--Item Pipeline负责处理被spider提取出来的item。典型的处理有清理、 验证及持久化(例如存取到数 据库中)
- 下载器中间件(Downloader middlewares)
    下载器中间件是在引擎及下载器之间的特定钩子(specific hook)，处理Downloader传递给引擎的 response。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能
- Spider中间件(Spider middlewares)
    Spider中间件是在引擎及Spider之间的特定钩子(specific hook)，处理spider的输入(response)和输出 (items及requests)。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能
- 数据流(Data flow)
    Scrapy中的数据流由执行引擎控制，其过程如下:


### 程序运行流程
* 引擎打开一个网站(open a domain)，找到处理该网站的Spider并向该spider请求第一个要爬取的 URL(s)。
* 引擎从Spider中获取到第一个要爬取的URL并在调度器(Scheduler)以 Request调度。
* 引擎向调度器请求下一个要爬取的URL。
* 调度器返回下一个要爬取的URL给引擎，引擎将URL通过下载中间件(请求(request)方向)转发给下载 器(Downloader)。
* 一旦页面下载完毕，下载器生成一个该页面的Response，并将其通过下载中间件(返回(response)方 向)发送给引擎。
* 引擎从下载器中接收到Response并通过Spider中间件(输入方向)发送给Spider处理。
* Spider处理Response并返回爬取到的Item及(跟进的)新的Request给引擎。
* 引擎将(Spider返回的)爬取到的Item给Item Pipeline，将(Spider返回的)Request给调度器。
* (从第二步)重复直到调度器中没有更多地request，引擎关闭该网站


#### 创建爬虫目录
```angular2html
scrapy startproject myproject
```
### 创建爬虫项目
```angular2html
scrapy startproject myproject [ project_dir ]
```


#### 执行爬虫
```
scrapy crawl  项目名称
```

- 进入scrapy shell
```angular2html
scrapy shell 'http://quotes.toscrape.com/page/1/'
```
- css选择器以及XPath选择元素， extract()方法，来返回一个列表 
```angular2html
response.css('title::text').extract_first()
response.css('title::text').extract()
response.css('title::text').re(r'Quotes.*') # 正则
response.xpath('//title')
```


#### 存取数据
最简单方法是直接制定导出文件，Scrapy会附加到给定文件，而不是覆盖其内容。如果你运行这个命令两次，没有在第二次之前删除文件，你会得到一个破碎的JSON文件。
```
scrapy crawl quotes -o quotes.json
```



#### 使用爬虫参数
可以通过-a 在运行它们时使用该选项为您的爬虫提供命令行参数：
```
scrapy crawl quotes -o quotes-humor.json -a tag=humor
```






