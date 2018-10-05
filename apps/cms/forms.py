# 进行表单校验
from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField
from wtforms.validators import Email,InputRequired,Length,EqualTo,URL
from wtforms.validators import ValidationError
from apps.cms.models import  User
from flask import jsonify
from apps.common.baseResp import  respParamErr
from apps.common.memcachedUtil import  getCache
from apps.common.models import Banner

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
    #校验邮箱
    def validate_email(self,filed):
        print("校验邮箱")
        user = User.query.filter(User.email == filed.data).first()
        if user:
            return jsonify(respParamErr(msg="邮箱已注册"))

class ResetEmailForm(ResetEmailSendCode):
    emailCode = StringField(validators=[InputRequired(message='必须输入'),Length(min=6,max=6,message="验证码必须是6位")])
    def validate_emailCode(self,filed):
        emailcode = getCache(filed.data)
        if not emailcode or emailcode != filed.data.upper():
            return jsonify(respParamErr(msg="验证码错误"))

class BannerForm(BaseForm):
    bannerName = StringField(validators=[InputRequired(message="不能为空")])
    imglink = StringField(validators=[InputRequired(message="不能为空"),URL(message="必须是一个url地址")])
    link = StringField(validators=[InputRequired(message="不能为空"),URL(message="必须是一个url地址")])
    priority = IntegerField(validators=[InputRequired(message='必须输入优先级')])

    def validate_imglink(self,filed):
        r = Banner.query.filter(Banner.imglink == filed.data).first()
        if r :
            raise ValidationError('图片的url已存在，请勿重复添加 ' + str(r.id) + r.bannerName)

    def validate_link(self, filed):
        r = Banner.query.filter(Banner.link == filed.data).first()
        if r:
            raise ValidationError('内容的url已存在，请勿重复添加 ' + str(r.id) + r.bannerName)

class BannerUpdate(BannerForm):
    id = IntegerField(validators=[InputRequired(message="请传入id")])
    def validate_imglink(self, filed):
        pass
    def validate_link(self, filed):
        pass