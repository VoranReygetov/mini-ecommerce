from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from core.config import settings

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=engine)

class Base(DeclarativeBase):
    """Base for all ORM models"""
    pass

#Init db tables in main
async def init_db():

    import models.product
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Async dependency to get a DB session
async def get_db():

    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()