from aiogram import Dispatcher, types
from Menu.markups import startup_markup, setting_markup
from bot_init import dp
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from Menu.phrases import about_flatty_msg, welcome_msg, help_msg, settings_msg, back_msg


async def send_welcome(message: types.Message):
    await message.answer(
        text=welcome_msg,
        reply_markup=startup_markup,
        parse_mode='Markdown'
    )


async def back(message: types.Message):
    await message.answer(
        text=back_msg,
        reply_markup=startup_markup,
        parse_mode='Markdown'
    )


async def send_help(message: types.Message, state: FSMContext):
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
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])
    dp.register_message_handler(about_flatty, commands=['about'])
    dp.register_message_handler(back, commands=['back'])
    dp.register_message_handler(settings, filters.Text(equals='settings'))
