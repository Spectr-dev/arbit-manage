from bot.handlers.admin.callback import StateGroupPromocode, StateGroupStrateg
from bot.keyboards.admin.inline_kb import main_menu_admin_kb
from bot.middlewares.admin_midd import HeIsAdmin

from database.manager import ManagerDb
from database.models import Panel

from misc.env import database_url
from misc.util import StatusQuery

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


admin_fsm_router = Router(name=__name__)
admin_fsm_router.message(HeIsAdmin())
manager = ManagerDb(url=database_url)


@admin_fsm_router.message(F.text, StateGroupPromocode.glob_promo)
async def get_new_promo(mess: Message, state: FSMContext) -> None:
    await state.update_data(glob_promo=mess.text)
    data = await state.get_data()
    promo: StatusQuery = await manager.add_new_promo(
        panel=Panel(glob_promo=data.get("glob_promo"))
    )
    await state.clear()

    await mess.answer(
        text=f"<i>Новигатор:</i> <b>Главное меню админа</b>\n\n<b>Выходные данные:</b>\n<u>Статус:</u> ✅<b>{promo.status}</b>\n<u>Операция</u>: <b>{promo.operation}</b>\n<u>Комментарий:</u> <b>{promo.comment}</b>",
        reply_markup=main_menu_admin_kb,
    )


@admin_fsm_router.message(F.photo, StateGroupStrateg.photo)
async def get_new_starteg(mess: Message, state: FSMContext) -> None:
    photo_id = mess.photo[-1].file_id
    await state.update_data(pool_strateg=photo_id)
    await manager.add_new_strateg(photo=str(photo_id))
    await state.clear()
