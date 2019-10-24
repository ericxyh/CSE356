from flask import Flask, request, render_template, jsonify, make_response
import time, random, smtplib
from flask.ext.cqlalchemy import CQLAlchemy

app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
app.config['CASSANDRA_KEYSPACE'] = "hw6"
db = CQLAlchemy(app)

@app.route('/deposit', methods = ['POST'])
def dep():
	fname = request.form.to_dict()['filename']
	f = request.files.to_dict()['contents']
	print(request.form.to_dict())
	print('b')
	print(request.files.to_dict())
	print('c')
	return jsonify(status='ok')

@app.route('/retrieve', methods = ['GET'])
def ret():
	fname = request.args.to_dict()['filename']
	print(request.args.to_dict())
	return jsonify(status='ok')

if __name__ == "__main__":
#	app.debug = True
	app.run(host='0.0.0.0',port=80)
