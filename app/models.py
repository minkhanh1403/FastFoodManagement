import enum
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship

from app import db


class UserRoleEnum(enum.Enum): #xoa emp
    USER = 1
    ADMIN = 2



class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin): #them addres
    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ = 'category'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(BaseModel):#menu items
    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(500))
    quantity = Column(Integer,nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    status = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


if __name__ == '__main__':
    from app import app

    with app.app_context():
        db.create_all()

        # Category
        c1 = Category(name='Main Course')
        c2 = Category(name='Side Dishes')
        c3 = Category(name='Dessert')
        c4 = Category(name='Drinks')
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.add(c4)
        db.session.commit()

        # Product
        # p1 = Product(name='Predictably Irrational', price=210000, quantity=10, category_id=1)
        # p2 = Product(name='How Psychology Works', price=250000, quantity=12, category_id=1)
        # p3 = Product(name='Finance Wheel', price=25000, quantity=12, category_id=3)
        # p4 = Product(name='Test', price=25000, quantity=12, category_id=3, image='https://www.foodiesfeed.com/wp-content/uploads/2023/06/burger-with-melted-cheese.jpg')
        # # p4 = Product(name='Cái dũng của thánh nhân', auhor_name='Nguyễn Duy Cần',price=240000, category_id=2)
        # # p5 = Product(name='Toán học cao cấp', auhor_name='Trần Trung Kiệt',price=290000, category_id=2)
        # db.session.add_all([p1, p2, p3, p4])
        m1 = Product(name='Noodle', price=7.50, category_id=1, quantity=50,
                     image='https://tiffycooks.com/wp-content/uploads/2021/09/Screen-Shot-2021-09-21-at-5.21.37-PM.png')
        m2 = Product(name='French Fried', price=6.80, category_id=1, quantity=50,
                     image='https://www.recipetineats.com/uploads/2022/09/Crispy-Fries_8.jpg')
        m3 = Product(name='Chicken Rice', price=8.20, category_id=1, quantity=50,
                     image='https://nomadette.com/wp-content/uploads/2022/05/Roasted-Chicken-Rice.jpg')
        m4 = Product(name='Bread With Grilled Meat', price=4.50, category_id=1, quantity=50,
                     image='https://www.hungrypaprikas.com/wp-content/uploads/2021/09/Arayes-Recipe-4.jpg')
        m5 = Product(name='Soup', price=7.00, category_id=2, quantity=50,
                     image='https://www.onceuponachef.com/images/2021/02/Tomato-Soup-3-scaled.jpg')
        m6 = Product(name='Coke', price=2.00, category_id=4, quantity=50,
                     image='https://www.cocoichibanya.vn/wp-content/uploads/2020/07/Coke_CoCo-Ichibanya.jpg')
        m7 = Product(name='333', price=3.50, category_id=4, quantity=50,
                     image='https://product.hstatic.net/200000459373/product/bia-sai-gon-333-lon-330ml_a10a58af749a4fda84d59631115b5b82_master.jpg')
        m8 = Product(name='Tiger', price=4.00, category_id=4, quantity=50,
                     image='https://lh3.googleusercontent.com/rB31FSU2QNetkqfJPiXKCZblzPPX5oRqqfFAiypMHRsIjq6S2jxKshps51OYSfh4rlE6H-EhYRKYv0iVwpmrSRLqAqr6pnc=rw')
        m9 = Product(name='Sting', price=2.00, category_id=4, quantity=50,
                     image='https://product.hstatic.net/1000141988/product/nuoc_ngot_sting_dau_320_ml__i0012143__375f4dd6b1bb42009f4df6bfac7c3dbd.jpg')
        m10 = Product(name='Greenbeans', price=5.59, category_id=2, quantity=50,
                      image='https://static01.nyt.com/images/2015/10/12/dining/12COOKING-GREENBEANS/12COOKING-GREENBEANS-superJumbo.jpg')
        m11 = Product(name='Smashed Potatoes', price=4.49, category_id=2, quantity=50,
                      image='https://www.spoonforkbacon.com/wp-content/uploads/2022/11/smashed-potatoes-recipe-card.jpg')
        m12 = Product(name='Banana Cake', price=3.19, category_id=3, quantity=50,
                      image='https://img.sndimg.com/food/image/upload/q_92,fl_progressive,w_1200,c_scale/v1/img/recipes/17/25/60/piczLfe61.jpg')
        m13 = Product(name='Pudding', price=3.19, category_id=3, quantity=50,
                      image='https://www.flavcity.com/wp-content/uploads/2021/03/vanilla-pudding.jpg')
        m14 = Product(name='Ice Cream', price=2.19, category_id=3, quantity=50,
                      image='https://handletheheat.com/wp-content/uploads/2021/06/homemade-vanilla-ice-cream.jpg')
        db.session.add_all([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13,m14])
        db.session.commit()


        import hashlib

        u = User(name='Admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)
        db.session.add(u)
        db.session.commit()

        import hashlib

        u = User(name='Thu', username='Employee', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)
        db.session.add(u)
        db.session.commit()

        import hashlib

        u = User(name='Nhi', username='user', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.USER)
        db.session.add(u)
        db.session.commit()

        # Comment
        c1 = Comment(content='Good', user_id=1, product_id=1)
        c2 = Comment(content='Nice', user_id=1, product_id=1)
        db.session.add_all([c1, c2])
        db.session.commit()

        r1 = Receipt(created_date='2024-1-1',user_id=1,status=True)
        r2 = Receipt(created_date='2024-1-23',user_id=2,status=True)
        r3 = Receipt(created_date='2024-2-1',user_id=3,status=True)
        r4 = Receipt(created_date='2024-2-4',user_id=1,status=True)
        r5 = Receipt(created_date='2024-3-1',user_id=1,status=True)
        r6 = Receipt(created_date='2023-12-1',user_id=1,status=True)
        db.session.add_all([r1,r2,r3,r4,r5,r6])
        db.session.commit()

        d1 = ReceiptDetails(receipt_id=1, product_id =1, quantity=2)
        d2 = ReceiptDetails(receipt_id=1, product_id=2, quantity=1)
        d3 = ReceiptDetails(receipt_id=1, product_id =5, quantity=1)
        d4 = ReceiptDetails(receipt_id=1, product_id =6, quantity=2)

        d5 = ReceiptDetails(receipt_id=2, product_id =2, quantity=2)
        d6 = ReceiptDetails(receipt_id=2, product_id =6, quantity=3)
        d7 = ReceiptDetails(receipt_id=2, product_id =11, quantity=2)

        d8 = ReceiptDetails(receipt_id=3, product_id =3, quantity=3)
        d9 = ReceiptDetails(receipt_id=3, product_id =5, quantity=2)

        d10 = ReceiptDetails(receipt_id=4, product_id =2, quantity=2)
        d11 = ReceiptDetails(receipt_id=4, product_id =6, quantity=3)
        d12 = ReceiptDetails(receipt_id=4, product_id=11, quantity=2)

        d13 = ReceiptDetails(receipt_id=5, product_id =2, quantity=2)
        d14 = ReceiptDetails(receipt_id=5, product_id =6, quantity=3)
        d15 = ReceiptDetails(receipt_id=5, product_id =11, quantity=2)
        db.session.add_all([d1, d2, d3, d5, d4, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15])
        db.session.commit()

        # a1 = Author(name='Lionel Messi', biography='Football Player', country='Argentina')
        # a2 = Author(name='Cristiano Ronaldo', biography='Football Player', country='Portugal')
        # # p3 = Product(name='Cái dũng của thánh nhân', auhor_name='Nguyễn Duy Cần',price=240000, category_id=2)
        # p4 = Product(name='Toán học cao cấp', auhor_name='Trần Trung Kiệt',price=290000, category_id=2)
        # a5 = Author(name='Neymar Jr', biography='Football Player', country='Brazil')
        # db.session.add_all([a1, a2, a5])
        # db.session.commit()

        # ba1 = BookAuthor(product_id=1, author_id=1)
        # ba2 = BookAuthor(product_id=1, author_id=2)
        # ba3 = BookAuthor(product_id=2, author_id=2)
        # ba4 = BookAuthor(product_id=3, author_id=3)
        # db.session.add_all([ba1, ba2, ba3, ba4])
        # db.session.commit()
