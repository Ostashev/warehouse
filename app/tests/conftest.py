import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.test_database import TestingSessionLocal, init_db

@pytest.fixture(scope="module")
def db_session():
    init_db()
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c