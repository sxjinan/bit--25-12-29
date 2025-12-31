import requests
import re

url = "https://www.xiaopian.org/"
response = requests.get(url)
response.encoding = "gbk"
page_content = response.text

obj1 = re.compile(r"2025新片精品.*?<ul>(?P<html>.*?)</ul>",re.S)
html = obj1.search(page_content).group("html")
# print(html)

obj2 = re.compile(r"<li><a href='(?P<href>.*?)' title")
obj2.finditer(html)
for item in obj2.finditer(html):
    href = item.group("href")
    print(href)