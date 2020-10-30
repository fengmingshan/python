# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 23:13:32 2020

@author: Administrator
"""

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()
engine_item = create_engine("mysql+pymysql://root:a123456@localhost:3306/item?charset=utf8",
                            pool_recycle=7200)
Session_item = sessionmaker(autocommit=False, autoflush=True, bind=engine_item)
session_item = Session_item()


@app.get("/items/{item_id}")
def read_item(item_id: int, name: str = None):
    item_data = session_item.execute(
        'SELECT `item_id`,`name` FROM items where `item_id` = {item_id}'.format(
            item_id=item_id))
    item_data = list(item_data)
    item_id = [x.item_id for x in item_data][0]
    name = [x.name for x in item_data][0]
    return {"item_id": item_id, "name": name}


@app.put("/put/{item}")
def update_item(item_id: int, name: str):
    session_item.execute(
        "INSERT INTO  items(`item_id`, `name`) VALUES ({item_id},'{name}')".format(
            item_id=item_id, name=name))
    session_item.commit()
    return {"item_id": item_id, "name": name}
