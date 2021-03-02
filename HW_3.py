import requests
import bs4
from requests.exceptions import Timeout, ConnectionError
from Database.db_fill import Database
from urllib.parse import urljoin
import json



# import typing


class ParseGB:
    # headers = {
    #     "Accept": "application/json",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    #                   "Chrome/88.0.4324.182 Safari/537.36 "
    #                   "Gecko/20100101 Firefox/85.0",
    # }

    def __init__(self, start_url, database: Database):
        self.db = database
        self.start_url = start_url
        self.main_url = "https://geekbrains.ru"
        self.done_urls = set()
        self.tasks = []

    def _get_response(self, url_page):
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
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        return soup

    def _get_task(self, url_page, callback):

        def task():
            soup = self._get_soup(url_page)
            return callback(url_page, soup)

        return task

    def _parse_page(self, url_page, soup):
        ul = soup.find("ul", attrs={"class": "gb__pagination"})
        pages_url = set(urljoin(url_page, link.attrs.get("href"))
                        for link in ul.find_all("a")
                        if link.attrs.get("href"))
        for page in pages_url:
            if page not in self.done_urls:
                self.tasks.append(self._get_task(page, self._parse_page))

        post_section = soup.find("div", attrs={"class": "post-items-wrapper"})
        posts_url = set(urljoin(url_page, link.attrs.get("href"))
                        for link in post_section.find_all("a", attrs={"class": "post-item__title"})
                        if link.attrs.get("href"))
        for url in posts_url:
            if url not in self.done_urls:
                self.tasks.append(self._get_task(url, self._parse_post))

    def _parse_post(self, url_page, soup):
        author_info = soup.find("div", attrs={"itemprop": "author"})
        data = {
            "post_data": {
                "title": soup.find("h1", attrs={"class": "blogpost-title"}).text,
                "url": url_page,
                "id": soup.find("comments").attrs.get("commentable-id"),
            },
            "author_data": {
                "url": urljoin(self.main_url, author_info.parent.attrs.get("href")),
                "name": author_info.text,
            },
            "tags_data": [
                {"name": tag.text, "url": urljoin(self.main_url, tag.attrs.get("href"))}
                for tag in soup.find_all("a", attrs={"class": "small"})
            ],
            "comments_data": self._get_comments(soup.find("comments").attrs.get("commentable-id")),
        }
        return data

    def _get_comments(self, post_id) -> list:
        api_comments = f"/api/v2/comments?commentable_type=Post&commentable_id={post_id}&order=desc"
        response = self._get_response(urljoin(self.start_url, api_comments))
        data = response.json()
        # with open("test.json", "a", encoding="utf-8") as file:
        #     json.dump(data, file)
        return data

    def run(self):
        self.tasks.append(self._get_task(self.start_url, self._parse_page))
        self.done_urls.add(self.start_url)
        for task in self.tasks:
            result = task()
            if isinstance(result, dict):
                self.db.create_post(result)


if __name__ == "__main__":
    database = Database("sqlite:///gb_blog.db")
    parser = ParseGB("https://geekbrains.ru/posts", database)
    parser.run()
