from sqlalchemy.orm import Session
from fastapi import Depends
from . import schemas, models, util, oauth2




def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = util.hash(user.password)
    db_user = models.Users(email=user.email, hashed_password = fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_animes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Anime).offset(skip).limit(limit).all()

def get_anime_by_title(db: Session, anime_title: str):
    return db.query(models.Anime).filter(models.Anime.title == anime_title).first()

def user_add_anime(db: Session, anime: schemas.AnimeCreate, user_id: int):
    db_item = models.Anime(**anime.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_mangas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Manga).offset(skip).limit(limit).all()

def get_manga_by_title(db: Session, manga_title: str):
    return db.query(models.Manga).filter(models.Manga.title == manga_title).first()

def user_add_manga(db: Session, manga: schemas.MangaCreate, user_id: int = Depends(oauth2.get_current_user)):
    db_item = models.Manga(owner_id = user_id.id, **manga.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item