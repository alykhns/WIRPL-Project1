import jwt
from datetime import datetime, timedelta

SECRET = "lumiere-secret"

def create_token(customer_id: int):
    payload = {
        "sub": customer_id,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token: str):
    return jwt.decode(token, SECRET, algorithms=["HS256"])