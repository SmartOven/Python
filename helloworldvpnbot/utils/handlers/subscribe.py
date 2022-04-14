from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.state import State, StatesGroup

import datetime
from datetime import timedelta

from utils.locals.data.keyboards import *
from utils.locals.data.subscription_options import prices, subscription_durations
from utils.locals.data.admins import admin_chat_id
from utils.locals.data.bot_init import bot

from utils.messages.subscribe import *

from utils.locals.data.users import users, save_users


# States map:
#
# /subscribe
# State=None
# Subscribed? -> Yes: State=Renew -> Want to renew your subscription? -> Yes: State=Choose subscription duration
#                                                                     ->  No: State=Finish()
#             ->  No: State=Choose server -> State=Choose subscription duration

class SubscribeUserFSM(StatesGroup):
    choose_server = State()                     # Choose server
    choose_subscription_duration = State()      # Choose subscription duration
    renew_subscription = State()                # Renew existing subscription


# /subscribe
# State = None
# Making new user if it doesn't already exist, going to state Choose server
async def register_user_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        username = str(message.from_user.username)
        if username in users:
            # If it does exist - asking if he wants to renew the subscription
            await message.reply(user_already_exist_message)
            # TODO state renew instead of "error" message
        else:
            # Making new user in memory storage
            data[username] = {
                'user_id': message.from_user.id,
                'login': '',
                'password': '',
                'server': '',
                'exp_year': -1,
                'exp_month': -1,
                'exp_day': -1,
                'price': prices['default'],
                'paid': 0
            }

            # Setting Choose server state
            await SubscribeUserFSM.choose_server.set()

            # Answering user
            await message.answer(register_user_message, reply_markup=types.ReplyKeyboardRemove())
            await message.answer(choose_server_message, reply_markup=servers_keyboard)


# TODO add /renew handler

# State = Choose server
# Choosing server, going to state Choose subscription duration
async def choose_server_handler(message: types.Message, state: FSMContext):
    # Checking if server is in list
    if message.text in servers_texts:
        username = str(message.from_user.username)
        async with state.proxy() as data:
            # Setting server for user in memory storage
            data[username]['server'] = message.text

        # Setting Choose subscription duration state
        await SubscribeUserFSM.choose_subscription_duration.set()

        # Answering user
        await message.reply(choose_subscription_duration_message, reply_markup=subscription_durations_keyboard)
    else:
        await message.reply(not_an_option_message)


# State = Choose subscription duration
# Choosing subscription duration, going to finish state
async def choose_subscribe_duration_handler(message: types.Message, state: FSMContext):
    if message.text in subscription_durations_texts:
        username = str(message.from_user.username)
        async with state.proxy() as data:
            if data[username]['exp_year'] == -1:
                # If its new subscription
                now = datetime.datetime.now()
            else:
                # If its renewing subscription
                now = datetime.date(data[username]['exp_year'], data[username]['exp_month'], data[username]['exp_day'])

            # Counting expiration date
            delta = timedelta(days=subscription_durations[message.text])
            expiration_date = now + delta

            # Setting expiration date in memory storage
            data[username]['exp_year'] = int(expiration_date.year)
            data[username]['exp_month'] = int(expiration_date.month)
            data[username]['exp_day'] = int(expiration_date.day)
            users[username] = data[username]

        # Saving users
        save_users(users)

        # Sending alert message in admins chat
        await bot.send_message(admin_chat_id, f"{username} : ожидается оплата")

        # Answering user
        price = users[username]['price']
        await message.reply(f"Пожалуйста, оплатите подписку по кнопке ниже.\nСтоимость: {price} руб")
        await message.answer(payment_requisites, reply_markup=payment_inline_keyboard)

        # Setting finish state
        await state.finish()
    else:
        await message.reply(not_an_option_message)


# /cancel
# Cancelling operation (setting State=None) if user had chosen "Cancel" or written /cancel
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.reply(operation_canceled_message, reply_markup=types.ReplyKeyboardRemove())


def register_handlers_subscribe(_dp: Dispatcher):
    # State=None
    # /subscribe
    _dp.register_message_handler(register_user_handler, commands=['subscribe'], state=None)

    # State=* (any state)
    # Setting any state into State=None if its cancelled
    _dp.register_message_handler(cancel_handler, commands=['cancel'], state="*")
    _dp.register_message_handler(cancel_handler, filters.Text(contains=['Отмена']), state="*")

    # Subscribing states handlers
    _dp.register_message_handler(choose_server_handler, content_types=['text'], state=SubscribeUserFSM.choose_server)
    _dp.register_message_handler(choose_subscribe_duration_handler, content_types=['text'], state=SubscribeUserFSM.choose_subscription_duration)
