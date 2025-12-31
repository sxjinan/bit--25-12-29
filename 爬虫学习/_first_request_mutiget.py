import requests

url = "https://movie.douban.com/j/chart/top_list"

data = {
    "type": "24",
"interval_id": "100:90",
"action": "",
"start": "0",
"limit": "20"
}

header ={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.6.8151 SLBChan/111 SLBVPV/64-bit"
}

resq = requests.get(url, params=data, headers=header)

print(resq.json())
print(resq.request.url)