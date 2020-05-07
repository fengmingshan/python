# -*- coding:utf-8 -*-
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static") # 挂载静态文件，指定目录


templates = Jinja2Templates(directory="templates") # 模板目录

@app.get("/data/{data}")
async def read_data(request: Request, data: str):
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)