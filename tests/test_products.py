from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_invalid_name():
    response = client.get("/products/search?name=a")
    assert response.status_code == 400
    assert response.json()["detail"] == "El término de búsqueda debe tener al menos 2 caracteres"
