from .app import app
from flask import render_template
from .dbtools import sorting, SelectData, Items
from .app.setup.order_form import AddToCart


class Promotional:
    def __init__(self, id):
        self.id = id

    def choose_id(self):
        return sorting.sort_id(self.id)

    def choose_brand(self, brand):
        return sorting.sort_brand(brand)

    def choose_min_price(self, min_price):
        return sorting.min_price_all(min_price)

    def choose_between_price(self, min_price, max_price):
        return sorting.between_price_all(min_price, max_price)

    def choose_max_price(self, max_price):
        return sorting.max_price_all(max_price)


@app.route('/product/macpro', methods=['POST', 'GET'])
def index_menu1():
    return render_template('view_product.html', form=AddToCart(), product=Promotional(7).choose_id())


@app.route('/product/msi', methods=['POST', 'GET'])
def index_menu2():
    return render_template('view_product.html', form=AddToCart(), product=Promotional(5).choose_id())


@app.route('/product/matebookd15', methods=['POST', 'GET'])
def index_menu3():
    return render_template('view_product.html', form=AddToCart(), product=Promotional(9).choose_id())


@app.route('/store/card1', methods=['POST', 'GET'])
def card1():
    return render_template('store.html', form=AddToCart(), data=Promotional(7).choose_brand('Apple'))


@app.route('/store/card2', methods=['POST', 'GET'])
def card2():
    max_price = 50000
    category = 'Ноутбуки'
    data = SelectData()._sort_all((Items.price < max_price) & (Items.category == category))
    return render_template('store.html', form=AddToCart(), data=data)
