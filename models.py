from app import db

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, default=0)




class User(db.Model):
    __tablename__ = 'users'
    id_email = db.Column(db.String, primary_key=True)
    user_data = db.relationship("UserData", back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserData(db.Model):
    __tablename__ = 'user_data'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String, db.ForeignKey('users.id_email'), nullable=False, unique=True)

    purpose = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    level = db.Column(db.String(50))
    frequency = db.Column(db.Integer)
    trauma = db.Column(db.String(255))
    muscles = db.Column(db.String(255))
    age = db.Column(db.Integer)

    user = db.relationship("User", back_populates="user_data")
