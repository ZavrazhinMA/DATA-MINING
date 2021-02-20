import time
import json
from pathlib import Path
import requests


class Parse:

    def __init__(self, start_url: str, categories_url: str, path_to_save: Path):
        self.start_url = start_url
        self.path_to_save = path_to_save
        self.categories_url = categories_url
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/88.0.4324.182 Safari/537.36 "
                          "Gecko/20100101 Firefox/85.0",
        }

    def _get_response(self, from_url):
        while True:
            response = requests.get(from_url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for category in self._get_categories():
            category["products"] = []
            from_url = f"{self.start_url}?categories={category['parent_group_code']}"
            file_path = self.path_to_save.joinpath(f"{category['parent_group_code']}.json")
            category["products"].extend(list(self._parse_site(from_url)))
            self._save(category, file_path)

    def _parse_site(self, from_url):
        while from_url:
            response = self._get_response(from_url)
            data_parse = response.json()
            from_url = data_parse["next"]
            for product in data_parse["results"]:
                yield product

    def _get_categories(self) -> list:
        response = self._get_response(self.categories_url)
        data = response.json()
        return data

    @staticmethod
    def _save(data: dict, file_path):
        j_data = json.dumps(data, ensure_ascii=False)
        file_path.write_text(j_data, encoding="UTF-8")


if __name__ == "__main__":
    dir_path = Path(__file__).parent.joinpath('cat')
    if not dir_path.exists():
        dir_path.mkdir()
    main_url = "https://5ka.ru/api/v2/special_offers/"
    cat_url = "https://5ka.ru/api/v2/categories/"
    parser = Parse(main_url, cat_url, dir_path)
    parser.run()
