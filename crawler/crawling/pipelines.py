# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime
#from scrapy.exceptions import LinkItem
from crawling.items import RawResponseItem

from elasticsearch import Elasticsearch
import os
import re
import hashlib
from simhash import Simhash
from scrapy import log
class KafkaPipeline(object):
    def get_features(self,s):
	width = 3
	s = s.lower()
	s = re.sub(r'[^\w]+', '', s)
	return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]
    def process_item(self,item,spider):
	m = hashlib.md5()
	m.update(item['url'])
	url_MD5 = m.hexdigest()
	content_simhash = Simhash(self.get_features(item['content'])).value
	language = 'en'
	query_json='{"fields":["url_MD5","content_simhash"],"query":{"filtered":{"filter":{"term":{"url_MD5":"'+url_MD5+'"}}}}}'
	es = Elasticsearch(host='192.168.1.14',port=9200,timeout=1000)
	res = es.search(index="hiddenwebs", body=query_json)
	if res['hits']['total'] == 0:
		es.index(index="hiddenwebs", doc_type="hiddenwebpages",body={"url":item['url'],"content":item['content'],"create_time":item['create_time'],"domain_name":item['domain_name'],"url_MD5":url_MD5,"title":item['title'],"content_simhash":content_simhash,"language":language})	
	else:	
		flag = 0
		for hit in res['hits']['hits']:
			#print content_simhash
			#print hit["fields"]["content_simhash"][0]
			if int(hit["fields"]["content_simhash"][0]) == int(content_simhash):
				log.msg('The similar pages in es %s'%(item['url']),level=log.INFO)
				flag = 1
				es.index(index="hiddenwebs", doc_type="hiddenwebpages", id=hit['_id'], body={"create_time":item['create_time']})
				break
		if flag == 0 :
			es.index(index="hiddenwebs", doc_type="hiddenwebpages",body={"url":item['url'],"content":item['content'],"create_time":item['create_time'],"domain_name":item['domain_name'],"url_MD5":url_MD5,"title":item['title'],"content_simhash":content_simhash,"language":language})
