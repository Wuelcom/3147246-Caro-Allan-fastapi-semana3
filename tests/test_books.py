from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_books():
    response = client.get("/punto4/books")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)
    assert len(books) >= 1
    assert "title" in books[0]

def test_add_book():
    new_book = {
        "title": "El Principito",
        "author": "Antoine de Saint-Exupéry",
        "genre": "Infantil",
        "year": 1943
    }
    response = client.post("/punto4/books", json=new_book)
    assert response.status_code == 200
    book = response.json()
    assert book["title"] == "El Principito"
    assert book["available"] is True

def test_borrow_and_return_book():
    # Pedir prestado el libro con ID=1
    response = client.post("/punto4/borrowing/borrow/1")
    assert response.status_code == 200
    book = response.json()
    assert book["available"] is False

    # Intentar pedirlo de nuevo debe fallar
    response = client.post("/punto4/borrowing/borrow/1")
    assert response.status_code == 400

    # Devolver el libro
    response = client.post("/punto4/borrowing/return/1")
    assert response.status_code == 200
    book = response.json()
    assert book["available"] is True

def test_list_genres():
    response = client.get("/punto4/categories")
    assert response.status_code == 200
    genres = response.json()
    assert isinstance(genres, list)
    assert "Novela" in genres or "Clásico" in genres
