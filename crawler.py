from datetime import date, datetime
import time
from bs4 import BeautifulSoup
from pybloom_live import ScalableBloomFilter
import requests
import pymongo
import json
import config
import re


# 配置trs请求头
def get_headers():
    headers = {
        "accept": config.accept,
        "accept-encoding": config.accept_encoding,
        "accept-language": config.accept_language,
        "Cookie": config.cookie,
        "User-Agent": config.user_agent
    }
    return headers


# 设置布隆过滤器
def get_bloom_filter():
    # 设置可自动扩容的布隆过滤器
    bloom = ScalableBloomFilter(initial_capacity=200, error_rate=0.001)
    # 锻炼过滤器
    with open(config.news_hash, "r") as b_hashid:
        line = b_hashid.readline()
        while line:
            # 开始锻炼
            bloom.add(line.strip())  # 为了防止有换行出现要用strip
            # print(line.strip())
            line = b_hashid.readline()
    return bloom

# 开爬
def reptile(pattern):
    # 设置日期
    now = "2023/0623/"
    # 设置请求头
    headers = get_headers()
    # 设置布隆过滤器
    bloom = get_bloom_filter()

    try:
        # 开始爬取
        i = 1
        while i <= config.end:  # end为爬取的天数
            # 设置请求
            url1 = "https://www.chinanews.com.cn/scroll-news/" + str(now) + "news.shtml"
            # 设置容器
            news_title = []
            news_url = []
            # 请求
            requests.packages.urllib3.disable_warnings()
            resp = requests.get(url1, headers=headers, timeout=200)
            bs = BeautifulSoup(resp.text, "lxml")
            tag_list = bs.find_all("div", class_="dd_bt")  # 定位div标签

            for n in tag_list:
                # 定位a标签
                a_tag = n.find("a")

                if a_tag:
                    try:
                        # 获取标题
                        tittle = a_tag.text.encode("iso-8859-1").decode("utf-8")
                        # print(tittle)
                    except Exception as e:
                        continue
                    # 对tittle过滤
                    if re.search(pattern, tittle):
                        # 判断是否已经爬取过
                        if bloom.add(tittle):
                            print(f"已经爬取过：{tittle}")
                            continue
                        # 获取标题
                        news_title.append(tittle)

                        # 获取url
                        if a_tag["href"].startswith("//www"):
                            url = str(a_tag["href"])[2:]
                            news_url.append(url)
                        else:
                            url = "https://www.chinanews.com" + str(a_tag["href"])
                            news_url.append(url)

            # 写入文件
            with open(config.news_hash, "a") as b_hashid:
                for t in news_title:
                    b_hashid.write(t + "\n")
            with open(config.urls_hash, "a") as u_hashid:
                for u in news_url:
                    u_hashid.write(u + "\n")
            print(f"{now},存储{len(news_title)}条新闻")
            # 休眠
            time.sleep(2)
            # 倒退一天
            now = config.date_deal(now)
            i += 1
    except Exception as e:
        print(f"爬取出错：{e}")

if __name__ == '__main__':
    pattern = r"(浙江|改革开放)"
    reptile(pattern)