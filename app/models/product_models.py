# app/models/product_models.py
from pydantic import BaseModel
from typing import Optional

# Modelo base con los campos principales
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

# Para crear un producto (lo mismo que el base)
class ProductCreate(ProductBase):
    pass

# Para actualizar un producto (los campos pueden ser opcionales)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

# Respuesta que devuelve el API
class ProductResponse(ProductBase):
    id: int
