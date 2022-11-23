from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas, util, database, crud, oauth2
from fastapi.security import OAuth2PasswordRequestForm
from sql_app.database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


def authenticate_user(username: str, password: str, db: Session):
    user = crud.get_user_by_email(db, email=username)
    if not user:
        return False
    if not util.verify(password, user.hashed_password):
        return False
    return user

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email exists already.")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not created")
    return db_user

@app.get("/users/manga", response_model=schemas.Manga)
def get_manga(user_id: int, manga_title: str, db: Session = Depends(database.get_db)):
    manga = crud.get_manga_by_title(db, manga_title=manga_title)
    if manga is None:
        raise HTTPException(status_code=404, detail="Manga not created")
    return manga

@app.get("/users/mangas/", response_model=list[schemas.Manga])
def get_mangas(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    mangas = crud.get_mangas(db, skip=skip, limit=limit)
    return mangas

@app.post("/users/mangas/", response_model=schemas.Manga)
def create_manga(manga: schemas.MangaCreate, db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):
    return crud.user_add_manga(db=db, manga=manga, user_id=user_id)

@app.get("/users/{user_id}/{anime_title}", response_model=schemas.Anime)
def get_anime(user_id: int, anime_title: str, db: Session = Depends(database.get_db)):
    anime = crud.get_anime_by_title(db, anime_title=anime_title)
    if anime is None:
        raise HTTPException(status_code=404, detail="Anime not created")
    return anime

@app.get("/users/{user_id}/anime/", response_model=list[schemas.Anime])
def get_animes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    animes = crud.get_animes(db, skip=skip, limit=limit)
    return animes

@app.post("/users/{user_id}/animes/", response_model=schemas.Anime)
def create_anime(user_id: int, anime: schemas.AnimeCreate, db: Session = Depends(database.get_db)):
    return crud.user_add_anime(db=db, anime=anime, user_id=user_id)

@app.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid")
    if not util.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@app.delete('/users')
def delete_user(user_email: str, db: Session = Depends(database.get_db)):
    deleted_user = crud.get_user_by_email(db=db, email=user_email)
    db.delete(deleted_user)
    db.commit()
    return {"deleted"}