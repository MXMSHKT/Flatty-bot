from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Buttons
help_btn = KeyboardButton('/help')
about_btn = KeyboardButton('/about')
back_btn = KeyboardButton('/back')
show_btn = KeyboardButton('/show')

price_btn = KeyboardButton('Цена')
area_btn = KeyboardButton('Общая площадь')
type_btn = KeyboardButton('Тип жилья')
show_param_btn = KeyboardButton('show parameters')


type_btn1 = KeyboardButton("Квартира")
type_btn2 = KeyboardButton("Апартаменты")
type_btn3 = KeyboardButton('Студия')

setting_btn = KeyboardButton("settings")
save_setting_btn = KeyboardButton("save parameters")

# Markups
startup_markup = ReplyKeyboardMarkup(resize_keyboard=True)
startup_markup.add(show_btn).add(show_param_btn).add(setting_btn).add(about_btn).add(help_btn)

type_markup = ReplyKeyboardMarkup(resize_keyboard=True)
type_markup.add(type_btn1).add(type_btn2).add(type_btn3).add(back_btn)

setting_markup = ReplyKeyboardMarkup(resize_keyboard=True)
setting_markup.add(save_setting_btn).add(price_btn).add(area_btn).add(type_btn).add(back_btn)