from urllib.request import urlopen

url  = "http://baidu.com"
response = urlopen(url)
html = response.read().decode("utf-8")
with open("baidu.html", "w", encoding="utf-8") as f:
    f.write(html)
print("已完成爬取")