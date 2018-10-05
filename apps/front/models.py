from exts import db
import  shortuuid
import datetime
from enum import Enum
from werkzeug.security import generate_password_hash,check_password_hash

class GenderEnum(Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4

class FrontUser(db.Model):
    __tablename__ = "front_user"
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))  # 头像
    signature = db.Column(db.String(100))  # 签名
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime, default=datetime.datetime.now)

    # 因为要特殊处理password
    def __init__(self, password, **kwargs):
        self.password = password
        kwargs.pop('password', None)
        super(FrontUser, self).__init__(**kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, frontpwd):
        # 1. 密码不希望外界访问 2.防止循环引用
        self._password = generate_password_hash(frontpwd)

    def checkPwd(self, frontpwd):
        # return self.password == generate_password_hash(frontpwd)
        return check_password_hash(self._password, frontpwd)