import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import urlparse
import urllib2
from bs4 import BeautifulSoup
from sets import Set
import os.path
from whoosh import index
from whoosh.fields import Schema, ID, TEXT
import datetime
#import whoosh.reading.IndexReader


def get_schema():
	#store the HTML content also for highliting the text
	return Schema(path=ID(unique=True, stored=True),time=TEXT, content=TEXT(stored = True));

def indexer(My_IndexDir,links):
	if (not os.path.exists(My_IndexDir)):
		os.mkdir(My_IndexDir)
	print "came into this"
	ix=index.create_in(My_IndexDir,schema=get_schema())
	ix = index.open_dir(My_IndexDir)
	already_indexed_paths=set()
	tobe_indexed_paths=set()
	print "no problem upto creating"
	#for searching in the directory
	with ix.searcher() as searcher:
		print "jeevitam start avaali"
		writer = ix.writer()
		reader=ix.reader()
		print "jeevitam dengindhi"
    
    #run a loop over already existing indexes

		for fields in reader.all_stored_fields():
			print "in the loop for taking previos information"
			already_indexed_paths.add(fields['path'])

			#this path might have got deleted since the last index,to handle this
			if not os.path.exists(fields['path']):
				writer.delete_by_term('path', fields['path'])
			else:
			#check whether this file has ever changed since the last index 
				previously_indexed_time=fields['time']
					#some how check whether it was changed or not
				try:
					checking_link=fields['path']
					#hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
					re=urllib2.Request(checking_link)
					re.add_header({'If-Modified-Since':previously_indexed_time})
					page = urllib2.urlopen(re)
				

				except urllib2.HTTPError, e:
					print "hi there"+ checking_link+"err"+e.fp.read()
					if e.code==304:
						#the file content is not changed
						print "file contents not changed.."+checking_link
						continue
					if e.code==200:
						writer.delete_by_term('path',fields['path'])
						tobe_indexed_paths.add(fields['path'])
						print "file contents CHANGED..."+checking_link


					else:
						continue
	writer.commit()


	#Now the incremental indexing starts:
	for link in links:
		if link in tobe_indexed_paths or link not in already_indexed_paths:
			print "chooodu oka vaipe chooodu"

			if link[-4:]=='.pdf':
				linko=link.replace("//","{")
				linko=linko.replace("/","{}")

				os.system("wget " + link +" -O "+linko)
				print "just downloaded "+link
				link=linko


				os.system("pdftotext "+link+" "+link[:-4]+".txt")

				#os.system("pdftotext gg1.pdf gg1.txt")
				if (not os.path.exists(link[:-4]+".txt")):
					print "please , ledhu ani okkka maata cheppu, chaalu"
					continue

				if open(link[:-4]+".txt",'r'):
					print "txt undhiraaaaa"
				with open(link[:-4]+".txt",'r') as f:
					entire_text=unicode(f.read().replace('\n',' '),'utf-8')
					
					ix = index.open_dir(My_IndexDir)
					writer=ix.writer()

					Path=unicode(link,"utf-8")
					modtime=unicode(datetime.datetime.strftime(datetime.datetime.now(), '%a, %Y %b %d %H:%M:%S GMT'),'utf-8')
					writer.add_document(path=Path,content=entire_text,time=modtime)
					writer.commit()

					continue



			try:
				#hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
				#req_link=urllib2.Request(link,headers=hdr)
				req_link=urllib2.Request(link)
				#page = urllib2.urlopen(req_link,context=ssl._create_unverified_context())
				page = urllib2.urlopen(req_link)

			except urllib2.HTTPError, e:
				continue
			if(page.info().type == 'text/html'):
				print link+"   srimnathuda"
				html_doc = page.read()
				soup = BeautifulSoup(html_doc,'html.parser')
				entire_text=soup.get_text()
				ix = index.open_dir(My_IndexDir)
				writer=ix.writer()
				Path=unicode(link,"utf-8")

				modtime=unicode(datetime.datetime.strftime(datetime.datetime.now(), '%a, %Y %b %d %H:%M:%S GMT'),'utf-8')
				writer.add_document(path=Path,content=entire_text,time=modtime)
				#print "stage 1"
				writer.commit()
				#print "stage 2"

lt=list()
with open('List_Of_URLS_to_be_indexed.txt') as f:
	lt = f.read().splitlines()
My_IndexDir="text_indexed_directory/"
indexer(My_IndexDir,lt)