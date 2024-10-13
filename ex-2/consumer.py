import pika
import time
from model import Contact
from mongoengine import connect


connect(host=f"mongodb+srv://stanislavv371:oO5U8eBiLlWZwRU3@cluster-hw8.aih4m.mongodb.net/?retryWrites=true&w=majority", ssl=True)

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='m_queue', durable=True)
print('[*] Waiting for messages. To exit press CTRL+C')

    
def sent_email(contact_email):
    time.sleep(1)
    print(f"Email sent to {contact_email}")

def callback(ch, method, properties, body):
    message = body
    print(f"[x] Received {message}")
    contact = Contact.objects.first()
    if contact:
        sent_email(contact.email)
        contact.update(is_sent=True)
    print(f"[x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='m_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
