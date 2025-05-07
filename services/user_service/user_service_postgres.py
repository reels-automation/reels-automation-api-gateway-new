from services.user_service.user_service import UserService
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class UserServicePostgres(UserService):

    async def create_user(self, db: AsyncSession, username: str, email: str) -> User:
        new_user = User(name=username, email=email)
        db.add(new_user)
        await db.flush()      # assign new_user.id
        await db.refresh(new_user)
        return new_user

    async def get_user_by_name(self, db: AsyncSession, username: str) -> User:
        stmt = select(User).filter_by(name=username)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_by_uuid(self, db: AsyncSession, uuid: str) -> User:
        stmt = select(User).filter_by(id=uuid)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User:
        stmt = select(User).filter_by(email=email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_credits(self, db: AsyncSession, uuid: str) -> int:
        user = await self.get_user_by_uuid(db, uuid)
        return user.credits if user else 0

    async def can_make_post(self, db: AsyncSession, uuid: str) -> bool:
        return await self.get_user_credits(db, uuid) > 0

    async def decrease_user_token(self, db: AsyncSession, username: str):
        user = await self.get_user_by_name(db, username)
        if user and user.credits > 0:
            user.credits -= 1
            db.add(user)
            await db.flush()
            await db.refresh(user)

    async def add_user_token(self, db: AsyncSession, uuid: str, amount_of_tokens:int):
        user = await self.get_user_by_uuid(db, uuid)
        print("user: ✅,", user)
        print("before user.credits: ", user.credits)
        if user:
            user.credits += amount_of_tokens
            print("after user.credits: ", user.credits)
            db.add(user)
            await db.flush()
            await db.refresh(user)
