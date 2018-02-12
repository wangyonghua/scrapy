# -*- coding: utf-8 -*-
import scrapy
import json
from test01.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyucdn.cn']
    offset = 0
    start_urls = [
        'http://capi.douyucdn.cn/api/v1/getVerticalRoom?aid=ios&client_sys=ios&limit=20&offset=' + str(offset)]

    def parse(self, response):
        data = json.loads(response.text)['data']
        if not data:
            return

        for it in data:
            item = DouyuItem()
            item["image_urls"] = it['vertical_src']
            item['name'] = it['nickname']
            yield item

        self.offset += 20
        yield scrapy.Request(
                'http://capi.douyucdn.cn/api/v1/getVerticalRoom?aid=ios&client_sys=ios&limit=20&offset=%s' % str(
                        self.offset), callback=self.parse)
