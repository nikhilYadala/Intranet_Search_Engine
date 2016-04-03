from whoosh.qparser import QueryParser
from whoosh import index
import sys

ix=index.open_dir("mehreen_index/")
with ix.searcher() as searcher:

	#write function for taking the qstring from file loaded by webinterface.
	qstring=unicode(sys.argv[1].replace('{}',' '),'utf-8')

#	qstring=unicode(sys.argv[1],'utf-8')
	query = QueryParser(u'content', schema=ix.schema).parse(qstring)

	#for correcting the query
	corrected=searcher.correct_query(query,qstring)
	#give an option for correct input

	if corrected.query!=query:
		print(corrected.string)
	else:
		pass


	#the limit here limits the number of results to be printed
	results = searcher.search(corrected.query,limit=50)
	results.fragmenter.charlimit=None  #nolimiting for proper highlithing
	print results
	
	#printing the reusults,text highliting to be done here
	for result in results:
		if(result['path'][-4:] == '.pdf'):
			print result['path'].replace('{}','/').replace('{','//')
		else:
			print result['path']
		print result.highlights('content').replace('\n','').replace('\r','').encode("utf-8").strip()
		#print(result.highlights('content'))