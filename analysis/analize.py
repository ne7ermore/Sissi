import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from const import *


class Analize(object):
    def __init__(self,
                 norml="mms",
                 inf="../shops_info.csv"):
        """
        参数：
            columns - 排序列，类型：list 可以有多个成员
            foodc - 菜系，默认为所有餐厅
        """

        self.df = pd.read_csv(inf)
        self.df["level"] = self.df["level"].apply(lambda x: LEVEL[x])  # 转换格式
        self.df = self.df.drop_duplicates(["id"])  # 去重

        if norml == "mms":
            self._mm_normal()
        elif norml == "std":
            self._std_normal()
        else:
            raise Exception("目前支持mms和std")

    def _mm_normal(self):
        filter_list = ["level", "taste", "envi", "service", "review"]
        df = self.df.filter(items=filter_list)
        data = MinMaxScaler().fit_transform(df)

        df = pd.DataFrame(data, columns=filter_list)

        self.df["sissi_std"] = df.apply(lambda x: sum(
            [x[k] * v for k, v in SISSISTD.items()]), axis=1)

    def _std_normal(self):
        # 归一化
        def norml(x):
            std = x.std()
            mean = x.mean()
            return x.apply(lambda x: (x - mean) / std)

        self.df["level_std"] = norml(self.df["level"])
        self.df["taste_std"] = norml(self.df["taste"])
        self.df["envi_std"] = norml(self.df["envi"])
        self.df["service_std"] = norml(self.df["service"])
        self.df["review_std"] = norml(self.df["review"])

        # 先乘以权重再累加
        self.df["sissi_std"] = self.df.apply(lambda x: sum(
            [x[k + "_std"] * v for k, v in SISSISTD.items()]), axis=1)

    def _rank_by_foodc(self, columns, foodc):
        """
        参数：
            columns - 排序列，类型：list 可以有多个成员
            foodc - 菜系，默认为所有餐厅
        """

        if foodc == "all":
            temp = self.df
        elif foodc in FOOD_C.keys():
            temp = self.df[self.df["foodtype"] == foodc]
        else:
            raise Exception(f"没有当前菜系 - {foodc}")

        return temp.sort_values(by=columns, ascending=False)

    def divine(self, columns,
               foodc="all",
               out_nums=40,
               show_names=True,
               show_pic=False):
        """
        按需展示排序结果,画图会出现中文乱码问题，解决办法请google :)
        参数：
            columns - 排序列，类型：list 可以有多个成员
            foodc - 菜系
            out_nums - 输出结果数
            show_names - 为True时显示餐厅名字
            show_pic - 为True时显示餐厅柱状图,仅仅在mac上可用，linux和windows不管
        """

        ranked = self._rank_by_foodc(columns, foodc).head(out_nums)

        names = ranked["name"]
        stds = ranked["sissi_std"]
        tastes = ranked["taste"]
        envis = ranked["envi"]
        # services = ranked["service"]
        reviews = ranked["review"]

        if show_names:
            print(f"筛选得到餐厅：\n{names}")

        if show_pic:
            import matplotlib.pyplot as plt
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False

            fig, ax = plt.subplots()
            n_groups = len(ranked)
            index = np.arange(n_groups)

            bar_width = 0.1
            opacity = 0.4
            error_config = {'ecolor': '0.3'}

            ax.bar(index, stds, bar_width, alpha=opacity,
                   color='b', error_kw=error_config, label=u'标准')

            ax.bar(index + bar_width, tastes, bar_width, alpha=opacity,
                   color='r', error_kw=error_config, label='口味')

            ax.bar(index + 2 * bar_width, envis, bar_width, alpha=opacity,
                   color='g', error_kw=error_config, label='服务')

            ax.set_xlabel(foodc)
            ax.set_ylabel('Scores')
            ax.set_title('{}-top{}'.format(foodc, n_groups))
            ax.set_xticks(index + bar_width / 2)
            ax.set_xticklabels(names, fontsize=8)
            ax.legend()

            fig.tight_layout()
            plt.show()


if __name__ == "__main__":
    a = Analize(norml="mms")
    a.divine(["sissi_std"], foodc="东南亚菜")
