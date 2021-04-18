import scrapy
import json
from ..items import MainUser
import datetime as dt


class InstaSpider(scrapy.Spider):
    name = 'insta_spider'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    _login_url = "https://www.instagram.com/accounts/login/ajax/"
    query_url = "https://www.instagram.com/graphql/query/"
    query = {
        'edge_follow': '3dec7e2c57367ef3da3d987d89f9dbc8',
        'edge_followed_by': '5aefa9893005572d237da5068082d8d5'
    }

    def __init__(self, login, password, users, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login = login
        self.password = password
        self.users = users

    def parse(self, response, *args, **kwargs):
        try:
            yield scrapy.FormRequest(
                self._login_url,
                method="POST",
                callback=self.parse,
                formdata={"username": self.login, "enc_password": self.password},
                headers={"x-csrftoken": self.script_json_info(response)["config"]["csrf_token"]}
            )
        except AttributeError:
            if response.json()['authenticated']:
                for user in self.users:
                    yield response.follow(f"/{user}/", callback=self.user_parse, cb_kwargs={"main_user": user})

    def script_json_info(self, response):
        script = response.xpath("//script[contains(text(), 'window._sharedData = ')]/text()").extract_first()
        script = script.replace("window._sharedData = ", "")[:-1]
        return json.loads(script)

    def user_parse(self, response, main_user, flw=None):
        main_user = main_user
        user_data = self.script_json_info(response)["entry_data"]["ProfilePage"][0]["graphql"]["user"]
        data = {}
        item = MainUser()
        item['date'] = dt.datetime.utcnow()
        item['flw_status'] = "main_page" if flw is None else flw
        item['main'] = "self_info" if flw is None else main_user
        user_id = user_data['id']
        for key, value in user_data.items():
            if not (isinstance(value, dict) or isinstance(value, list)):
                data[key] = value
        item['data'] = data
        for flw in self.query.keys():
            yield response.follow(self.get_api_url(user_id, flw=flw), callback=self.parse_followings,
                                  cb_kwargs={"main_user": main_user, 'flw': flw, 'user_id': user_id})

        yield item

    def get_api_url(self, user_id, flw, after=''):

        variables = {"id": user_id,
                     "include_reel": False,
                     "fetch_mutual": False,
                     "first": 24,
                     "after": after}
        return f'{self.query_url}?query_hash={self.query[flw]}&variables={json.dumps(variables)}'

    def parse_followings(self, response, main_user, flw, user_id):
        flw_data = response.json()
        flw_users = flw_data['data']['user'][flw]['edges']
        end_cursor = flw_data['data']['user'][flw]['page_info']['end_cursor']
        user_id = user_id
        for node in flw_users:
            user = node['node']['username']
            yield response.follow(f"/{user}/", callback=self.user_parse, cb_kwargs={"main_user": main_user, "flw": flw})
        if flw_data['data']['user'][flw]['page_info']['has_next_page']:
            yield response.follow(
                self.get_api_url(user_id=user_id, after=end_cursor, flw=flw),
                callback=self.parse_followings, cb_kwargs={"main_user": main_user, 'flw': flw, 'user_id': user_id})
