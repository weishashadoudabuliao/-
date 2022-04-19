import requests
import pandas as pd
import json
from pyecharts import options as opts
from pyecharts.charts import Map

url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44"
}

get_text = requests.get(url=url, headers=headers).json()

result = json.loads(get_text["data"])

result_chinaTotal = result["chinaTotal"]

result_children = result["areaTree"][0]["children"]

province_list = []

for i in result_children:
    province = {}

    province["name"] = i["name"]
    province["today confirm"] = i["today"]["confirm"]
    province["total nowConfirm"] = i["total"]["nowConfirm"]
    province["total confirm"] = i["total"]["confirm"]
    province["total dead"] = i["total"]["dead"]
    province["total heal"] = i["total"]["heal"]

    province_list.append(province)

DataFrame = pd.DataFrame(province_list)

pieces = [
    {"value": 0},
    {"min": 1, "max": 9},
    {"min": 10, "max": 99},
    {"min": 100, "max": 999},
    {"min": 1000, "max": 9999},
    {"min": 10000, "label": "大于10000或等于10000"}]

c = (
    Map(init_opts=opts.InitOpts(page_title="中国疫情"))
        .add("今日确诊", [list(z) for z in zip(DataFrame["name"], DataFrame["today confirm"])], "china", is_selected=True)
        .add("现有确诊", [list(z) for z in zip(DataFrame["name"], DataFrame["total nowConfirm"])], "china", is_selected=False)
        .add("累计确诊", [list(z) for z in zip(DataFrame["name"], DataFrame["total confirm"])], "china", is_selected=False)
        .add("累计死亡", [list(z) for z in zip(DataFrame["name"], DataFrame["total dead"])], "china", is_selected=False)
        .set_global_opts(
        title_opts=opts.TitleOpts(title="CHINA covid-19", subtitle="更新时间"+result["lastUpdateTime"]),
        legend_opts=opts.LegendOpts(selected_mode="single"),
        visualmap_opts=opts.VisualMapOpts(pieces=pieces, is_piecewise=True),
    )
        .render("CHINA covid-19.html")
)
