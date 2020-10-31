# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 21:51:56 2020

@author: Administrator
"""

#图书列表返回
#查询指定图书的信息（书名，价格，作者）
#新增一本书
#删除一本书
#更新书本的信息（涨价了）


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
api = Api(app)

books = {
    1:{
        'title': '论语',
        'auther': '孔子',
        'price': 18
    },
    2:{
        'title': '道德经',
        'auther': '老子',
        'price': 15
    },
    3:{
        'title': '三体',
        'auther': '刘慈欣',
        'price': 25
    }
}

def abort_if_todo_doesnt_exist(book_id):
    if book_id not in books:
        abort(404, message="book_id {} not exist".format(book_id))

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='need book title')
parser.add_argument('auther', type=str, required=True, help='need book auther')
parser.add_argument('price', type=int, required=True, help='need book price')

# single_book
# shows a single book and lets you modify or delete a book
class Book(Resource):
    def get(self, book_id):
        abort_if_todo_doesnt_exist(book_id)
        return {book_id:books[book_id]}

    def delete(self, book_id):
        abort_if_todo_doesnt_exist(book_id)
        del books[book_id]
        return 'delete success!', 204

    def put(self, book_id):
        args = parser.parse_args()
        book = {
            'title': args['title'],
            'auther': args['auther'],
            'price': args['price']
        }
        books[book_id] = book
        return {book_id:book}, 201

# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class Book_list(Resource):
    def get(self):
        return books

    def post(self):
        args = parser.parse_args()
        book_id = int(max(books.keys())) + 1
        books[book_id] = {
            'title': args['title'],
            'auther': args['auther'],
            'price': args['price']
        }
        return {book_id:books[book_id]}, 201

# Actually setup the Api resource routing here
api.add_resource(Book_list, '/books')
api.add_resource(Book, '/books/<int:book_id>')


if __name__ == '__main__':
    app.run(debug=True)
