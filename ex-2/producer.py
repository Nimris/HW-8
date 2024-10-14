import json
import pika
from model import Contact
from mongoengine import connect
import faker

connect(host=f"mongodb+srv://stanislavv371:oO5U8eBiLlWZwRU3@cluster-hw8.aih4m.mongodb.net/?retryWrites=true&w=majority", ssl=True)

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials, heartbeat=60, blocked_connection_timeout=300))
channel = connection.channel()

channel.exchange_declare(exchange='email_sender', exchange_type='direct')
channel.queue_declare(queue='m_queue', durable=True)
channel.queue_bind(exchange='email_sender', queue='m_queue')


def main():
    for i in range(1):
        contact = Contact(name=f"Contact {i + 1}", email=f"{faker.Faker().email()}", is_sent=False, adress=f"{faker.Faker().address()}")
        contact.save()
    
    for contact in Contact.objects(is_sent=False):
        if contact.is_sent:
            continue
        message = {"contact_id": str(contact.id)}
        
        channel.basic_publish(
            exchange='email_sender',
            routing_key='m_queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        print(f"[x] Sent {message}")
    connection.close()
    
if __name__ == '__main__':
    main()