# model
# 操作数据库使用sqlalchemy
    # 1.先创建数据库   bbs


from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    _password = db.Column(db.String(200),nullable=False) # 加密过的
    email = db.Column(db.String(30),unique=True,nullable=False)
    join_time = db.Column(db.DateTime,default=datetime.now)

    # 因为要特殊处理password
    def __init__(self,password,**kwargs):
        self.password = password
        kwargs.pop('password',None)
        super(User,self).__init__(**kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,frontpwd):
        # 1. 密码不希望外界访问 2.防止循环引用
        self._password = generate_password_hash(frontpwd)

    def checkPwd(self,frontpwd):
        #return self.password == generate_password_hash(frontpwd)
        return check_password_hash(self._password,frontpwd)