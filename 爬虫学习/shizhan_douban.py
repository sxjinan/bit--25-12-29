#思路 拿到页面源代码
# 编写正则提取数据

import requests
import re
with open("top250.csv", mode="w", encoding="utf-8") as f:
    for i in range(0, 250, 25):
    #逐页提取
        url = f"https://movie.douban.com/top250?start={i}&filter="
        headers = {"User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.6.8151 SLBChan/111 SLBVPV/64-bit"}
        request = requests.get(url, headers=headers)

        page_content = request.text
        print(page_content)

        #编写正则表达式
        #re.S 让.匹配换行符
        obj = re.compile(r'<div class="item">.*?<span class="title">(?P<name>.*?)'
                        r'</span>.*?<p>.*?导演:(?P<director>.*?)&nbsp;.*?主演:(?P<actor>.*?)'
                        r'<br>(?P<year>.*?)&nbsp;.*?<span class="rating_num" property="v:average">(?P<rating>.*?)</span>'
                        r'.*?<span>(?P<num_people>.*?)人评价</span>',re.S)
        result = obj.finditer(page_content)
    
        for item in result:
            name = item.group("name").strip()
            director = item.group("director").strip()   
            actor = item.group("actor").strip()
            year = item.group("year").strip()
            rating = item.group("rating").strip()
            num_people = item.group("num_people").strip()
            f.write(f"{name},{director},{actor}，{year},{rating},{num_people}\n")
            print(name, director, actor, year, rating, num_people)