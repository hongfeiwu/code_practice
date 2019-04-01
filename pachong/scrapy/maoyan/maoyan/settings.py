# -*- coding: utf-8 -*-

BOT_NAME = 'maoyan'
SPIDER_MODULES = ['maoyan.spiders']
NEWSPIDER_MODULE = 'maoyan.spiders'
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
DOWNLOAD_DELAY = 3
LOG_LEVEL = 'DEBUG'
RANDOMIZE_DOWNLOAD_DELAY = True
# 关闭重定向
REDIRECT_ENABLED = False
# 返回302时,按正常返回对待,可以正常写入cookie
HTTPERROR_ALLOWED_CODES = [302]
ITEM_PIPELINES = {
    'maoyan.pipelines.MongoDBPipeline': 300,
}
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'maoyan'
MONGODB_COLLECTION = 'movies'
