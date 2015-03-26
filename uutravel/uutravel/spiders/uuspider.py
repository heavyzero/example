# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
from  scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from uutravel.items import UutravelItem
class UuspiderSpider(CrawlSpider):
    name = "uuspider"
    allowed_domains = ["uuhw.cn"]
    start_urls = (
	'http://www.uuhw.cn/forum.php?mod=forumdisplay&fid=2',#&jdfwkey=cdzww3',
    )

    rules = (
	Rule(LinkExtractor(allow=('forum\.php\?mod=forumdisplay\&fid=2\&page=\d+', ))),
#	Rule(LinkExtractor(allow=('forum\.php\?mod=viewthread', )), callback='parse_item'),
	Rule(LinkExtractor(restrict_xpaths='//tr/th[@class="common"]/a[starts-with(@href,"http")]'), callback='parse_item'),
    )
    def parse_item(self, response):
	item = UutravelItem()
	item['tid'] = int(response.url[response.url.rindex('=')+1:])
	item['url'] = response.url
	xpaths = ['//div[@id="postlist"]/div[2]//div[@align="left"]/text()','//div[@id="postlist"]/div[2]//strong/text()']
	item['signup'] = []
	for i in xpaths:
	    signup= [] 
	    results= response.xpath(i).extract()
	    for i in results:
		if i != '\n' and i != '\r\n':
		    i = i.rstrip()
		    try:
			i = i[i.rindex(' ') + 1:] 
		    except ValueError:
			pass
		    signup.append(i)
	    if len(signup) > 0:
		item['signup'] = signup
		return item
	return item
