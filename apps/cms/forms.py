# 进行表单校验
from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField
from wtforms.validators import Email,InputRequired,Length,EqualTo

class BaseForm(FlaskForm):
    @property    # 把函数变成了属性来调用
    def err(self):
        return self.errors.popitem()[1][0]


class UserForm(BaseForm):
    email = StringField(validators=[Email(message="必须为邮箱"),InputRequired(message="不能为空")])
    password = StringField(validators=[InputRequired(message="必须输入密码"),Length(min=6,max=40,message="密码长度是6-40位")])

class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[InputRequired(message='必须输入旧密码')])
    newpwd = StringField(validators=[InputRequired(message='必须输入新密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd", message='密码不一致')])

class ResetEmailSendCode(BaseForm):
    email = StringField(validators=[Email(message = '必须为邮箱'),InputRequired(message="不能为空")])

class ResetEmailForm(ResetEmailSendCode):
    emailCode = StringField(validators=[InputRequired(message='必须输入'),Length(min=6,max=6,message="验证码必须是6位")])