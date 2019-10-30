import pika, hw4_speak

connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='hw4', exchange_type='direct')

res = channel.queue_declare(queue='', exclusive=True)
qn = res.method.queue

print('waiting')

def callback(ch, method, properties, body):
	hw4_speak.switchbuff(str(body))

def chbc_key(key):
	channel.queue_bind(
		exchange='direct_logs', queue=qn, routing_key=key)
	channel.basic_consume(
		queue=qn, on_message_callback=callback, auto_ack=True)

#chbc_key('ericxyh')

channel.start_consuming()
