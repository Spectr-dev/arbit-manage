from functools import wraps
from typing import Any

from misc.util import StatusQuery

from rich import print as pp

from aiogram.exceptions import TelegramBadRequest

from sqlalchemy.exc import IntegrityError

oper_tools = {
    "add_new_promo": ["Добавление промокода", "✅Промокод успешно добавлен"],
    "get_last_glob_promo": [
        "Просмотр действующего промокод",
        "✅Действующий промокод активный",
    ],
    "delete_promo": [
        "Отчистка стека промокодов",
        "✅Я обнулил все промокоды, кроме последнего",
    ],
    "add_referal_link": [
        "Установка новой реферальной ссылки",
        "✅ Ссылка успешно установленна",
    ],
}


def basic(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except TelegramBadRequest:
            ...
        except Exception as __e:
            pp(
                f"[yellow bold]Warning:[/] [yellow]{__e}[/]\n\n[bold green]Summarize:[/] [green]An attempt was made to write new data to the table, but the new entry violated the `unique=True` instruction[/]"
            )

    return wrapper


def connection(method):
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        async with self.async_session() as session:
            try:
                result: StatusQuery | Any = await method(self, session, *args, **kwargs)

                name_operation: str = method.__name__

                if name_operation in oper_tools:
                    operation, comment = oper_tools[name_operation]
                    result.operation = operation
                    result.comment = comment

                await session.commit()
                return result
            except IntegrityError as __e:
                await session.rollback()
                pp(
                    f"[yellow bold]Warning:[/] [yellow]{__e}[/]\n\n[bold green]Summarize:[/] [green]An attempt was made to write new data to the table, but the new entry violated the `unique=True` instruction[/]"
                )
            except Exception as __e:
                await session.rollback()
                pp(
                    f"[yellow bold]Warning:[/] [yellow]{__e}[/]\n\n[bold green]Summarize:[/] [green]An attempt was made to write new data to the table, but the new entry violated the `unique=True` instruction[/]"
                )
            finally:
                await session.close()

    return wrapper
