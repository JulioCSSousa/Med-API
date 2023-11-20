from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from passlib.context import CryptContext
from app.crud import *
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
db = Session(engine)


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'qwe4544e5d9v83x2c4v8s79f843s2165sv798cv46x5c4vs98d7f98465xv3zx54d8'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES = 30

def verify_pwd(hashed_password, plain_password):
    return check_password_hash(hashed_password, plain_password)

def get_pwd_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    email = get_user_by_email(db, username)
    if not email:
        return False
    pwd = get_user_pwd(db, email[0])
    pwdd = pwd[0]
    if not verify_pwd(pwdd, password):
        return False
    print('emaill', email[0])
    return email[0]

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='Acesso Negado', headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(email=username)
    except JWTError:
        raise credential_exception
    user = token_data
    if user is None:
        raise credential_exception
    return user



