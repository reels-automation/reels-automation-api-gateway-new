from services.roles_service.roles_service import RolesService
from models.roles import Roles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class RolesServicePostgres(RolesService):

    async def add_role(self, db: AsyncSession, role_name: str):
        new_role = Roles(name=role_name)
        async with db.begin():
            db.add(new_role)
        await db.refresh(new_role)

    async def delete_role(self, db: AsyncSession):
        pass

    async def update_role(self, db: AsyncSession):
        pass

    async def get_role_by_name(self, db: AsyncSession, role: str):
        stmt = select(Roles).where(Roles.name == role)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        return user.id if user else None

    async def get_role_name_by_uuid(self, db: AsyncSession, uuid: str) -> str:
        stmt = select(Roles).where(Roles.id == uuid)
        result = await db.execute(stmt)
        role = result.scalar_one_or_none()
        return role.name if role else None

    async def get_premium_roles(self, db: AsyncSession) -> list:
        return ["Admin"]
