from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.render import make_snapshot

from snapshot_phantomjs import snapshot

bar = Bar()
bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
bar.reversal_axis()
bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
bar.set_global_opts(title_opts=opts.TitleOpts(title="Bar-测试渲染图片"))

make_snapshot(snapshot, bar.render(), r"d:\bar0.png")


