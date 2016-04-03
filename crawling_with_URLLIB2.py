import urllib2
from bs4 import BeautifulSoup
from sets import Set

deny=['jee','csea','news','csesoftwarerepo','news/user','eventcal','calendar','hss/reservation','cclrs','resources/resources','icann']
	

def is_not_wrong(url):
	deny=['jee','csea','news','csesoftwarerepo','news/user','eventcal','calendar','hss/reservation','cclrs','resources/resources','icann']
	for use_less in deny:
		if use_less in url:
			return 0;
		i=-2
		count=0
		length = len(url)
		while(count!=1 and (-i)<length):
			if (url[i] =='/'):
				count+=1
			i-=1
		word=url[length+i+2:]
		if(word in url[:length+i+1]):
			return 0;
	return 1;

def crawler(given_url):
	global integer
	global allowed_urls
	flag=0
	try:
		try:
			page = urllib2.urlopen(given_url)
			visited_urls.add(given_url)
			print given_url
			if(page.info().type == 'text/html'):
				html_doc = page.read()
				soup = BeautifulSoup(html_doc)
				for l in soup.findAll('a'):
					href=l.get('href')
					if(href and (len (href)<200)):
						if(href[0] == '#' or ('mailto' in href)):
							continue
						if(href[0] == '/' and given_url[-1] == '/'):
							href = given_url + href[1:]
						if(href[-1] != '/'):
								href += '/'
						if(href not in visited_urls):
							for allowed in allowed_urls:
								if allowed in href:
									flag=1
									break
							if(flag==1):
								flag=0		
								if(len(href)<200 and (is_not_wrong(href)==1 )):
									crawler(href)
		except ValueError, e:
			print ''
	except urllib2.URLError, e:
		print '404 error: ' + given_url
	return;

visited_urls= Set(["http://local.iitg.ernet.in/aboutus/"])

integer=1
allowed_urls=["202.141.80","iitg.ernet.in","iitg.ac.in"]
fish_url = "http://intranet.iitg.ernet.in/"
# page = urllib2.urlopen(fish_url)
#print page.info()

paaku(fish_url)
for x in visited_urls:
  print x
