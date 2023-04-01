from .app import app
from flask import render_template
from .app.setup.order_form import AddToCart
from .paginate_config import Paginate


class Catalogue:
    def __init__(self, category, url_page):
        self.__html_page = 'store.html'
        self.__form = AddToCart()
        self._category = category
        self._url_page = url_page

    def _render_template(self):
        data = Paginate().paginate_page(self._category)
        next_url = Paginate().next_page(self._url_page, data)
        prev_url = Paginate().prev_page(self._url_page, data)
        return render_template(self.__html_page,
                               data=data.items,
                               form=self.__form,
                               next_url=next_url, prev_url=prev_url)


@app.route('/catalogue', methods=['POST', 'GET'])
def catalogue_page():
    return render_template('catalogue.html')


@app.route('/store/laptops/', methods=['POST', 'GET'])
def store():
    render = Catalogue('Ноутбуки', 'store')
    return render._render_template()


@app.route('/store_bags', methods=['POST', 'GET'])
def store_bags():
    render = Catalogue('Сумки', 'store_bags')
    return render._render_template()


@app.route('/store_keyboards', methods=['POST', 'GET'])
def store_keyboards():
    render = Catalogue('Клавиатуры', 'store_keyboards')
    return render._render_template()


@app.route('/store_charger', methods=['POST', 'GET'])
def store_charger():
    render = Catalogue('Зарядные устройства', 'store_charger')
    return render._render_template()


@app.route('/store_po', methods=['POST', 'GET'])
def store_po():
    render = Catalogue('ПО', 'store_po')
    return render._render_template()


@app.route('/store_spares', methods=['POST', 'GET'])
def store_spares():
    render = Catalogue('Комплектующие и запчасти', 'store_spares')
    return render._render_template()
