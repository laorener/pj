# 后台
from flask import Blueprint
from flask.views import  MethodView
from flask import render_template,session
from apps.cms.forms import UserForm,ResetPwdForm,ResetEmailForm,ResetEmailSendCode
from flask import request,jsonify
from apps.common.baseResp import *
from exts import db,mail
from flask_mail import Message
from apps.cms.models import *
from config import REMBERME,LOGIN,CURRENT_USER_ID,CURRENT_USER
import string
import random
from apps.common.memcachedUtil import saveCache,getCache

bp = Blueprint('cms',__name__,url_prefix="/cms")

@bp.route("/")
def loginView():
    return render_template("cms/login.html")

@bp.route('/login/',methods=['post'])
def login():
    fm = UserForm(formdata=request.form)
    if fm.validate():
        email = fm.email.data # name=email的值
        pwd = fm.password.data
        user = User.query.filter(User.email == email).first()
        if not user : # 没有查询到用户
            return jsonify(respParamErr('用户名不对'))
        #if user.password == pwd : # 登陆成功
        if user.checkPwd(pwd):
            remberme = request.values.get("remberme")
            session[REMBERME] = LOGIN
            session[CURRENT_USER_ID] = user.id
            print(remberme)
            if remberme == '1':
                session.permanent=True
            return jsonify(respSuccess('登陆成功'))
        else: # 密码错误
            return jsonify(respParamErr("密码错误"))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.route('/index/')
def cms_index():
    login = session.get(REMBERME)
    if login ==LOGIN:
        return render_template('cms/cms_index.html')
    else:
        return render_template('cms/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return render_template("cms/login.html")

@bp.route("/user_infor/")
def user_infor():
    return render_template("cms/userInfo.html")

class ResetPwd(MethodView):
    def get(self):
        return render_template('cms/resetpwd.html')
    def post(self):
        fm = ResetPwdForm(formdata=request.form)
        if fm.validate():
            userid = session[CURRENT_USER_ID]
            user = User.query.get(userid)
            r = user.checkPwd(fm.oldpwd.data)
            if r:  # 旧密码是对
                user.password = fm.newpwd.data
                db.session.commit()
                return jsonify(respSuccess(msg='修改成功'))
            else:
                return jsonify(respParamErr(msg='修改失败,旧密码错误'))
        else:
            return jsonify(respParamErr(msg=fm.err))
bp.add_url_rule('/resetpwd/',endpoint='resetpwd',view_func=ResetPwd.as_view('resetpwd'))

class ResetEmail(MethodView):
    def get(self):
        return render_template('cms/resetemail.html')
    def post(self):
        fm = ResetEmailForm(formdata=request.form)
        if fm.validate():
            user = User.query.filter(User.email == fm.email.data).first()
            if user:
                return jsonify(respParamErr(msg="邮箱已注册"))
            emailcode = getCache(fm.email.data)
            if not emailcode or emailcode != fm.emailCode.data.upper():
                return jsonify(respParamErr(msg='请输入正确的邮箱验证码'))
            # 修改邮箱
            user = User.query.get(session[CURRENT_USER_ID])
            user.email = fm.email.data
            db.session.commit()
            return jsonify(respSuccess(msg='修改邮箱成功'))
        else:
            return jsonify(respParamErr(msg=fm.err))
bp.add_url_rule("/resetemail/",endpoint='resetemail',view_func=ResetEmail.as_view('resetemail'))

@bp.route("/send_email_code/",methods = ['post'])
def sendEmailCode():
    fm = ResetEmailSendCode(formdata=request.form)
    if fm.validate():
        user = User.query.filter(User.email == fm.email.data).first()
        if user:
            return jsonify(respParamErr(msg='邮箱已注册'))
        else:  # 发送邮件
            r = string.ascii_letters+string.digits
            r = ''.join(random.sample(r,6))
            saveCache(fm.email.data,r.upper(),30*60)
            msg = Message("我的邮箱验证码",recipients=[fm.email.data], body="验证码为" + r)
            mail.send(msg)
            return jsonify(respSuccess(msg="发送成功,请查看邮箱"))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.context_processor
def requestUser():
    login = session.get(REMBERME)
    if login == LOGIN:
        userid = session[CURRENT_USER_ID]
        user = User.query.get(userid)
        return {'user':user}
    return {}