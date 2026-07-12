from fastapi import Header, HTTPException
from app.services.jwt_service import verify_token

def get_current_user(authorization: str = Header(None)):

    print("AUTH HEADER =", authorization)

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid token format"
        )

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload