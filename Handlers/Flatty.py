import time
from aiogram import Dispatcher, types
from Menu.markups import *
from aiogram.dispatcher import filters
from bot_init import dp, bot
from Default_values import *
from aiogram.dispatcher import FSMContext
import os
import random
import math
from db import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from Menu.phrases import *
from aiogram.types import Message


class Sorting(StatesGroup):
    price_sort = State()  # done
    area_sort = State()  # done
    type_sort = State()  # done
    rooms_sort = State()
    county_sort = State()
    nearest_metro = State()
    time_sort = State()  # за сегодня


async def show_param(message: types.Message):
    if tdb.find_one({"_id": message.from_user.id})["active_param"] == "NO":
        await message.answer(no_param_msg, parse_mode='Markdown')
    else:
        param_data = tdb.find_one({"_id": message.from_user.id})
        await message.answer(
            text=show_param_msg(param_data),
            reply_markup=startup_markup,
            parse_mode='Markdown'
        )


async def send_price(message: types.Message, state: FSMContext):
    await message.answer(
        text=price_msg,
        reply_markup=startup_markup,
        parse_mode='Markdown'
    )
    await state.set_state(Sorting.price_sort)


async def set_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text.lower())
    await state.update_data(id=message.from_user.id)
    user_data = await state.get_data()
    if "-" in user_data['price']:
        sp = [x.strip() for x in user_data['price'].split("-")]
        if sp[0].isdigit() and sp[1].isdigit() and int(sp[0]) >= int(sp[1]):
            await message.answer(
                text=dif_msg,
                reply_markup=setting_markup,
                parse_mode='Markdown'
            )
        elif not sp[0] and not sp[1]:
            await message.answer(
                text=empty_price_msg,
                reply_markup=setting_markup,
                parse_mode='Markdown'
            )
            await state.set_state(state=None)
        elif (sp[0].isdigit() or not sp[0]) and (sp[1].isdigit() or not sp[1]):
            if sp[0].isdigit():
                await state.update_data(low_price=int(sp[0].strip()))
                user_data = await state.get_data()
                tdb.update_one({'_id': user_data['id']},
                               {'$set': {'low_price': user_data['low_price'],
                                         "active_param": "YES"}})
            if not sp[0]:
                tdb.update_one({'_id': user_data['id']},
                               {'$set': {'low_price': MIN_PRICE}})
            if sp[1].isdigit():
                await state.update_data(high_price=int(sp[1].strip()))
                user_data = await state.get_data()
                tdb.update_one({'_id': user_data['id']},
                               {'$set': {'high_price': user_data['high_price'],
                                         "active_param": "YES"}
                                })
            if not sp[1]:
                tdb.update_one({'_id': user_data['id']},
                               {'$set': {'high_price': MAX_PRICE}})

            await message.answer(text=set_msg, parse_mode='Markdown')
            await state.set_state(state=None)
        else:
            await message.answer(
                text=Incorrect_price_msg,
                reply_markup=setting_markup,
                parse_mode='Markdown'
            )
    else:
        await message.answer(
            text=Incorrect_price_msg,
            reply_markup=setting_markup,
            parse_mode='Markdown'
        )


async def send_area(message: types.Message, state: FSMContext):
    await message.answer(
        text=area_msg,
        reply_markup=setting_markup,
        parse_mode='Markdown'
    )
    await state.set_state(Sorting.area_sort)


async def set_area(message: types.Message, state: FSMContext):
    await state.update_data(area=message.text.lower())
    await state.update_data(id=message.from_user.id)
    user_data = await state.get_data()
    if "-" in user_data['area']:
        sp = [x.strip() for x in user_data['area'].split("-")]
        if sp[0].isdigit() and sp[1].isdigit() and int(sp[0]) >= int(sp[1]):
            await message.answer(
                text=dif_msg,
                reply_markup=setting_markup,
                parse_mode='Markdown'
            )
        elif not sp[0] and not sp[1]:
            await message.answer(
                text=empty_area_msg,
                reply_markup=setting_markup,
                parse_mode='Markdown'
            )
            await state.set_state(state=None)
        elif (sp[0].isdigit() or not sp[0]) and (sp[1].isdigit() or not sp[1]):
            if sp[0].isdigit():
                await state.update_data(low_area=float(sp[0].strip()))
                user_data = await state.get_data()
                tdb.update_one({'_id': user_data['id']},
                               {'$set': {'low_area': user_data['low_area'],
                                         "active_param": "YES"}
                                })
            if not sp[0]:
                tdb.update_one({'_id': user_data['id']},
                               {'$set': {'low_area': MIN_AREA}
                                })
            if sp[1].isdigit():
                await state.update_data(high_area=float(sp[1].strip()))
                user_data = await state.get_data()
                tdb.update_one({'_id': user_data['id']},
                               {'$set': {'high_area': user_data['high_area'],
                                         "active_param": "YES"}
                                })
            if not sp[1]:
                tdb.update_one({'_id': user_data['id']},
                               {'$set': {'high_area': MAX_AREA}
                                })
            await message.answer(text=set_msg, parse_mode='Markdown')
            await state.set_state(state=None)
        else:
            await message.answer(
                text=Incorrect_area_msg,
                reply_markup=startup_markup,
                parse_mode='Markdown'
            )
    else:
        await message.answer(
            text=Incorrect_area_msg,
            reply_markup=setting_markup,
            parse_mode='Markdown'
        )


async def send_type(message: types.Message, state: FSMContext):
    await message.answer(
        text=type_msg,
        reply_markup=type_markup,
        parse_mode='Markdown'
    )
    await state.set_state(Sorting.type_sort)


async def set_type(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text.lower())
    await state.update_data(id=message.from_user.id)
    user_data = await state.get_data()
    # print(user_data['price'])
    if message.text.lower() in ['квартира', 'апартаменты', 'студия']:
        tdb.update_one({'_id': user_data['id']},
                       {'$set': {'type': user_data['type'],
                                 "active_param": "YES"}
                        })
        await message.answer(text=set_msg, parse_mode='Markdown')
        await state.set_state(state=None)
    else:
        await message.answer(
            text=type_wrong_msg,
            reply_markup=type_markup,
            parse_mode='Markdown'
        )


async def show(message: types.Message, state: FSMContext):
    await state.update_data(id=message.from_user.id)
    user_data = await state.get_data()

    sort_data = tdb.find_one({"_id": user_data['id']})
    low_price = sort_data['low_price']
    high_price = sort_data['high_price']
    low_area = sort_data['low_area']
    high_area = sort_data['high_area']
    typee = sort_data['type']
    data = col.find({"FlatParams.Total_area": {"$gte": low_area, '$lte': high_area},
                     "Price": {"$gte": low_price, '$lte': high_price},
                     'FlatParams.Rooms_number': {'$regex': typee}
                     })

    data_list = list(data)
    FlatCount = len(data_list)
    await message.answer(f"Нашел для тебя {FlatCount} вариантов")
    random_number = 4
    if FlatCount <= 4:
        random_number = FlatCount
    await message.answer(text=f"Показываю по {random_number} квартир", parse_mode='Markdown')
    time.sleep(1)

    for i in random.choices(data_list, k=random_number):
        photo_list = []
        try:
            for filename in os.listdir(f"photos/{i['_id']}"):
                photo_list.append(str(filename))
        except Exception as e:
            with open("logs_bot.txt", "a", encoding="utf8") as file:
                file.write(str(e) + f" нет пути - photos/{i['_id']}\n")
        images = random.choices(photo_list[:10], k=4)
        photo_group = types.MediaGroup()
        for image in images:
            try:
                photo_group.attach_photo(types.InputFile(f"photos/{i['_id']}/{image}"), caption="ere")
            except Exception as e:
                await message.answer(no_image)
                with open("logs_bot.txt", "a", encoding="utf8") as file:
                    file.write(str(e) + f" нет фоток/{i['_id']}\n")
        msg = flat_msg(i)
        await bot.send_media_group(message.from_user.id, media=photo_group)
        await message.answer(msg, parse_mode="Markdown", disable_web_page_preview=True)


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(show, commands=['show'])
    dp.register_message_handler(show_param, filters.Text(equals='show parameters'))

    dp.register_message_handler(send_price, filters.Text(equals='Цена'))
    dp.register_message_handler(set_price, state=Sorting.price_sort)

    dp.register_message_handler(send_area, filters.Text(equals='Общая площадь'))
    dp.register_message_handler(set_area, state=Sorting.area_sort)

    dp.register_message_handler(send_type, filters.Text(equals='Тип жилья'))
    dp.register_message_handler(set_type, state=Sorting.type_sort)

