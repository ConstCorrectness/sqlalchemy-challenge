import pytest
from app import app

def test_home():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200

def test_precipitation():
    with app.test_client() as client:
        response = client.get("/api/v1.0/precipitation")
        assert response.status_code == 200

def test_stations():
    with app.test_client() as client:
        response = client.get("/api/v1.0/stations")
        assert response.status_code == 200

def test_tobs():
    with app.test_client() as client:
        response = client.get("/api/v1.0/tobs")
        assert response.status_code == 200

def test_start():
    with app.test_client() as client:
        response = client.get("/api/v1.0/2017-03-01")
        assert response.status_code == 200

def test_start_end():
    with app.test_client() as client:
        response = client.get("/api/v1.0/2017-01-01/2017-03-07")
        assert response.status_code == 200

