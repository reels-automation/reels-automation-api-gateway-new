import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Configuración básica pero más robusta del engine
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Esto verifica que la conexión esté activa antes de usarla
    pool_recycle=300,  # Recicla conexiones después de 5 minutos (300 segundos)
    connect_args={
        "ssl": True,
        "server_settings": {
            "idle_in_transaction_session_timeout": "30000"  # 30 segundos
        },
    },
)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()  # Asegura que la sesión siempre se cierre
