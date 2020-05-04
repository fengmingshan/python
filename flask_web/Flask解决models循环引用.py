#1.分开models的目的：为了让代码更加方便的管理。
#2.如何解决循环引用：把db放在一个单独的文件中，切断循环引用的线条就可以了
#3.代码：
#app.py
    from flask import Flask
    from models import Article 
    from exts import db    
    import config
    
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    
    with app.app_context():
       db.create_all()
       
    @app.route('/')
    def hello_world():
       return 'index'
    
    if __name__ == '__main__':
       app.run(debug=True)

#models.py
    from exts import db
    class Article(db.Model):
       __tablename__='article'
       id=db.Column(db.Integer,primary_key=True,autoincrement=True)
       title=db.Column(db.String(100),nullable=False)

#exts.py
    from flask_sqlalchemy import SQLAlchemy
    db=SQLAlchemy()
