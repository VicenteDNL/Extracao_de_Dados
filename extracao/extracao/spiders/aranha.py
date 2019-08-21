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
            yield response.follow(link+"?mode=full", self.infoArtigo)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)     

    def infoArtigo(self, response):
        itens = ExtracaoItem()
        tags  = response.css('tr td[headers="s1"]::text').extract()
        conteudo =  response.css('tr td[headers="s2"]::text').extract()

        autores =[]
        palavrachave=[]
        addTitulo = False
        addResumo =False
        for i in range (len(tags)):
            if tags[i]=='dc.title':
                if addTitulo==False:
                    itens['titulo']= conteudo[i]
                    addTitulo=True
            elif tags[i]=='dc.description.abstract':
                if addResumo==False:
                    itens['resumo']= conteudo[i]
                    addResumo=True
            elif tags[i]=='dc.contributor.author':
                autores.append(conteudo[i])
            elif tags[i]=='dc.date.issued':
                itens['data']= conteudo[i]
            elif tags[i]=='dc.identifier.uri':
                itens['url']= conteudo[i]
            elif tags[i]=='dc.type':
                itens['tipo']= conteudo[i]
            elif tags[i]=='dc.subject.keyword':
                palavrachave.append(conteudo[i])
        itens['autores']= autores
        itens['palavrachave']= palavrachave

        
        yield itens

