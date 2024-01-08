from extensions import db, app, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class BaseModel:
  def create(self):
    db.session.add(self)
    db.session.commit()
  
  def save(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()



class PostModel(db.Model, BaseModel):
  id = db.Column(db.Integer, primary_key=True)
  image = db.Column(db.String, nullable=False)
  title = db.Column(db.String(25), nullable=False)
  description = db.Column(db.String(75), nullable=False)
  date = db.Column(db.DateTime, default=datetime.utcnow())
  user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
  user = db.relationship('UserModel', backref='post', lazy=True)



class UserModel(db.Model, BaseModel, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(10), nullable=False)
  password = db.Column(db.String(20), nullable=False)
  birthDate = db.Column(db.DateTime(), default=datetime.utcnow())
  signUpDate = db.Column(db.DateTime(), default=datetime.utcnow())
  role = db.Column(db.String())

  def __init__(self, birthDate, signUpDate, username, password, role="guest"):
    self.username = username
    self.password = generate_password_hash(password)
    self.birthDate = birthDate
    self.signUpDate = signUpDate
    self.role = role

  def check_password(self, password):
    return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
  return UserModel.query.get(user_id)

class CommentModel(db.Model, BaseModel):
   id = db.Column(db.Integer, primary_key=True)
   comment = db.Column(db.String(50))
   date = db.Column(db.DateTime, default=datetime.utcnow())
   post_id = db.Column(db.Integer, db.ForeignKey('post_model.id'))
   post = db.relationship('PostModel', backref='comments')
   user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
   user = db.relationship('UserModel')



if __name__ == "__main__":
  with app.app_context():
    db.create_all()
    admin_user = UserModel(username="Admin_User", password="password123@2008", role="admin", signUpDate=None, birthDate=None)
    admin_user.create()
