import scrapy

from war3map.items import War3MapItem

import urllib


class MapSpider(scrapy.Spider):
    name = 'map'
    allowed_domains = ['www.feifeishijie.com', 'www.lanzoui.com']
    start_urls = ['http://www.feifeishijie.com/juese/']

    def parse(self, response):
        li_list = response.xpath("/html/body/div[@class='wrap']/div[@class='layA']/div[@class='artList']/ul/li")
        for li in li_list:
            name = li.xpath("div[@class='dBody']/span[@class='intro']/node()[1]").extract_first()[5:]
            href = li.xpath("div[@class='dTitle']/b/a/@href").extract_first()
            yield scrapy.Request(url=href, callback=self.parse2, meta={
                'name': name
            })

    def parse2(self, response):
        href = response.xpath(
            "/html/body/div[@class='wrap']/div[@class='layA']/div[@class='modA dSoft']/div[@class='tbA'][2]/div[@class='dL']/div[@class='tbBtn']/a[@class='downUrl']/@href").extract_first()
        return scrapy.Request(url=href, callback=self.parse3, meta={
            'name': response.meta['name']
        })
        # return War3MapItem(name=response.meta['name'], file_url='')

    def parse3(self, response):
        href = response.xpath("/html/body/a/@href").extract_first()
        return scrapy.Request(url=href, callback=self.parse4, meta={
            'name': response.meta['name']
        })

    def parse4(self, response):
        href = response.xpath(
            "/html/body/div[@class='d']/div[@class='d2']/div[@class='ifr']/iframe[@class='ifr2']/@src").extract_first()
        url = "https://www.lanzoui.com" + href
        return scrapy.Request(url=url, callback=self.parse5, meta={
            'name': response.meta['name']
        })

    def parse5(self, response):
        url = response.xpath("/html/body/div[@id='go']/a/@href").extract_first()
        return War3MapItem(name=response.meta['name'], file_url=url)
