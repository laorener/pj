from exts import db
import datetime # 模块
from apps.front.models import  *

class Banner(db.Model):
    __tablename__ ='banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bannerName = db.Column(db.String(20), nullable=False)
    imglink = db.Column(db.String(200), nullable=False, unique=True)
    link = db.Column(db.String(200), nullable=False, unique=True)
    priority = db.Column(db.Integer, default=1)

class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    boardname = db.Column(db.String(20),nullable=False)
    postnum = db.Column(db.String(200),nullable=False,default=0)
    create_time =db.Column(db.DateTime,default=datetime.datetime.now)

class Post(db.Model) :
    __tablename__ = "common_post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship('Board', backref='posts')
    # 前台用户id使用的short_uuid, 类型和长度，约束必须一直
    user_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), default=shortuuid.uuid)
    user = db.relationship('FrontUser', backref='posts') # orm查询的时候使用