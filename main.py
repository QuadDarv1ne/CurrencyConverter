import sys
import requests
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QIcon, QFont
from ui import Ui_MainWindow
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse
from currency_converter import CurrencyConverter  # импортируем ui интерфейс

class CurrencyConv(QtWidgets.QMainWindow):
    def __init__(self):
        super(CurrencyConv, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()


    def init_UI(self):
        self.setWindowTitle('Конвертер валют')
        self.setWindowIcon(QIcon('exchanging.png'))
        self.ui.input_currency.setPlaceholderText('Из валюты:')
        self.ui.input_amount.setPlaceholderText('У меня есть:')
        self.ui.output_currency.setPlaceholderText('В валюту:')
        self.ui.output_amount.setPlaceholderText('Я получу:')
        self.ui.pushButton.clicked.connect(self.converter)

        QToolTip.setFont(QFont('SansSerif', 10))
        self.ui.input_currency.setToolTip('Введите валюту, которую хотите конвертировать:\nRUB - рубли / USD - доллары / EUR - евро')
        self.ui.input_amount.setToolTip('Введите сумму выбранной валюты 💶')
        self.ui.output_currency.setToolTip('Выберите валюту, в которую хотите конвертировать:\nRUB - рубли / USD - доллары / EUR - евро')
        self.ui.output_amount.setToolTip('Здесь будет отображаться конвертированная сумма 💹')


    @staticmethod
    def convert_currency_xe(src, dst, amount):
        def get_digits(text):
            new_text = ""
            for c in text:
                if c.isdigit() or c == ".":
                    new_text += c
            return float(new_text)

        url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={src}&To={dst}"
        content = requests.get(url).content
        soup = bs(content, "html.parser")
        exchange_rate_html = soup.find_all("p")[2]
        # get the last updated datetime
        last_updated_datetime = parse(re.search(r"Last updated (.+)", exchange_rate_html.parent.parent.find_all("div")[-2].text).group()[12:])
        return last_updated_datetime, get_digits(exchange_rate_html.text)


    def converter(self):
        input_currency = self.ui.input_currency.text()
        output_currency = self.ui.output_currency.text()
        input_amount = float(self.ui.input_amount.text())
        last_updated_datetime, exchange_rate = self.convert_currency_xe(input_currency, output_currency, input_amount)
        output_amount = exchange_rate
        self.ui.output_amount.setText(str(output_amount))
        print(f"{input_amount} {input_currency} = {exchange_rate} {output_currency}")


app = QtWidgets.QApplication([])
application = CurrencyConv()
application.show()
sys.exit(app.exec_())

# TODO: Заметки 📑
## 🐉 Разработчик: Дуплей Максим Игоревич 🏆
## 🪪 GitHub профиль: https://github.com/QuadDarv1ne
## 💎 Telegram группа: «QuadD4rv1n7 & Фишки программиста» 💎
##    Ссылка: https://t.me/it_baza_znaniy