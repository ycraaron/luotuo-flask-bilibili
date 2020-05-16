import os

from flask import Flask

## 数据库实例的创建
## 利用工厂模式去创建flask这个实例

## 下一期视频会讲crud操作

## https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
## 用sqlite不需要你去搭建另外的数据库服务器


## 工厂模式 是一个很常用的用于创建对象的设计模式

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    from . import db
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

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

    return app