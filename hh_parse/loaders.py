from scrapy.loader import ItemLoader
from urllib.parse import urljoin
from itemloaders.processors import TakeFirst


def hh_emp_url(emp_id):
    return urljoin("https://hh.ru/", emp_id[0])


class VacancyLoader(ItemLoader):
    default_item_class = dict
    title_out = TakeFirst()
    salary_out = " ".join
    employer_url_out = hh_emp_url
    description_out = "\n".join


class EmployerLoader(ItemLoader):
    default_item_class = dict
    employer_website_out = TakeFirst()
    employer_out = TakeFirst()
    employer_description_out = " ".join
