from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    id: int
    hashed_password: str
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class AnimeBase(BaseModel):
    currEpisode: int
    title: str
    recurring: str
    caughtUp: bool | None = False
    notes: str | None = None

class AnimeCreate(AnimeBase):
    pass

class Anime(AnimeBase):
    id: int

    class Config:
        orm_mode = True

class MangaBase(BaseModel):
    currChapter: int
    title: str
    recurring: str
    caughtUp: bool | None = False
    notes: str | None = None

class MangaCreate(MangaBase):
    pass

class Manga(MangaBase):
    id: int
    owner_id: int
    owner: User
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str
