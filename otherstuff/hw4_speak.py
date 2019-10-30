# Not finished

from flask import Flask, request,jsonify
import pika, hw4_listen

ip = ''

app = Flask(__name__)

@app.route('/listen', methods = ['GET','POST'])
def listen():
	k = request.get_json()['keys']
	global ip, count
	ip = request.remote_addr
	for a in k:
		print(a)
		hw4_listen.chbc_key(a)

@app.route('/speak', methods = ['GET','POST'])
def speak():
	k = request.get_json()['key']
	m = request.get_json()['msg']
	connection = pika.BlockingConnection(
        	pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.exchange_declare(exchange='hw4', exchange_type='direct')
	channel.basic_publish(
		exchange='hw4', routing_key = k, body = m)
	connection.close()
	return jsonify(msg=m)

def switchback(m):
	global ip
	requests.post(ip, data = jsonify(msg=m))

if __name__ == "__main__":
#       app.debug = True
	app.run(host='0.0.0.0',port=80)
	hw4_listen.chbc_key('ericzyh')
