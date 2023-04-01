import base64

# Decoding the images


class FileException(Exception):
    def __init__(self, data):
        self.__data = data

    def __str__(self):
        return f'Ошибка при декодировании файла {self.__data}'


class RenderPicture(FileException):
    def __init__(self, data):
        self.__data = data

    def get_data(self):
        return self.__data

    def render_picture(self):
        render_pic = base64.b64encode(self.__data).decode('ascii')
        return render_pic
