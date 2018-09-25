# flask_script 使用命令行管理项目
from flask_script import Manager
# flask_migrate 数据库迁移脚本
from flask_migrate import Migrate,MigrateCommand

from pjjk import app
from exts import db

from apps.cms.models import User

# flask-script的使用
manage = Manager(app)
# 要使用flask-migrate必须绑定app和db
Migrate(app,db)
# 把MigrateCommand(数据库迁移)命令添加到manager
manage.add_command("db",MigrateCommand)

@manage.option('-e','--email',dest='email')
@manage.option('-u','--username',dest='username')
@manage.option('-p','--password',dest='password')
def addcmsuser(email,username,password):
    user = User(email=email,username=username,password=password)
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manage.run()


