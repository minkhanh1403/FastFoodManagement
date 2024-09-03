import hashlib

from flask_login import current_user
from sqlalchemy import func

from app import db
from app.models import Category, Product, User, ReceiptDetails, Receipt, Comment, UserRoleEnum


def load_categories():
    return Category.query.all()


def count_user_in_register():
    return db.session.query(func.count(User.id)).all()



def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()



def get_user_by_id(user_id):
    return User.query.get(user_id)


def load_users_in_register():
    query = db.session.query(User.id, User.name, User.username)
    return query.all()





def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password, avatar=avatar)
    # if avatar:
    #     res=cloudinary.uploader.upload(avatar)
    #     print(res)
    #     u.avatar=res['secure_url']
    db.session.add(u)
    db.session.commit()


def create_employee(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password, avatar=avatar, user_role=UserRoleEnum.EMPLOYEE)
    # if avatar:
    #     res=cloudinary.uploader.upload(avatar)
    #     print(res)
    #     u.avatar=res['secure_url']
    db.session.add(u)
    db.session.commit()




if __name__ == '__main__':
    from app import app

    with app.app_context():

