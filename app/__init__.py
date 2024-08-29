from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = '3487ywheenujbhreriu4ui$$&()&^^^9erjrtunbr'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/fastfoodonline?charset=utf8mb4" % quote(
    "Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 2
db = SQLAlchemy(app=app)
login = LoginManager(app=app)
import cloudinary

cloudinary.config(
  cloud_name = "dnmsyzmjf",
  api_key = "769711456479333",
  api_secret = "4wV-HXrE341NRq1Q7D27G74wcI8"
)


