import requests
from json import loads, dumps
from random import randint

def test(links, params):
	b = []
	for i in range(len(links)):
		b.append({'img': {'url': links[i], 'param': params[i]}})
		
	u = 'http://localhost:8080'	 
	res = requests.post(u, data=dumps(b))
	print(res.content)

def main():
	l = [
		"https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12225919/Pembroke-Welsh-Corgi-On-White-01.jpg",
		"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Welchcorgipembroke.JPG/1200px-Welchcorgipembroke.JPG",
		"https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12225906/Pembroke-Welsh-Corgi-On-White-05.jpg",
		"https://img.buzzfeed.com/buzzfeed-static/static/2014-09/23/12/enhanced/webdr10/longform-original-22600-1411489016-22.jpg?downsize=700:*&output-format=auto&output-quality=auto",
		"https://g77v3827gg2notadhhw9pew7-wpengine.netdna-ssl.com/wp-content/uploads/2018/01/corgi-2168005_1920-1024x575.jpg"
	]

	p = [randint(0, 256) for i in range(len(l))]
	test(l, p)

if __name__ == '__main__':
	main()