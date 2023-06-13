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


# Підключаємося до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створюємо чергу
channel.queue_declare(queue='email_queue')

# Генерація фейкових контактів та запис до бази даних


def generate_contacts(num_contacts):
    contacts = []
    for i in range(num_contacts):
        contact = Contact(
            full_name=f"Contact {i+1}",
            email=f"contact{i+1}@example.com",
            sent=False
        )
        contact.save()
        contacts.append(contact)
    return contacts

# Відправка повідомлення до черги RabbitMQ


def send_message(contact):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')
    message = str(contact.id)
    channel.basic_publish(exchange='', routing_key='email_queue', body=message)
    print(f"Message sent for Contact: {contact.full_name}")
    connection.close()

# Генерація контактів та відправка повідомлень до черги


def main():
    num_contacts = 10
    contacts = generate_contacts(num_contacts)
    for contact in contacts:
        send_message(contact)


if __name__ == '__main__':
    main()
