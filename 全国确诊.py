import json
import requests
from pyecharts import options as opts
from pyecharts.charts import Map
import pandas as pd


#爬腾讯的
resp = requests.get(
    "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
)

result = json.loads(resp.json()["data"])

china_total = result["chinaTotal"]

area_tree = result["areaTree"]

children = result["areaTree"][0]["children"]


province_list = []
for child in children:
    province = {"name": child["name"],
                "nowConfirm": child["total"]["nowConfirm"],
                "dead": child["total"]["dead"],
                "confirm": child["total"]["confirm"],
                "today_confirm": child["today"]["confirm"]}

    province_list.append(province)

df = pd.DataFrame(province_list)



c = (
    Map()
    .add(
        "当前确诊",
        [
             list(z) for z in zip(df["name"],
                                  df["nowConfirm"])
         ],
        "china"
         )
    .add(
        "累计确诊",
        [
            list(z) for z in zip(df["name"],
                                 df["confirm"])
        ],
        "china"
    )
    .add(
        "今日确诊",
        [
            list(z) for z in zip(df["name"],
                                 df["today_confirm"])
        ],
        "china"
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="全国疫情当前数据"
        ),
        legend_opts=opts.LegendOpts(
            selected_mode="single"
        ),
        visualmap_opts=opts.VisualMapOpts(
            is_piecewise=True,
            pieces=[
                {"value": 0},
                {"min": 1, "max": 9},
                {"min": 10, "max": 99},
                {"min": 100, "max": 499},
                {"min": 500, "max": 999},
                {"min": 1000, "max": 9999},
                {"min": 10000, "label": "10000以上"}
            ]
        ),
    )
    .render("全国确诊.html")
)
