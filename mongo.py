import json

from mongoengine import (Document, ListField, ReferenceField, StringField,
                         connect)

# Підключення до хмарної бази даних MongoDB

connect(db='my_test',
        username='kara89',
        password='321321',
        host='mongodb+srv://kara89:321321@cluster0.9wjid2s.mongodb.net/',
        port=27017,
        authentication_source='admin')
# Модель автора


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

    def __str__(self):
        return self.fullname.encode('utf-8')

# Модель цитати


class Quote(Document):
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)
    tags = ListField(StringField())

    def __str__(self):
        return self.quote

# Завантаження авторів з файлу authors.json


def load_authors():
    with open('authors.json') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(
                fullname=author_data['fullname'],
                born_date=author_data['born_date'],
                born_location=author_data['born_location'],
                description=author_data['description']
            )
            author.save()

# Завантаження цитат з файлу quotes.json


def load_quotes():
    with open('quotes.json') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            author = Author.objects(fullname=author_name).first()
            if author:
                quote = Quote(
                    tags=quote_data['tags'],
                    author=author,
                    quote=quote_data['quote']
                )
                quote.save()

# Функція для пошуку цитат за тегом, ім'ям автора або набором тегів



def search_quotes(query):
    command, value = query.split(':', 1)
    value = value.strip()

    if command == 'name':
        author = Author.objects(fullname=value).first()
        if author:
            quotes = Quote.objects(author=author)
            return [quote for quote in quotes]

    elif command == 'tag':
        quotes = Quote.objects(tags__in=[value])
        return [quote for quote in quotes]

    elif command == 'tags':
        tags = value.split(',')
        quotes = Quote.objects(tags__in=tags)
        return [quote for quote in quotes]
    return []
# Основний цикл для виконання команд


def main():
    while True:
        query = input(
            "Введіть команду (наприклад, name: Steve Martin, tag:life, tags:life,live,  exit):")
        if query.startswith('exit'):
            break

        quotes = search_quotes(query)
        for quote in quotes:
            print(quote)
  

if __name__ == '__main__':
    load_authors()
    load_quotes()

    main()
