import os,ast
from pymongo import MongoClient
client = MongoClient()
db = client.hw2
col = db.factbook

for a,b,c in os.walk('data'):
	for js in c:
		if '.json' in js:
			f = open(os.path.join(a,js),'r')
			fdb = ast.literal_eval(f.read())
			col.insert_one(fdb)
			f.close()
