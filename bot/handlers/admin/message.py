from bot.middlewares.admin_midd import HeIsAdmin
from bot.keyboards.admin.inline_kb import main_menu_admin_kb
from misc.env import bot

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

admin_router = Router(name=__name__)
admin_router.message.middleware(HeIsAdmin())


@admin_router.message(Command("admin"))
async def comm_admin(mess: Message) -> None:
    user_id = mess.from_user.id
    await mess.delete()
    await bot.send_message(
        chat_id=user_id,
        text="Привет, админ. Чего воротить сегодня будем?",
        reply_markup=main_menu_admin_kb,
    )
