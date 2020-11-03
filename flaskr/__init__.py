import os

from flask import Flask
from flask import request

## 数据库实例的创建
## 利用工厂模式去创建flask这个实例

## 下一期视频会讲crud操作

## https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
## 用sqlite不需要你去搭建另外的数据库服务器


## 工厂模式 是一个很常用的用于创建对象的设计模式

#基本的crud

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    from . import db
    db.init_app(app)

    def query_db(query, args=(), one=False):
        cur = db.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

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
    # R: Read 读取创建的user profile /GET
    # C: Create 创建一个user profile /POST
    # U: Update 更新创建的user profile /PUT
    # D: Delete 删除创建的user profile /DELETE
    @app.route('/userProfile', methods=["GET","POST","PUT","DELETE"])
    def userProfile():
        if request.method == 'GET':
            # name = request.args.get('name', '')
            uid = request.args.get('uid',7)
            # 3. 写sql
            query = "SELECT * FROM userProfile WHERE id = {}".format(uid)
            # 通过用户的id来查询用户资料
            result = query_db(query,one=True)
            # 1. 获取数据库连接
            # 2. 获取一个数据库的游标 cursor
            # 4. 执行sql
            # not robust at all !
            # 别学我！
            if result is None:
                return dict(message="user doesn't exist")
            else:
                username=result['username']
                fans=result['fans']
                print(result['username'])
                print(result['fans'])
                return dict(username=username,fans=fans)
            # 5. 处理从数据库里读取的数据
            # 6. 将数据返回给调用者
        elif request.method =='POST':
            # name
            # fans
            print(request.json)
            name = request.json.get('name')
            fans = request.json.get('fans')
            # 获取post body中的name和fans
            # 插入新的数据到数据库
            #1. 获取数据库连接
            connection = db.get_db()
            query = "INSERT INTO userProfile (username,fans) values('{}',{})".format(name,fans)
            print(query)
            #2. 执行
            try:
                cursor = connection.execute(query)
                # 3. DML data manipulate language 没关系
                # 当你对数据库的数据有改动的时候，需要commit，否则改动不会生效
                # execute的时候就回去数据库里执行这条sql，如果有错误，会报错
                connection.commit()
                print(cursor.lastrowid)
                # select * from userProfile where id =5
                return dict(success=True)
            except:
                return dict(success=False,message="username exist",errorCode=1)
        elif request.method == 'PUT':
            # update
            return '1'
        elif request.method =='DELETE':
            # delete
            uid=request.args.get('uid',1)
            connection = db.get_db()
            query = "delete from userProfile where id = {}".format(uid)
            connection.execute(query)
            connection.commit()
            return dict(success=True)
    return app