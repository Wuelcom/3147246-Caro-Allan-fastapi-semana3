from fastapi import FastAPI

app = FastAPI(title="My First API")

# ANTES (Semana 1)
@app.get("/")
def hello_world():
    return {"message": "My first FastAPI!"}

# DESPUÉS (con type hints)
@app.get("/")
def hello_world() -> dict:
    return {"message": "My first FastAPI!"}

# Si tenías endpoint con parámetro
@app.get("/greeting/{name}")
def greet_user(name: str) -> dict:
    return {"greeting": f"Hello {name}!"}

# Endpoint con múltiples parámetros
@app.get("/calculate/{num1}/{num2}")
def calculate(num1: int, num2: int) -> dict:
    result = num1 + num2
    return {"result": result, "operation": "sum"}



from typing import List, Dict

# Lista de strings
@app.get("/fruits")
def get_fruits() -> List[str]:
    return ["apple", "banana", "orange"]

# Lista de números
@app.get("/numbers")
def get_numbers() -> List[int]:
    return [1, 2, 3, 4, 5]

# Diccionario con estructura conocida
@app.get("/user/{user_id}")
def get_user(user_id: int) -> Dict[str, str]:
    return {
        "id": str(user_id),
        "name": "Demo User",
        "email": "demo@example.com"
    }

from pydantic import BaseModel

# Definir QUÉ datos esperas
class User(BaseModel):
    name: str
    age: int
    email: str

@app.post("/users")
def create_user(user: User):
    # Pydantic garantiza que los datos son correctos
    return {"user": user.dict()}

from pydantic import BaseModel

app = FastAPI(title="My API with Pydantic")

# Tu primer modelo de datos
class Product(BaseModel):
    name: str
    price: int  # en centavos para evitar decimales
    available: bool = True  # valor por defecto

# Lista temporal para guardar productos
products = []

# Endpoint GET (como antes)
@app.get("/")
def hello_world() -> dict:
    return {"message": "API with Pydantic!"}

# NUEVO: Endpoint POST con Pydantic
@app.post("/products")
def create_product(product: Product) -> dict:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)
    return {"message": "Product created", "product": product_dict}

# Endpoint para ver todos los productos
@app.get("/products")
def get_products() -> dict:
    return {"products": products, "total": len(products)}


# Parámetro de ruta simple
@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    return {"error": "Product not found"}

# Múltiples parámetros de ruta
@app.get("/categories/{category}/products/{product_id}")
def product_by_category(category: str, product_id: int) -> dict:
    return {
        "category": category,
        "product_id": product_id,
        "message": f"Searching product {product_id} in {category}"
    }

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    available: bool
    message: str = "Product retrieved successfully"

class ProductListResponse(BaseModel):
    products: list
    total: int
    message: str = "List retrieved successfully"



from typing import Optional

# Query parameters opcionales
@app.get("/search")
def search_products(
    name: Optional[str] = None,
    max_price: Optional[int] = None,
    available: Optional[bool] = None
) -> dict:
    results = products.copy()

    if name:
        results = [p for p in results if name.lower() in p["name"].lower()]
    if max_price:
        results = [p for p in results if p["price"] <= max_price]
    if available is not None:
        results = [p for p in results if p["available"] == available]

    return {"results": results, "total": len(results)}

@app.get("/products", response_model=ProductListResponse)
def get_products() -> ProductListResponse:
    return ProductListResponse(
        products=products,
        total=len(products)
    )

@app.post("/products", response_model=ProductResponse)
def create_product(product: Product) -> ProductResponse:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)

    return ProductResponse(
        id=product_dict["id"],
        name=product_dict["name"],
        price=product_dict["price"],
        available=product_dict["available"],
        message="Product created successfully"
    )
