def flat_msg(data):
    Metr_msg = " "
    for i in data['Metro']:
        Metr_msg += "м." + "".join(i) + ",\n"
    flatmsg = (
        f" * {data['FlatParams']['Rooms_number']}, {data['FlatParams']['Total_area']} м²*, этаж {data['FlatParams']['floor']}/{data['FlatParams']['Total_floors']}\n"
        f"{data['Address']['City']}, {data['Address']['County']}, {data['Address']['District']}, {data['Address']['Street']}, {data['Address']['BlockNumber']}\n"
        f"*Ближайщее метро*:\n"
        f"{Metr_msg}"
        f"*Цена:* {data['Price']}₽/месяц\n"
        f"Дата публикации обьявления: {data['Date']}, {data['Time']} \n"
        f"*Подробности:*\n"
        f"{data['Link']}")
    return flatmsg


def show_param_msg(data):
    low_price = data['low_price']
    high_price = data['high_price']
    low_area = data['low_area']
    high_area = data['high_area']
    typee = data['type']
    param_msg = "Параметры по которым осуществляется поиск:\n"

    if low_price == 0 and high_price != 10000000:
        param_msg += f"*Цена:* до {high_price}\n"
    elif high_price == 10000000 and low_price != 0:
        param_msg += f"*Цена:* от {low_price}\n"
    elif high_price != 10000000 and low_price != 0:
        param_msg += f"*Цена:* от {low_price} до {high_price}\n"

    if low_area == 0 and high_area != 1000:
        param_msg += f"*Обшая плошадь:* до {high_area}\n"
    elif high_area == 1000 and low_area != 0:
        param_msg += f"*Обшая плошадь:* от {low_area}\n"
    elif high_area != 1000 and low_area != 0:
        param_msg += f"*Обшая плошадь:* от {low_area} до {high_area}\n"

    if typee != " ":
        param_msg += f"*Тип жилья:* {typee}"

    return param_msg


no_param_msg = "Нет параметров для сортировки\n" \
               "Для настройки параметров зайдите в *settings*"


welcome_msg = """
Привет! Это Flatty Bot! Помогаю в поиске квартир

*Доступные команды:*
`/show` — показывает информацию о квартирах
`settings` — показывает параметры которы можно настроить для лучшего поиска
`show parameters` - показывает настроенные параметры
`/help` — показывает информацию о боте
`/about` — узнать о боте
"""

help_msg = """
*Доступные команды:*
`/show` — показывает информацию о квартирах
`settings` — показывает параметры которы можно настроить для лучшего поиска
`show parameters` - показывает настроенные параметры
`/help` — показывает информацию о боте
`/about` — узнать о боте
"""

about_flatty_msg = """
Это бот для поиска квартир для аренды в Москва с циана. В Setting вы можете настроить параметры выдачи.
"""

settings_msg = """
Здесь вы можете настроить подходящие вам параметры
"""

back_msg = """
Вернулись в начало.
"""

show_msg = f"""
Показываю по 4 квартиры
"""

no_show_msg = """
Под ваши параметры нет квартир 
"""

save_msg = """
Cохраняем параметры...
"""
save_toDB_msg = """
Все параметры сохранены! 
"""

no_image = """
К сажелению фото нет
"""

price_msg = """
Введите желаемый диапозон цены в формате "цена 1 - цена 2".
Можно не заполнять одно значение.
Пример: "цена 1 - " или " - цена 2"
"""
set_msg = """
Принято! Будем искать!
"""

Incorrect_price_msg = """
Неправильный формат ввода, введите еще раз
"""
dif_msg = """
Первое значение должно быть меньше второго, введите еще раз
"""
empty_price_msg = """
ОК! По цене сортировать не будем.
"""

area_msg = """
Введите желаемый диапозон плошади в м^2 в формате "площадь 1 - площадь 2".
Можно не заполнять одно значение.
Пример: "площадь 1 - " или " - площадь 2"
"""

Incorrect_area_msg = """
Неправильный формат ввода, введите еще раз
"""

empty_area_msg = """
ОК! По площади сортировать не будем.
"""

type_msg = """
Выберите тип жилья.
"""

type_wrong_msg = """
Ой, такого типа жилья у нас нет, выберите что-то другое.
"""
