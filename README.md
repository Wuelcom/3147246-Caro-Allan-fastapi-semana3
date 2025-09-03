# 📚 Library & Products Management API

API REST construida con **FastAPI** que integra dos módulos principales:

- **Gestión de Productos** (ejercicios 1, 2, 3 y 5).
- **Gestión de Biblioteca** (ejercicio 4: libros, géneros, préstamos, estadísticas).

Incluye pruebas automáticas con `pytest`.

---

## ⚙️ Installation

1. Clonar el repositorio:
    -Terminal
    git clone <URL_DEL_REPO>
    cd 3147246-Caro-Allan-fastapi-semana3

Crear y activar entorno virtual:
    -Terminal
    Copy code
    python -m venv venv
    source venv/Scripts/activate   # En Linux/Mac: source venv/bin/activate
   
Instalar dependencias:
    -Terminal
    Copy code
    pip install -r requirements.txt

Ejecutar el servidor:
    -Terminal
    Copy code
    uvicorn app.main:app --reload
El servidor correrá en: 👉 http://127.0.0.1:8000
La documentación interactiva estará en: 👉 http://127.0.0.1:8000/docs

🚀 Quick Start
Ejemplo rápido con cURL:

-Terminal
Copy code   
# 1. Health check
curl http://127.0.0.1:8000/health

# 2. Obtener lista de productos
curl http://127.0.0.1:8000/products/

# 3. Agregar un libro
curl -X POST "http://127.0.0.1:8000/api/v1/books/" \
-H "Content-Type: application/json" \
-d '{"title":"El Principito","author":"Antoine de Saint-Exupéry","genre":"Ficción","year":1943}'
Ejemplo rápido con Swagger UI:

Ir a 👉 http://127.0.0.1:8000/docs

Probar los endpoints con formularios interactivos.

📌 API Endpoints
✅ Products (ejercicios 1, 2, 3, 5)
GET /health → Verificar estado de la API

GET /products/ → Listar todos los productos

GET /products/search?name= → Buscar productos por nombre

✅ Books (ejercicio 4)
GET /api/v1/books/ → Listar libros

POST /api/v1/books/ → Agregar un nuevo libro

GET /api/v1/books/search?... → Buscar libros por título, autor, género o año

GET /api/v1/books/stats → Obtener estadísticas de la biblioteca

✅ Borrowing (Préstamos)
POST /api/v1/borrowing/borrow/{book_id} → Prestar un libro

POST /api/v1/borrowing/return/{book_id} → Devolver un libro

GET /api/v1/borrowing/active → Listar préstamos activos

✅ Categories
GET /api/v1/categories/ → Listar todos los géneros

GET /api/v1/categories/{genre}/books → Listar libros por género

📝 Examples
1. Buscar productos por nombre
    Copy code
    curl "http://127.0.0.1:8000/products/search?name=mouse"

2. Buscar libros de un autor
    Copy code
    curl "http://127.0.0.1:8000/api/v1/books/search?author=Gabriel Garcia Marquez"

3. Prestar un libro
    Copy code
    curl -X POST http://127.0.0.1:8000/api/v1/borrowing/borrow/1
    
4. Ver estadísticas de la biblioteca
    Copy code
    curl http://127.0.0.1:8000/api/v1/books/stats


👩‍💻 Development
Ejecutar pruebas automáticas
    -Terminal
    Copy code
    python -m pytest -v
Salida esperada
arduino
Copy code
tests/test_books.py::test_get_books PASSED
tests/test_books.py::test_add_book PASSED
tests/test_books.py::test_borrow_and_return_book PASSED
tests/test_books.py::test_list_genres PASSED
tests/test_products.py::test_health_check PASSED
tests/test_products.py::test_get_products PASSED
tests/test_products.py::test_search_invalid_name PASSED
Estructura del proyecto



Copy code
app/
├── main.py           # Punto de entrada FastAPI
├── routers/          # Rutas (productos, libros, etc.)
├── models/           # Modelos Pydantic
├── data/             # Datos en memoria
└── punto4/           # Lógica de biblioteca (libros)
tests/
├── test_products.py  # Tests productos
└── test_books.py     # Tests libros