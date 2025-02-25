from misc.enums.client.callback import ClientMainMenuEnum, ClientBegineMenuEnum
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu_client_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать", callback_data=ClientMainMenuEnum.EARN)],
        [
            InlineKeyboardButton(
                text="Политика", callback_data=ClientMainMenuEnum.POLITIC
            )
        ],
    ]
)

begine_menu_client_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="BetusX - стратегии",
                callback_data=ClientBegineMenuEnum.SHOW_BETUSX_STRATEGY,
            )
        ],
        [
            InlineKeyboardButton(
                text="Xuy - стратегии",
                callback_data=ClientBegineMenuEnum.SHOW_XUY_STRATEGY,
            )
        ],
    ]
)

politic_menu_client_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Я принимаю политику данного сервиса",
                callback_data=ClientMainMenuEnum.ACCEPT_POLITIC,
            )
        ],
        [
            InlineKeyboardButton(
                text="Я не принимаю политику данного сервиса",
                callback_data=ClientMainMenuEnum.DONT_ACCEPT_POLITIC,
            )
        ],
    ]
)
