from scrapy.crawler import CrawlerProcess  # процесс управляет пауками
from scrapy.settings import Settings  # настройки
from hh_parse.spiders.head_hunter import HeadHunterSpider  # паук

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule('hh_parse.settings')  # взять настройки из модуля settings
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(HeadHunterSpider)
    crawler_process.start()
