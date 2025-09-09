from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


# Fetch all products
async def get_all_products(db: AsyncSession) -> List[Product]:
    result = await db.execute(select(Product))
    return result.scalars().all()


# Search products by name (case-insensitive)
async def search_products_by_name(db: AsyncSession, name: str) -> List[Product]:
    result = await db.execute(
        select(Product)
        .filter(Product.name.ilike(f"%{name}%"))
    )
    return result.scalars().all()


# Create one or more products (bulk insert supported)
async def create_products(db: AsyncSession, products: List[ProductCreate]) -> List[Product]:
    db_products = [Product(**p.model_dump()) for p in products]
    try:
        db.add_all(db_products)
        await db.commit()
        # Refresh each product to get auto-generated fields (like id)
        for product in db_products:
            await db.refresh(product)
        return db_products
    except IntegrityError as e:  #duplicate SKU
        await db.rollback()
        logger.error(f"Integrity error while creating products: {e}")
        raise
    except SQLAlchemyError as e:  # any other DB error
        await db.rollback()
        logger.error(f"Database error while creating products: {e}")
        raise


# Update product by id; returns None if not found
async def update_product(db: AsyncSession, product_id: int, product_in: ProductUpdate) -> Optional[Product]:
    result = await db.execute(select(Product).filter(Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        return None

    # Update only fields that were provided (exclude_unset=True)
    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)

    try:
        await db.commit()
        await db.refresh(db_product)
        return db_product
    except IntegrityError as e:  #SKU conflict
        await db.rollback()
        logger.error(f"Integrity error while updating product {product_id}: {e}")
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error while updating product {product_id}: {e}")
        raise


# Delete product by id; returns True if deleted, False if not found
async def delete_product(db: AsyncSession, product_id: int) -> bool:
    result = await db.execute(select(Product).filter(Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        return False

    try:
        await db.delete(db_product)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Failed to delete product {product_id}: {e}")
        raise
