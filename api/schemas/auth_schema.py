from pydantic import BaseModel


class RegisterSchema(BaseModel):

    username: str
    password: str
    full_name: str



class LoginSchema(BaseModel):

    username: str
    password: str