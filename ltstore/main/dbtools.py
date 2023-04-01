
from .app import db, app
from .model import Items, OrderItem


class DataException(Exception):
    def __init__(self, data):
        self._data = data

    def __repr__(self):
        return f'Ошибка при добавлении в бд'


class SubmitData(DataException):

    def add_data(self):
        db.session.add(self._data)
        db.session.commit()

    def delete_data(self):
        db.session.delete(self._data)
        db.session.commit()


class SelectData:
    """Механизм сортировки"""
    def _sort_all(self, conditions):
        with app.app_context():
            return Items.query.filter(conditions).order_by(Items.id).all()

    def _sort_first(self, condition):
        with app.app_context():
            return Items.query.filter(condition).order_by(Items.id).first()

    def _sort_order_item_all(self, email):
        with app.app_context():
            return OrderItem.query.filter_by(profiles_id=email).all()

    def _sort_order_item_first(self, email):
        with app.app_context():
            return OrderItem.query.filter_by(profiles_id=email).first()


class Sort(SelectData):
    """Сортировка товаров"""
    def sort_id(self, id):
        return SelectData()._sort_first(Items.id == id)

    def sort_brand(self, brand):
        return SelectData()._sort_all(Items.item_brand == brand)

    def sort_name(self, name):
        return SelectData()._sort_first(Items.item_name == name)

    def sort_category(self, category):
        return SelectData()._sort_all(Items.category == category)

    def min_price_all(self, price):
        return SelectData()._sort_all(Items.price > price)

    def between_price_all(self, min_price, max_price):
        return SelectData()._sort_all((Items.price > min_price) & (Items.price < max_price))

    def max_price_all(self, price):
        return SelectData()._sort_all(Items.price < price)


sorting = Sort()
products_in_cart = SelectData()
