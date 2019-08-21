# -*- coding: utf-8 -*-
import scrapy
from ..items import ExtracaoItem

class SpiderUfrgsSpider(scrapy.Spider):
    name = 'Spider_UFRGS'
    start_urls = ['https://lume.ufrgs.br/handle/10183/1/discover?query=saude+mental']

    


    def parse(self, response):
        linkDocs = response.css('div[class="col-sm-9 artifact-description"] a::attr(href)').extract()
        
        next_page = response.css('.pagination  li:last-child > a::attr(href)').get()

        for link in linkDocs:
            yield response.follow(link+"?show=full", self.infoArtigo)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)     

    def infoArtigo(self, response):
        itens = ExtracaoItem()
        tags  = response.css('td[class="label-cell"]::text').extract()
        conteudo =  response.css('td[style="text-align: justify;"]::text').extract()


        autores =[]
        palavrachave=[]
    
        addResumo =False
        for i in range (len(tags)):
            if tags[i]=='dc.title':
                itens['titulo']= conteudo[i]
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
            elif tags[i]=='dc.subject':
                palavrachave.append(conteudo[i])
        itens['autores']= autores
        itens['palavrachave']= palavrachave
        yield itens
