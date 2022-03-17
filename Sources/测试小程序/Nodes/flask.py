from flask import Flask

app = Flask(__name__)

@app.route('/')  #映射根目录
def hello_world():
    return 'Hello World!'  #返回网页信息

if __name__ == '__main__':
    app.run()