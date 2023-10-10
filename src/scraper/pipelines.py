# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class CnbcScrapperPipeline:
    def process_item(self, item, spider):
        # Check the 'type' field and adjust the feed URI accordingly
        if item.get('type') == 'saved':
            spider.crawler.engine.exporter._settings['FEEDS'] = {
                'saved_links.json': {
                    'format': 'json',
                    'encoding': 'utf8',
                    'store_empty': False,
                    'fields': None,
                }
            }
        elif item.get('type') == 'to_save':
            spider.crawler.engine.exporter._settings['FEEDS'] = {
                'links_to_save.json': {
                    'format': 'json',
                    'encoding': 'utf8',
                    'store_empty': False,
                    'fields': None,
                }
            }
        return item