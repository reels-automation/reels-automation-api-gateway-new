from services.user_roles_service.user_roles_service import UserRolesService
from models.roles import UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class UserRolesServicePostgres(UserRolesService):

    async def create_user_role(self, db: AsyncSession, role_uuid: str, user_uuid: str) -> str:
        new_role = UserRole(user_id=user_uuid, role_id=role_uuid)
        async with db.begin():
            db.add(new_role)
        await db.refresh(new_role)
        return new_role.id

    async def get_role_from_user_uuid(self, db: AsyncSession, user_uuid: str) -> UserRole:
        stmt = select(UserRole).where(UserRole.user_id == user_uuid)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
