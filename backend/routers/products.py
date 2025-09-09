from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.session import AsyncSessionLocal
from crud import product as crud
from schemas.product import ProductCreate, ProductUpdate, ProductOut
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

router = APIRouter(prefix="/products", tags=["products"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/", response_model=List[ProductOut])
async def list_products(
    db: AsyncSession = Depends(get_db)
):
    try:
        return await crud.get_all_products(db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

@router.get("/search", response_model=List[ProductOut])
async def search_products(
    name: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    try:
        results = await crud.search_products_by_name(db, name)
        if not results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No products found"
            )
        return results
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

@router.post("/", response_model=List[ProductOut], status_code=status.HTTP_201_CREATED)
async def create_products(
    products: list[ProductCreate] | ProductCreate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    # Normalize single object to list
    if isinstance(products, ProductCreate):
        products = [products]
    
    try:
        created_products = await crud.create_products(db, products)
        return created_products
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product already exists or invalid data"
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create products"
        )

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int, 
    product_in: ProductUpdate, 
    db: AsyncSession = Depends(get_db)
):
    try:
        updated = await crud.update_product(db, product_id, product_in)
        if not updated:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invalid data provided"
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product"
        )

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, 
    db: AsyncSession = Depends(get_db)
):
    try:
        ok = await crud.delete_product(db, product_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Product not found")
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product"
        )