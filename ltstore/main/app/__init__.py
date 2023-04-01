#web project - laptopstore v.1.0

from flask import Flask,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_basicauth import BasicAuth
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ltstore.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/yourdb'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'nfjsgnij435u39jfisan321h355'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message = "Необходима авторизация"
login_manager.login_message_category =  "info"


app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '12345'

basic_auth = BasicAuth(app)


app.config['APP_PER_PAGE'] = 9
