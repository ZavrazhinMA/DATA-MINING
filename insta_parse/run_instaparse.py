import os
import dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from insta_parse.spiders.insta_spider import InstaSpider

if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    users = ["batman"]
    login = os.getenv('INST_LOGIN'),
    print(login)
    password = os.getenv("INST_PASSWORD")
    crawler_settings = Settings()
    crawler_settings.setmodule("insta_parse.settings")
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(
        InstaSpider,
        login=login,
        password=password,
        users=users,
    )
    crawler_proc.start()
