# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class NewsJSONPipeline:
    def open_spider(self, spider):
        self.file = open("news.json", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=True) + "\n"
        self.file.write(line)
        return item

class NewsCSVPipeline:
    def open_spider(self, spider):
        self.file = open("news.csv", "w")
        self.file.write('Header;Source;DateTime;URL\n')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line_dict = ItemAdapter(item).asdict()
        line = line_dict['header'] + ";" + line_dict['source'] + ";" + line_dict['datetime'] + ";" + line_dict['url'] + "\n"
        self.file.write(line)
        return item
