import datetime as dt
from urllib.parse import urljoin
import requests
from requests.exceptions import Timeout, ConnectionError
import bs4
import pymongo


class Parse:
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/88.0.4324.182 Safari/537.36 "
                      "Gecko/20100101 Firefox/85.0",
    }

    def __init__(self, start_url, clint_db):
        self.start_url = start_url
        self.db = clint_db["magnit_mining_db"]
        self.collection = self.db["magnit_promo"]

    @staticmethod
    def _get_response(url_page):
        page = ''
        try:
            page = requests.get(url_page)
            if page.status_code != 200:
                print('Ошибка: ', page.status_code)
        except Timeout:
            print('The request timed out')
        except ConnectionError:
            print('A Connection error occurred')
        return page

    def _get_soup(self, url_page):
        response = self._get_response(url_page)
        return bs4.BeautifulSoup(response.text, "lxml")

    def run(self):
        soup = self._get_soup(self.start_url)
        catalog = soup.find("div", attrs={"class": "сatalogue__main"})
        for prod_a in catalog.find_all("a", recursive=False):
            product_data = self._parse(prod_a)
            if len(product_data) > 3:  # отсечь рекламные баннеры
                self._save(product_data)

    def get_template(self):
        return {
            "product_name": lambda a: a.find("div", attrs={"class": "card-sale__title"}).text,
            "url": lambda a: urljoin(self.start_url, a.attrs.get("href", "")),
            "promo_name": lambda a: a.find("div", attrs={"class": "card-sale__name"}).text,
            "old_price": lambda a: float(
                ".".join(
                    itm for itm in a.find("div", attrs={"class": "label__price_old"}).text.split()
                )
            ),
            "new_price": lambda a: float(
                ".".join(
                    itm for itm in a.find("div", attrs={"class": "label__price_new"}).text.split()
                )
            ),
            "image_url": lambda a: urljoin(self.start_url, a.find("img").attrs.get("data-src")),
            "date_from": lambda a: self.__get_date(
                a.find("div", attrs={"class": "card-sale__date"}).text
            )[0],
            "date_to": lambda a: self.__get_date(
                a.find("div", attrs={"class": "card-sale__date"}).text
            )[1],
        }

    @staticmethod
    def __get_date(date_string) -> list:
        date_list = date_string.replace("с ", "", 1).replace("\n", "").split("до")
        result = []
        for date in date_list:
            temp_date = date.split()
            year = dt.datetime.now().year
            temp_month = dt.datetime.now().month
            day = int(temp_date[0])
            month = int(month_dict[temp_date[1][:3]])
            # print(year, day, month)
            if (month >= 9) and (temp_month <= 3):  # из условия, что акции не идут больше 3х месяцев
                year -= 1  # для акций которые парсились в первые месяцы после НГ
            if (month <= 3) and (temp_month >= 9):  # из условия, что акции не идут больше 3х месяцев
                year += 1  # для акций которые парсились в последние месяцы перед НГ
            result.append(
                dt.datetime(year, day, month)
            )
        return result

    def _parse(self, product_a) -> dict:
        data = {}
        for key, func in self.get_template().items():
            try:
                data[key] = func(product_a)
            except (AttributeError, ValueError):
                pass
        return data

    def _save(self, data: dict):
        self.collection.insert_one(data)


if __name__ == "__main__":

    month_list = [
        "январь",
        "февраль",
        "март",
        "апрель",
        "май",
        "июнь",
        "июль",
        "август",
        "сентябрь",
        "октябрь",
        "ноябрь",
        "декабрь"
    ]
    month_dict = {}
    for num, month in enumerate(month_list, 1):
        month_dict[month[:3]] = num

    url = "https://magnit.ru/promo/"
    db_client = pymongo.MongoClient("mongodb://localhost:27017")
    parser = Parse(url, db_client)
    parser.run()
