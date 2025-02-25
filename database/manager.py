from datetime import datetime, timedelta

from database.models import Base, User, Panel, Strategy
from misc.util import StatusQuery
from misc.decorations.admin_dec import connection

from rich import print as pp

from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


class ManagerDb:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url=url)
        self.async_session = async_sessionmaker(bind=self.engine, class_=AsyncSession)

    async def create_or_connect(self) -> None:
        try:
            async with self.engine.connect() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as __e:
            pp(f"[red bold]Error:[/] [red]{__e}[/]")

    @connection
    async def add_user(self, session: AsyncSession, user: User) -> None:
        session.add(user)
        return

    @connection
    async def check_user(self, session: AsyncSession, id: str) -> bool:
        result = await session.execute(select(User).where(User.telegram_id == id))
        return result.scalar_one_or_none() is not None

    async def check_user_and_register(self, id: str) -> None:
        result = await self.check_user(id=id)
        if result:
            return
        else:
            await self.add_user(user=User(telegram_id=id))

    @connection
    async def add_new_promo(self, session: AsyncSession, panel: Panel) -> StatusQuery:
        session.add(panel)
        return StatusQuery()

    @connection
    async def get_last_glob_promo(self, session: AsyncSession) -> StatusQuery:
        result = await session.execute(
            select(Panel).order_by(Panel.glob_promo.desc()).limit(1)
        )
        obj_panel = result.scalar_one_or_none()
        try:
            if obj_panel.glob_promo is not None:
                return StatusQuery(result=obj_panel.glob_promo)
        except AttributeError:
            return StatusQuery(result="Промокодов нет")

    @connection
    async def delete_promo(self, session: AsyncSession) -> StatusQuery:
        last_promo = (
            select(Panel.id).order_by(Panel.id.desc()).limit(1).scalar_subquery()
        )
        stmt = delete(Panel).where(Panel.id != last_promo)
        await session.execute(stmt)
        return StatusQuery()

    @connection
    async def update_polic_status(
        self, session: AsyncSession, id: str, status: bool
    ) -> None:
        await self.check_user_and_register(id=id)
        await session.execute(
            update(User).where(User.telegram_id == id).values(status_polic=status)
        )

    @connection
    async def get_polic_status(self, session: AsyncSession, id: str) -> bool | None:
        user = await self.check_user(id=id)
        if user:
            result = await session.execute(
                select(User.status_polic).where(User.telegram_id == id)
            )
            status = result.scalar_one_or_none()
            return status
        elif user is False:
            await self.add_user(user=User(telegram_id=id))
            result = await session.execute(
                select(User.status_polic).where(User.telegram_id == id)
            )
            status = result.scalar_one_or_none()
            return status

    @connection
    async def user_access(self, session: AsyncSession, id: str) -> bool | str:
        result = await session.execute(select(User).where(User.telegram_id == id))
        user = result.scalar_one_or_none()
        if user is None:
            return "Доступ закрыт"

        now = datetime.now()
        reg_time = user.time_reg

        if reg_time is not None and now - reg_time > timedelta(seconds=10):
            return True
        else:
            return "Для того чтобы получать от нас готовые стратегии, необходимо сделать 50 прокруток"

    @connection
    async def get_strategs(self, session: AsyncSession, id: str) -> str | None | bool:
        result = await session.execute(select(User).where(User.telegram_id == id))
        user = result.scalar_one_or_none()

        if user is None:
            print("Пользователь не найден")
            return None

        now = datetime.now()
        if (
            user.last_strategy_time is not None
            and now - user.last_strategy_time < timedelta(seconds=40)
        ):
            return False

        if user.last_strategy_id is None:
            stmt = select(Strategy).order_by(Strategy.id).limit(1)
        else:
            stmt = (
                select(Strategy)
                .where(Strategy.id > user.last_strategy_id)
                .order_by(Strategy.id)
                .limit(1)
            )

        result = await session.execute(statement=stmt)
        strategy = result.scalar_one_or_none()

        if strategy is None:
            result = await session.execute(
                select(Strategy).order_by(Strategy.id).limit(1)
            )
            strategy = result.scalar_one_or_none()

        if strategy is None:
            return None

        user.last_strategy_id = strategy.id
        user.last_strategy_time = now

        return strategy.pool_strateg

    @connection
    async def add_new_strateg(self, session: AsyncSession, photo: str) -> None:
        await session.execute(insert(Strategy).values(pool_strateg=photo))


async def init_database(url: str) -> None:
    manager = ManagerDb(url)
    await manager.create_or_connect()
    del manager
