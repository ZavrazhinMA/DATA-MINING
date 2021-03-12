import os
import dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from insta_parse.spiders.instagram_parser import InstagramParserSpider


if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    tags = ["judo"]
    crawler_settings = Settings()
    crawler_settings.setmodule("insta_parse.settings")
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(
        InstagramParserSpider,
        login=os.getenv("LOGIN"),
        password=os.getenv("PASSWORD"),
        tags=tags,
    )
    crawler_proc.start()
