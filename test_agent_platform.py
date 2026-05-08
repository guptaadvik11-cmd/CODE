from fastapi.testclient import TestClient
from agent_platform import app

client = TestClient(app)

# Trigger startup event manually for testing
@app.on_event("startup")
async def startup_event():
    pass # Already defined in agent_platform.py, but TestClient triggers it

def test_read_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "Welcome to AgentNet" in response.json()["message"]

def test_registry_contains_builtins():
    with TestClient(app) as client:
        response = client.get("/registry")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        ids = [srv["id"] for srv in data]
        assert "core.weather.v1" in ids
        assert "core.calculator.v1" in ids

def test_search_services():
    with TestClient(app) as client:
        response = client.get("/registry/search?query=weather")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "core.weather.v1"

def test_weather_service():
    with TestClient(app) as client:
        response = client.post("/services/weather", json={"location": "London"})
        assert response.status_code == 200
        assert response.json()["location"] == "London"
        assert "temperature_celsius" in response.json()

def test_calculator_service():
    with TestClient(app) as client:
        response = client.post("/services/calculator", json={"expression": "10 * 5"})
        assert response.status_code == 200
        assert response.json()["result"] == 50

def test_register_new_service():
    new_service = {
        "id": "test.dummy.v1",
        "name": "DummyService",
        "description": "A dummy service for testing",
        "endpoint": "/services/dummy",
        "method": "GET",
        "parameters": []
    }
    with TestClient(app) as client:
        response = client.post("/registry/register", json=new_service)
        assert response.status_code == 201

        # Verify it's in the registry
        res2 = client.get("/registry")
        ids = [srv["id"] for srv in res2.json()]
        assert "test.dummy.v1" in ids
