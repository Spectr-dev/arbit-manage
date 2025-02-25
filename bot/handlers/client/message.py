from misc.enums.texts import ClientTextsEnum

from bot.keyboards.client.inline_kb import main_menu_client_kb

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart

client_router = Router(name=__name__)


@client_router.message(CommandStart())
async def comm_start(mess: Message) -> None:
    await mess.answer(
        text=ClientTextsEnum.WELLCOME_TEXT,
        reply_markup=main_menu_client_kb,
    )
