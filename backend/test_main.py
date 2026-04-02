import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

class TestAPI:
    def test_health_check(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "OK"

    def test_admin_login_invalid(self):
        response = client.post("/api/admin/login", json={"username": "bad", "password": "bad"})
        assert response.status_code == 401

    def test_admin_login_valid(self):
        response = client.post("/api/admin/login", json={"username": "admin", "password": "admin123"})
        assert response.status_code == 200
        assert response.json()["access"] == True

    def test_create_fiche_stage(self):
        fiche_data = {
            "nom_etudiant": "TEST ETUDIANT",
            "contact_etudiant": "07 00 00 00 00",
            "niveau_etude": "Licence 3",
            "filiere_classe": "Informatique",
            "date_fiche": "2026-04-01",
            "en_stage": "OUI",
            "nom_entreprise": "Test Corp",
            "situation_entreprise": "Plateau",
            "contact_entreprise": "20 00 00 00",
            "date_debut_stage": "2026-04-01",
            "date_fin_stage": "2026-07-31"
        }
        response = client.post("/api/soumettre-fiche", json=fiche_data)
        assert response.status_code == 200
        assert response.json()["nom_etudiant"] == "TEST ETUDIANT"
