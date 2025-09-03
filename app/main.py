from fastapi import FastAPI
from app.routers import products
from exceptions.handlers import setup_exception_handlers
from app.punto1_2_3_5.router import router as router1235
from app.punto4.router import router as router4

app = FastAPI(title="Mi API con FastAPI", version="1.0")

# Configurar manejo de errores
setup_exception_handlers(app)

# Incluir rutas
app.include_router(products.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Incluye los puntos 1, 2, 3 y 5
app.include_router(router1235, prefix="/puntos1235", tags=["Puntos 1, 2, 3 y 5"])

# Incluye el punto 4 (si quieres probarlo también)
app.include_router(router4, prefix="/punto4", tags=["Punto 4"])
