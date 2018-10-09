# 打开debug模式之后修改项目python代码不用重复启动
# 但是上线的时候必须要关掉
DEBUG=True

# 打开之后，模板修改了也不需要重启服务器
TEMPLATES_AUTO_RELOAD=True


# 数据库的配置项
# 数据库连接
DB_USERNAME='root'
DB_PASSWORD="root"
DB_HOST="127.0.0.1"
DB_PORT="3306"
DB_NAME="bbs"
DB_URL="mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI=DB_URL
SQLALCHEMY_COMMIT_ON_TEARDOWN=False # 设置是否在每次连接结束后自动提交数据库中的变动

SQLALCHEMY_POOL_SIZE = 10 #  数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）。
SQLALCHEMY_MAX_OVERFLOW = 5 # 控制在连接池达到最大值后可以创建的连接数。当这些额外的连接使用后回收到连接池后将会被断开和抛弃。保证连接池只有设置的大小；
SQLALCHEMY_POOL_TIMEOUT = 10 # 指定数据库连接池的超时时间。默认是 10。

# 下面两项调试阶段启动，部署时关闭
SQLALCHEMY_TRACK_MODIFICATIONS=False  #如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存，如果不必要的可以禁用它。
SQLALCHEMY_ECHO=True #如果设置成 True，SQLAlchemy 将会记录所有发到标准输出(stderr)的语句，这对调试很有帮助;默认为false；

#session
SECRET_KEY = 'abc'
REMBERME = 'remberme'
LOGIN = 'login'
CURRENT_USER_ID='user_id'
CURRENT_USER = "current_user"
FRONT_USER_ID = "front_user_id"
# flask-mail
MAIL_SERVER = 'smtp.qq.com'
MAIL_PROT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "995304793@qq.com"
MAIL_PASSWORD = "aklwmontjyqubcjd"  # 不是登录
MAIL_DEFAULT_SENDER='995304793@qq.com' # 默认的发件人

#MAIL_USE_TLS 端口号 587
#MAIL_USE_SSL 端口号 467
# QQ邮箱不支持非加密方式发送邮件

# 富文本编辑器上传七牛云
import os

UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'images')

UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "gixRZTC9nnM_ODSEyAmDtFPVBD5sBWJo1dsfszvB"
UEDITOR_QINIU_SECRET_KEY = "X8TYRWzELi-hfyzl1MeAkEbS9i5DKL_8qI4m_o3l"
UEDITOR_QINIU_BUCKET_NAME = "pjbbs"
UEDITOR_QINIU_DOMAIN = "peouv6xac.bkt.clouddn.com"

#celery
BROKER_URL = 'redis://127.0.0.1:6379/1'  # 消息代理地址
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1' #任务结果存放地址
CELERY_TASK_SERIALIZER = 'json' #任务序列化与反序列化方案
CELERY_RESULT_SERIALIZER = 'json' #读取任务结果
CELERY_TASK_RESULT_EXPIRES = 24 * 60 * 60 # 任务过期时间
CELERY_ACCEPT_CONTENT = ['json'] # 指定接受的内容类型

