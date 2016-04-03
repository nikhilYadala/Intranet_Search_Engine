import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from mehr.items import MehrItem
import urlparse
import urllib2
from bs4 import BeautifulSoup
from sets import Set
import os.path
from whoosh import index
from whoosh.fields import Schema, ID, TEXT
urls=list()





class Crawspider(CrawlSpider):
	name = "nani"
	allowed_domains = ["iitg.ernet.in","202.141.80"]
	start_urls = ["http://intranet.iitg.ernet.in/"]
	final_links=list()
	
	rules = [Rule(LinkExtractor(allow=('iitg.ernet.in'), deny_extensions=('jpg'), deny=('csea','news','csesoftwarerepo','news/user','eventcal','calendar','hss/reservation','cclrs','resources/resources','icann'), unique =True), callback='parse_item', process_links='link_filter',follow=True), ]
	def parse_item(self, response):
		global urls
		item = MehrItem()
		lt=list()
		link=list()

		print response.url

		link = response.xpath('//a/@href').extract()
		for lin in link:
			if(lin[0] == '#'):
				continue
			elif(lin[0:3]!='http'):
				lin=urlparse.urljoin(response.url,lin)
				lt.append(lin)
				urls.append(lin)
			else:
				lt.append(lin)
				urls.append(lin)
			#print lin
		item['link']=lt	
		item['desc'] = response.xpath('//td[@id="item_description"]/text()').extract()

		return item
	
	# def pr():
	# 	print urls
	# pr()
	def link_filter(self, links):
		ret = []
		#if(len(urls) < 100):
		for link in links:
			if(len(link.url)<200):
				ret.append(link)
		return ret


	#lt=list()
	#lt.append("http://iitg.ernet.in/")
