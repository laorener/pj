# 前台
from flask import Blueprint,make_response
from flask import render_template,session
from flask import views,request,jsonify
from apps.front.forms import SendSmsCodeForm,\
    SignupFrom,SigninForm,FindpwdFrom,\
    SendCodeForm,AddPostForm
import string,random
from apps.common.baseResp import *
import json
from dysms_python.demo_sms_send import send_sms
from apps.common.captcha.xtcaptcha import Captcha
from io import BytesIO
from apps.common.memcachedUtil import saveCache,delete
from apps.front.models import *
from apps.common.models import Banner,Board,Post,Common,Tag
from functools import wraps
from config import FRONT_USER_ID
from flask import redirect
from flask import url_for
import math
from flask_paginate import Pagination,get_page_parameter
from task import setphone
#
bp = Blueprint('front',__name__)

def lonigDecotor(func):
    """限制登录的装饰器"""
    @wraps(func)
    def inner(*args,**kwargs):
        if not session.get(FRONT_USER_ID,None): # 没有登陆
            return redirect(location=url_for("front.signin"))
        else:
            r = func(*args,**kwargs)
            return r
    return inner

class Page:
    countofpage = 10
    @property
    def page(self): # 一共有多少页
         count = Post.query.count()
         return   math.ceil(count / self.countofpage)
    currentpage = 0 #默认是第0页
    posts = None


@bp.route("/")
def index():
    banners = Banner.query.order_by(Banner.priority.desc()).limit(4)
    board = Board.query.all()
    board_id = request.args.get("boarder_id") # 可选参数

    # page = Page() # 封装分页的信息
    # currentpage = int(request.args.get("current_page")) # 获取到当前是第几页
    # if not currentpage or currentpage < 0 : # 如果没有传递页面。默认是第0页
    #     currentpage = 0
    # if currentpage >= page.page : # 如果最后一页数字还大
    #     currentpage = page.page-1 # 默认显示最后一页
    # begin = currentpage * page.countofpage
    # end = begin + page.countofpage
    # if board_id : # 存在
    #     posts = Post.query.filter(Post.board_id == board_id).slice(begin,end)
    # else:  # 不存在
    #     posts = Post.query.slice(begin,end)
    # page.posts = posts
    # page.currentpage = currentpage
    # flask分页插件
    # 当前页
    page = request.args.get(get_page_parameter(), type=int, default=1)
    begin = (page - 1) * 10
    end = begin + 10
    # 按照阅读阅读量进行排序
    readCount = request.args.get("readcount",None)
    jinghua = request.args.get("jinghua", None)
    if board_id:  # 存在
       if readCount :
           tup = (Post.readCount.desc(),Post.create_time.desc())
       else:
           tup = (Post.create_time.desc())
       posts = Post.query.filter(Post.board_id == board_id).order_by(tup).slice(begin,end)
       count = Post.query.filter(Post.board_id == board_id).count()
    else:  # 不存在
        if readCount:
            posts = Post.query.order_by(Post.readCount.desc(),Post.create_time.desc()).slice(begin, end)
        elif jinghua:
            posts = Post.query.outerjoin(Tag, Post.id == Tag.post_id ).order_by(Tag.create_time.desc()).slice(begin, end)
        else:
            posts = Post.query.order_by(Post.create_time.desc()).slice(begin, end)
            #Post.query.order_by(Post.tag.create_time.desc(),Post.create_time.des)
        count = Post.query.count()

    pagination = Pagination(bs_version=3,page=page, total=count)
    context = {
        'banners': banners,
        "boards":board,
        'posts':posts,
        #'page':page
        'pagination':pagination
    }
    return render_template("front/index.html",**context)

@bp.route('/logout/')
def logout():
    session.pop(FRONT_USER_ID)
    return redirect(url_for("front.index"))

class Signup(views.MethodView):
    def get(self):
        return render_template("front/signup.html")
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

@bp.route("/send_sms_code/",methods=["post"])
def send_sms_code():
    fm =SendSmsCodeForm(formdata=request.form)
    if fm.validate():
        rs = string.digits
        rs = ''.join(random.sample(rs, 4))
#         r = send_sms(phone_numbers=fm.telephone.data,
#                      smscode=rs)
#         print(json.loads(r.decode("utf-8"))['Code'])
# # b'{"Message":"OK","RequestId":"26F47853-F6CD-486A-B3F7-7DFDCE119713","BizId":"102523637951132428^0","Code":"OK"}'
#         if json.loads(r.decode("utf-8"))['Code'] == 'OK':
#             saveCache(fm.telephone.data,rs,30*60)
#             return jsonify(respSuccess(msg="短信验证码发送成功，请查收"))
#         else:  # 发送失败
#             return jsonify(respParamErr(msg="请检查网络"))
        data = fm.telephone.data
        setphone.delay(data,rs)
        saveCache(data, rs, 30 * 60)
        return jsonify(respSuccess(msg="短信验证码发送成功，请查收"))
    else:
        return jsonify(respParamErr(fm.err))

@bp.route("/img_code/")
def ImgCode():
    # 生成6位的字符串
    # 把这个字符串放在图片上
    #  用特殊字体
    #  添加横线
    #  添加噪点
    text, img = Captcha.gene_code()  # 通过工具类生成验证码
    print(text)
    out = BytesIO()  # 初始化流对象
    img.save(out, 'png')  # 保存成png格式
    out.seek(0)  # 从文本的开头开始读
    saveCache(text, text, 60)
    resp = make_response(out.read())  # 根据流对象生成一个响应
    resp.content_type = "image/png"  # 设置响应头中content-type
    return resp

class Signin(views.MethodView):
    def get(self):
        location = request.headers.get("Referer")
        if not location:  # 如果直接输入的注册的连接，location为空
            location = '/'
        context = {
            'location': location
        }
        return render_template("front/signin.html",**context)
    def post(self):
        fm = SigninForm(formdata=request.form)
        if fm.validate():
                rember = request.values.get("rember")
                if str(rember) == "1":  # 前端勾选了记住我
                    session.permanent = True  # 设置这个属性之后回去config访问过期天数，如果没有设置，默认是31天
                return jsonify(respSuccess(msg="登陆成功"))
        else:
            return jsonify(respParamErr(fm.err))

class FindPws(views.MethodView):
    def get(self):
        return render_template("front/findpwd.html")
    def post(self):
        fm = FindpwdFrom(formdata=request.form)
        if fm.validate():
            r = FrontUser.query.filter(FrontUser.telephone == fm.telephone.data).first()
            r.password = fm.password.data
            db.session.commit()
            return jsonify(respSuccess(msg="修改成功"))
        else:
            return jsonify(respParamErr(fm.err))
@bp.route("/sendcode/",methods=["post"])
def sendcode():
    fm =SendCodeForm(formdata=request.form)
    if fm.validate():
        rs = string.digits
        rs = ''.join(random.sample(rs,4))
        print(rs)
        data = fm.telephone.data
        setphone.delay(data,rs)
        saveCache(data, rs, 30 * 60)
        return jsonify(respSuccess(msg="短信验证码发送成功，请查收"))
    else:
        return jsonify(respParamErr(fm.err))


class Addpost(views.MethodView):
    decorators = [lonigDecotor]
    def get(self):
        # 查询所有的板块
        board = Board.query.all()
        context = {
            "boards": board
        }
        return render_template("front/addpost.html",**context)

    def post(self):
        fm = AddPostForm(formdata=request.form)
        if fm.validate() :
            # 存储到数据库中
            user_id = session[FRONT_USER_ID]
            post = Post(title=fm.title.data,content=fm.content.data,
                 board_id=fm.boarder_id.data,user_id=user_id)
            db.session.add(post)
            db.session.commit()
            return jsonify(respSuccess("发布成功"))
        else:
            print(respParamErr(fm.err))
            return jsonify(respParamErr(fm.err))


# 展示帖子的内容
@bp.route("/showpostdetail/")
def showpostdetail():
    # 根据帖子的id查找到帖子
    post_id = request.args.get("post_id")
    if not post_id :
        return render_template("/")
    post = Post.query.filter(Post.id==post_id).first()
    if not post :
        return render_template("/")
    post.readCount +=1
    db.session.commit()
    commons = Common.query.filter(Common.post_id == post_id).all()
    context = {
        'post':post,
        'commoms':commons
    }
    return render_template("front/postdetail.html",**context)

@bp.route("/addcommon/",methods=['post'])
def addCommon():
    # 判断用户有没有登录
    # 获取当前用户的id
    user_id = session.get(FRONT_USER_ID,None)
    if not user_id :
        return jsonify(respParamErr("请先登录"))
    # 获取帖子的id
    post_id = request.values.get("post_id")
    # 获取评论的内容
    content = request.values.get("content")
    if not content:
        return jsonify(respParamErr("贴子内容不能为空"))
    # 在数据库中插入
    commom = Common(content=content,post_id=post_id,user_id=user_id)
    db.session.add(commom)
    db.session.commit()
    return jsonify(respSuccess("评论成功"))


@bp.context_processor
def request_befor():
    front_user_id = session.get(FRONT_USER_ID,None)
    if front_user_id:
        user = FrontUser.query.filter(FrontUser.id == front_user_id).first()
        return {"user":user}
    else:
        return {}


bp.add_url_rule("/addpost/",endpoint='addpost',view_func=Addpost.as_view('addpost'))
bp.add_url_rule("/findpwd/",endpoint='findpwd',view_func=FindPws.as_view('findpwd'))
bp.add_url_rule("/signin/",endpoint='signin',view_func=Signin.as_view('signin'))
bp.add_url_rule("/signup/",endpoint='signup',view_func=Signup.as_view('signup'))








