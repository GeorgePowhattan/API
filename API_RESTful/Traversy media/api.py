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
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    review = db.relationship('Review', backref='reviews', lazy=True)   # this is not a columns! Only running addtional querry in the background
    def __repr__(self):
        return f"Book('{self.isbn}','{self.title}','{self.author}','{self.year}')"

class Review(db.Model):
    #__tablename__= 'reviews'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rating = db.Column(db.Integer, nullable = False)  # 1 to 5?
    text = db.Column(db.Text, nullable = False)
    book_isbn = db.Column(db.String, db.ForeignKey('book.isbn'), nullable=False)
    def __repr__(self):
        return f"Review('{self.id}','{self.rating}','{self.text}','{self.book_isbn}')"
