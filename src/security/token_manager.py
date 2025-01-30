import jwt
from datetime import datetime, timedelta, timezone
from jwt import PyJWTError
from fastapi import HTTPException, status

SECRET_KEY = "e88731089b8fdcc5539e5f9017dc7d83bcfaf38367fd777caaa5e69f63bd935f"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 3
REFRESH_TOKEN_EXPIRE_DAYS = 7

class TokenManager:
    def create_access_token(self, data: dict) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


    def create_refresh_token(self, data: dict) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
