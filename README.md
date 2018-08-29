## 献给最爱的芃女神

> 何故丹青隐芳语, 渐渐花雨锁心绪。


## 介绍

爬取大众点评成都所有美食<br>
按美食分类：<br> 火锅 川菜 自助餐 咖啡厅 西餐 面包甜点 烧烤 韩国料理 串串香 小龙虾 日本菜 东南亚菜 其他美食 素菜 粤菜 下午茶 海鲜 粉面馆 新疆菜 私房菜 人气餐厅


## 依赖包
```
pip install -r requirement
```

## 使用

### 爬虫
```
cd ./dz.spider
python3 spider.py
```

### 分析

**绘图仅仅在mac上可用，linux和windows不管**

目前支持两种归一化算法：
1、最大最小值
2、标准差
```
cd ./analysis
python3 analize.py
```

具体使用说明
```
# 使用MinMaxScaler算法, 会生成一列中间结果 - ”sissi_std“
a = Analize(norml="mms")

# 按中间结果， 东南亚菜菜系生成最后结果
a.divine(["sissi_std"], foodc="东南亚菜")

筛选得到餐厅：
7781          清漫香草海鲜火锅(保利198店)
7788          青柠记忆泰式海鲜火锅(优品道店)
7780         曼忆莲·泰式海鲜火锅(武侯万达店)
7795            阿诺泰·泰国菜餐厅(光华店)
7789             Breeze In微风小馆
7802                  萌新儿越南pho
7792         GOGO Plate(环球中心店)
7784            卷恋越南料理(凯德来福士店)
7787                    心悦轩泰餐厅
7786            清迈泰式海鲜火锅(铁像寺店)
7867                      印度甩饼
7798                  可美马来西亚餐厅
7866                  咖喱屋(北辰店)
7799    青柠叶·泰式冬阴功海鲜火锅(龙湖北城天街店)
7804            叁月拾二泰餐厅(东能财富店)
7828                      泰色天香
7783           万象·泰式海鲜火锅(创意山店)
7863               泰龙风·纯正东南亚味道
7797                    泰悦泰式料理
7875                        茗苑
7793                  6号泰式海鲜火锅
7864                      灵魂咖喱
7803                      十里春风
7791       泰柠小馆泰式料理·火锅(伊藤洋华堂店)
7801            苏梅泰式海鲜火锅(都江堰店)
7868                  稻米香冻粑叶儿粑
7800               辛格印度餐厅(新都店)
7794             青葵泰式海鲜火锅(郫县店)
7870                    力泰亚洲小厨
7807                小象花园泰式海鲜火锅
7805              泰Basil泰式特色餐厅
7860                    马六甲宴会厅
7811                泰Basil泰国餐厅
7748           泰香米泰国餐厅(春熙路群光店)
7809                 你好北柳泰国传统菜
7833                  泰喜欢(环球店)
7865                       特味轩
7872            新加坡业园区2站自行车租赁点
7790                    泰乙泰国餐厅
7869                      印巴精舍
Name: name, dtype: object
```
