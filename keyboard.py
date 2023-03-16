from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

group = InlineKeyboardButton('DarkHub', url="https://t.me/Dark_Hub_info")
buy_follow = InlineKeyboardButton('Купить подписку', callback_data='get_follower')

kb_sub = InlineKeyboardMarkup().add(group)
kb_follow = InlineKeyboardMarkup().add(buy_follow)
