from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from  datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(255), primary_key=True, default=str(uuid4()))
    username = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    password = db.Column(db.Text(), nullable = False)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_user_by_id(self, id):
        return User.query.get(id)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


    def save(    
        self
    ):
        db.session.add(self)
        db.session.commit()

    def delete(
        self
    ):
        db.session.delete(self)
        db.session.commit()


class TokenBlockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"<TokenBlockList {self.jti}>"

    def save(
        self
    ):
        db.session.add(self)
        db.session.commit()