main 1 --------------------------------------------------------------------------------------------------------------------------------------------

from fastapi import FastAPI, HTTPException, Query, Path, status
from models.product_models import ProductCreate, ProductUpdate, ProductResponse, ProductList, CategoryEnum
from data.products_data import get_all_products, get_product_by_id, create_product, update_product, delete_product, filter_products

app = FastAPI(
    title="API de Inventario - Semana 3",
    description="API REST completa para manejo de productos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 🏠 Root endpoint
@app.get("/")
async def root():
    return {"message": "API de Inventario - Semana 3", "docs": "/docs"}

# 📖 GET todos los productos (con filtros y paginación)
@app.get("/products", response_model=ProductList)
async def get_products(
    category: CategoryEnum | None = Query(None),
    in_stock: bool | None = Query(None),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None)
):
    products = filter_products(
        category=category.value if category else None,
        in_stock=in_stock,
        min_price=min_price,
        max_price=max_price
    )

    if search:
        products = [p for p in products if search.lower() in p["name"].lower()]

    total = len(products)
    start, end = (page - 1) * page_size, page * page_size
    return ProductList(products=products[start:end], total=total, page=page, page_size=page_size)

# 📖 GET producto por ID
@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int = Path(..., gt=0)):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(404, f"Producto {product_id} no encontrado")
    return ProductResponse(**product)

# ➕ POST crear producto
@app.post("/products", response_model=ProductResponse, status_code=201)
async def create_new_product(product: ProductCreate):
    if any(p["name"].lower() == product.name.lower() for p in get_all_products()):
        raise HTTPException(409, f"Ya existe producto '{product.name}'")
    return ProductResponse(**create_product(product.dict()))

# ✏️ PUT actualizar producto
@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_existing_product(product_id: int, product: ProductUpdate):
    existing = get_product_by_id(product_id)
    if not existing:
        raise HTTPException(404, f"Producto {product_id} no encontrado")
    if any(p["id"] != product_id and p["name"].lower() == product.name.lower() for p in get_all_products()):
        raise HTTPException(409, f"Ya existe producto '{product.name}'")
    return ProductResponse(**update_product(product_id, product.dict()))

# ❌ DELETE eliminar producto
@app.delete("/products/{product_id}", status_code=204)
async def delete_existing_product(product_id: int):
    if not get_product_by_id(product_id):
        raise HTTPException(404, f"Producto {product_id} no encontrado")
    delete_product(product_id)
    return None




main 2 --------------------------------------------------------------------------------------------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel, field_validator, model_validator

app = FastAPI()

# -----------------------------
# MODELO DE USUARIO
# -----------------------------
class User(BaseModel):
    id: int
    nombre: str
    correo: str

    # Validador de correo
    @field_validator("correo")
    def validar_correo(cls, v):
        if "@" not in v:
            raise ValueError("El correo debe contener '@'")
        return v


# -----------------------------
# MODELO DE ORDEN
# -----------------------------
class Order(BaseModel):
    product_id: int
    quantity: int
    price: float

    # Validación después de construir el modelo
    @model_validator(mode="after")
    def validar_datos(cls, values):
        if values.quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        if values.price <= 0:
            raise ValueError("El precio debe ser mayor que 0")
        return values


# -----------------------------
# RUTAS DE LA API
# -----------------------------
@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a mi API con FastAPI 🚀"}


@app.post("/usuarios/")
def crear_usuario(usuario: User):
    return {"mensaje": "Usuario creado correctamente", "usuario": usuario}


@app.post("/ordenes/")
def crear_orden(orden: Order):
    total = orden.quantity * orden.price
    return {
        "mensaje": "Orden registrada correctamente",
        "orden": orden,
        "total": total,
    }


main 3 --------------------------------------------------------------------------------------------------------------------------------------------

from fastapi import FastAPI, HTTPException
from datetime import datetime
import logging

app = FastAPI()

# -----------------------------
# Configuración de Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# Base de datos simulada
# -----------------------------
products = [
    {"id": 1, "name": "Laptop", "price": 1500.0, "stock": 10},
    {"id": 2, "name": "Mouse", "price": 25.0, "stock": 50},
    {"id": 3, "name": "Teclado", "price": 75.0, "stock": 0},
]

# -----------------------------
# Funciones de Respuesta
# -----------------------------
def create_error_response(message: str, status_code: int, details: dict = None):
    return {
        "success": False,
        "error": {
            "message": message,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
    }

def create_success_response(message: str, data: dict = None):
    return {
        "success": True,
        "message": message,
        "data": data or {},
        "timestamp": datetime.now().isoformat()
    }

# -----------------------------
# Endpoints
# -----------------------------
@app.get("/")
def home():
    return create_success_response("Bienvenido a la API de productos 🚀")

@app.get("/products")
def get_all_products():
    logger.info("Consultando todos los productos")
    return create_success_response(
        message=f"Se encontraron {len(products)} productos",
        data={"products": products, "total": len(products)}
    )

@app.get("/products/{product_id}")
def get_product(product_id: int):
    logger.info(f"Buscando producto con ID: {product_id}")

    if product_id <= 0:
        logger.warning(f"ID inválido recibido: {product_id}")
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="ID del producto debe ser mayor a 0",
                status_code=400,
                details={"provided_id": product_id, "min_id": 1}
            )
        )

    for product in products:
        if product["id"] == product_id:
            logger.info(f"Producto encontrado: {product['name']}")
            return create_success_response(
                message="Producto encontrado",
                data={"product": product}
            )

    logger.warning(f"Producto no encontrado: ID {product_id}")
    raise HTTPException(
        status_code=404,
        detail=create_error_response(
            message=f"Producto con ID {product_id} no encontrado",
            status_code=404,
            details={"requested_id": product_id, "available_ids": [p["id"] for p in products]}
        )
    )

@app.post("/products")
def create_product(product: dict):
    logger.info(f"Intentando crear producto: {product.get('name', 'SIN_NOMBRE')}")

    # Validaciones
    if "name" not in product:
        logger.error("Intento de crear producto sin nombre")
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="El campo 'name' es obligatorio",
                status_code=400,
                details={"missing_field": "name", "received_fields": list(product.keys())}
            )
        )

    if "price" not in product:
        logger.error(f"Intento de crear producto '{product.get('name', 'SIN_NOMBRE')}' sin precio")
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="El campo 'price' es obligatorio",
                status_code=400,
                details={"missing_field": "price", "received_fields": list(product.keys())}
            )
        )

    if product["price"] <= 0:
        logger.error(f"Precio inválido para producto '{product['name']}': {product['price']}")
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="El precio debe ser mayor a 0",
                status_code=400,
                details={"provided_price": product["price"], "min_price": 0.01}
            )
        )

    for existing in products:
        if existing["name"].lower() == product["name"].lower():
            logger.warning(f"Intento de crear producto duplicado: '{product['name']}'")
            raise HTTPException(
                status_code=409,
                detail=create_error_response(
                    message=f"Ya existe un producto con el nombre '{product['name']}'",
                    status_code=409,
                    details={"conflicting_name": product["name"], "existing_product_id": existing["id"]}
                )
            )

    # Crear producto
    new_id = max([p["id"] for p in products]) + 1 if products else 1
    new_product = {
        "id": new_id,
        "name": product["name"],
        "price": product["price"],
        "stock": product.get("stock", 0)
    }

    products.append(new_product)
    logger.info(f"Producto creado exitosamente: ID {new_id}, Nombre: {new_product['name']}")

    return create_success_response(
        message=f"Producto '{new_product['name']}' creado exitosamente",
        data={"product": new_product}
    )

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    logger.info(f"Intentando eliminar producto con ID: {product_id}")

    for i, product in enumerate(products):
        if product["id"] == product_id:
            deleted_product = products.pop(i)
            logger.info(f"Producto eliminado: ID {product_id}, Nombre: {deleted_product['name']}")
            return create_success_response(
                message=f"Producto '{deleted_product['name']}' eliminado exitosamente",
                data={"deleted_product": deleted_product}
            )

    logger.warning(f"Intento de eliminar producto inexistente: ID {product_id}")
    raise HTTPException(
        status_code=404,
        detail=create_error_response(
            message=f"No se puede eliminar: producto con ID {product_id} no existe",
            status_code=404,
            details={"requested_id": product_id, "available_ids": [p["id"] for p in products]}
        )
    )

@app.get("/stats")
def get_stats():
    logger.info("Consultando estadísticas de la API")

    total_products = len(products)
    total_stock = sum(p.get("stock", 0) for p in products)
    avg_price = sum(p["price"] for p in products) / total_products if total_products > 0 else 0

    stats = {
        "total_products": total_products,
        "total_stock": total_stock,
        "average_price": round(avg_price, 2)
    }

    logger.info(f"Estadísticas calculadas: {stats}")
    return create_success_response("Estadísticas calculadas exitosamente", data={"stats": stats})



main 4 --------------------------------------------------------------------------------------------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import products

app = FastAPI(title="Mi API Organizada", version="1.0.0")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringirlo a ["http://localhost:3000"] si usas frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(products.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}




Ejercicios ----------------------------------------------------------------------------------------------------------------------------------------

