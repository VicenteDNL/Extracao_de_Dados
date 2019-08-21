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
            yield response.follow(link+'?show=full', self.infoArtigo)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)     

    def infoArtigo(self, response):
        itens = ExtracaoItem()
        tags  = response.xpath('//*[@id="aspect_artifactbrowser_ItemViewer_div_item-view"]/table[1]/tr/td[1]/text()').extract()
        conteudo  = response.xpath('//*[@id="aspect_artifactbrowser_ItemViewer_div_item-view"]/table[1]/tr/td[2]/text()').extract()
        if len(tags)==len(conteudo):
            
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
                elif tags[i]=='dc.subject.classification':
                    palavrachave.append(conteudo[i])
            itens['autores']= autores
            itens['palavrachave']= palavrachave

        else:
            itens['titulo']= 'vazio001'
            itens['resumo']= 'vazio001'
            itens['autores']= 'vazio001'
            itens['palavrachave']= 'vazio001'
            itens['data']= 'vazio001'
            itens['url']= 'vazio001'
            itens['tipo']= 'vazio001'


        yield itens
