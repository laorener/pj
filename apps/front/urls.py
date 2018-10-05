# 前台
from flask import Blueprint,request,make_response
from flask import render_template
from flask.views import MethodView
from apps.front.forms import SendSmsCodeForm,SignupFrom,SigninForm
import string
import random
from dysms_python.demo_sms_send import send_sms
from flask import jsonify
from apps.common.baseResp import *
import json
from apps.common.captcha.xtcaptcha import Captcha
from apps.common.memcachedUtil import saveCache,delete
from io import BytesIO
from apps.front.models import FrontUser
from exts import db


#
bp = Blueprint('front',__name__)

@bp.route("/")
def loginView():
    return render_template("front/index.html")

class Signup(MethodView):
    def get(self):
        # 从那个页面点击的注册按钮  (Referer: http://127.0.0.1:9000/signin/)
        location = request.headers.get("Referer")
        if not location:  # 如果直接输入的注册的连接，location为空
            location = '/'
        context = {
            'location': location
        }
        return render_template("front/signup.html", **context)
    def post(self):
        fm = SignupFrom(formdata=request.form)
        if fm.validate():
            # 把这个用户保存到数据库中
            u = FrontUser(telephone=fm.telephone.data,
                          username=fm.username.data,
                          password=fm.password.data)
            db.session.add(u)
            db.session.commit()
            delete(fm.telephone.data)  # 注册成功，删除手机验证码
            return jsonify(respSuccess("注册成功，真不容易啊"))
        else:
            return jsonify(respParamErr(fm.err))

@bp.route("/send_sms_code/",methods = ['post'])
def sendSMSCode():
    fm = SendSmsCodeForm(formdata=request.form)
    if fm.validate():
        source = string.digits
        source = ''.join(random.sample(source,4))
        r = send_sms(phone_numbers=fm.telephone.data,smscode=source)
        if json.loads(r.decode("utf-8"))['Code'] == 'OK':
            print(json.loads(r.decode("utf-8"))['Code'])
            saveCache(fm.telephone.data,source,30*60)
            return jsonify(respSuccess("短信验证码发送成功，请查收"))
        else:  # 发送失败
            return jsonify(respParamErr("请检查网络"))
    else:
        return jsonify(respParamErr(fm.err))
@bp.route("/img_code/")
def ImgCode():
    text, img = Captcha.gene_code()  # 通过工具类生成验证码
    print(text)
    out = BytesIO()  # 初始化流对象
    img.save(out, 'png')  # 保存成png格式
    out.seek(0)  # 从文本的开头开始读
    saveCache(text, text, 60)
    resp = make_response(out.read())  # 根据流对象生成一个响应
    resp.content_type = "image/png"  # 设置响应头中content-type
    return resp

class Signin(MethodView):
    def get(self):
        return render_template("front/signin.html")
    def post(self):
        fm = SigninForm(formdata=request.form)
        if fm.validate():
            user = FrontUser.query.filter(FrontUser.telephone == fm.telephone.data).first()
            r = user.checkPwd(fm.password.data)
            if r:
                return jsonify(respSuccess("登录成功"))
            else:
                return jsonify(respParamErr("密码错误"))
        else:
            return jsonify(respParamErr(fm.err))

bp.add_url_rule("/signup/",endpoint='signup',view_func=Signup.as_view('signup'))
bp.add_url_rule("/signin/",endpoint='signin',view_func=Signin.as_view('signin'))