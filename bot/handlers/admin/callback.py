from bot.keyboards.admin.inline_kb import main_menu_admin_kb

from database.manager import ManagerDb

from misc.env import bot, database_url
from misc.enums.admin.callback import AdminMainMenu
from misc.util import StatusQuery
from misc.decorations.admin_dec import basic

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


admin_callback_router = Router(name=__name__)
manager = ManagerDb(database_url)


class StateGroupPromocode(StatesGroup):
    glob_promo = State()


class StateGroupStrateg(StatesGroup):
    photo = State()


@admin_callback_router.callback_query(F.data == AdminMainMenu.CLOSE_PANEL)
async def close_admin_panel_handl(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    await call.message.delete()
    await bot.send_message(chat_id=user_id, text="/admin")


@admin_callback_router.callback_query(F.data == AdminMainMenu.ADD_PROMO)
async def add_new_promo_handl(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(StateGroupPromocode.glob_promo)
    await call.message.edit_text(text="⬇️Напиши новый промокод⬇️")


@admin_callback_router.callback_query(F.data == AdminMainMenu.DELETE_PROMO)
@basic
async def delete_promos_handl(call: CallbackQuery) -> None:
    result: StatusQuery = await manager.delete_promo()
    await call.answer()
    await call.message.edit_text(
        text=f"<i>Новигатор:</i> <b>Главное меню админа</b>\n\n<b>Выходные данные:</b>\n<u>Статус:</u> <b>{result.status}</b>\n<u>Операция</u>: <b>{result.operation}</b>\n<u>Коментарий:</u> <b>{result.comment}</b>",
        reply_markup=main_menu_admin_kb,
    )


@admin_callback_router.callback_query(F.data == AdminMainMenu.SHOW_ACTIVE)
@basic
async def show_activate_promo_handl(call: CallbackQuery) -> None:
    result: StatusQuery = await manager.get_last_glob_promo()
    await call.message.edit_text(
        text=f"<i>Навигатор:</i> <b>Главное меню админа</b>\n\n<b>Выходные данные:</b>\n<u>Статус:</u> <b>{result.status}</b>\n<u>Операция</u>: <b>{result.operation}</b>\n<u>Коментарий:</u> <b>{result.comment}</b>\n<u>Результат:</u> <b>{result.result}</b>",
        reply_markup=main_menu_admin_kb,
    )


@admin_callback_router.callback_query(F.data == AdminMainMenu.ADD_STRATEG)
async def add_new_strateg_handler(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(StateGroupStrateg.photo)
    await call.message.edit_text(text="⬇️Сбрось фоточку)⬇️")
