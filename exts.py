"""第三方的初始化"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # 为来防止循环导入