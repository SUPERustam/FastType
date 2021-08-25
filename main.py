# для работы с системой
import sys
import sqlite3
import datetime as dt
from itertools import zip_longest
from random import choice

# импорт дополнительного файла
from pic import Statistic, FILES_FROM_PIC

# для удобной работы с qt designer
from PyQt5 import uic
# основные модули для pyqt5
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QAction, qApp, QFileDialog

# импорт дизайна главной программы
from main_design import Ui_MainWindow

# импорт дизайна дополнительной программы программы
from about_design import Ui_about

# id means in shortcuts table(sqlite3):
# 1 - processing buttons from en/ru to ru/en
# 2 - open file
# 3 - save file
# 4 - save file as ...
# 5 - show stats
# 6 - show about info
# 7 - exit application


# главное окно
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # скачивание дизайна
        self.setupUi(self)

        # для окна about
        self.about_window = About()

        # случайный выбор смешной картинки
        self.stats_window = Statistic(choice(FILES_FROM_PIC))

        #  узнаем дату сегодня
        self.today_date = dt.datetime.today().date()

        # переменная куда сохраняем путь к файлу .txt
        self.file_now = ''

        #  подключаем бд
        con = sqlite3.connect('base.db')
        # наводим курсор
        cur = con.cursor()

        # находим все гор клавиши
        self.shortcuts = cur.execute(
            '''SELECT shortcut from shortcuts''').fetchall()

        # находим дату послед. активности прил.
        self.last_active = cur.execute(
            '''SELECT mydate from stat WHERE mystatus = 'last_active' ''').fetchone()

        # изменяем дату послед. акт. прил. на дату сегодня
        self.cash = cur.execute(
            """UPDATE stat SET mydate=? WHERE mystatus = 'last_active' """, (self.today_date,))

        # сохраняем все в бд
        con.commit()
        # закрываем бд
        con.close()

        # выводим дату посл. акт.
        self.text_for_date = f'Last active: {self.last_active[0]}'
        self.setStatusTip(self.text_for_date)

        #  обраб. все горю клавиши в удобный формат
        self.shortcuts = tuple(map(lambda x: str(x[0]), self.shortcuts))

        # подключаем дополнительный дизайн к глав-окну
        self.initUI()

    # дополнительный дизайн к глав-окну
    def initUI(self):

        # подготовка гор. клавиш к использованию - смена клавиш ru/en -> en/ru
        self.trans_action = QAction('Change keys', self)
        self.trans_action.setShortcut(self.shortcuts[0])
        self.trans_action.setStatusTip('Change en/ru keys to ru/en')
        self.trans_action.triggered.connect(self.trans)

        # подготовка гор. клавиш к использованию - открытие файла
        self.open_file_action = QAction('Open', self)
        self.open_file_action.setShortcut(self.shortcuts[1])
        self.open_file_action.setStatusTip('Open file')
        self.open_file_action.triggered.connect(self.open_file)

        # подготовка гор. клавиш к использованию - сохранение файла
        self.save_file_action = QAction('Save', self)
        self.save_file_action.setShortcut(self.shortcuts[2])
        self.save_file_action.setStatusTip('Save file in the last directory')
        self.save_file_action.triggered.connect(self.save_file)

        # подготовка гор. клавиш к использованию - сохранение файла в директории
        self.save_as_file_action = QAction('Save as', self)
        self.save_as_file_action.setShortcut(self.shortcuts[3])
        self.save_as_file_action.setStatusTip('Save file as in the directory')
        self.save_as_file_action.triggered.connect(self.save_as_file)

        # подготовка гор. клавиш к использованию - показ статистики(на самом деле смешных картинок :) )
        self.stats_action = QAction('Show stats', self)
        self.stats_action.setShortcut(self.shortcuts[4])
        self.stats_action.setStatusTip('Show some statistices about you')
        self.stats_action.triggered.connect(self.stats)

        # подготовка гор. клавиш к использованию - показ окна about
        self.about_action = QAction('About', self)
        self.about_action.setShortcut(self.shortcuts[5])
        self.about_action.setStatusTip('Show about info')
        self.about_action.triggered.connect(self.show_about)

        # подготовка гор. клавиш к использованию - выход из программы
        self.exit_action = QAction('Exit', self)
        self.exit_action.setShortcut(self.shortcuts[6])
        self.exit_action.setStatusTip('Exit application')
        self.exit_action.triggered.connect(qApp.quit)

        # создание статус бара
        self.statusBar()

        # подключение меню бара
        self.menubar = self.menuBar()

        # настройка меню
        self.fileMenu = self.menubar.addMenu('File')

        # подключение вывода окна about к меню
        self.fileMenu.addAction(self.about_action)

        # подключение функции открытия файла к меню
        self.fileMenu.addAction(self.open_file_action)

        # подключение функции сохранения файла к меню
        self.fileMenu.addAction(self.save_file_action)

        # подключение функции сохранения файла(как) к меню
        self.fileMenu.addAction(self.save_as_file_action)

        # подключение функции перевода символов к меню
        self.fileMenu.addAction(self.trans_action)

        # подключение  функции показа статистики(смешных картинок) к меню
        self.fileMenu.addAction(self.stats_action)

        # подключение функции выхода из программы к меню
        self.fileMenu.addAction(self.exit_action)

    # функция перевода символов
    def trans(self):

        # сохранение выделенного текста в переменную
        text_trans = self.plainTextEdit.textCursor().selectedText()

        # проверка наличия символов в переменнной
        if ''.join(text_trans.split()):

            # итоговая строка
            text_result = ''

            # подключение к бд
            con = sqlite3.connect('base.db')

            # ставим курсор
            cur = con.cursor()

            # все буквы en раскладки
            letters_en = cur.execute('''SELECT en from letters''').fetchall()

            # все буквы ru раскладки
            letters_ru = cur.execute('''SELECT ru from letters''').fetchall()

            # закрытие бд
            con.close()

            # обработка информации англ. раскладки
            letters_en = map(lambda x: str(x[0]), letters_en)

            # обработка информации русс. раскладки
            letters_ru = map(lambda x: str(x[0]), letters_ru)

            # слияние списков в словарь
            letters = dict(zip_longest(letters_en, letters_ru))

            # алгоритм перевода символов
            for i in text_trans:
                end = i
                if i in list(letters.keys()):
                    end = letters[i]

                elif i in list(letters.values()):
                    # поиск ключей по значению
                    end = list(letters.keys())[list(letters.values()).index(i)]

                text_result += end

            # заменяем выделленый текст новым
            self.plainTextEdit.insertPlainText(text_result)

    # функция открытия файла
    def open_file(self):
        # находим файл
        self.file_now = QFileDialog.getOpenFileName(
            self, 'Choose file', '',
            'text file(*.txt)')[0]

        # пробуем открыть и сохранить данные
        try:
            with open(self.file_now) as f:
                self.plainTextEdit.setPlainText(f.read())

        # выводим ошибку в случае неудачи
        except:
            self.setStatusTip('Error. Please, try agian to open file.')

        # все хорошо: выводим прежнию информацию
        else:
            self.setStatusTip(self.text_for_date)

    # функция сохр. текста в файл
    def save_file(self):

        # пробуем сохранить
        try:
            with open(self.file_now, 'w') as f:
                f.write(self.plainTextEdit.toPlainText())

        # выводим ошибку в случае неудачи
        except:
            self.setStatusTip('Error. Please, open file.')

        # все хорошо: выводим прежнию информацию
        else:
            self.setStatusTip(self.text_for_date)

    # функция сохр. текста в файл в директории
    def save_as_file(self):

        # находим файл
        self.file_now = QFileDialog.getOpenFileName(
            self, 'Choose file', '',
            'text file(*.txt)')[0]

        # пробуем открыть и сохранить в файл все
        try:
            with open(self.file_now, 'w') as f:
                f.write(self.plainTextEdit.toPlainText())

        # выводим ошибку в случае неудачи
        except:
            self.setStatusTip('Error. Please, try agian to open file.')

        # все хорошо: выводим прежнию информацию
        else:
            self.setStatusTip(self.text_for_date)

    # функция показа окна about
    def show_about(self):

        # показ окна about
        self.about_window.show()

    # функция отображения картинок
    def stats(self):

        # выбираем случайную картинку
        self.file_from_pic = choice(FILES_FROM_PIC)

        # обрабатываем
        self.stats_window = Statistic(self.file_from_pic)

        # выводим
        self.stats_window.show()


# окно about
class About(QWidget, Ui_about):
    def __init__(self):
        super().__init__()

        # подключение дизайна about окна
        self.setupUi(self)


# обработка ошибок в pyqt5
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# включение программы
# начальная настройка
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
