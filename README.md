# Currency Converter - Конвертер Валют
<b>Конвертер валют</b> — это приложение, позволяющее быстро переводить одну валюту в другую по курсу.
Такие инструменты массово доступны в интернете, воспользоваться ими можно бесплатно.

> Конвертер валют на PyQT5 c использованием серсиса Xe.

[Xe](https://www.xe.com/ "Всплывающая подсказка") — это компания, предоставляющая инструменты и услуги по обмену иностранной валюты онлайн.
Наиболее известна Xe своим онлайн-конвертером валют.
В этом разделе мы воспользуемся такими библиотеками, как <u>[requests](https://pypi.org/project/requests/)</u> и  <u>[BeautifulSoup](https://pypi.org/project/beautifulsoup4/)</u>, чтобы сделать на их основе собственный конвертер валют.

Пример кода:
```python
import requests
from bs4 import BeautifulSoup as bs
import re
from dateutil.parser import parse
```
Теперь давайте создадим функцию, которая принимает исходную валюту, целевую валюту и сумму, которую мы хотим конвертировать, а затем возвращает конвертированную сумму вместе с датой и временем обменного курса.

Выглядеть это будет следующим образом:
```python
def convert_currency_xe(src, dst, amount):
    def get_digits(text):
        """Returns the digits and dots only from an input `text` as a float
        Args:
            text (str): Target text to parse
        """
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
```

На момент написания данного руководства обменный курс находился в третьем абзаце HTML-страницы.
Это объясняет строчку: ```soup.find_all("p")[2]```.
Не забывайте вносить правки, когда в HTML-страницу вносятся изменения.

В HTML DOM последняя дата и время обменного курса находятся во втором родителе абзаца exchange rate.

Поскольку обменный курс содержит строковые символы, мы создали функцию get_digits() для извлечения из заданной строки только цифр и точек.

Что ж, давайте воспользуемся нашей функцией:
```python
if __name__ == "__main__":
    import sys
    source_currency = sys.argv[1]
    destination_currency = sys.argv[2]
    amount = float(sys.argv[3])
    last_updated_datetime, exchange_rate = convert_currency_xe(source_currency, destination_currency, amount)
    print("Last updated datetime:", last_updated_datetime)
    print(f"{amount} {source_currency} = {exchange_rate} {destination_currency}")
```

На этот раз нам нужно передать исходную и целевую валюты, а также сумму из командной строки.
Мы также попытаемся конвертировать 1000 евро в доллары США с помощью команды в консоли:
```commandline
python xe_currency_converter.py EUR USD 1000
```

Мы получим следующий результат:
```commandline
Last updated datetime: 2022-02-01 13:04:00+00:00
1000.0 EUR = 1125.8987 USD
```
Замечательно!
Xe обычно обновляется каждую минуту, так что мы получаем результат в режиме реального времени 👀

[Qt Creator](https://doc.qt.io/qtcreator/ "Qt Creator — это кроссплатформенная, полностью интегрированная среда разработки (IDE) для разработчиков приложений, позволяющая создавать приложения для нескольких платформ настольных, встроенных и мобильных устройств, таких как Android и iOS. Он доступен для операционных систем Linux, macOS и Windows") — кроссплатформенная свободная IDE для разработки на С, С++ и QML.
Разработана Trolltech для работы с фреймворком Qt.
Включает в себя графический интерфейс отладчика и визуальные средства разработки интерфейса как с использованием QtWidgets, так и QML.

![image](https://github.com/QuadDarv1ne/CurrencyConverter/assets/51045274/940baaca-152b-40e5-af7c-9847e289ea00)

> Дата: 12.03.2024
> 
> Разработчик: Дуплей Максим Игоревич
