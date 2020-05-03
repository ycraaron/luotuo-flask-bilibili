## 实现 api，并且演示 api的get post，以及他的request里的param， query ，body
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/name', methods=['GET', 'POST'])
def get_name():
    if request.method == 'POST':
        return 'luotuo from POST'
    else:
        return 'luotuo from GET'

@app.route('/fans')
def get_fans():
    return '100000'

## 用户资料endpoint
@app.route('/userProfile', methods=["GET","POST"])
def get_profile():
    if request.method == 'GET':
        name = request.args.get('name', '')
        print(name)
        if(name=='luotuo'):
            return dict(name='luotuo from GET', fans=100000)
        else:
            return dict(name='bushi luotuo from GET', fans=1000000)
    elif request.method =='POST':
        print(request.form)
        print(request.data)
        print(request.json)
        name = request.json.get('name')
        if(name=='luotuo'):
            return dict(name='luotuo from POST', fans=100000)
        else:
            return dict(name='bushi luotuo from POST', fans=1000000)
        return '1'

