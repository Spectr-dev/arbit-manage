from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage


class BaseSett(BaseSettings):
    token: str
    admin_ids: List[int]
    database_url: str

    ref_link: str = "https://xplinks.cc/krgUI"

    model_config = SettingsConfigDict(env_file="./misc/.env")


s = BaseSett()

bot = Bot(token=s.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

database_url = s.database_url
ref = s.ref_link
