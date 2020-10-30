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

from flask import Flask, jsonify, abort, request
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

books = [
    {
        'id': 1,
        'title': '论语',
        'auther': '孔子',
        'price': 18
    },
    {
        'id': 2,
        'title': '道德经',
        'auther': '老子',
        'price': 15
    },
    {
        'id': 3,
        'title': '三体',
        'auther': '刘慈欣',
        'price': 25
    }
]

# 查询全部图书
@app.route('/api/books/', methods=['GET'])
def get_tasks():
    return jsonify({'books': books})

# 按id查询图书
@app.route('/api/books/<int:bookid>', methods=['GET'])
def get_task(bookid):
    for book in books:
        if book['id']==bookid:
            return jsonify({'book': book})
    abort(404)

@app.route('/api/books/', methods=['POST'])
def create_task():
    if not request.form or not 'title' in request.form:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'title': request.form['title'],
        'auther': request.form['auther'],
        'price': int(request.form['price']),
    }
    books.append(book)
    return jsonify({'book': book}), 201

@app.route('/api/books/<int:bookid>', methods=['PUT'])
def update_book(bookid):
    for book in books:
        if book['id']==bookid:
            book["title"] = request.form['title']
            book["auther"] = request.form['auther']
            book["price"] = int(request.form['price'])
        return jsonify({'books': books})
    abort(400)

@app.route('/api/books/<int:bookid>', methods=['DELETE'])
def delete_task(bookid):
    for book in books:
        if book['id']==bookid:
            books.remove(book)
            return jsonify({'result': True})
    abort(404)

    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)