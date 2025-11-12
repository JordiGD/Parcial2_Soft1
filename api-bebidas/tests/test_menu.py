import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import BebidaDB

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override de la dependencia de base de datos para tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Configura la base de datos para cada test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Cliente de prueba"""
    return TestClient(app)

class TestMenu:
    """Tests para el menú de bebidas"""
    
    def test_get_menu_vacio(self, client):
        """Test: menú vacío al inicio"""
        response = client.get("/menu")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_bebida_valida(self, client):
        """Test: crear bebida válida"""
        bebida = {
            "name": "Café Latte",
            "size": "medium",
            "price": 3.50
        }
        response = client.post("/menu", json=bebida)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Café Latte"
        assert data["size"] == "medium"
        assert data["price"] == 3.50
        assert "id" in data
    
    def test_create_bebida_sin_nombre(self, client):
        """Test: rechazar bebida sin nombre"""
        bebida = {
            "name": "",
            "size": "small",
            "price": 2.00
        }
        response = client.post("/menu", json=bebida)
        assert response.status_code == 422
    
    def test_create_bebida_precio_negativo(self, client):
        """Test: rechazar precio negativo"""
        bebida = {
            "name": "Café",
            "size": "small",
            "price": -1.00
        }
        response = client.post("/menu", json=bebida)
        assert response.status_code == 422
    
    def test_get_bebida_by_name(self, client):
        """Test: buscar bebida por nombre"""
        bebida = {
            "name": "Cappuccino",
            "size": "large",
            "price": 4.00
        }
        client.post("/menu", json=bebida)
        
        response = client.get("/menu/Cappuccino")
        assert response.status_code == 200
        assert response.json()["name"] == "Cappuccino"
    
    def test_get_bebida_no_existe(self, client):
        """Test: bebida no encontrada"""
        response = client.get("/menu/NoExiste")
        assert response.status_code == 404
    
    def test_no_duplicar_bebidas(self, client):
        """Test: no permitir bebidas duplicadas"""
        bebida = {
            "name": "Espresso",
            "size": "small",
            "price": 2.00
        }
        client.post("/menu", json=bebida)
        response = client.post("/menu", json=bebida)
        assert response.status_code == 400