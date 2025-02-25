from misc.enums.admin.callback import AdminMainMenu

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu_admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Добавить промокод", callback_data=AdminMainMenu.ADD_PROMO
            ),
            InlineKeyboardButton(
                text="Активный промо", callback_data=AdminMainMenu.SHOW_ACTIVE
            ),
        ],
        [
            InlineKeyboardButton(
                text="Удалить промокоды", callback_data=AdminMainMenu.DELETE_PROMO
            ),
        ],
        [
            InlineKeyboardButton(
                text="Добавить новы=ую стратегию",
                callback_data=AdminMainMenu.ADD_STRATEG,
            )
        ],
        [
            InlineKeyboardButton(
                text="❌Закрыть❌", callback_data=AdminMainMenu.CLOSE_PANEL
            )
        ],
    ]
)
