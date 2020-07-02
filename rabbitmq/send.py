import pika 

## connect to a broker on the local machine
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

## check if a queue exists or not, create one if not there
channel.queue_declare(queue='hello')

## go through exchange to send msg to queue
channel.basic_publish(exchange='',
					  ## specify queue name
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
