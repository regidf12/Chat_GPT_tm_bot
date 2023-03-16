from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from config import CHAT_ID


class IsAdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(CHAT_ID, message.from_user.id)
        return member.is_chat_admin()
