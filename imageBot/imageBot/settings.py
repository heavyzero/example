# -*- coding: utf-8 -*-

# Scrapy settings for imageBot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'imageBot'

SPIDER_MODULES = ['imageBot.spiders']
NEWSPIDER_MODULE = 'imageBot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'imageBot (+http://www.yourdomain.com)'
ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
IMAGES_STORE = 'images/'
