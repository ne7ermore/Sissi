import pandas as pd
from bs4 import BeautifulSoup
import requests

from const import *


_my_header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Accept-Encoding': 'gzip,deflate,sdch',
    #'Host': CrawlerOption['headder_host'],
    'DNT': '1'
}


class Commnet(object):
    def __init__(self,
                 inf="../shops_info.csv"):
        self.df = pd.read_csv(inf)

    def _page_parse(self, url):
        r = requests.get(url, headers=_my_header)
        print(r.text)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html5lib')

        else:
            print(f"http status code: {r.status_code}, url: {x}")
            return


if __name__ == "__main__":
    c = Commnet()
    c._page_parse("http://www.dianping.com/shop/93195650/")
