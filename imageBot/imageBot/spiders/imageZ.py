# -*- coding: utf-8 -*-
import scrapy

from scrapy.selector import Selector

from imageBot.items import ImagebotItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class ImagezSpider(CrawlSpider):
    name = "imageZ"
    allowed_domains = ["uuhw.cn"]
    start_urls = ['http://www.uuhw.cn/api.php?mod=ad&adid=custom_3&jdfwkey=frrvo3']
    rules = (
        Rule(LinkExtractor(allow=('forum\.php', )), callback='forum_parse'),
    )
    def forum_parse(self,response):
        sel = Selector(response)
	item = ImagebotItem()
	item['image_urls'] = []
	for i in sel.xpath('//img/@src').extract():
	    if i.startswith("http"):
		item['image_urls'].append(i)
	    else:
		item['image_urls'].append("http://www.uuhw.cn/" + i)
	return item
