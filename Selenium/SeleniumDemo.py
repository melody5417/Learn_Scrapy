# coding=utf-8
# https://cuiqingcai.com/2599.html

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

# 打开网页
# driver.get("http://www.python.org")

# 模拟提交
# <input id="id-search-field" name="q" type="search" role="textbox" class="search-field" placeholder="Search" value="" tabindex="1">
driver.get("http://www.python.org")
assert "Python" in driver.title

# 查找元素
# elem = driver.find_element_by_id("id-search-field")
# elem = driver.find_element_by_name("q")
# elem = driver.find_element_by_class_name('search-field')
# elem = driver.find_element_by_tag_name("input")
elem = driver.find_element_by_xpath('//input[@class="search-field"]')

# 输入内容
elem.send_keys("pycon")
elem.clear()
elem.send_keys('py')
elem.send_keys(Keys.RETURN)


print(driver.page_source)

# 页面交互
