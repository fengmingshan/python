#导入模块
import requests
from bs4 import BeautifulSoup


def url_open(url):  # 打开每个地址
    #添加header，伪装成浏览器
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    res = requests.get(url, headers=headers)

    return res


# 创建三个储存信息的列表
name_list = []
info_list = []
rate_list = []

#获取电影名字
def get_name(soup, name_list):
    targets = soup.find_all("div", class_="hd")
    for each in targets:
        name_list.append(each.a.span.text)

#获取电影信息
def get_info(soup, info_list):
    targets = soup.find_all("div", class_='bd')
    for each in targets:
        try:
            info_list.append(each.p.text.split('\n')[1].strip() + each.p.text.split('\n')[2].strip())
        except:
            continue
#获取电影评分
def get_rate(soup, rate_list):
    targets = soup.find_all("span", class_="rating_num")
    for each in targets:
        rate_list.append(each.text)

#将获取信息写入TXT文件
def write_into(name_list, info_list, rate_list):
    with open("d:/豆瓣Top250电影.txt", "w", encoding="utf-8") as f:
        for i in range(250):
            f.write(name_list[i]+ '    评分:'+ rate_list[i]+'   ' + info_list[i] +'\n\n')


url = []
for i in range(10):  # 得到十个页面地址
    url.append("https://movie.douban.com/top250?start=%d&filter=" \
               % (i * 25))


def main():
    #遍历每个页面链接并获取信息
    for each_url in url:
        res = url_open(each_url)
        soup = BeautifulSoup(res.text, "html.parser")
        get_name(soup, name_list)
        get_info(soup, info_list)
        get_rate(soup, rate_list)

    write_into(name_list, info_list, rate_list)

#该模块既可以导入到别的模块中使用，另外该模块也可自我执行
if __name__ == "__main__":
    main()