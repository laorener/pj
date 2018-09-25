from flask import Flask
import config
from apps.cms.urls import bp as cms_bp
from apps.front.urls import bp as front_bp
from exts import db,mail
from flask_wtf import CSRFProtect
from flask_mail import Message

app = Flask(__name__)
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)

# 加载配置文件
app.config.from_object(config)
CSRFProtect(app=app)
db.init_app(app)
mail.init_app(app)

if __name__ == '__main__':
    app.run()






