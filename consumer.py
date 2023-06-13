
import pika
from mongoengine import BooleanField, Document, StringField, connect

# Підключення до бази даних
connect(db='my_test',
        username='kara89',
        password='321321',
        host='mongodb+srv://kara89:321321@cluster0.9wjid2s.mongodb.net/',
        port=27017,
        authentication_source='admin')

# Визначення моделі для контакту


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)

# Функція-заглушка для надсилання повідомлення по email


def send_email(contact):
    # Реалізуйте код для надсилання повідомлення по email
    print(f"Email sent to Contact: {contact.full_name}")
    contact.sent = True
    contact.save()

# Отримання повідомлення з черги


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()
    if contact:
        send_email(contact)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Очікування повідомлень з черги


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')
    channel.basic_consume(queue='email_queue',
                          on_message_callback=callback, auto_ack=False)
    print('Consumer started. Waiting for messages...')
    channel.start_consuming()


if __name__ == '__main__':
    main()
