# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class BilingualArticlePipeline(object):
#    def __init__(self):
#        self.a = 1
    def process_item(self, item, spider):
        filename = item['time']
        f = open(filename,'ab')
        file_content = json.dumps(dict(item))
        f.write(file_content)
#        self.a += 1
        return item
