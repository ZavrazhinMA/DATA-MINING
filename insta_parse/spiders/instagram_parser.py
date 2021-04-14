import scrapy
import json
from ..items import InstaTag, InstaPost
import datetime as dt
from urllib.parse import urlencode


class InstagramParserSpider(scrapy.Spider):
    name = 'instagram_parser'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    _login_url = "https://www.instagram.com/accounts/login/ajax/"
    tag_url = "https://www.instagram.com/explore/tags/"
    query_url = "https://www.instagram.com/graphql/query/"

    def __init__(self, login, password, tags, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login = login
        self.password = password
        self.tags = tags

    def parse(self, response, *args, **kwargs):
        try:
            yield scrapy.FormRequest(
                self._login_url,
                method="POST",
                callback=self.parse,
                formdata={"username": self.login, "enc_password": self.password},
                headers={"x-csrftoken": self.js_data_extract(response)["config"]["csrf_token"]}
            )
        except AttributeError as err:
            print(err)
            if response.json().get('authenticated'):
                for tag in self.tags:
                    yield response.follow(f"{self.tag_url}{tag}/", callback=self.tag_parse)

    def js_data_extract(self, response):
        script = response.xpath("//script[contains(text(), 'window._sharedData = ')]/text()").extract_first()
        script = script.replace("window._sharedData = ", "")[:-1]
        return json.loads(script)

    def tag_parse(self, response):
        js_info = self.js_data_extract(response)
        insta_tag = InstTag(js_info["entry_data"]["TagPage"][0]["graphql"]["hashtag"])
        yield insta_tag.get_tag_item()
        yield from insta_tag.get_post_items()
        yield response.follow(f"{self.query_url}?{urlencode(insta_tag.page_parse())}", callback=self.api_tag_parse)

    def api_tag_parse(self, response):
        js_api = response.json()
        insta_tag = InstTag(js_api["data"]["hashtag"])
        yield from insta_tag.get_post_items()
        yield response.follow(f"{self.query_url}?{urlencode(insta_tag.page_parse())}", callback=self.api_tag_parse)


class InstTag:
    query_hash = "9b498c08113f1e09617a1703c22b2f32"  # совпадает почему то

    def __init__(self, hash_tag: dict):
        self.hash_tag = hash_tag
        self.info_tag = {
            "tag_name": hash_tag["name"],
            "first": 8,
            "after": hash_tag["edge_hashtag_to_media"]["page_info"]["end_cursor"],
        }

    def page_parse(self):
        url_query = {"query_hash": self.query_hash, "variables": json.dumps(self.info_tag)}
        return url_query

    def get_tag_item(self):
        item = InstaTag()  # Переделано после разбора
        item["date_parse"] = dt.datetime.utcnow()
        tag_info = {}
        for key, value in self.hash_tag.items():
            if not (isinstance(value, dict) or isinstance(value, list)):
                tag_info[key] = value
        item["data"] = tag_info
        return item

    def get_post_items(self):
        for edge in self.hash_tag["edge_hashtag_to_media"]["edges"]:
            yield InstaPost(date_parse=dt.datetime.utcnow(), data=edge["node"])
