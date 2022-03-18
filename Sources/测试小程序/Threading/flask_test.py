from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    a = 1
    b = 2
    c = a + b
    return str(c) + ' Hello world!'
 
if __name__ == '__main__':
    app.run(debug = True)