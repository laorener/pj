# model
# 操作数据库使用sqlalchemy
    # 1.先创建数据库   bbs


from exts import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(30),unique=True,nullable=False)
    join_time = db.Column(db.DateTime,default=datetime.now)


