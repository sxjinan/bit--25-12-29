import requests

url = "http://wwww.baidu.com"
resp  = requests.get(url)
resp.encoding = "utf-8"
