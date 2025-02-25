from misc.env import database_url, ref, bot
from misc.enums.client.callback import ClientMainMenuEnum, ClientBegineMenuEnum
from misc.enums.texts import ClientTextsEnum

from database.manager import ManagerDb

from bot.keyboards.client.inline_kb import (
    politic_menu_client_kb,
    main_menu_client_kb,
    begine_menu_client_kb,
)

from aiogram import F, Router
from aiogram.types import CallbackQuery


manager = ManagerDb(url=database_url)

client_callback_router = Router(name=__name__)


@client_callback_router.callback_query(F.data == ClientMainMenuEnum.EARN)
async def earn_callback_handler(call: CallbackQuery) -> None:
    status = await manager.get_polic_status(id=str(call.from_user.id))
    if status is True or status is None:
        await manager.update_polic_status(id=str(call.from_user.id), status=True)
        await call.message.edit_text(
            text=ClientTextsEnum.ERNE_WARR_TEXT + f"<b>{ref}</b>",
            reply_markup=begine_menu_client_kb,
        )

    else:
        await call.message.edit_text(
            text="Чтобы продолжить нужно согласиться с политикой данного сервиса",
            reply_markup=main_menu_client_kb,
        )


@client_callback_router.callback_query(F.data == ClientMainMenuEnum.POLITIC)
async def get_politic_handler(call: CallbackQuery) -> None:
    await call.message.edit_text(
        text=ClientTextsEnum.POLICE_TEXT, reply_markup=politic_menu_client_kb
    )


@client_callback_router.callback_query(F.data == ClientMainMenuEnum.ACCEPT_POLITIC)
async def accept_poliric_handler(call: CallbackQuery) -> None:
    await manager.update_polic_status(id=str(call.from_user.id), status=True)
    await call.message.edit_text(
        text=ClientTextsEnum.WELLCOME_TEXT, reply_markup=main_menu_client_kb
    )


@client_callback_router.callback_query(F.data == ClientMainMenuEnum.DONT_ACCEPT_POLITIC)
async def dont_accept_polic_handler(call: CallbackQuery) -> None:
    await manager.update_polic_status(id=str(call.from_user.id), status=False)
    await call.message.edit_text(
        text=ClientTextsEnum.WELLCOME_TEXT, reply_markup=main_menu_client_kb
    )


@client_callback_router.callback_query(
    F.data == ClientBegineMenuEnum.SHOW_BETUSX_STRATEGY
)
async def show_strategy_handler(call: CallbackQuery) -> None:
    result: str | bool = await manager.user_access(id=str(call.from_user.id))
    if type(result) == bool:
        if result is True:
            result = await manager.get_strategs(id=str(call.from_user.id))
            if result == False:
                await call.answer(text="На сегодня стратегия уже была", show_alert=True)
            elif type(result) is str:
                user_id = call.from_user.id
                await call.message.delete()
                await bot.send_photo(
                    chat_id=user_id,
                    caption="<b>Возвращайтесь завтра</b> за новой стратегией",
                    photo=result,
                    reply_markup=begine_menu_client_kb,
                )
