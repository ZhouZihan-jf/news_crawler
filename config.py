from datetime import datetime

import pymongo
# header相关
accept = "*/*"
accept_encoding = "gzip, deflate, br"
accept_language = "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
cookie = ""
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51"

# 参数相关
end = 10

# 文件相关
news_hash = "files/news.txt"
urls_hash = "files/urls.txt"

# 时间相关
def date_deal(date):
    if date is None:
        return
    # 将"YY/MMDD/"格式的日期转换为datetime对象
    format_string = "%Y/%m%d/"
    date_object = datetime.strptime(date, format_string)

    # 将datetime对象转换为时间戳
    timestamp = date_object.timestamp()

    # 倒退一天
    previous_day_timestamp = timestamp - 24 * 60 * 60  # 减去24小时对应的秒数

    # 将倒退后的时间戳转换为datetime对象
    previous_day_datetime = datetime.fromtimestamp(previous_day_timestamp)

    # 将datetime对象转换回"/YY/MMDD/"格式的日期
    previous_day_date_string = previous_day_datetime.strftime("%Y/%m%d/")

    # print(previous_day_date_string)  # 输出倒退一天后的日期字符串

    return previous_day_date_string


