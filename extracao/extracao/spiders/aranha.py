# -*- coding: utf-8 -*-
import scrapy
from ..items import ExtracaoItem


class AranhaSpider(scrapy.Spider):
    name = 'aranha'
    start_urls = ['http://repositorio.unb.br/simple-search?query=saude+mental']

    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'extracao.pipelines.ExtracaoPipeline': 400
    #     },
    #     'LOG_FILE': 'extracao.log',
    #     'FEED_FORMAT': 'csv',
    #     'JOBDIR': 'crawls\\extracao',
    #     'FEED_URI': 'extracao_resultados.csv'
    # }


    def parse(self, response):
        linkDocs = response.css('td[headers="t3"] a::attr(href)').extract()
        next_page = response.css('.pagination  li:last-child > a::attr(href)').get()
        for link in linkDocs:
            yield response.follow(link, self.infoArtigo)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)     

    def infoArtigo(self, response):
        itens = ExtracaoItem()
        titulo = response.css('td[class="metadataFieldValue dc_title"]::text').extract()
        resumo = response.css('td[class="metadataFieldValue dc_description_abstract"]::text').extract()
        data =  response.css('td[class="metadataFieldValue dc_date_issued"]::text').extract()

        itens['titulo']= titulo
        itens['resumo']= resumo
        itens['data']= data
        
        yield itens

