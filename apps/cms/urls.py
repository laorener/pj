# 后台
from flask import Blueprint
from flask import render_template
from apps.cms.forms import UserForm
from flask import request,jsonify
from apps.common.baseResp import *
from exts import db
from apps.cms.models import *

bp = Blueprint('cms',__name__,url_prefix="/cms")

@bp.route("/")
def loginView():
    return render_template("cms/login.html")

@bp.route('/login/',methods = ['post'])
def login():
    fm = UserForm(formdata=request.form)
    if fm.validate():
        email = fm.email.data
        pwd = fm.password.data
        user = User.query.filter(User.email == email).first()
        if not user :
            return jsonify(respParamErr('用户名不对'))
        if user.password == pwd :
            return jsonify(respSuccess('登陆成功'))
        else:
            return jsonify(respParamErr("密码错误"))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.route('/index/')
def cms_index():
    return render_template('cms/cms_index.html')