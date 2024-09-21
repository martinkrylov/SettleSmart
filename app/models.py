from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    condition = db.Column(db.String(100))
    city = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.now())
