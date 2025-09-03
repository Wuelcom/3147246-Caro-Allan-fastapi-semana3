from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from data.products_data import products_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[dict])
def get_products():
    return products_db

@router.get("/search", response_model=List[dict])
def search_products(
    name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """Buscar productos por nombre y rango de precio"""
    results = products_db.copy()

    if name:
        name_lower = name.lower().strip()
        if len(name_lower) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El término de búsqueda debe tener al menos 2 caracteres"
            )
        results = [p for p in results if name_lower in p["name"].lower()]

    if min_price is not None:
        if min_price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio mínimo no puede ser negativo"
            )
        results = [p for p in results if p["price"] >= min_price]

    if max_price is not None:
        if max_price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio máximo no puede ser negativo"
            )
        results = [p for p in results if p["price"] <= max_price]

    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio mínimo no puede ser mayor al máximo"
        )

    return results
