from flask import Flask
# from flask import jsonify, abort, make_response   # for error handling
# from flask import request               # for POST method
# from flask import url_for               # to swap the task id for an URI
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# 1:n relationship - Many reviews can share 1 book (1 book can have many reviews, but a review can only have 1 book)
class Book(db.Model):
    #__tablename__= 'books'
    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    review = db.relationship('Review', backref='book_isbn', lazy=True)

class Review(db.Model):
    #__tablename__= 'reviews'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rating = db.Column(db.Integer, nullable = False)  # 1 to 5?
    text = db.Column(db.Text, nullable = False)
    book_isbn = db.Column(db.Integer, db.ForeignKey('Book.isbn'), nullable=False)