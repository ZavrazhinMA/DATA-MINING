from urllib.parse import urljoin

from scrapy import Selector
from scrapy.loader import ItemLoader
import re
from itemloaders.processors import TakeFirst, MapCompose  # MC- передать по одному


def get_car_info(item) -> dict:
    selector = Selector(text=item)
    return {
        selector.xpath("//div[contains(@class, 'AdvertSpecs_label')]/text()").extract_first():
            selector.xpath("//div[contains(@class, 'AdvertSpecs_data')]//text()").extract_first()
    }


def get_author_id(item):
    selector = Selector(text=item)
    start_url = 'https://youla.ru'
    re_pattern = re.compile(r'youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar')
    try:
        result = re.findall(re_pattern, selector.xpath("//text()").extract_first())
        url = urljoin(start_url, f'/user/{result[0]}') if result else 'no author_id'
        return url
    except TypeError:
        pass


class AutoyoulaLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    car_model = TakeFirst()
    characteristics_in = MapCompose(get_car_info)
    author_in = MapCompose(get_author_id)
    price_out = TakeFirst()
