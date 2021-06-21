from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

books = {"Witcher": {"bookId": "1", "author": "Sapkowski", "name": "Witcher"},
            "LOTR": {"bookId": "2", "author": "Tolkien", "name": "LOTR"} }

# parser = reqparse.RequestParser()
# parser.add_argument("bookId", type=int, help='Insert integer.', location = 'args')

class Book(Resource):
    
    def get(self, bookId):

        return(books[bookId])

api.add_resource(Book, "/books/<int:bookId>")




if __name__ == '__main__':
    app.run(debug=True)