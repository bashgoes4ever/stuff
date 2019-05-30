import requests

def get_html(url, useragent=None, proxy=None):
	r = requests.get(url, headers=useragent, proxies=proxy)
	return r.text

print(get_html('https://yadi.sk/d/ScA2D9LuvvSMp'))