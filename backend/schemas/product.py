from pydantic import BaseModel, Field, field_validator
from typing import Optional
from decimal import Decimal
from typing_extensions import Annotated


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2, gt=0)]
    stock: int = Field(..., ge=0)
    category: Optional[str] = None
    image: Optional[str] = None

class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[Annotated[Decimal, Field(max_digits=10, decimal_places=2, gt=0)]] = None
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    image: Optional[str] = None


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
