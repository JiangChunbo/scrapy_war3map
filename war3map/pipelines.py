# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import urllib.request

class War3MapPipeline:

    def open_spider(self, spider):
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ("accept-language", "zh-CN,zh;q=0.9"),
            ('Cookie', 'down_ip=1'),
            ('Accept', '*/*'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        self.fp = open('map.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(item['name'] + ", " + item['file_url'])
        urllib.request.urlretrieve(item['file_url'], 'maps/' + item['name'] + ".w3x")
        return item

    def close_spider(self, spider):
        self.fp.close()