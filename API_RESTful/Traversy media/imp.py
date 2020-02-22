import csv
from api import *
import os

path = os.path.dirname(__file__)
print(path)

with open(path+'/input.csv') as books_input:
    csv_reader = csv.reader(books_input, delimiter=',')
    for isbn, title, author, year in csv_reader:
        # print(f"Types : {type(isbn), type(title), type(author), type(year)}")
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        print("{} by {} from {} added into the database.".format(title, author, year))
    db.session.commit()