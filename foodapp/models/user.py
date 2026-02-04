from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    email: str


class UserIn(User):
    password: str


class Token(BaseModel):
    token: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
