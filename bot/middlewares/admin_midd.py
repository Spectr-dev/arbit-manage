from misc.env import s

from typing import Awaitable, Callable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, User


class HeIsAdmin(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        return await handler(event, data) if user.id in s.admin_ids else None
