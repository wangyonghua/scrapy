import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

from scrapy.exceptions import DropItem

import os


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MyImagesPipeline(ImagesPipeline):
    IMAGE_STORE = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        image_url = item['image_urls']
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no iamges")

        os.rename((self.IMAGE_STORE + "/" + image_paths[0]), self.IMAGE_STORE + "/" + item['name'] + ".jpg")
        item['image_paths'] = self.IMAGE_STORE + "/" + item['name']
        return item
