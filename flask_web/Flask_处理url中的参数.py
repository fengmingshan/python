# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 19:07:55 2020

@author: Administrator
"""

# curl -i "localhost:5000/api/foo?a=hello&b=world"


from flask import Flask, request

app = Flask(__name__)

@app.route('/api/foo/', methods=['GET','POST'])
def foo():
    bar = request.args.to_dict()
    return str(bar)

if __name__ == '__main__':
    app.run(debug=True)