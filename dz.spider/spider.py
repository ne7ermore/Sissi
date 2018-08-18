import re
from collections import namedtuple
import time

import requests
from bs4 import BeautifulSoup
import pandas as pd

from const import *


class Shop(object):
    def __init__(self):
        self.comments = namedtuple('comments', ['taste', 'envi', 'service'])
        self.shop_info = namedtuple(
            'shop_info', ['foodtype', 'name', 'id', 'url', 'level', 'price', 'comments', 'review'])

    def _parse_infos(self, shop, foodtype):
        if not self._is_spide(shop):
            return None

        name = shop.find("h4").renderContents().decode()
        info = shop.find(
            "a", {"data-click-name": "shop_title_click"})

        _id = info["data-shopid"]
        url = info["href"]

        price = shop.find("a", {"class": "mean-price"}
                          ).renderContents().decode()
        price = re.search('￥(.+)<', price)
        if price is None:
            price = -1
        else:
            price = price.group(1)

        comment_list = shop.find(
            "span", {"class": "comment-list"})

        comments = comment_list.find_all("b")
        comments = self.comments._make(
            [c.renderContents().decode() for c in comments])

        review = shop.find("a", {"class": "review-num"}
                           )
        if review is None:
            review = -1
        else:
            review = review.b.renderContents().decode()

        level = shop.find("span", {"class": "sml-rank-stars"})
        if level is None:
            level = "无"
        else:
            level = level["title"]

        result = self.shop_info._make(
            [foodtype, name, _id, url, level, price, comments, review])
        return result

    def _is_destination(self, soup):
        # 页面不存在
        return soup.find("p", {"class": "not-found-suggest"})

    def _is_spide(self, shop):
        # 要不要爬呢
        if shop.find("span", {"class": "istopTrade"}) is not None:
            # 没开业
            return False

        if shop.find("span", {"class": "comment-list"}) is None:
            # 没有评价
            return False

        return True

    def _page_parse(self, x, foodtype, results):
        r = requests.get(x, headers=DZHEADER)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html5lib')
            if self._is_destination(soup) is not None:
                return

            shops = soup.find('div', id='shop-all-list').find_all('li')

            results += [self._parse_infos(shop, foodtype) for shop in shops]
        else:
            print(f"http status code: {r.status_code}, url: {x}")
            return

    def run(self):
        results = []

        for k, v in FOOD_C.items():
            print(f"爬{k}ing......")
            for num in range(1, 51):
                url = "{}/{}p{}".format(CHENGDU, v, num)
                self._page_parse(url, k, results)

                # 不慢点要被针对
                time.sleep(1)

        row_0 = ['foodtype', 'name', 'id', 'url', 'level',
                 'price', 'taste', 'envi', 'service', 'review']

        datas = [[r.foodtype, r.name, r.id, r.url, r.level, r.price,
                  r.comments.taste, r.comments.envi, r.comments.service, r.review] for r in results if r is not None]
        df = pd.DataFrame(datas, columns=row_0)
        df.to_csv("../shops_info.csv")


if __name__ == "__main__":
    s = Shop()
    s.run()
