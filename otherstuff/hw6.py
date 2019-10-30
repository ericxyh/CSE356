from flask import Flask, request, render_template, jsonify, make_response, send_file
import time, random, smtplib
from flask_cqlalchemy import CQLAlchemy

app = Flask(__name__)

@app.route('/deposit', methods = ['POST'])
def dep():
	fname = request.form.to_dict()['filename']
	f = request.files.to_dict()['contents']
	f.save('/home/ubuntu/fakecass/'+fname)
	return jsonify(status='ok')

@app.route('/retrieve', methods = ['GET'])
def ret():
	fname = request.args.to_dict()['filename']
	res = make_response(send_file('/home/ubuntu/fakecass/'+fname))
	return res

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0',port=80)
