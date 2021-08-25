import sys

# подк. библ. случайного выбора
from random import choice

# для работы с картинками в pyqt5
from PyQt5.QtGui import QPixmap

# основные модули для pyqt5
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QHBoxLayout

# список картинок
FILES_FROM_PIC = ('pic/mem_1.jpg', 'pic/mem_2.jpg', 'pic/mem_3.jpg',
                  'pic/mem_4.jpg', 'pic/mem_5.jpg', 'pic/mem_6.jpg')


# окно вывода картинок
class Statistic(QMainWindow):
    def __init__(self, file_from_pic):
        super().__init__()

        # сохранение запроса
        self.file_from_pic = file_from_pic

        # подключение дизайна
        self.initUI()

    # дизайн
    def initUI(self):

        #размещение окна на столе пользователя
        self.move(400, 400)

        # название окна
        self.setWindowTitle('Статистика :)')

        # создание лейоута
        self.hbox = QHBoxLayout(self)

        # Изображение
        self.pixmap = QPixmap(self.file_from_pic)

        # место разм. картинки
        self.image = QLabel(self)

        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

        # настройка размеров картинки
        self.image.resize(self.pixmap.width(), self.pixmap.height())

        # настройка размера окна
        self.resize(self.pixmap.width(), self.pixmap.height())

        # фиксация размера окна
        self.setFixedSize(self.pixmap.width(), self.pixmap.height())

        # добовление виджета в лейоут
        self.hbox.addWidget(self.image)

        # настройка лейоута
        self.setLayout(self.hbox)
