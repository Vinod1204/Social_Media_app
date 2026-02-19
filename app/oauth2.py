from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models, utils, database
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data:dict):
    to_encode=data.copy()
    #code to create jwt token
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentails_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")

        if id is None:
            raise credentails_exception
        
        token_data=schemas.TokenData(id=str(id))

    except JWTError:
        raise credentails_exception
     
    return token_data

def get_current_user(token:str= Depends(oauth2_scheme), db:Session= Depends(database.get_db)):
    credentails_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentails",
                                        headers={"WWW-Authenticate":"Bearer"})
    
    token=verify_access_token(token, credentails_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user