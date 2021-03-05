from scrapy.crawler import CrawlerProcess  # процесс управляет пауками
from scrapy.settings import Settings  # настройки
from ay_parse.spiders.autoyoula import AutoyoulaSpider  # паук

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule('ay_parse.settings')  # взять настройки из модуля settings
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(AutoyoulaSpider)
    crawler_process.start()
