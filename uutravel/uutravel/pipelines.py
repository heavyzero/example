# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import db
class UutravelPipeline(object):
    def process_item(self, item, spider):
	for i in item['signup']:
	    db.save_travel_signup(i,item['tid'])
        return item
