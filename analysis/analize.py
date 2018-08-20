import pandas as pd
import numpy as np
from const import *

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class Analize(object):
    def __init__(self, inf="../shops_info.csv"):
        self.df = pd.read_csv(inf)
        self.df = self.df.drop_duplicates(["id"])  # 去重

        self._normalize()
        self._add_std()

    def _normalize(self):
        # 归一化
        def norml(x):
            std = x.std()
            mean = x.mean()
            return x.apply(lambda x: (x - mean) / std)

        self.df["level_std"] = self.df["level"].apply(lambda x: LEVEL[x])
        self.df["level_std"] = norml(self.df["level_std"])

        self.df["taste_std"] = norml(self.df["taste"])
        self.df["envi_std"] = norml(self.df["envi"])
        self.df["service_std"] = norml(self.df["service"])
        self.df["review_std"] = norml(self.df["review"])

    def _add_std(self):
        self.df["sissi_std"] = self.df.apply(lambda x: sum(
            [x[k + "_std"] * v for k, v in SISSISTD.items()]), axis=1)

    def _rank_by_foodc(self, foodc, columns):
        # df = self.df[self.df["foodtype"] == foodc]
        return self.df.sort_values(by=columns, ascending=False)

    def draw(self, ranked, foodc):
        fig, ax = plt.subplots()
        n_groups = len(ranked)
        index = np.arange(n_groups)

        names = ranked["name"]
        stds = ranked["sissi_std"]
        tastes = ranked["taste"]
        envis = ranked["envi"]
        # services = ranked["service"]
        reviews = ranked["review"]

        bar_width = 0.1
        opacity = 0.4
        error_config = {'ecolor': '0.3'}

        ax.bar(index, stds, bar_width, alpha=opacity,
               color='b', error_kw=error_config, label=u'标准')

        ax.bar(index + bar_width, tastes, bar_width, alpha=opacity,
               color='r', error_kw=error_config, label='口味')

        ax.bar(index + 2 * bar_width, envis, bar_width, alpha=opacity,
               color='g', error_kw=error_config, label='服务')

        print(names)

        ax.set_xlabel(foodc)
        ax.set_ylabel('Scores')
        ax.set_title('{}-top{}'.format(foodc, n_groups))
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(names, fontsize=8)
        ax.legend()

        fig.tight_layout()
        plt.show()


if __name__ == "__main__":
    a = Analize()
    fc = "东南亚菜"
    ranked = a._rank_by_foodc(fc, ["sissi_std"]).head(40)
    a.draw(ranked, fc)
