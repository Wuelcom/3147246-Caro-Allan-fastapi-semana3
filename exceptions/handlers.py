from fastapi import Request
from fastapi.responses import JSONResponse
from .custom_exceptions import ProductNotFoundError, DuplicateProductError

def setup_exception_handlers(app):
    @app.exception_handler(ProductNotFoundError)
    async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error_code": "PRODUCT_NOT_FOUND",
                "message": f"Producto con ID {exc.product_id} no encontrado"
            }
        )

    @app.exception_handler(DuplicateProductError)
    async def duplicate_product_handler(request: Request, exc: DuplicateProductError):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error_code": "DUPLICATE_PRODUCT",
                "message": f"El producto '{exc.name}' ya existe"
            }
        )
