from urllib.parse import urljoin
import scrapy
import re
from ..loaders import AutoyoulaLoader


class AutoyoulaSpider(scrapy.Spider):
    name = "autoyoula"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]

    _css_selectors = {
        "brands": "div.TransportMainFilters_brandsList__2tIkv  .ColumnItemList_item__32nYI a.blackLink",
        "pages": "div.Paginator_block__2XAPy a.Paginator_button__u1e7D",
        "car_page": ".SerpSnippet_titleWrapper__38bZM a.SerpSnippet_name__3F7Yu"
    }

    # auto_info1 = {
    #     "name": lambda rsp: rsp.css("div.AdvertCard_advertTitle__1S1Ak::text").get(),
    #     "price": lambda rsp: float(rsp.css("div.AdvertCard_price__3dDCr::text").get().replace("\u2009", "")),
    #     "images": lambda rsp: [itm.attrib.get("src") for itm in rsp.css("figure.PhotoGallery_photo__36e_r img")],
    #     "characteristics": lambda rsp: [{
    #         str(itm.css(".AdvertSpecs_label__2JHnS::text").extract_first()):
    #             str(itm.css(".AdvertSpecs_data__xK2Qx::text").extract_first())
    #     } for itm in rsp.css("div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX")],
    #     "descriptions": lambda rsp: rsp.css(".AdvertCard_descriptionInner__KnuRi::text").extract_first(),
    #     "author": lambda rsp: AutoyoulaSpider.get_author_id(rsp)
    #     # диллеры и частные юзеры имеют разные url
    # }

    auto_info = {
        "car_model": "//div[@data-target='advert-title']/text()",
        "photos": "//div[@data-target='advert']//"
                  "figure[contains(@class, 'PhotoGallery_photo')]//img/@src",
        "characteristics": "//div[@data-target='advert']//h3[contains(text(), 'Характеристики')]/../div/div",
        "description": "//div[@data-target='advert-info-descriptionFull']/text()",
        "price": str("//div[@data-target='advert-price']/text()").replace("\u2009", ""),
        "author": '//script[contains(text(), "window.transitState = decodeURIComponent")]'
    }

    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            link = a.attrib.get("href")
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(
            response, self._css_selectors["brands"], self.brand_parse,
        )

    def brand_parse(self, response):
        yield from self._get_follow(response, self._css_selectors["pages"], self.brand_parse, )
        yield from self._get_follow(response, self._css_selectors["car_page"], self.car_parse)

    def car_parse(self, response):
        loader = AutoyoulaLoader(response=response)
        for key, xpath in self.auto_info.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()
