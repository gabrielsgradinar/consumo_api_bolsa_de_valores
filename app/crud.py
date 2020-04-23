from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_companies(db: Session, skip: int = 0, limit: int = 10, order=None):
    return db.query(models.Companie).order_by(order).offset(skip).limit(limit).all()

def create_companie(db: Session, companie: schemas.CompanieBase):
    db_companie = models.Companie(
        symbol=companie.symbol,
        name=companie.name,
        type=companie.type,
        region=companie.region,
        currency=companie.currency,
        matchScore=companie.matchScore
        )
    db.add(db_companie)
    db.commit()
    db.refresh(db_companie)
    return db_companie

def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(
        name= user.name,
        email= user.email,
        password= pwd_context.hash(user.password),
        type_id = user.type_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(db_user)
    return db_user



def get_users(db: Session):
    return db.query(models.User).all()
        #.join(models.UserType, models.User.type_id == models.UserType.id)

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

