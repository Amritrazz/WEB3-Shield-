import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.models import Base

# Armed with your true Docker fallback parameters
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:password123@localhost:5432/web3_shield"
)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    """Initializes the database connection matrix and creates tables if missing."""
    async with engine.begin() as conn:
        print("[Database Engine] Booting connection matrices and structural schemas...")
        await conn.run_sync(Base.metadata.create_all)
    print("[Database Engine] PostgreSQL structural tables verified/created successfully.")