from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.auth.jwt import hash_password, verify_password, create_access_token, decode_token

router = APIRouter()
security = HTTPBearer()

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# In production replace with real DB calls
USERS_DB = {}

@router.post("/register")
async def register(req: RegisterRequest):
    if req.email in USERS_DB:
        raise HTTPException(400, "Email already registered")
    USERS_DB[req.email] = {
        "id": req.email,
        "email": req.email,
        "password_hash": hash_password(req.password)
        }
    token = create_access_token(req.email)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
async def login(req: LoginRequest):
    user = USERS_DB.get(req.email)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(req.email)
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    user_id = decode_token(creds.credentials)
    if not user_id:
        raise HTTPException(401, "Invalid or expired token")
    return user_id