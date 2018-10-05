from exts import db
class Banner(db.Model):
    __tablename__ ='banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bannerName = db.Column(db.String(20), nullable=False)
    imglink = db.Column(db.String(200), nullable=False, unique=True)
    link = db.Column(db.String(200), nullable=False, unique=True)
    priority = db.Column(db.Integer, default=1)