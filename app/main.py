from datetime import datetime, timedelta
import requests 
import json
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import crud, models, schemas
from fastapi.openapi.utils import get_openapi

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
api_key = 'TPBMLAJYV2XGTM3Z'

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Teste PontoTel",
        version="1.0.0",
        description="API que faz o consumo da Alpha Vantage para consultar dados do Bovespa",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/companies/{companie}")
async def get_companies_api(companie: str, db: Session = Depends(get_db)):
    api = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={companie}&apikey={api_key}'
    # transforma a resposta da requisição em json
    resp = json.loads(requests.get(api).content.decode('utf-8'))
    companies = resp['bestMatches']
    filter_companies = []
   
    # itera na lista que vem da api e filtra as empresas brasileira
    filter_companies = brazil_companies(companies)

    for companie in filter_companies:
        # Verifica se as empresas que foram filtradas estão no banco de dados
        if verify_companie(companie['1. symbol'], db):
            print('Gravando...', companie['1. symbol'],)
            db_companie = models.Companie(
            symbol=companie['1. symbol'],
            name=companie['2. name'],
            type=companie['3. type'],
            region=companie['4. region'],
            currency=companie['8. currency'],
            matchScore=companie['9. matchScore']
            )
            crud.create_companie(db=db, companie=db_companie)

    return filter_companies


@app.get('/companies', response_model=List[schemas.Companie])
def get_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    companies = crud.get_companies(db, skip=skip, limit=limit, order=models.Companie.matchScore.desc())
    return companies

@app.post('/user', response_model = schemas.UserSelect)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    #type_user = crud.get_user_types()
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_db = crud.create_user(db=db, user=user)
    return {
        "name": user_db.name,
        "email": user_db.email,
        "type_id": user_db.type_id,
    }

@app.get('/user')
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)



def verify_companie(companie, db: Session = Depends(get_db)):
    db_companies = crud.get_companies(db, limit=None) 
    db_companies = jsonable_encoder(db_companies)

    for c in db_companies: 
        if c['symbol'] in companie:
            print("Tem no banco")
            return False
        else:
            print("Não tem no banco")
    
    return True


def brazil_companies(companies):
    filtered_companies = []
    for c in companies:
        if 'Brazil/Sao Paolo' in c['4. region']:
            filtered_companies.append(c)
    
    return filtered_companies




    
        