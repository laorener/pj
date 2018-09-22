# 进行表单校验
from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField
from wtforms.validators import Email,InputRequired,Length

class BaseForm(FlaskForm):
    @property    # 把函数变成了属性来调用
    def err(self):
        return self.errors.popitem()[1][0]


class UserForm(BaseForm):
    email = StringField(validators=[Email(message="必须为邮箱"),InputRequired(message="不能为空")])
    password = StringField(validators=[InputRequired(message="必须输入密码"),Length(min=6,max=40,message="密码长度是6-40位")])