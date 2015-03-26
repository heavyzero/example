# -*- coding: utf-8 -*-

# Scrapy settings for uutravel project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'uutravel'

SPIDER_MODULES = ['uutravel.spiders']
NEWSPIDER_MODULE = 'uutravel.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.UutravelItem'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'uutravel (+http://www.yourdomain.com)'
ITEM_PIPELINES = {'uutravel.pipelines.UutravelPipeline': 1}
