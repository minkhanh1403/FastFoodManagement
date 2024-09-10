import math

import cloudinary.uploader
from flask import render_template, request, redirect, session, jsonify
from flask_login import login_user, logout_user, current_user

import dao
from app import app, db
from app.decorators import annonymous_user
from app.models import User


@app.route('/')
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get("page")

    cates = dao.load_categories()
    product = dao.load_products(kw=kw, cate_id=cate_id, page=page)

    total = dao.count_product()
    return render_template('index.html', categories=cates, products=product,
                           pages=math.ceil(total / app.config['PAGE_SIZE']))


def detail(id):
    p = dao.get_product_by_id(id)
    comments = dao.get_comments_by_product(id)
    return render_template('detail.html', product=p, comments=comments)

def comments(product_id):
    data = []
    for c in dao.load_comments(product_id=product_id):
        data.append({
            'id': c.id,
            'content': c.content,
            'created_date': str(c.created_date),
            'user': {
                'name': c.user.name,
                'avatar': c.user.avatar
            }
        })

    return jsonify(data)


def load_users_in_register():
    query = db.session.query(User.id, User.name, User.username)
    return query.all()


def login_admin():
    username = request.form.get('username')
    password = request.form.get('pwd')

    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    return redirect('/admin')


@annonymous_user
def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            n = request.args.get('next')
            return redirect(n if n else '/')

    return render_template('login.html')


def logout_my_user():
    logout_user()
    return redirect('/login')


def register():
    err_msg = ''
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']  # name cua html
        confirm = request.form['confirm']

        # birthday = request.form['birthday']
        # gender = request.form['sex']
        # telephone = request.form['telephone']
        # address = request.form['address']

        # return gender

        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']
            try:
                danh_sach_user = dao.load_users_in_register()
                # return str(danh_sach_user[0][2])
                so_luong_user = dao.count_user_in_register()[0][0]

                for i in range(0, int(so_luong_user)):
                    if str(danh_sach_user[i][2]).__eq__(username):
                        err_msg = "Tên đăng nhập đã tồn tại"
                        return render_template('register.html', err_msg=err_msg)
                else:
                    dao.register(name=name, username=username, password=password, avatar=avatar)

                    return redirect('/login')
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


# NVL
def add_to_cart():
    data = request.json

    cart = session.get('cart')
    if cart is None:
        cart = {}

    id = str(data.get("id"))
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart

    """
        {
            "1": {
                "id": "1",
                "name": "...",
                "price": 123,
                "quantity": 2
            },  "2": {
                "id": "2",
                "name": "...",
                "price": 1234,
                "quantity": 1
            }
        }
    """

    return jsonify(ultis.cart_stats(cart))


def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        quantity = request.json.get('quantity')
        cart[product_id]['quantity'] = int(quantity)

    session['cart'] = cart
    return jsonify(ultis.cart_stats(cart))


def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart
    return jsonify(ultis.cart_stats(cart))




#NVL
@app.route("/generate_csv")
def generate_csv():
    if len(users) == 0:
        return "No data to generate CSV."

    # Create a CSV string from the user data
    csv_data = "Name,Email\n"
    for user in users:
        csv_data += f"{user['name']},{user['email']}\n"

    return render_template("index.html", csv_data=csv_data)


@app.route("/download_csv")
def download_csv():
    if len(users) == 0:
        return "No data to download."

    # Create a CSV string from the user data
    csv_data = "Name,Email\n"
    for user in users:
        csv_data += f"{user['name']},{user['email']}\n"

    # Create a temporary CSV file and serve it for download
    with open("users.csv", "w") as csv_file:
        csv_file.write(csv_data)

    return send_file("users.csv", as_attachment=True, download_name="users.csv")




#DVH

#NVL
def cashier():
    return render_template("cashier.html", u=current_user)


def add_to_cart_emp():
    data = request.json

    cartCashier = session.get('cartCashier')
    if cartCashier is None:
        cartCashier = {}

    id = str(data.get("id"))
    if id in cartCashier:
        cartCashier[id]['quantity'] += 1
    else:
        cartCashier[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cartCashier'] = cartCashier

    """
        {
            "1": {
                "id": "1",
                "name": "...",
                "price": 123,
                "quantity": 2
            },  "2": {
                "id": "2",
                "name": "...",
                "price": 1234,
                "quantity": 1
            }
        }
    """

    return jsonify(ultis.cart_stats(cartCashier))


def comments(product_id):
    data = []
    for c in dao.load_comments(product_id=product_id):
        data.append({
            'id': c.id,
            'content': c.content,
            'created_date': str(c.created_date),
            'user': {
                'name': c.user.name,
                'avatar': c.user.avatar
            }
        })

    return jsonify(data)


def update_cart_emp(product_id):
    cartCashier = session.get('cartCashier')
    if cartCashier and product_id in cartCashier:
        quantity = request.json.get('quantity')
        cartCashier[product_id]['quantity'] = int(quantity)

    session['cartCashier'] = cartCashier
    return jsonify(ultis.cart_stats(cartCashier))


def delete_cart_emp(product_id):
    cartCashier = session.get('cartCashier')
    if cartCashier and product_id in cartCashier:
        del cartCashier[product_id]

    session['cartCashier'] = cartCashier
    return jsonify(ultis.cart_stats(cartCashier))
#NVL\

#DVH
    # @login_required
def pay():
    cart = session.get('cart')
    # import pdb
    # pdb.set_trace()
    try:
        dao.save_receipt(cart)
    except Exception as ex:
        print(str(ex))
        return jsonify({'status': 500})
    else:
        del session['cart']

    return jsonify({'status': 200})


# @login_required
def pay_emp():
    cartCashier = session.get('cartCashier')
    # import pdb
    # pdb.set_trace()
    try:
        dao.save_receipt(cartCashier)
    except Exception as ex:
        print(str(ex))
        return jsonify({'status': 500})
    else:
        session['print_cart'] = cartCashier
        del session['cartCashier']

    return jsonify({'status': 200})
