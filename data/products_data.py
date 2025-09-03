from app.models.product_models import ProductCreate, ProductUpdate, ProductResponse

# Base de datos simulada
products_db = []
next_id = 1

def get_all_products():
    return products_db

def get_product_by_id(product_id: int):
    return next((p for p in products_db if p.id == product_id), None)

def create_product(product: ProductCreate):
    global next_id
    new_product = ProductResponse(id=next_id, **product.dict())
    products_db.append(new_product)
    next_id += 1
    return new_product

def update_product(product_id: int, product: ProductUpdate):
    existing = get_product_by_id(product_id)
    if not existing:
        return None
    updated_data = existing.dict()
    for key, value in product.dict(exclude_unset=True).items():
        updated_data[key] = value
    updated_product = ProductResponse(**updated_data)
    products_db[products_db.index(existing)] = updated_product
    return updated_product

def delete_product(product_id: int):
    global products_db
    product = get_product_by_id(product_id)
    if not product:
        return None
    products_db = [p for p in products_db if p.id != product_id]
    return product
