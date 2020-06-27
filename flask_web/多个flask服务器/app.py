from flask import Flask
import time
app = Flask(__name__)

@app.route('/')
def mainsleep():
    time.sleep(15)
    return 'wake up!'

if __name__ == '__main__':
    app.run(port = 8001)
