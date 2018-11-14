import re
from collections import namedtuple
import time
import os

import requests
from bs4 import BeautifulSoup
import pandas as pd

from const import *


def save_urls(urls):
    with open("urls", "w") as f:
        for u in urls:
            f.write(u + "\r\n")

        f.close()


def save_datas(datas):
    row_0 = ['楼盘名', '价格', '项目地址', '开发商', '物业公司', '最新开盘',
             '交房时间', '容积率', '产权年限', '绿化率', '规划户数', '物业费用', '车位情况']
    df = pd.DataFrame(datas, columns=row_0)
    df.to_csv("lp_info.csv")


class Home(object):
    def __init__(self):
        self.infos = []

    def _page_parse(self, x, urls):
        r = requests.get(x, headers=HEADER)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html5lib')
            if self._is_exist(soup) is None:
                return

            lps = soup.find(
                'ul', {"class": "resblock-list-wrapper"}).find_all('li')

            urls += [self.gather_lp_url(lp) for lp in lps]

    def gather_lp_url(self, lp):
        return lp.find("a", {"class": "name"})["href"]

    def _is_exist(self, soup):
        # 页面存在
        return soup.find("div", {"class": "no-result-wrapper hide"})

    def gather_lp_info(self, x):
        x = LOUPAN + x
        r = requests.get(x, headers=HEADER)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html5lib')
            if soup.find("span", {"class": "junjia"}) is None:
                return

            name = soup.find("h1", {"class": "DATA-PROJECT-NAME"}).string
            price = soup.find("span", {"class": "junjia"}).string
            infos = soup.find(
                "div", {"class": "box-loupan"}).find_all("p", {"class": "desc-p clear"})

            datas = {}
            for info in infos:
                v = info.find("span", {"class": "label-val"}).string.strip()
                k = info.find("span", {"class": "label"}).string.strip()
                datas[k] = v

            self.infos.append([name, price, datas["项目地址："], datas["开发商："], datas["物业公司："], datas["最新开盘："], datas["交房时间："],
                               datas["容积率："], datas["产权年限："], datas["绿化率："], datas["规划户数："], datas["物业费用："], datas["车位情况："]])

        else:
            print(f"访问链接 {x} 失败， code {r.status_code}")

    def run(self, online=True):
        if online:
            self.gather_urls()
        else:
            self.urls = [line.strip() for line in open("urls")]

        [self.gather_lp_info(u) for u in self.urls]

        save_datas(self.infos)

    def gather_urls(self):
        urls = []

        for num in range(1, PAGE_NUM):
            print(f"爬页面{num} ing...")
            url = f"{CHENGDU}{num}"
            self._page_parse(url, urls)

            time.sleep(1)

        save_urls(urls)

        self.urls = urls


if __name__ == "__main__":
    Home().run()
