import json
from random import choice
import pika
from model import Contact
from mongoengine import connect
import faker

connect(host=f"mongodb+srv://stanislavv371:oO5U8eBiLlWZwRU3@cluster-hw8.aih4m.mongodb.net/?retryWrites=true&w=majority", ssl=True)

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials, heartbeat=60, blocked_connection_timeout=300))
channel = connection.channel()

channel.exchange_declare(exchange='m_sender', exchange_type='direct')

channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange='m_sender', queue='email_queue')

channel.queue_declare(queue='sms_queue', durable=True)
channel.queue_bind(exchange='m_sender', queue='sms_queue')


faker = faker.Faker()

def main():
    for i in range(1):
        contact = Contact(
            name=f"Contact {i + 1}", 
            email=f"{faker.email()}", 
            is_sent=False, 
            adress=f"{faker.address()}", 
            phone=f"{faker.phone_number()}", 
            sending_method=choice(["email", "sms"]))
        contact.save()
    
    for contact in Contact.objects(is_sent=False):
        message = {"contact_id": str(contact.id)}
        
        if contact.sending_method == "email":
            routing_key = 'email_queue'
            print(f"[x] Sent by email: {message}")
        else:
            routing_key = 'sms_queue'
            print(f"[x] Sent by sms: {message}")
        
        channel.basic_publish(
            exchange='m_sender',
            routing_key=routing_key,
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
                        
    connection.close()
    
    
if __name__ == '__main__':
    main()