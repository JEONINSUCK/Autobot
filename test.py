import requests
import json

base_url = "https://www.coindeskkorea.com/news/articleList.html"
data = {"input":"bitcoin"}
r = requests.post(base_url,data=json.dumps(data))
print(r.text)