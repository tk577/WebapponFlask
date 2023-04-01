
class CalcException(Exception):
    def __init__(self, code):
        self.__code = code

    def __str__(self):
        return f" Недопустимое значение: {self.__code}. \n" \
               f"Значение должно быть натуральным числом от 1 до 90"


class CountTotalPrice:
    def __init__(self, products):
        self._products = products
        self._count = 0

    def calculate_price(self):
        for item in self._products:
            self._count += item.price
        return self._count


class DiscountCalc(CalcException):
    def __init__(self):
        self.__code = 0

    @classmethod
    def __type(cls, code):
        return type(code) == int

    @property
    def discount_check(self):
        return self.__code

    @discount_check.setter
    def discount_check(self, code):
        if self.__type(code):
            if 0 < code < 90:
                self.__code = code
            else:
                raise CalcException(code)
        else:
            raise CalcException(code)

    def introduce_code(self, products):
        total_price = CountTotalPrice(products).calculate_price()
        return total_price * (1 - self.__code/100)


class DiscountPrice:
    def __init__(self, code, products):
        self._code = code
        self._products = products

    def calculate_total_price(self):
        discount = DiscountCalc()
        discount.discount_check = self._code
        return discount.introduce_code(self._products)
