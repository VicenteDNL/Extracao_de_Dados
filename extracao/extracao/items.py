# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExtracaoItem(scrapy.Item):
    # define the fields for your item here like:
    titulo = scrapy.Field()
    resumo = scrapy.Field()
    data = scrapy.Field()
    autores = scrapy.Field()
    url = scrapy.Field()
    palavrachave = scrapy.Field()
    tipo  = scrapy.Field()
    pass   
