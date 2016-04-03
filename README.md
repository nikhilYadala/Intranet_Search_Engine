# Intranet_Search_Engine
A searching facility over the webpages and pdfs over the intranet

The whole code is developed in python and the webinterface by PHP, using Bootstrap for its desgining.

This code bast has a crawler, that performs a DFS by using Urllib2 for requesting the html source of the URLS,
and also a crawler implemnetd in scrapy.

The incremental indexer indexes the list of URL'S that have been crawled(in List_Of_URLS_to_be_indexed.txt), by indexing
the essential html content. PDFs ,if had been crawled,shall be downloaded and converted to txt for indexing by using 
linux system calls

The 'searcher' files( the files with 'searcher' as a substring of the file names') are for parsing the query (from engine.php)
and search form the indexed directory(text_indexed_directory). The searacher files also give recommendations as of spell
checking and all that.


