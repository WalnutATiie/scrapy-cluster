# -*- coding: utf-8 -*-

# Define here the models for your scraped items

from scrapy import Item, Field

class RawResponseItem(Item):
    appid = Field()
    crawlid = Field()
    url = Field()
    response_url = Field()
    status_code = Field()
    status_msg = Field()
    headers = Field()
    #body = Field()
    links = Field()
    attrs = Field()
    content = Field()
    domain_name = Field()
    create_time = Field()
    title = Field()
    proxy = Field()
