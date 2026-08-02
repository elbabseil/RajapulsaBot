from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


SECRET_KEY = "RAJAPULSA_SECRET_KEY"

ALGORITHM = "HS256"



def hash_password(password):

    return pwd_context.hash(password)



def verify_password(password, hashed):

    return pwd_context.verify(
        password,
        hashed
    )



def create_token(username):

    payload = {

        "sub": username,

        "exp":
        datetime.utcnow()
        +
        timedelta(hours=24)

    }


    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )