from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    id: int
    firstname: str
    username: str | None = None
    secondname: str | None = None
    lang_code: str | None = None
    is_active: bool = True

    class Config:
        orm_mode = True


class UserWithEmail(User):
    email: str
