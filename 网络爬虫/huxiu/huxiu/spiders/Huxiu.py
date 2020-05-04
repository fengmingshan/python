# -*- coding: utf-8 -*-
import scrapy


class HuxiuSpider(scrapy.Spider):
    name = 'Huxiu'
    allowed_domains = ['huxiu.com']
    start_urls = ['http://huxiu.com/']

    def parse(self, response):
        for s in response.xpath('//div[@class="clearfix article-box"]/div[@class="article-item"]'):
            item = HuxiuItem()
            item['title'] = s.xpath('/div/a/div[@class="article-item__content"]/h5/text()')[0].extract()
            item['link'] = s.xpath('/div/a/@href')[0].extract()
            url = response.urljoin(item['link'])
            print(item)