from asyncio import run

from database.manager import init_database
from bot.handlers.client.message import client_router
from bot.handlers.client.callback import client_callback_router
from bot.handlers.admin.message import admin_router
from bot.handlers.admin.callback import admin_callback_router
from bot.handlers.admin.fsm import admin_fsm_router

from misc.env import dp, bot, database_url


async def get_to_work() -> None:
    await init_database(database_url)

    dp.include_routers(
        client_router,
        client_callback_router,
        admin_router,
        admin_callback_router,
        admin_fsm_router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main=get_to_work())
