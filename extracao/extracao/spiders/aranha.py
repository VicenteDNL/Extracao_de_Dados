# -*- coding: utf-8 -*-
import scrapy
from ..items import ExtracaoItem


class AranhaSpider(scrapy.Spider):
    name = 'aranha'
    start_urls = ['http://repositorio.unb.br/simple-search?location=&query=saude+mental&rpp=1788&sort_by=score&order=DESC&etal=0&submit_search=Atualizar']

    custom_settings = {
        'ITEM_PIPELINES': {
            'extracao.pipelines.ExtracaoPipeline': 400
        },
        'LOG_FILE': 'extracao.log',
        'FEED_FORMAT': 'csv',
        'JOBDIR': 'crawls\\extracao',
        'FEED_URI': 'extracao_resultados.csv'
    }


    def parse(self, response):
        linkDocs = response.css('td[headers="t3"] a::attr(href)').extract()
        for link in linkDocs:
            yield response.follow(link, self.infoArtigo)

        
    def infoArtigo(self, response):
        itens = ExtracaoItem()

        titulo = response.css('td[class="metadataFieldValue dc_title"]::text').extract()
        resumo = response.css('td[class="metadataFieldValue dc_description_abstract"]::text').extract()
        data =  response.css('td[class="metadataFieldValue dc_date_issued"]::text').extract()

        itens['titulo']= titulo
        itens['resumo']= resumo
        itens['data']= data
        
        yield itens

#div.artifact-title a
