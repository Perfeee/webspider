#!/usr/bin/env python
# coding=utf-8

import scrapy
from bilingual_article.items import BilingualArticleItem
from bs4 import BeautifulSoup
import re

class BilingualSpider(scrapy.Spider):
    name = 'chinadaily'
    allowed_domains = ["language.chinadaily.com.cn"]
    start_urls = ["http://language.chinadaily.com.cn/news_bilingual.html"]
    def parse(self,response):
        soup = BeautifulSoup(response.body)
        tag = soup.find("div","all-left")
        articles_link = tag.find_all("h3")
        for link in articles_link:
            url = response.urljoin(link.a['href'])
            yield scrapy.Request(url,callback=self.article_parse)
        next_link = tag.find("a",text="下一页")['href']
        next_link_url = response.urljoin(next_link)
        yield scrapy.Request(next_link_url,callback=self.parse)
    
    def article_parse(self,response):
        item = BilingualArticleItem()
        article = BeautifulSoup(response.body)
        item["chinese_title"] = article.h1.get_text()
        item["english_title"] = article.h1.find_next_sibling().get_text()
        item["time"] = article.find("span",text=re.compile(r'\d{4}(-\d\d){2} \d{2}:\d{2}')).get_text()
        tag = article.find("div",id="Content")
        text = []
        for link in tag.find_all("p"):
            phase = link.get_text()
            if "." in phase:
                text.append(phase)
        item["article"] = text
        yield item
        if article.find(text="下一页"):
            link = article.find("a",text="下一页")['href']
            next_url = response.urljoin(link)
            yield scrapy.Request(next_url,callback=self.article_parse)
#        else:
#            item["article"] = text
#            yield item
#        item["article"] = text
#        yield item
#当前仍然没有将同一篇文章里面的多页迭代弄好，这样会导致同一个文件多次写，同一篇文章多次yield item，也就是在同一个文件里会出现多个字典，但每个字典的title和time都是一样的，字典个数取决与文章的页数。

#一种可行的解决的办法应该是在pipeline中对item进行判断，并进行不同的操作。

#    def page_parse(self,response):
#        text = []
#        article = BeautifulSoup(response.body)
#        tag = article.find("div",id="Content")
#        for link in tag.find_all("p"):
#            phase = link.get_text()
#            if "." in phase:
#                text.extend(phase)
#        if article.find(text="下一页").get_text() == "下一页":
#            parse
#        return text
