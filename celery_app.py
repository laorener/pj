from flask import Flask
from celery import Celery
import config
from exts import mail
from flask_mail import Message

app = Flask(__name__)
app.config.from_object(config)
celery_server = Celery(__name__,include=['task'])
celery_server.config_from_object(config)
mail.init_app(app)

if __name__ == '__main__':
    app.run(port=9000)

