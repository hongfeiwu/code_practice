# -*- coding: utf-8 -*-
# 官方文档的例子很详细，建议先看文档了解一下
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('http://www.23us.com/')
assert "顶点" in driver.title
# 确定搜索输入框:
elem = driver.find_element_by_name('q')
# 模拟键盘输入书名:
elem.send_keys('七界传说')
# 模拟键盘点击回车:
elem.send_keys(Keys.RETURN)