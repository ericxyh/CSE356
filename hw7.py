import os, json
from elasticsearch import Elasticsearch
es = Elasticsearch()


a = open('movies.json')
b = json.load(a)
i=1
for c in b:
	res = es.index(index="hw7", id=i, body=c)
	print(res)
	i+=1
