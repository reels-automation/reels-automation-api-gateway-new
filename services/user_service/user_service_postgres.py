from services.user_service.user_service import UserService
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class UserServicePostgres(UserService):

    async def create_user(self, db: AsyncSession, username: str, email: str) -> User:
        new_user = User(name=username, email=email)
        async with db.begin():
            db.add(new_user)
        await db.refresh(new_user)
        return new_user

    async def get_user_by_name(self, db: AsyncSession, username: str) -> User:
        stmt = select(User).filter_by(name=username)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_credits(self, db: AsyncSession, username: str) -> int:
        user = await self.get_user_by_name(db, username)
        return user.credits if user else 0

    async def can_make_post(self, db: AsyncSession, username: str) -> bool:
        return await self.get_user_credits(db, username) > 0

    async def decrease_user_token(self, db: AsyncSession, username: str):
        user = await self.get_user_by_name(db, username)
        if user and user.credits > 0:
            user.credits -= 1
            async with db.begin():
                db.add(user)
            await db.refresh(user)
