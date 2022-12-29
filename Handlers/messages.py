from aiogram import Dispatcher, types
from Menu.markups import startup_markup, setting_markup
from bot_init import dp
from db import *
from Default_values import *
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from Menu.phrases import about_flatty_msg, welcome_msg, help_msg, settings_msg, back_msg


async def start_bot(message: types.Message, state: FSMContext):
    await message.answer(
        text=welcome_msg,
        reply_markup=startup_markup,
        parse_mode='Markdown'
    )
    await state.update_data(id=message.from_user.id)
    user_data = await state.get_data()
    user_init(user_data['id'])


async def back(message: types.Message):
    await message.answer(
        text=back_msg,
        reply_markup=startup_markup,
        parse_mode='Markdown'
    )


async def send_help(message: types.Message):
    await message.answer(
        text=help_msg,
        reply_markup=startup_markup,
        parse_mode='Markdown'
    )


async def about_flatty(message: types.Message):
    await message.answer(
        text=about_flatty_msg,
        reply_markup=startup_markup,
        parse_mode='Markdown'
    )


async def settings(message: types.Message):
    await message.answer(
        text=settings_msg,
        reply_markup=setting_markup,
        parse_mode='Markdown'
    )


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])
    dp.register_message_handler(about_flatty, commands=['about'])
    dp.register_message_handler(back, commands=['back'])
    dp.register_message_handler(settings, filters.Text(equals='settings'))
