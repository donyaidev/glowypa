from fastapi import HTTPException, Header, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt  # Make sure this is PyJWT
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "domoraduocpass"
ALGORITHM = "HS256"

def generate_token(email: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode(
        {"email": email, "exp": expiration}, 
        SECRET_KEY, 
        algorithm=ALGORITHM
    )
    return token

async def verify_token(authorization: str = Header(..., description="Bearer token needed")) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format. Expected 'Bearer <token>'."
        )
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("email")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
