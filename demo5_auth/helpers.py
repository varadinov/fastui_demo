import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Annotated
from fastapi import HTTPException, Header

def encode_token(
    jwt_secret: str, subject: str, claims: Optional[Dict] = None, expiration_hours: int = 24
) -> str:
    payload = claims.copy() if claims else {}
    payload.update({
        "sub": subject,
        "exp": datetime.utcnow() + timedelta(hours=expiration_hours),
        "id": subject
    })

    return jwt.encode(payload, jwt_secret, algorithm="HS256")

def decode_token(jwt_secret: str, token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, jwt_secret, algorithms=["HS256"])

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(401, "Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")


async def get_user(authorization: Annotated[str, Header()] = ''):
    try:
        token = authorization.split(' ', 1)[1]
        decoded_token = decode_token('test', token)
        return decoded_token['id']
    except Exception:
        return None
