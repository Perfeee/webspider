
import urllib.request,urllib,urllib.parse
url = 'http://www.baibai.com/'
response = urllib.request.urlopen('http://www.baidu.com/')
html = response.read()
#print(html)

print('helloworld')

data = {}
data['name'] = 'WHY'
data['location'] = 'SDU'
data['language'] = 'Python'

urlvalue = urllib.parse.urlencode(data)
print(urlvalue)

#req = urllib.Request('www.baibai.com')
try: 
	web = urllib.request.urlopen(url)
	print(web.read())
except urllib.error.URLError:
	print(urllib.error.URLError.reason)
	
print('github learning ')