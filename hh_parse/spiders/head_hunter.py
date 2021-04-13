import scrapy
from ..loaders import VacancyLoader, EmployerLoader
from .info_xpath import _vacancy_info, _employer_info, _page_selectors


class HeadHunterSpider(scrapy.Spider):
    name = 'head_hunter'
    allowed_domains = ['hh.ru']
    # start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&schedule=remote&L_save_area=true'
                  '&area=1946&from=cluster_area&showClusters=true']
    main_url = 'https://hh.ru/'

    def _get_follow(self, response, select_str, callback, **kwargs):
        for link in response.xpath(select_str):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(response, _page_selectors["pages"], self.parse)
        yield from self._get_follow(response, _page_selectors["employer_vacancies_page"], self.parse)
        yield from self._get_follow(response, _page_selectors["vacancies"], self.parse_vacancy)
        yield from self._get_follow(response, _page_selectors["employer_page"], self.parse_employer)

    def parse_vacancy(self, response):
        loader = VacancyLoader(response=response)
        for key, xpath in _vacancy_info.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()

    def parse_employer(self, response):
        loader = EmployerLoader(response=response)
        for key, xpath in _employer_info.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()
