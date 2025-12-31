import requests

url = "http://www.sogou.com/web?query="

headers = {
    "User-Agent":
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.6.8151 SLBChan/111 SLBVPV/64-bit"
}

content  = input("请输入搜索内容：")
resp  = requests.get(url + content, headers=headers)

print(resp.request.headers)