# -*- coding: utf-8 -*-
import scrapy
from ..items import ExtracaoItem


class SpiderUfscSpider(scrapy.Spider):
    name = 'Spider_UFSC'
    start_urls = ['https://repositorio.ufsc.br/handle/123456789/74645/discover?query=saude+mental']


    def parse(self, response):
        linkDocs = response.css('div[class="artifact-title"] a::attr(href)').extract()
        next_page = response.css('a[class="next-page-link"]::attr(href)').get()
        
        for link in linkDocs:
            link +='?show=full'
            yield response.follow(link, self.infoArtigo)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)     

    def infoArtigo(self, response):
        itens = ExtracaoItem()
        tags  = response.xpath('//*[@id="aspect_artifactbrowser_ItemViewer_div_item-view"]/table[1]/tr/td[1]/text()').extract()
        conteudo  = response.xpath('//*[@id="aspect_artifactbrowser_ItemViewer_div_item-view"]/table[1]/tr/td[2]/text()').extract()
        try:
            itens['titulo'] = conteudo[tags.index('dc.title')]
        except Exception:
            itens['titulo'] =[]
        try:
            itens['resumo'] = conteudo[tags.index('dc.description.abstract')]
        except Exception:
            itens['resumo'] =[]
        try:
            itens['data'] = conteudo[tags.index('dc.date.issued')]
        except Exception:
            itens['data'] =[]

        yield itens
