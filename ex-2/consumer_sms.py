import json
import pika
from model import Contact
from mongoengine import connect


connect(host=f"mongodb+srv://stanislavv371:oO5U8eBiLlWZwRU3@cluster-hw8.aih4m.mongodb.net/?retryWrites=true&w=majority", ssl=True)

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='sms_queue', durable=True)
print('[*] Waiting for messages. To exit press CTRL+C')

    
def send_sms(contact_phone):
    print(f"Sms sent to {contact_phone}")
    
    
def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode())
        print(f"[x] Received: {message}")

        contact_id = message.get("contact_id") or message.get("id")
        if not contact_id:
            print("[!] No contact ID in message")
            return

        contact = Contact.objects(id=contact_id).first()
        if contact:
            send_sms(contact.phone)
            contact.update(is_sent=True)
        else:
            print("[!] Contact not found")

    except json.JSONDecodeError:
        print("[!] Failed to decode message")
    except Exception as e:
        print(f"[!] Error: {e}")
        
        
    print(f"[x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='sms_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
