# _*_ coding=utf-8 _*_
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import FormRequest
# 请求登录
import scrapy

from douban.items import DoubanItem


class DouBanSpider(Spider):
    """
    每个其他爬虫必须继承 scrapy.spiders.Spider 它不提供任何特殊功能。
    它只是提供了一个默认start_requests()实现，
    它从start_urlsspider属性发送请求，并parse 为每个结果响应调用spider的方法。
    """

    name = 'db'   # 标识爬虫,在项目中需要唯一
    start_urls = ['https://movie.douban.com/top250']
    # 可直接使用start_requests()，此时start_urls无效
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    # parse() 是spider的一个方法。
    # 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。
    # 该方法负责解析返回的数据(response data)，
    # 提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象
    def parse(self, response):
        # seletor的方法返回后一定要用它的 extract()方法，来返回一个列表 ；
        # extract()文档的定义：串行化并将匹配到的节点返回一个unicode字符串列表。
        selector = Selector(response)
        movies = selector.xpath('//div[@class="info"]')

        for movie in movies:

            # 项目加载器，Items提供了抓取数据的容器，
            # 而Item Loader提供了填充该容器的机制。提供了许多有趣的方式整合数据、格式化数据、清理数据
            # ItemLoaders和处理函数是专为有抓取需求的爬虫编写者、维护者开发的工具集。
            # http://doc.scrapy.org/en/latest/topics/loaders
            # l = ItemLoader(item=DoubanItem(), response=movie)
            # l.add_xpath('movie_name', 'div[@class="hd"]/a/span/text()')
            # l.add_xpath('movie_star', 'div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')
            # l.add_xpath('movie_quote', 'div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()')
            # ItemLoader.load_item()方法被称为实际上返回填充先前提取并与收集到的数据的项目add_xpath()， add_css()和add_value()调用。
            # return l.load_item()

            movie_name = movie.xpath('div[@class="hd"]/a/span/text()').extract()
            movie_star = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            movie_quote = movie.xpath('div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()').extract()

            item = DoubanItem()
            item['movie_name'] = movie_name
            item['movie_star'] = movie_star
            item['movie_quote'] = movie_quote

            yield item
            print movie_name
            print movie_star
            print movie_quote
        #
        next_page = selector.xpath('//span[@class="next"]/link/@href').extract()
        if next_page:
            next_page = next_page[0]
            # print next_page
            yield scrapy.Request("https://movie.douban.com/top250" + next_page, callback=self.parse)
