from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app, get_db

user_db = 'postgres'
pwd_db = '123789123'

SQLALCHEMY_DATABASE_URL = f"postgresql://{user_db}:{pwd_db}@localhost/teste_pontotel"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
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

def test_read_companie_from_api():
    response = client.get("/companies/Ambev")
    assert response.status_code == 200
    assert response.json() == [
        {
        "1. symbol": "ABEV3.SAO",
        "2. name": "Ambev S.A.",
        "3. type": "Equity",
        "4. region": "Brazil/Sao Paolo",
        "5. marketOpen": "10:00",
        "6. marketClose": "17:30",
        "7. timezone": "UTC-03",
        "8. currency": "BRL",
        "9. matchScore": "0.6667"
        }
    ]

def test_read_companie_from_db():
    response = client.get("/companies")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_user():
    response = client.post(
        '/user',
        json={
                "name": "teste",
                "email": "teste@hotmail.com",
                "password": "1234",
                "type_id": 1  
            })

    assert response.status_code == 200 
    assert response.json() == {
                "name": "teste",
                "email": "teste@hotmail.com",
                "type_id": 1  
            }

def test_create_user_error():
    response = client.post(
        '/user',
        json={
                "name": "teste",
                "email": "teste@hotmail.com",
                "password": "1234",
                "type_id": 1  
            })

    assert response.status_code == 400
    assert response.json() == {
                "detail": "Email already registered"
            }