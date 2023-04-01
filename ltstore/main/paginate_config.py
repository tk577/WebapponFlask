
from .app import app
from flask import request, url_for
from .model import Items


class Paginate:
    def __init__(self):
        self.__page = request.args.get('page', 1, type=int)
        self.__per_page = app.config['APP_PER_PAGE']
        self.__error_out = False

    def paginate_page(self, category):
        return Items.query.filter(Items.category == category).paginate(page=self.__page,
                                                                       per_page=self.__per_page,
                                                                       error_out=self.__error_out)

    def next_page(self, url_page, list):
        return url_for(url_page, page=list.next_num) if list.has_next else None

    def prev_page(self, url_page, list):
        return url_for(url_page, page=list.prev_num) if list.has_prev else None
