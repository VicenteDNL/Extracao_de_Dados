# -*- coding: utf-8 -*-
import scrapy
from ..items import ExtracaoItem

class SpiderUfrgsSpider(scrapy.Spider):
    name = 'Spider_UFRGS'
    start_urls = ['https://lume.ufrgs.br/handle/10183/1/discover?query=saude+mental']

    


    def parse(self, response):
        linkDocs = response.css('div[class="col-sm-9 artifact-description"] a::attr(href)').extract()
        
        next_page = response.xpath('.pagination  li:last-child > a::attr(href)').get()

        for link in linkDocs:
            yield response.follow(link, self.infoArtigo)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)     

    def infoArtigo(self, response):
        itens = ExtracaoItem()
        titulo = response.css('  div.item-summary-view-metadata h2 ::text').extract()
        resumo = response.xpath('//*[@id="abstract-to-hide-pt_BR" or @id="abstract-to-hide-pt"]/text()').extract()
        data =  response.css(' div.simple-item-view-date.word-break.item-page-field-wrapper.table::text').extract()

        itens['titulo']= titulo
        itens['resumo']= resumo
        itens['data']= data
        
        yield itens