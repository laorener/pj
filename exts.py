"""第三方的初始化"""

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
db = SQLAlchemy() # 为来防止循环导入
mail = Mail()