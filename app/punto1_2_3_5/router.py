from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# ----- MODELOS -----
class Product(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# ----- BASE DE DATOS EN MEMORIA -----
products_db: List[Product] = [
    Product(id=1, name="Manzana", price=1.5, description="Fruta fresca"),
    Product(id=2, name="Pera", price=2.0, description="Verde y jugosa"),
]

# ----- ENDPOINTS -----
@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/products", response_model=List[Product])
def get_products():
    return products_db

@router.get("/products/search", response_model=List[Product])
def search_products(name: Optional[str] = Query(None, min_length=1)):
    if not name:
        raise HTTPException(status_code=400, detail="Debes ingresar un nombre")
    results = [p for p in products_db if name.lower() in p.name.lower()]
    if not results:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return results

@router.post("/products", response_model=Product)
def create_product(product: ProductCreate):
    new_id = max(p.id for p in products_db) + 1 if products_db else 1
    new_product = Product(id=new_id, **product.dict())
    products_db.append(new_product)
    return new_product

@router.get("/categories", response_model=List[str])
def get_categories():
    return ["Frutas", "Verduras", "Lácteos"]