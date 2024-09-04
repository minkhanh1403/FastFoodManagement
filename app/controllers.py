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

