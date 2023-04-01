
from .app import db, bcrypt, login_manager
from datetime import datetime, date
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Profiles.query.get(int(user_id))


class Profiles(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False)
    lastname = db.Column(db.String(length=50), nullable=False)
    email = db.Column(db.String(length=50), unique=True)
    phone = db.Column(db.Integer(), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    city = db.Column(db.String(length=50), nullable=False)

    orders = db.relationship('OrderItem', backref='profile', lazy='dynamic')
    posts = db.relationship('Comment', backref='profiles', lazy='dynamic')

    def __repr__(self):
        return f"<profiles {self.id}>"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Items(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    item_brand = db.Column(db.String(100), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    barcode = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(), default=date.today())
    price = db.Column(db.Integer(), nullable=False)
    display = db.Column(db.String(50), nullable=True)
    cpu = db.Column(db.String(50), nullable=True)
    rom = db.Column(db.String(50), nullable=True)
    ram = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text())
    quantity = db.Column(db.Integer(), nullable=False)
    image = db.Column(db.LargeBinary())
    rendered_data = db.Column(db.Text())

    items = db.relationship('OrderItem', backref='item', lazy='dynamic')
    posts = db.relationship('Comment', backref='items', lazy='dynamic')

    def __repr__(self):
        return f'Item {self.item_name}, bc:{self.barcode}'


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.Text())
    profiles_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    items_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    def __repr__(self):
        return f"<comment {self.id} from {self.profiles_id} >"


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profiles_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    items_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item_name = db.Column(db.String(100))
    item_brand = db.Column(db.String(100))
    barcode = db.Column(db.String(100))
    price = db.Column(db.Integer())


class SubmitOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profiles_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    client_name = db.Column(db.String(length=50))
    email = db.Column(db.String(length=50))
    phone = db.Column(db.Integer())
    payment = db.Column(db.String(100))
    total_price = db.Column(db.Integer())

    def __repr__(self):
        return f"<Order {self.id} price {self.total_price} for {self.client_name}>"
