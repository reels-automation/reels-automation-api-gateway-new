from services.user_service.user_service import UserService
from models.passwords import UserPassword
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class PasswordServicePostgres(UserService):
    
    async def create_password(self, db: AsyncSession, user_id: str, password: str):
        hashed_password = generate_password_hash(password)
        new_password = UserPassword(user_id=user_id, password_hash=hashed_password)

        async with db.begin():
            db.add(new_password)

    async def _get_password_by_user(self, db: AsyncSession, user_uuid: str):
        stmt = select(UserPassword).filter_by(user_id=user_uuid)
        result = await db.execute(stmt)
        password = result.scalar_one_or_none()
        return password.password_hash if password else None

    async def is_same_password(self, db: AsyncSession, user_id: str, password: str) -> bool:
        user_password = await self._get_password_by_user(db, user_id)
        return check_password_hash(user_password, password) if user_password else False
