import hashlib

from flask_login import current_user
from sqlalchemy import func

from app import db
from app.models import Category, Product, User, ReceiptDetails, Receipt, Comment, UserRoleEnum


def load_categories():
    return Category.query.all()

def load_comments(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id)).order_by(-Comment.id).all()


def load_products(kw=None, cate_id=None, page=None):
    products = Product.query

    if kw:
        products = products.filter(Product.name.contains(kw))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return products.slice(start, start + page_size)

    return products.all()


def count_product():
    return Product.query.count()

def get_product_by_id(id):
    return Product.query.get(id)


def count_user_in_register():
    return db.session.query(func.count(User.id)).all()

def get_comments_by_product(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id)).all()


def add_comment(product_id, content):
    c = Comment(product_id=product_id, content=content, user=current_user)
    db.session.add(c)
    db.session.commit()

    return c

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



